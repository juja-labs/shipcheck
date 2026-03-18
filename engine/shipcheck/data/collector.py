"""DataCollector — JSONL 기록 + 세션 집계. Thread-safe."""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import asdict
from pathlib import Path

from ..core.types import StepLog, SessionLog

logger = logging.getLogger(__name__)


class DataCollector:
    """실험 데이터 수집. JSONL 파일에 thread-safe하게 기록."""

    def __init__(self, experiment_id: str, output_dir: Path | None = None) -> None:
        self.experiment_id = experiment_id
        self.output_dir = output_dir or Path("runs") / experiment_id
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._steps_path = self.output_dir / "steps.jsonl"
        self._sessions_path = self.output_dir / "sessions.jsonl"

        self._steps_path.touch()
        self._sessions_path.touch()

        self._step_count = 0
        self._session_count = 0
        self._lock = threading.Lock()

    def record_step(self, step: StepLog) -> None:
        """StepLog를 JSONL에 기록."""
        data = asdict(step)
        data["experiment_id"] = self.experiment_id
        self._append_jsonl(self._steps_path, data)
        with self._lock:
            self._step_count += 1

    def record_session(self, session: SessionLog) -> None:
        """SessionLog를 JSONL에 기록."""
        data = asdict(session)
        data["experiment_id"] = self.experiment_id
        self._append_jsonl(self._sessions_path, data)
        with self._lock:
            self._session_count += 1

    @property
    def stats(self) -> dict[str, int]:
        with self._lock:
            return {"steps": self._step_count, "sessions": self._session_count}

    def _append_jsonl(self, path: Path, data: dict) -> None:
        """JSONL 파일에 한 줄 추가. Lock으로 동시 쓰기 방지."""
        line = json.dumps(data, ensure_ascii=False, default=str) + "\n"
        with self._lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line)
