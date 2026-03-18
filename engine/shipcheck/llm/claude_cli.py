"""Claude Code CLI -p 모드 subprocess 래퍼.

두 가지 모드:
1. 텍스트 전용: `claude -p --output-format text` (기존)
2. 멀티모달: `claude -p --verbose --input-format stream-json --output-format stream-json`
   → base64 이미지를 포함한 메시지 전송 가능
"""

from __future__ import annotations

import base64
import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ClaudeCliError(Exception):
    """Claude CLI 호출 실패."""


class ClaudeCli:
    """Claude Code CLI -p 모드로 단일 LLM 호출."""

    def __init__(
        self,
        model: str = "sonnet",
        timeout_seconds: int = 120,
        max_retries: int = 2,
    ) -> None:
        self._model = model
        self._timeout = timeout_seconds
        self._max_retries = max_retries

    def complete(
        self,
        prompt: str,
        system: str = "",
    ) -> str:
        """텍스트 전용 LLM 호출."""
        return self._retry(lambda: self._call_text(prompt, system))

    def complete_json(
        self,
        prompt: str,
        system: str = "",
    ) -> dict[str, Any]:
        """텍스트 전용 LLM 호출 → JSON 파싱."""
        raw = self.complete(prompt, system)
        return self._parse_json(raw)

    def complete_with_image(
        self,
        prompt: str,
        image_path: Path | None = None,
        image_base64: str | None = None,
        system: str = "",
    ) -> str:
        """이미지 포함 멀티모달 LLM 호출.

        Args:
            prompt: 텍스트 프롬프트
            image_path: 스크린샷 PNG 파일 경로 (image_base64와 둘 중 하나)
            image_base64: base64 인코딩된 이미지 (image_path와 둘 중 하나)
            system: 시스템 프롬프트
        """
        return self._retry(lambda: self._call_multimodal(prompt, image_path, image_base64, system))

    def complete_json_with_image(
        self,
        prompt: str,
        image_path: Path | None = None,
        image_base64: str | None = None,
        system: str = "",
    ) -> dict[str, Any]:
        """이미지 포함 멀티모달 LLM 호출 → JSON 파싱."""
        raw = self.complete_with_image(prompt, image_path, image_base64, system)
        return self._parse_json(raw)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _retry(self, fn) -> str:
        for attempt in range(1, self._max_retries + 1):
            try:
                return fn()
            except (subprocess.TimeoutExpired, ClaudeCliError) as e:
                logger.warning("Claude CLI 시도 %d/%d 실패: %s", attempt, self._max_retries, e)
                if attempt == self._max_retries:
                    raise
                time.sleep(2 ** attempt)
        raise ClaudeCliError("max retries 초과")

    def _call_text(self, prompt: str, system: str) -> str:
        """텍스트 전용 모드: claude -p --output-format text"""
        cmd = ["claude", "-p", "--model", self._model, "--output-format", "text"]
        if system:
            cmd.extend(["--system-prompt", system])

        logger.debug("Claude CLI [text]: model=%s, prompt_len=%d", self._model, len(prompt))
        start = time.time()

        result = subprocess.run(
            cmd, input=prompt,
            capture_output=True, text=True, timeout=self._timeout,
        )

        elapsed = time.time() - start
        logger.debug("Claude CLI 응답: %.1fs, stdout_len=%d", elapsed, len(result.stdout))

        if result.returncode != 0:
            raise ClaudeCliError(f"returncode={result.returncode}, stderr={result.stderr[:500]}")

        response = result.stdout.strip()
        if not response:
            raise ClaudeCliError("빈 응답")
        return response

    def _call_multimodal(
        self,
        prompt: str,
        image_path: Path | None,
        image_base64: str | None,
        system: str,
    ) -> str:
        """멀티모달 모드: stream-json으로 이미지 + 텍스트 전송."""
        # 이미지 base64 준비
        if image_path and not image_base64:
            image_bytes = Path(image_path).read_bytes()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # content blocks 구성
        content: list[dict[str, Any]] = []
        if image_base64:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_base64,
                },
            })
        content.append({"type": "text", "text": prompt})

        # stream-json input 메시지
        input_msg = json.dumps({
            "type": "user",
            "message": {
                "role": "user",
                "content": content,
            },
        })

        cmd = [
            "claude", "-p", "--verbose",
            "--model", self._model,
            "--input-format", "stream-json",
            "--output-format", "stream-json",
        ]
        if system:
            cmd.extend(["--system-prompt", system])

        logger.debug(
            "Claude CLI [multimodal]: model=%s, prompt_len=%d, has_image=%s",
            self._model, len(prompt), bool(image_base64),
        )
        start = time.time()

        result = subprocess.run(
            cmd, input=input_msg,
            capture_output=True, text=True, timeout=self._timeout,
        )

        elapsed = time.time() - start
        logger.debug("Claude CLI 응답: %.1fs, stdout_len=%d", elapsed, len(result.stdout))

        if result.returncode != 0:
            raise ClaudeCliError(f"returncode={result.returncode}, stderr={result.stderr[:500]}")

        # stream-json 출력에서 assistant 텍스트 추출
        response_text = ""
        for line in result.stdout.strip().splitlines():
            try:
                obj = json.loads(line)
                if obj.get("type") == "assistant":
                    for block in obj.get("message", {}).get("content", []):
                        if block.get("type") == "text":
                            response_text += block["text"]
                elif obj.get("type") == "result":
                    # result 메시지에도 텍스트가 있을 수 있음
                    if obj.get("result"):
                        response_text = response_text or obj["result"]
            except json.JSONDecodeError:
                continue

        if not response_text.strip():
            raise ClaudeCliError("빈 응답 (multimodal)")
        return response_text.strip()

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        """LLM 응답에서 JSON 추출. ```json``` 블록도 처리."""
        text = raw.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            json_lines = []
            inside = False
            for line in lines:
                if line.startswith("```") and not inside:
                    inside = True
                    continue
                if line.startswith("```") and inside:
                    break
                if inside:
                    json_lines.append(line)
            text = "\n".join(json_lines)
        return json.loads(text)
