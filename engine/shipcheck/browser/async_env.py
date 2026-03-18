"""AsyncBrowserEnv — CDP Enhanced DOM Tree 기반 비동기 브라우저 환경.

기존 env.py의 접근성 스냅샷(aria_snapshot)을 CDP 직접 호출로 교체:
- DOMSnapshot.captureSnapshot + Accessibility.getFullAXTree 병합
- backendNodeId 기반 인덱스 매핑
- CDP로 좌표 획득 → Playwright로 실제 조작 (하이브리드)

SessionRunner에서 `await env.navigate()`, `await env.step()` 으로 호출.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from playwright.async_api import async_playwright, Page, Browser, Playwright

from ..core.types import Action, ActionType, Observation
from . import cdp_dom, dom_tree, cdp_actions

logger = logging.getLogger(__name__)


class AsyncBrowserEnv:
    """비동기 Playwright 브라우저 환경. CDP Enhanced DOM Tree 사용."""

    def __init__(
        self,
        headless: bool = True,
        screenshot_dir: Path | None = None,
        viewport: dict[str, int] | None = None,
    ) -> None:
        self._headless = headless
        self._screenshot_dir = screenshot_dir
        self._viewport = viewport or {"width": 1280, "height": 720}
        self._pw: Playwright | None = None
        self._browser: Browser | None = None
        self._page: Page | None = None
        self._cdp = None  # CDPSession
        self._step_count = 0
        self._prev_url: str = ""

        # 마지막 _observe()에서 생성된 selector_map
        # index → backendNodeId
        self._selector_map: dict[int, int] = {}

    async def __aenter__(self) -> AsyncBrowserEnv:
        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.launch(headless=self._headless)
        context = await self._browser.new_context(
            viewport=self._viewport,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            ),
        )
        self._page = await context.new_page()
        self._cdp = await self._page.context.new_cdp_session(self._page)
        if self._screenshot_dir:
            self._screenshot_dir.mkdir(parents=True, exist_ok=True)
        return self

    async def __aexit__(self, *args) -> None:
        if self._cdp:
            try:
                await self._cdp.detach()
            except Exception:
                pass
        if self._browser:
            await self._browser.close()
        if self._pw:
            await self._pw.stop()

    async def navigate(self, url: str) -> Observation:
        """초기 URL로 이동하고 첫 관찰을 반환."""
        logger.info("탐색 시작: %s", url)
        await self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await self._wait_for_idle()
        self._prev_url = self._page.url
        return await self._observe()

    async def step(self, action: Action) -> tuple[Observation, bool]:
        """액션 실행 후 관찰 반환."""
        self._step_count += 1
        succeeded = await self._execute_action(action)
        await self._wait_for_idle()

        url_changed = self._page.url != self._prev_url
        self._prev_url = self._page.url
        succeeded = succeeded or url_changed

        obs = await self._observe()
        return obs, succeeded

    async def take_screenshot(self, name: str) -> Path | None:
        """스크린샷 저장."""
        if not self._screenshot_dir or not self._page:
            return None
        path = self._screenshot_dir / f"{name}.png"
        await self._page.screenshot(path=str(path))
        return path

    # ------------------------------------------------------------------
    # Observation — CDP Enhanced DOM Tree
    # ------------------------------------------------------------------

    async def _observe(self) -> Observation:
        """CDP로 DOM + AX 추출 → 직렬화 → Observation 생성."""
        await self._ensure_cdp()

        try:
            raw_nodes = await cdp_dom.extract_raw_tree(self._cdp)
        except Exception as e:
            logger.error("DOM 추출 실패: %s", e)
            raw_nodes = []

        # 스크롤 위치 (문서 좌표 → 뷰포트 필터링에 필요)
        scroll_info = await self._get_scroll_info()
        scroll_y = scroll_info.get("scrollY", 0.0)

        if raw_nodes:
            serialized = dom_tree.filter_and_serialize(
                raw_nodes, scroll_y=scroll_y, viewport=self._viewport
            )
            self._selector_map = serialized.selector_map
            html_summary = serialized.text
            element_count = serialized.interactive_count
            text_length = serialized.text_length
        else:
            self._selector_map = {}
            html_summary = "[DOM 추출 실패]"
            element_count = 0
            text_length = 0

        return Observation(
            url=self._page.url,
            page_title=await self._page.title(),
            html_summary=html_summary,
            element_count=element_count,
            text_length=text_length,
            scroll_ratio=scroll_info.get("ratio", 0.0),
        )

    async def _get_scroll_info(self) -> dict[str, Any]:
        """현재 스크롤 위치 정보."""
        try:
            return await self._page.evaluate("""() => {
                const vh = window.innerHeight;
                const scrollY = window.scrollY || document.documentElement.scrollTop;
                const scrollMax = document.documentElement.scrollHeight - vh;
                return {
                    ratio: scrollMax > 0
                        ? Math.round(scrollY / scrollMax * 100) / 100
                        : 0,
                    scrollY: scrollY,
                    scrollMax: scrollMax,
                };
            }""")
        except Exception:
            return {"ratio": 0.0, "scrollY": 0.0}

    async def _ensure_cdp(self) -> None:
        """CDP 세션이 유효한지 확인하고, 닫혔으면 재생성."""
        try:
            await self._cdp.send("Target.getTargetInfo")
        except Exception:
            logger.info("CDP 세션 재생성")
            self._cdp = await self._page.context.new_cdp_session(self._page)

    # ------------------------------------------------------------------
    # Action Execution — CDP 좌표 + Playwright 실행 (하이브리드)
    # ------------------------------------------------------------------

    async def _execute_action(self, action: Action) -> bool:
        """Action → 하이브리드 실행.

        CDP: backendNodeId → scrollIntoView → 좌표 획득
        Playwright: page.mouse.click / page.keyboard.type 등 실제 조작
        """
        await self._ensure_cdp()

        try:
            if action.action_type == ActionType.CLICK:
                bid = self._resolve_index(action.target)
                if bid is None:
                    return False
                return await cdp_actions.click_element(
                    self._page, self._cdp, bid
                )

            elif action.action_type == ActionType.TYPE:
                bid = self._resolve_index(action.target)
                if bid is None or not action.value:
                    return False
                return await cdp_actions.type_text(
                    self._page, self._cdp, bid, action.value
                )

            elif action.action_type == ActionType.SELECT:
                bid = self._resolve_index(action.target)
                if bid is None or not action.value:
                    return False
                return await self._js_select_option(bid, action.value)

            elif action.action_type == ActionType.HOVER:
                bid = self._resolve_index(action.target)
                if bid is None:
                    return False
                return await cdp_actions.hover_element(
                    self._page, self._cdp, bid
                )

            elif action.action_type == ActionType.KEY_PRESS:
                if not action.value:
                    return False
                if action.target:
                    bid = self._resolve_index(action.target)
                    if bid is not None:
                        await self._cdp.send(
                            "DOM.focus", {"backendNodeId": bid}
                        )
                return await cdp_actions.dispatch_key(
                    self._page, action.value
                )

            elif action.action_type == ActionType.BACK:
                await self._page.go_back(timeout=10000)
                return True

            elif action.action_type == ActionType.GOTO_URL:
                if action.value:
                    await self._page.goto(
                        action.value,
                        wait_until="domcontentloaded",
                        timeout=15000,
                    )
                    return True
                return False

            elif action.action_type == ActionType.SCROLL:
                direction = (action.value or "down").lower()
                return await cdp_actions.scroll_page(
                    self._page, direction
                )

            elif action.action_type == ActionType.TERMINATE:
                return True

            else:
                logger.warning("알 수 없는 액션: %s", action.action_type)
                return False

        except Exception as e:
            logger.warning("액션 실행 실패: %s — %s", action, e)
            return False

    def _resolve_index(self, target: str | None) -> int | None:
        """target 문자열 (인덱스) → backendNodeId 변환."""
        if target is None:
            logger.warning("target이 None")
            return None
        try:
            idx = int(target)
        except (ValueError, TypeError):
            logger.warning("target을 정수로 변환 실패: %r", target)
            return None

        bid = self._selector_map.get(idx)
        if bid is None:
            logger.warning(
                "selector_map에 인덱스 %d 없음 (map_size=%d)",
                idx,
                len(self._selector_map),
            )
        return bid

    async def _js_select_option(self, backend_node_id: int, value: str) -> bool:
        """<select> 요소의 옵션 선택 (JS)."""
        import json as _json
        try:
            result = await self._cdp.send(
                "DOM.resolveNode", {"backendNodeId": backend_node_id}
            )
            object_id = result["object"]["objectId"]
            await self._cdp.send(
                "Runtime.callFunctionOn",
                {
                    "objectId": object_id,
                    "functionDeclaration": f"""function() {{
                        this.value = {_json.dumps(value)};
                        this.dispatchEvent(new Event('change', {{bubbles: true}}));
                    }}""",
                },
            )
            return True
        except Exception as e:
            logger.warning("select 옵션 선택 실패 (bid=%d): %s", backend_node_id, e)
            return False

    # ------------------------------------------------------------------
    # Wait
    # ------------------------------------------------------------------

    async def _wait_for_idle(self, timeout_ms: int = 5000) -> None:
        """페이지 로드 대기."""
        try:
            await self._page.wait_for_load_state(
                "domcontentloaded", timeout=timeout_ms
            )
            await self._page.wait_for_load_state(
                "networkidle", timeout=timeout_ms
            )
            # SPA 프레임워크 렌더링 대기 (기존 2500ms → 1000ms로 단축)
            await self._page.wait_for_timeout(1000)
        except Exception:
            pass
