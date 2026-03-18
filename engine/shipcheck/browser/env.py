"""BrowserEnv — Playwright 접근성 스냅샷 기반 브라우저 환경.

parser.js를 제거하고 Playwright 네이티브 접근성 API를 사용:
- page.locator('body').aria_snapshot() → YAML 접근성 트리
- page.get_by_role() / page.get_by_text() → 정확한 요소 선택
- 모달, Shadow DOM, contenteditable 자동 처리
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright, Page, Browser, Playwright

from ..core.types import Action, ActionType, Observation

logger = logging.getLogger(__name__)


class BrowserEnv:
    """Playwright 브라우저 환경. 접근성 스냅샷 기반."""

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
        self._step_count = 0
        self._prev_url: str = ""

    def __enter__(self) -> BrowserEnv:
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=self._headless)
        context = self._browser.new_context(
            viewport=self._viewport,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )
        self._page = context.new_page()
        if self._screenshot_dir:
            self._screenshot_dir.mkdir(parents=True, exist_ok=True)
        return self

    def __exit__(self, *args) -> None:
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()

    def navigate(self, url: str) -> Observation:
        """초기 URL로 이동하고 첫 관찰을 반환."""
        logger.info("탐색 시작: %s", url)
        self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
        self._wait_for_idle()
        self._prev_url = self._page.url
        return self._observe()

    def step(self, action: Action) -> tuple[Observation, bool]:
        """액션 실행 후 관찰 반환."""
        self._step_count += 1
        playwright_ok = self._execute_action(action)
        self._wait_for_idle()

        url_changed = self._page.url != self._prev_url
        self._prev_url = self._page.url
        succeeded = playwright_ok or url_changed

        obs = self._observe()
        return obs, succeeded

    def take_screenshot(self, name: str) -> Path | None:
        """스크린샷 저장."""
        if not self._screenshot_dir or not self._page:
            return None
        path = self._screenshot_dir / f"{name}.png"
        self._page.screenshot(path=str(path))
        return path

    # ------------------------------------------------------------------
    # Observation — 접근성 스냅샷 기반
    # ------------------------------------------------------------------

    def _observe(self) -> Observation:
        """Playwright 접근성 스냅샷으로 Observation 생성."""
        try:
            aria_yaml = self._page.locator("body").aria_snapshot()
        except Exception as e:
            logger.error("접근성 스냅샷 실패: %s", e)
            aria_yaml = "[스냅샷 생성 실패]"

        # 스크롤 상태
        scroll_info = self._get_scroll_info()

        # 인터랙티브 요소 수 추정 (YAML에서 role 기반 카운트)
        interactive_count = len(re.findall(
            r'- (button|link|textbox|checkbox|radio|combobox|tab|menuitem|switch)',
            aria_yaml,
        ))

        # 텍스트 길이 추정 (YAML에서 text: 라인)
        text_length = sum(
            len(line) for line in aria_yaml.splitlines()
            if line.strip().startswith("- text:")
            or line.strip().startswith("text:")
            or (": " in line and not line.strip().startswith("- "))
        )

        return Observation(
            url=self._page.url,
            page_title=self._page.title(),
            html_summary=aria_yaml,  # HTML 대신 접근성 스냅샷 YAML
            element_count=interactive_count,
            text_length=text_length,
            scroll_ratio=scroll_info.get("ratio", 0.0),
        )

    def _get_scroll_info(self) -> dict[str, Any]:
        """현재 스크롤 위치 정보."""
        try:
            return self._page.evaluate("""() => {
                const vh = window.innerHeight;
                const scrollY = window.scrollY || document.documentElement.scrollTop;
                const scrollMax = document.documentElement.scrollHeight - vh;
                return {
                    ratio: scrollMax > 0 ? Math.round(scrollY / scrollMax * 100) / 100 : 0,
                    scrollY: scrollY,
                    scrollMax: scrollMax,
                };
            }""")
        except Exception:
            return {"ratio": 0.0}

    # ------------------------------------------------------------------
    # Action Execution — role 기반 요소 선택
    # ------------------------------------------------------------------

    def _execute_action(self, action: Action) -> bool:
        """Action → Playwright API 호출.

        target은 접근성 스냅샷의 'role "name"' 형태 또는 텍스트.
        예: 'button "Create a free form"', 'tab "HR"', 'textbox "Form title"'
        """
        try:
            if action.action_type == ActionType.CLICK:
                locator = self._resolve_locator(action.target)
                if locator:
                    self._highlight(locator)
                    locator.click(timeout=5000)
                    return True
                return False

            elif action.action_type == ActionType.TYPE:
                locator = self._resolve_locator(action.target)
                if locator and action.value:
                    self._highlight(locator, color="#2222ff")
                    locator.fill(action.value, timeout=5000)
                    return True
                return False

            elif action.action_type == ActionType.SELECT:
                locator = self._resolve_locator(action.target)
                if locator and action.value:
                    locator.select_option(value=action.value, timeout=5000)
                    return True
                return False

            elif action.action_type == ActionType.HOVER:
                locator = self._resolve_locator(action.target)
                if locator:
                    locator.hover(timeout=5000)
                    return True
                return False

            elif action.action_type == ActionType.KEY_PRESS:
                if action.value:
                    # target이 있으면 해당 요소에 포커스 후 키 입력
                    if action.target:
                        locator = self._resolve_locator(action.target)
                        if locator:
                            locator.focus(timeout=3000)
                    self._page.keyboard.press(action.value)
                    return True
                return False

            elif action.action_type == ActionType.BACK:
                self._page.go_back(timeout=10000)
                return True

            elif action.action_type == ActionType.GOTO_URL:
                if action.value:
                    self._page.goto(action.value, wait_until="domcontentloaded", timeout=15000)
                    return True
                return False

            elif action.action_type == ActionType.SCROLL:
                direction = (action.value or "down").lower()
                amount = 400 if direction == "down" else -400
                self._page.mouse.wheel(0, amount)
                return True

            elif action.action_type == ActionType.TERMINATE:
                return True

            else:
                logger.warning("알 수 없는 액션: %s", action.action_type)
                return False

        except Exception as e:
            logger.warning("액션 실행 실패: %s — %s", action, e)
            return False

    @staticmethod
    def _normalize_quotes(s: str) -> str:
        """curly quotes → straight quotes (LLM 출력 정규화)."""
        return s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")

    def _is_interactable(self, locator) -> bool:
        """요소가 실제 인터랙션 가능한지 확인 (hidden file input 등 제외)."""
        try:
            tag = locator.evaluate("el => el.tagName.toLowerCase()")
            if tag == "input":
                input_type = locator.evaluate("el => el.type")
                if input_type == "file":
                    return False
            # visibility 체크
            if not locator.is_visible():
                return False
            return True
        except Exception:
            return False

    def _find_first_interactable(self, locator):
        """locator 결과 중 인터랙션 가능한 첫 번째 요소 반환."""
        count = min(locator.count(), 10)  # 최대 10개만 확인
        for i in range(count):
            candidate = locator.nth(i)
            if self._is_interactable(candidate):
                return candidate
        return None

    def _resolve_locator(self, target: str | None):
        """target 문자열 → Playwright locator.

        지원 형태:
        1. 'role "name"' → page.get_by_role(role, name=name)
           예: 'button "Create a free form"', 'tab "HR"', 'textbox "Form title"'
        2. 'text: ...' → page.get_by_text(text)
        3. 그 외 → page.get_by_text(target) fallback
        """
        if not target:
            return None

        # curly quotes 정규화
        target = self._normalize_quotes(target)

        try:
            # 패턴 1: role "name" (접근성 스냅샷 형태)
            match = re.match(r'^(\w+)\s+"(.+)"$', target)
            if match:
                role, name = match.group(1), match.group(2)
                locator = self._page.get_by_role(role, name=name)
                result = self._find_first_interactable(locator)
                if result:
                    return result
                # role만으로 안 되면 텍스트로 fallback
                locator = self._page.get_by_text(name, exact=False)
                result = self._find_first_interactable(locator)
                if result:
                    return result

            # 패턴 2: 일반 텍스트
            locator = self._page.get_by_text(target, exact=False)
            result = self._find_first_interactable(locator)
            if result:
                return result

            # 패턴 3: role만 (name 없이)
            locator = self._page.get_by_role(target)
            result = self._find_first_interactable(locator)
            if result:
                return result

            logger.warning("요소 못 찾음: %s", target)
            return None

        except Exception as e:
            logger.warning("locator 해석 실패: %s — %s", target, e)
            return None

    def _highlight(self, locator, color: str = "#ff2222") -> None:
        """headless=false일 때 요소 하이라이트."""
        if self._headless:
            return
        try:
            locator.evaluate(f"""el => {{
                const box = el.getBoundingClientRect();
                const overlay = document.createElement('div');
                overlay.style.cssText = `
                    position: fixed;
                    left: ${{box.left - 3}}px; top: ${{box.top - 3}}px;
                    width: ${{box.width + 6}}px; height: ${{box.height + 6}}px;
                    border: 3px solid {color}; border-radius: 4px;
                    background: {color}22; z-index: 999999;
                    pointer-events: none;
                `;
                document.body.appendChild(overlay);
                setTimeout(() => overlay.remove(), 1200);
            }}""")
            time.sleep(0.6)
        except Exception:
            pass

    def _wait_for_idle(self, timeout_ms: int = 5000) -> None:
        """페이지 로드 대기. SPA 렌더링까지 기다림."""
        try:
            self._page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
            # networkidle 대기 — SPA의 API 호출 완료까지
            self._page.wait_for_load_state("networkidle", timeout=timeout_ms)
            # 추가 대기 — SPA 프레임워크 렌더링 완료
            self._page.wait_for_timeout(2500)
        except Exception:
            pass
