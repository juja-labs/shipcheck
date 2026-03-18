"""하이브리드 액션 실행 — CDP로 좌표 획득, Playwright로 실제 조작.

CDP: backendNodeId → scrollIntoView → getContentQuads → 좌표
Playwright: page.mouse.click(x, y), page.keyboard.type(text) 등

CDP 직접 조작 대비 장점:
- page.keyboard.type("/") → keydown+keyup 자연 발생 → SPA 프레임워크(Tally 등) 인식
- Playwright의 auto-wait, 안정적 이벤트 시퀀스 활용
- contenteditable + React/Vue onChange 정상 동작
"""

from __future__ import annotations

import asyncio
import json
import logging

from playwright.async_api import Page

logger = logging.getLogger(__name__)


async def click_element(
    page: Page,
    cdp_session,
    backend_node_id: int,
) -> bool:
    """backendNodeId 요소를 클릭.

    CDP: scrollIntoView + 좌표 획득
    Playwright: page.mouse.click(x, y)
    Fallback: JS element.click()
    """
    try:
        await cdp_session.send(
            "DOM.scrollIntoViewIfNeeded",
            {"backendNodeId": backend_node_id},
        )
        await asyncio.sleep(0.05)

        cx, cy = await _get_element_center(cdp_session, backend_node_id)
        if cx is None:
            return await _js_click(cdp_session, backend_node_id)

        await page.mouse.click(cx, cy)
        return True

    except Exception as e:
        logger.warning("클릭 실패 (bid=%d): %s — JS fallback", backend_node_id, e)
        return await _js_click(cdp_session, backend_node_id)


async def type_text(
    page: Page,
    cdp_session,
    backend_node_id: int,
    text: str,
) -> bool:
    """backendNodeId 요소에 텍스트 입력.

    1. CDP: scrollIntoView + 좌표 획득
    2. Playwright: 클릭으로 포커스
    3. Playwright: Ctrl+A → Delete → type(text)
    4. Fallback: JS value 설정
    """
    try:
        await cdp_session.send(
            "DOM.scrollIntoViewIfNeeded",
            {"backendNodeId": backend_node_id},
        )
        await asyncio.sleep(0.05)

        # 클릭으로 포커스
        cx, cy = await _get_element_center(cdp_session, backend_node_id)
        if cx is not None:
            await page.mouse.click(cx, cy)
        else:
            await cdp_session.send(
                "DOM.focus", {"backendNodeId": backend_node_id}
            )

        await asyncio.sleep(0.1)

        # 기존 내용 지우기 + 입력
        await page.keyboard.press("Control+a")
        await asyncio.sleep(0.03)
        await page.keyboard.press("Delete")
        await asyncio.sleep(0.03)
        await page.keyboard.type(text, delay=20)
        return True

    except Exception as e:
        logger.warning(
            "입력 실패 (bid=%d): %s — JS fallback", backend_node_id, e
        )
        return await _js_set_value(cdp_session, backend_node_id, text)


async def hover_element(
    page: Page,
    cdp_session,
    backend_node_id: int,
) -> bool:
    """backendNodeId 요소에 마우스 호버."""
    try:
        await cdp_session.send(
            "DOM.scrollIntoViewIfNeeded",
            {"backendNodeId": backend_node_id},
        )
        cx, cy = await _get_element_center(cdp_session, backend_node_id)
        if cx is None:
            return False
        await page.mouse.move(cx, cy)
        return True
    except Exception as e:
        logger.warning("호버 실패 (bid=%d): %s", backend_node_id, e)
        return False


async def scroll_page(
    page: Page,
    direction: str = "down",
    amount: int = 400,
) -> bool:
    """페이지 스크롤."""
    delta_y = amount if direction == "down" else -amount
    try:
        await page.mouse.wheel(0, delta_y)
        return True
    except Exception as e:
        logger.warning("스크롤 실패: %s", e)
        return False


async def dispatch_key(page: Page, key: str) -> bool:
    """키 입력 (Enter, Tab, Escape 등)."""
    try:
        await page.keyboard.press(key)
        return True
    except Exception as e:
        logger.warning("키 입력 실패 (%s): %s", key, e)
        return False


# -------------------------------------------------------------------
# 내부: CDP 좌표 획득 + JS fallback
# -------------------------------------------------------------------


async def _get_element_center(
    cdp_session, backend_node_id: int
) -> tuple[float | None, float | None]:
    """backendNodeId → 뷰포트 기준 중심 좌표.

    getContentQuads → getBoxModel fallback.
    """
    # getContentQuads
    try:
        result = await cdp_session.send(
            "DOM.getContentQuads",
            {"backendNodeId": backend_node_id},
        )
        quads = result.get("quads", [])
        if quads and len(quads[0]) >= 8:
            q = quads[0]
            cx = (q[0] + q[2] + q[4] + q[6]) / 4
            cy = (q[1] + q[3] + q[5] + q[7]) / 4
            return cx, cy
    except Exception:
        pass

    # getBoxModel fallback
    try:
        result = await cdp_session.send(
            "DOM.getBoxModel",
            {"backendNodeId": backend_node_id},
        )
        model = result.get("model", {})
        content = model.get("content", [])
        if len(content) >= 8:
            cx = (content[0] + content[2] + content[4] + content[6]) / 4
            cy = (content[1] + content[3] + content[5] + content[7]) / 4
            return cx, cy
    except Exception:
        pass

    return None, None


async def _js_click(cdp_session, backend_node_id: int) -> bool:
    """JS fallback: element.click()"""
    try:
        result = await cdp_session.send(
            "DOM.resolveNode", {"backendNodeId": backend_node_id}
        )
        object_id = result["object"]["objectId"]
        await cdp_session.send(
            "Runtime.callFunctionOn",
            {
                "objectId": object_id,
                "functionDeclaration": "function() { this.click(); }",
            },
        )
        return True
    except Exception as e:
        logger.warning("JS 클릭도 실패 (bid=%d): %s", backend_node_id, e)
        return False


async def _js_set_value(cdp_session, backend_node_id: int, text: str) -> bool:
    """JS fallback: value 직접 설정 + input/change 이벤트 발생."""
    try:
        result = await cdp_session.send(
            "DOM.resolveNode", {"backendNodeId": backend_node_id}
        )
        object_id = result["object"]["objectId"]
        await cdp_session.send(
            "Runtime.callFunctionOn",
            {
                "objectId": object_id,
                "functionDeclaration": f"""function() {{
                    if (this.contentEditable === 'true') {{
                        this.textContent = {json.dumps(text)};
                    }} else {{
                        this.value = {json.dumps(text)};
                    }}
                    this.dispatchEvent(new Event('input', {{bubbles: true}}));
                    this.dispatchEvent(new Event('change', {{bubbles: true}}));
                }}""",
            },
        )
        return True
    except Exception as e:
        logger.warning("JS 입력도 실패 (bid=%d): %s", backend_node_id, e)
        return False
