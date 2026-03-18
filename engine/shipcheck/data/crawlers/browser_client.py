"""browser-operator REST API Python 클라이언트.

로컬 Chrome + 확장 프로그램을 통해 실제 브라우저를 제어한다.
Cloudflare 등 봇 탐지를 우회하기 위해 사람의 실제 브라우저를 사용.

사전 조건:
    1. browser-operator 서버 실행 중 (npm run dev)
    2. Chrome에 browser-operator 확장 로드 + 연결됨
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
import time
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import URLError

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "http://127.0.0.1:9002"


class BrowserOperatorError(Exception):
    pass


class BrowserClient:
    """browser-operator 서버에 REST API로 명령을 보내는 동기 클라이언트."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def _post(self, method: str, params: dict[str, Any] | None = None) -> Any:
        """POST /api/command 호출."""
        payload = json.dumps({"method": method, "params": params or {}}).encode()
        req = Request(
            f"{self.base_url}/api/command",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read())
                if "error" in body and body["error"]:
                    raise BrowserOperatorError(body["error"])
                return body.get("result")
        except URLError as e:
            raise BrowserOperatorError(
                f"browser-operator 서버 연결 실패 ({self.base_url}). "
                "서버가 실행 중이고 Chrome 확장이 연결되어 있는지 확인하세요."
            ) from e

    # -- 상태 확인 --

    def status(self) -> dict:
        """서버 상태 확인."""
        req = Request(f"{self.base_url}/status")
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    def is_ready(self) -> bool:
        """서버 + 확장 연결 상태 확인."""
        try:
            st = self.status()
            return st.get("extensionConnected", False)
        except Exception:
            return False

    # -- 네비게이션 --

    def navigate(self, url: str, **kwargs: Any) -> Any:
        return self._post("browser.navigate", {"url": url, **kwargs})

    # -- 페이지 콘텐츠 --

    def extract_text(self, **kwargs: Any) -> str:
        """페이지 전체 텍스트 추출."""
        result = self._post("browser.extractText", kwargs)
        # CDP Runtime.evaluate 결과 구조: { result: { value: "..." } }
        if isinstance(result, dict):
            inner = result.get("result", {})
            if isinstance(inner, dict):
                return inner.get("value", "")
        return str(result) if result else ""

    def evaluate(self, expression: str, **kwargs: Any) -> Any:
        """JavaScript 실행."""
        result = self._post("browser.evaluate", {"expression": expression, **kwargs})
        if isinstance(result, dict):
            inner = result.get("result", {})
            if isinstance(inner, dict):
                return inner.get("value")
        return result

    def screenshot(self, fmt: str = "png", **kwargs: Any) -> str:
        """스크린샷 (base64 인코딩)."""
        result = self._post("browser.screenshot", {"format": fmt, **kwargs})
        if isinstance(result, dict):
            return result.get("data", "")
        return ""

    # -- 인터랙션 --

    def click(self, selector: str | None = None, x: int | None = None, y: int | None = None, **kwargs: Any) -> Any:
        params: dict[str, Any] = {**kwargs}
        if selector:
            params["selector"] = selector
        elif x is not None and y is not None:
            params["x"] = x
            params["y"] = y
        return self._post("browser.click", params)

    def type_text(self, text: str, **kwargs: Any) -> Any:
        return self._post("browser.type", {"text": text, **kwargs})

    def fill(self, selector: str, value: str, **kwargs: Any) -> Any:
        return self._post("browser.fill", {"selector": selector, "value": value, **kwargs})

    # -- 탭 관리 --

    def tabs(self) -> list[dict]:
        result = self._post("browser.tabs")
        if isinstance(result, dict):
            return result.get("tabs", [])
        return []

    def attach_to_tab(self, tab_id: int) -> Any:
        return self._post("browser.attachToTab", {"tabId": tab_id})

    def new_tab(self, url: str = "about:blank") -> int:
        """새 탭을 열고 탭 ID를 반환한다. 기존 탭을 방해하지 않음."""
        before = {t["id"] for t in self.tabs()}

        # 방법 1: CDP Target.createTarget (팝업 차단 우회)
        active = self.active_tab_id
        if active is not None:
            try:
                self.attach_to_tab(active)
                self.cdp(active, "Target.createTarget", {"url": url})
                time.sleep(1.5)
                after = self.tabs()
                new_tabs = [t for t in after if t["id"] not in before]
                if new_tabs:
                    new_id = new_tabs[0]["id"]
                    self.attach_to_tab(new_id)
                    logger.info(f"새 탭 생성 (CDP): id={new_id}")
                    return new_id
            except Exception:
                pass

        # 방법 2: window.open 폴백
        try:
            self.evaluate(f"window.open({json.dumps(url)}, '_blank')")
            time.sleep(1.5)
            after = self.tabs()
            new_tabs = [t for t in after if t["id"] not in before]
            if new_tabs:
                new_id = new_tabs[0]["id"]
                self.attach_to_tab(new_id)
                logger.info(f"새 탭 생성 (window.open): id={new_id}")
                return new_id
        except Exception:
            pass

        raise BrowserOperatorError("새 탭 생성 실패")

    def close_tab(self, tab_id: int) -> None:
        """특정 탭 닫기."""
        self.cdp(tab_id, "Page.close", {})

    @property
    def active_tab_id(self) -> int | None:
        """현재 활성 탭 ID."""
        for t in self.tabs():
            if t.get("active"):
                return t["id"]
        return None

    # -- CDP 직접 접근 --

    def cdp(self, tab_id: int, method: str, params: dict | None = None) -> Any:
        return self._post("cdp", {"tabId": tab_id, "method": method, "params": params or {}})

    # -- 유틸리티 --

    def wait(self, min_s: float = 1.5, max_s: float = 4.0) -> None:
        """사람처럼 보이는 랜덤 딜레이."""
        time.sleep(random.uniform(min_s, max_s))

    def scroll_down(self, pixels: int = 500, **kwargs: Any) -> Any:
        """페이지 아래로 스크롤."""
        return self.evaluate(f"window.scrollBy(0, {pixels})", **kwargs)

    def scroll_to_bottom(self, **kwargs: Any) -> Any:
        """페이지 끝까지 스크롤."""
        return self.evaluate("window.scrollTo(0, document.body.scrollHeight)", **kwargs)

    def get_page_url(self) -> str:
        """현재 페이지 URL."""
        result = self.evaluate("window.location.href")
        return str(result) if result else ""

    def get_page_html(self) -> str:
        """현재 페이지 HTML."""
        result = self.evaluate("document.documentElement.outerHTML")
        return str(result) if result else ""

    def query_selector_all_text(self, selector: str) -> list[str]:
        """셀렉터에 매칭되는 모든 요소의 텍스트 반환."""
        result = self.evaluate(
            f"Array.from(document.querySelectorAll({json.dumps(selector)}))"
            f".map(el => el.innerText.trim())"
        )
        return result if isinstance(result, list) else []

    def query_selector_all_attrs(self, selector: str, attrs: list[str]) -> list[dict]:
        """셀렉터에 매칭되는 모든 요소에서 지정된 속성들 추출."""
        attrs_js = json.dumps(attrs)
        result = self.evaluate(
            f"Array.from(document.querySelectorAll({json.dumps(selector)}))"
            f".map(el => {{"
            f"  const obj = {{}};"
            f"  {attrs_js}.forEach(a => obj[a] = a === 'innerText' ? el.innerText.trim() : el.getAttribute(a));"
            f"  return obj;"
            f"}})"
        )
        return result if isinstance(result, list) else []
