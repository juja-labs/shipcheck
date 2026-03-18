"""ExperimentRunner — Claude CLI 페르소나 에이전트 오케스트레이션.

각 페르소나를 독립된 `claude -p` subprocess로 실행.
asyncio + Semaphore로 동시성 제어.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import tempfile
import time
import uuid
from pathlib import Path

import yaml

from ..data.exporter import ANOVAExporter
from ..layer1_persona.models import PersonaProfile
from ..prompt_builder import build_system_prompt

logger = logging.getLogger(__name__)

ENGINE_DIR = Path(__file__).resolve().parent.parent.parent  # engine/


def load_personas(persona_dir: Path) -> list[Path]:
    """페르소나 YAML 파일 경로 목록 반환."""
    return sorted(persona_dir.glob("*.yaml"))


async def _run_session_init(
    persona_yaml: Path,
    product_url: str,
    product_name: str,
    session_id: str,
    state_dir: str,
) -> dict:
    """session_init 도구 실행."""
    cmd = [
        "python3", "-m", "shipcheck.tools.session_init",
        "--persona", str(persona_yaml),
        "--product-url", product_url,
        "--product-name", product_name,
        "--session-id", session_id,
        "--state-dir", state_dir,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd, cwd=str(ENGINE_DIR),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"session_init 실패: {stderr.decode()}")
    return json.loads(stdout.decode())


async def _run_one_persona(
    persona_yaml: Path,
    product_name: str,
    product_url: str,
    output_dir: Path,
    model: str,
    max_steps: int,
    state_dir: str,
    semaphore: asyncio.Semaphore,
    session_idx: int,
    total_sessions: int,
) -> str:
    """단일 페르소나 세션 실행."""
    async with semaphore:
        persona_id = persona_yaml.stem
        session_id = f"{persona_id}_{product_name}_{uuid.uuid4().hex[:6]}"
        tag = f"[{session_idx}/{total_sessions}] {persona_id} → {product_name}"

        logger.info("%s 시작 (session_id=%s)", tag, session_id)
        start = time.time()

        try:
            # 1. 세션 초기화
            init_result = await _run_session_init(
                persona_yaml, product_url, product_name, session_id, state_dir,
            )
            logger.info("%s 초기화 완료: %s (%s)", tag, init_result["persona_name"], init_result["segment"])

            # 2. system prompt 생성
            system_prompt = build_system_prompt(
                persona_yaml_path=str(persona_yaml),
                session_id=session_id,
                product_url=product_url,
                product_name=product_name,
                engine_dir=str(ENGINE_DIR),
                output_dir=str(output_dir),
                state_dir=state_dir,
                max_steps=max_steps,
            )

            # 3. system prompt를 임시 파일로 저장 (argv 길이 제한 회피)
            prompt_file = tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", prefix=f"shipcheck_{session_id}_",
                delete=False,
            )
            prompt_file.write(system_prompt)
            prompt_file.close()
            prompt_path = prompt_file.name

            try:
                # max_turns: 스텝당 약 4턴 (snapshot + action + step_update + 사고)
                max_turns = max_steps * 4
                cmd = [
                    "claude", "-p",
                    "--model", model,
                    "--system-prompt", f"$(cat {prompt_path})",
                    "--allowedTools", "Bash",
                    "--max-turns", str(max_turns),
                    "--output-format", "json",
                    "--permission-mode", "bypassPermissions",
                ]

                proc = await asyncio.create_subprocess_shell(
                    " ".join(cmd),
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(ENGINE_DIR),
                )

                # 초기 메시지
                initial_msg = (
                    f"{product_url}을 사용하십시오. "
                    f"세션 ID: {session_id}. "
                    f"playwright-cli open {product_url} 으로 시작하세요."
                )

                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(input=initial_msg.encode()),
                    timeout=600,  # 10분 타임아웃
                )

                elapsed = time.time() - start

                if proc.returncode != 0:
                    logger.error("%s 실패 (rc=%d): %s", tag, proc.returncode, stderr.decode()[:500])
                    return f"{tag} 실패 (rc={proc.returncode}, {elapsed:.0f}s)"

                logger.info("%s 완료 (%.0fs)", tag, elapsed)
                return f"{tag} 완료 ({elapsed:.0f}s)"
            finally:
                os.unlink(prompt_path)

        except asyncio.TimeoutError:
            logger.error("%s 타임아웃 (10분)", tag)
            return f"{tag} 타임아웃"
        except Exception as e:
            logger.error("%s 에러: %s", tag, e)
            return f"{tag} 에러: {e}"


class ExperimentRunner:
    """실험 전체 실행. 페르소나별 claude -p subprocess 병렬 실행."""

    def __init__(self, config_path: Path) -> None:
        self.config = yaml.safe_load(config_path.read_text())
        self.experiment_id = self.config.get(
            "experiment_id", f"exp_{uuid.uuid4().hex[:8]}"
        )

    def run(self) -> Path:
        """실험 실행. output 디렉토리 경로 반환."""
        return asyncio.run(self._run_async())

    async def _run_async(self) -> Path:
        products = self.config["products"]
        max_steps = self.config.get("max_steps", 25)
        model = self.config.get("llm_model", "sonnet")
        concurrency = self.config.get("concurrency", 2)
        persona_dir = Path(self.config["persona_dir"])
        state_dir = self.config.get("state_dir", "/tmp")

        persona_yamls = load_personas(persona_dir)
        output_dir = Path("runs") / self.experiment_id
        output_dir.mkdir(parents=True, exist_ok=True)

        # 세션 목록: persona × product
        sessions = []
        for product in products:
            for yaml_path in persona_yamls:
                sessions.append((yaml_path, product["name"], product["url"]))

        total = len(sessions)
        logger.info(
            "실험 시작: id=%s, personas=%d, products=%d, sessions=%d, concurrency=%d",
            self.experiment_id, len(persona_yamls), len(products), total, concurrency,
        )
        start = time.time()

        # 병렬 실행
        semaphore = asyncio.Semaphore(concurrency)
        tasks = [
            _run_one_persona(
                persona_yaml=yaml_path,
                product_name=prod_name,
                product_url=prod_url,
                output_dir=output_dir,
                model=model,
                max_steps=max_steps,
                state_dir=state_dir,
                semaphore=semaphore,
                session_idx=idx,
                total_sessions=total,
            )
            for idx, (yaml_path, prod_name, prod_url) in enumerate(sessions, 1)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                logger.error("세션 예외: %s", r)
            else:
                logger.info(r)

        elapsed = time.time() - start
        logger.info(
            "실험 완료: %d 세션, %.1f분 소요 (concurrency=%d)",
            total, elapsed / 60, concurrency,
        )

        # ANOVA CSV
        try:
            exporter = ANOVAExporter(output_dir)
            csv_path = exporter.export()
            logger.info("ANOVA CSV: %s", csv_path)
        except Exception as e:
            logger.warning("ANOVA CSV 생성 실패: %s", e)

        # 메타데이터
        meta = {
            "experiment_id": self.experiment_id,
            "total_personas": len(persona_yamls),
            "total_products": len(products),
            "total_sessions": total,
            "concurrency": concurrency,
            "elapsed_seconds": elapsed,
            "config": self.config,
        }
        meta_path = output_dir / "experiment.json"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2, default=str))

        return output_dir
