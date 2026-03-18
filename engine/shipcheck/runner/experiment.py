"""ExperimentRunner — 전체 실험 오케스트레이션.

ThreadPoolExecutor로 병렬 실행. 각 세션은 독립된 브라우저 + LLM 프로세스.
각 스레드 안에서 asyncio.run()으로 AsyncBrowserEnv를 구동한다.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

from ..browser.pw_cli_env import PlaywrightCliEnv
from ..data.collector import DataCollector
from ..data.exporter import ANOVAExporter
from ..layer1_persona.models import PersonaProfile
from ..llm.claude_cli import ClaudeCli
from .session import SessionRunner
from .naive_session import NaiveSessionRunner

logger = logging.getLogger(__name__)

_PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"
_completed_lock = threading.Lock()


def load_prompts() -> dict[str, str]:
    """프롬프트 템플릿 로드."""
    return {
        # 새 구조: 페르소나(스크린샷) + 액션 실행기(접근성 트리+스크린샷)
        "persona_react": (_PROMPTS_DIR / "persona_react.txt").read_text(),
        "action_executor": (_PROMPTS_DIR / "action_executor.txt").read_text(),
        # legacy (이전 버전 호환)
        "emotion_eval": (_PROMPTS_DIR / "emotion_eval.txt").read_text(),
        "action_decide": (_PROMPTS_DIR / "action_decide.txt").read_text(),
        # ablation
        "naive_single": (_PROMPTS_DIR / "naive_single.txt").read_text(),
    }


def load_personas(persona_dir: Path) -> list[PersonaProfile]:
    """YAML 페르소나 파일들 로드."""
    profiles = []
    for path in sorted(persona_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        profiles.append(PersonaProfile.from_dict(data))
    return profiles


def _run_one_session(
    persona: PersonaProfile,
    product_name: str,
    product_url: str,
    collector: DataCollector,
    prompts: dict[str, str],
    model: str,
    max_steps: int,
    headless: bool,
    session_idx: int,
    total_sessions: int,
    mode: str = "full",  # "full" | "naive"
) -> str:
    """단일 세션 실행 (스레드 안에서 호출됨).

    각 스레드가 asyncio.run()으로 자체 이벤트 루프를 생성하여
    AsyncBrowserEnv를 구동한다.
    """
    return asyncio.run(
        _run_one_session_async(
            persona, product_name, product_url, collector, prompts,
            model, max_steps, headless, session_idx, total_sessions, mode,
        )
    )


async def _run_one_session_async(
    persona: PersonaProfile,
    product_name: str,
    product_url: str,
    collector: DataCollector,
    prompts: dict[str, str],
    model: str,
    max_steps: int,
    headless: bool,
    session_idx: int,
    total_sessions: int,
    mode: str = "full",
) -> str:
    """비동기 세션 실행."""
    llm = ClaudeCli(model=model)
    mode_tag = "" if mode == "full" else f"[{mode.upper()}]"
    tag = f"[{session_idx}/{total_sessions}]{mode_tag} {persona.name} → {product_name}"
    logger.info("%s 시작", tag)

    try:
        async with PlaywrightCliEnv(
            headless=headless,
            screenshot_dir=collector.output_dir / "screenshots",
        ) as env:
            if mode == "naive":
                raise NotImplementedError(
                    "NaiveSessionRunner는 아직 async 미지원. "
                    "mode='full'로 실행하거나 NaiveSessionRunner를 async로 전환 필요."
                )
            else:
                runner = SessionRunner(
                    profile=persona,
                    browser_env=env,
                    product_url=product_url,
                    product_name=product_name,
                    collector=collector,
                    llm=llm,
                    prompts=prompts,
                    max_steps=max_steps,
                )
                session_log = await runner.run()
            return f"{tag} 완료 (steps={session_log.total_steps}, {session_log.terminated_by})"
    except Exception as e:
        logger.error("%s 실패: %s", tag, e)
        return f"{tag} 실패: {e}"


class ExperimentRunner:
    """실험 전체 실행. 병렬 지원."""

    def __init__(self, config_path: Path) -> None:
        self.config = yaml.safe_load(config_path.read_text())
        self.experiment_id = self.config.get(
            "experiment_id", f"exp_{uuid.uuid4().hex[:8]}"
        )

    def run(self) -> Path:
        """실험 실행. output 디렉토리 경로 반환."""
        products = self.config["products"]
        max_steps = self.config.get("max_steps", 25)
        model = self.config.get("llm_model", "sonnet")
        headless = self.config.get("headless", True)
        concurrency = self.config.get("concurrency", 2)
        persona_dir = Path(self.config["persona_dir"])

        # mode: "full" (파이프라인), "naive" (단일 콜), "ablation" (둘 다 실행)
        mode = self.config.get("mode", "full")

        personas = load_personas(persona_dir)
        prompts = load_prompts()
        collector = DataCollector(self.experiment_id)

        # 전체 세션 목록 생성: (persona, product_name, product_url, mode)
        sessions = []
        modes = ["full", "naive"] if mode == "ablation" else [mode]
        for m in modes:
            for product in products:
                for persona in personas:
                    sessions.append((persona, product["name"], product["url"], m))

        total = len(sessions)
        logger.info(
            "실험 시작: id=%s, personas=%d, products=%d, sessions=%d, concurrency=%d, mode=%s",
            self.experiment_id, len(personas), len(products), total, concurrency, mode,
        )
        start = time.time()

        # 병렬 실행
        completed = 0
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = {}
            for idx, (persona, prod_name, prod_url, m) in enumerate(sessions, 1):
                f = pool.submit(
                    _run_one_session,
                    persona=persona,
                    product_name=prod_name,
                    product_url=prod_url,
                    collector=collector,
                    prompts=prompts,
                    model=model,
                    max_steps=max_steps,
                    headless=headless,
                    session_idx=idx,
                    total_sessions=total,
                    mode=m,
                )
                futures[f] = idx

            for future in as_completed(futures):
                completed += 1
                result = future.result()
                logger.info("(%d/%d 완료) %s", completed, total, result)

        elapsed = time.time() - start
        logger.info(
            "실험 완료: %d 세션, %.1f분 소요 (concurrency=%d)",
            total, elapsed / 60, concurrency,
        )

        # ANOVA CSV
        exporter = ANOVAExporter(collector.output_dir)
        csv_path = exporter.export()
        logger.info("ANOVA CSV: %s", csv_path)

        # 메타데이터
        meta = {
            "experiment_id": self.experiment_id,
            "total_personas": len(personas),
            "total_products": len(products),
            "total_sessions": total,
            "concurrency": concurrency,
            "elapsed_seconds": elapsed,
            "config": self.config,
            "stats": collector.stats,
        }
        meta_path = collector.output_dir / "experiment.json"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2, default=str))

        return collector.output_dir
