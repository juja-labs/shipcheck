"""PlaywrightCliEnv — playwright-cli subprocess 래퍼.

playwright-cli의 스냅샷(ref 기반) + 안정적 액션 실행을 활용.
CDP 직접 호출 760줄 → 이 파일 ~100줄로 교체.

사용법:
    async with PlaywrightCliEnv("session1") as env:
        obs = await env.navigate("https://tally.so")
        obs = await env.click("e15")
        obs = await env.type_text("/")
"""

from __future__ import annotations

import asyncio
import logging
import shlex
import uuid
from pathlib import Path
from typing import Any

from ..core.types import Observation

logger = logging.getLogger(__name__)


class PlaywrightCliEnv:
    """playwright-cli subprocess 래퍼."""

    def __init__(
        self,
        headless: bool = True,
        screenshot_dir: Path | None = None,
        viewport: dict[str, int] | None = None,
    ) -> None:
        self._headless = headless
        self._screenshot_dir = screenshot_dir
        self._viewport = viewport or {"width": 1280, "height": 720}
        self._session = f"sc_{uuid.uuid4().hex[:8]}"
        self._step_count = 0
        self._prev_url = ""
        self._opened = False

    async def __aenter__(self) -> PlaywrightCliEnv:
        if self._screenshot_dir:
            self._screenshot_dir.mkdir(parents=True, exist_ok=True)
        return self

    async def __aexit__(self, *args) -> None:
        if self._opened:
            try:
                await self._run(f"playwright-cli -s={self._session} close")
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    async def navigate(self, url: str) -> Observation:
        """브라우저 열기 + URL 이동."""
        logger.info("탐색 시작: %s", url)

        if not self._opened:
            cmd = f"playwright-cli -s={self._session} open {shlex.quote(url)}"
            await self._run(cmd)
            self._opened = True
            # 뷰포트 설정
            vw, vh = self._viewport["width"], self._viewport["height"]
            await self._run(f"playwright-cli -s={self._session} resize {vw} {vh}")
        else:
            await self._run(
                f"playwright-cli -s={self._session} goto {shlex.quote(url)}"
            )

        return await self._observe()

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    async def click(self, ref: str) -> tuple[Observation, bool]:
        """ref 기반 클릭."""
        self._step_count += 1
        result = await self._run(
            f"playwright-cli -s={self._session} click {ref}"
        )
        succeeded = "Error" not in result and "error" not in result.lower()
        obs = await self._observe()
        url_changed = obs.url != self._prev_url
        self._prev_url = obs.url
        return obs, succeeded or url_changed

    async def fill(self, ref: str, text: str) -> tuple[Observation, bool]:
        """ref 기반 텍스트 입력 (input/textarea/contenteditable)."""
        self._step_count += 1
        result = await self._run(
            f"playwright-cli -s={self._session} fill {ref} {shlex.quote(text)}"
        )
        succeeded = "Error" not in result and "error" not in result.lower()
        obs = await self._observe()
        return obs, succeeded

    async def type_text(self, text: str) -> tuple[Observation, bool]:
        """현재 포커스 요소에 타이핑 (keydown+keyup 발생)."""
        self._step_count += 1
        result = await self._run(
            f"playwright-cli -s={self._session} type {shlex.quote(text)}"
        )
        succeeded = "Error" not in result and "error" not in result.lower()
        obs = await self._observe()
        return obs, succeeded

    async def press(self, key: str) -> tuple[Observation, bool]:
        """키 입력 (Enter, Tab, Escape 등)."""
        self._step_count += 1
        result = await self._run(
            f"playwright-cli -s={self._session} press {key}"
        )
        succeeded = "Error" not in result and "error" not in result.lower()
        obs = await self._observe()
        return obs, succeeded

    async def scroll(self, direction: str = "down") -> tuple[Observation, bool]:
        """스크롤."""
        self._step_count += 1
        delta = 400 if direction == "down" else -400
        await self._run(
            f"playwright-cli -s={self._session} mousewheel 0 {delta}"
        )
        obs = await self._observe()
        return obs, True

    async def go_back(self) -> tuple[Observation, bool]:
        """뒤로 가기."""
        self._step_count += 1
        await self._run(f"playwright-cli -s={self._session} go-back")
        obs = await self._observe()
        return obs, True

    async def hover(self, ref: str) -> tuple[Observation, bool]:
        """ref 기반 호버."""
        self._step_count += 1
        result = await self._run(
            f"playwright-cli -s={self._session} hover {ref}"
        )
        succeeded = "Error" not in result
        obs = await self._observe()
        return obs, succeeded

    async def select(self, ref: str, value: str) -> tuple[Observation, bool]:
        """ref 기반 select 옵션 선택."""
        self._step_count += 1
        result = await self._run(
            f"playwright-cli -s={self._session} select {ref} {shlex.quote(value)}"
        )
        succeeded = "Error" not in result
        obs = await self._observe()
        return obs, succeeded

    # ------------------------------------------------------------------
    # Observation
    # ------------------------------------------------------------------

    async def take_screenshot(self, name: str) -> Path | None:
        """스크린샷 저장."""
        if not self._screenshot_dir:
            return None
        path = self._screenshot_dir / f"{name}.png"
        await self._run(
            f"playwright-cli -s={self._session} screenshot --filename={path}"
        )
        return path if path.exists() else None

    async def _observe(self) -> Observation:
        """스냅샷 촬영 → Observation 생성."""
        snapshot_raw = await self._run(
            f"playwright-cli -s={self._session} snapshot"
        )

        # 스냅샷에서 URL과 제목 추출
        url = self._extract_field(snapshot_raw, "Page URL:")
        title = self._extract_field(snapshot_raw, "Page Title:")
        snapshot_text = self._extract_snapshot(snapshot_raw)

        # 인터랙티브 요소 수 (ref= 개수로 추정)
        element_count = snapshot_text.count("[ref=")

        self._prev_url = url or self._prev_url

        return Observation(
            url=url or self._prev_url,
            page_title=title or "",
            html_summary=snapshot_text,
            element_count=element_count,
            text_length=len(snapshot_text),
            scroll_ratio=0.0,
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _run(self, cmd: str, timeout: int = 30) -> str:
        """subprocess 실행."""
        logger.debug("pw-cli: %s", cmd.split("playwright-cli ")[-1])
        try:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout
            )
            output = stdout.decode("utf-8", errors="replace")
            if proc.returncode != 0:
                err = stderr.decode("utf-8", errors="replace")
                logger.warning("pw-cli 에러 (rc=%d): %s", proc.returncode, err[:200])
            return output
        except asyncio.TimeoutError:
            logger.warning("pw-cli 타임아웃: %s", cmd[:100])
            proc.kill()
            return ""
        except Exception as e:
            logger.error("pw-cli 실행 실패: %s", e)
            return ""

    @staticmethod
    def _extract_field(raw: str, prefix: str) -> str | None:
        """스냅샷 출력에서 특정 필드 추출."""
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith(prefix):
                return line[len(prefix):].strip()
        return None

    @staticmethod
    def _extract_snapshot(raw: str) -> str:
        """스냅샷 출력에서 YAML 스냅샷 부분만 추출."""
        # playwright-cli snapshot 출력 형식:
        # ### Page
        # - Page URL: ...
        # - Page Title: ...
        # ### Snapshot
        # [Snapshot](path.yml)
        #
        # 실제 스냅샷 내용은 파일에 저장됨 → 파일 읽기
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("[Snapshot](") and line.endswith(")"):
                path = line[len("[Snapshot]("):-1]
                try:
                    return Path(path).read_text(encoding="utf-8")
                except Exception:
                    pass

        # fallback: ### Snapshot 이후 텍스트 전체
        in_snapshot = False
        lines = []
        for line in raw.splitlines():
            if "### Snapshot" in line or "Snapshot" in line and "[ref=" in raw:
                in_snapshot = True
                continue
            if in_snapshot:
                lines.append(line)

        return "\n".join(lines) if lines else raw
