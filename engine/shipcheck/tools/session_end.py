#!/usr/bin/env python3
"""세션 종료 — SessionLog 기록 + 리뷰 생성.

세션이 끝났을 때 (이탈, 목표 달성, max_steps) Claude가 호출.

사용법:
    python3 -m shipcheck.tools.session_end \
        --session-id abc123 \
        --terminated-by abandoned \
        --output-dir runs/exp_001

출력 (stdout JSON):
    {
        "session_id": "abc123",
        "persona_id": "b005",
        "total_steps": 12,
        "terminated_by": "abandoned",
        "final_pad": {"pleasure": -0.45, "arousal": 0.2, "dominance": -0.3},
        "unique_pages": 4,
        "review": {"overall_rating": 2.0, "likes": "...", "dislikes": "..."}
    }
"""

import argparse
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from shipcheck.core.types import SessionLog, StepLog
from shipcheck.layer1_persona.models import PersonaProfile
from shipcheck.review.generator import generate_review
from shipcheck.llm.claude_cli import ClaudeCli

logger = logging.getLogger(__name__)


def _build_session_log(state: dict, terminated_by: str, abandonment_step: int | None) -> SessionLog:
    """상태 파일 dict → SessionLog dataclass."""
    last_step = state["steps"][-1] if state["steps"] else {}
    return SessionLog(
        session_id=state["session_id"],
        persona_id=state["persona_id"],
        segment=state["segment"],
        product_name=state.get("product_name", ""),
        product_url=state["product_url"],
        total_steps=state["step_count"],
        terminated_by=terminated_by,
        abandonment_step=abandonment_step,
        final_pad_pleasure=state["pad"]["pleasure"],
        final_pad_arousal=state["pad"]["arousal"],
        final_pad_dominance=state["pad"]["dominance"],
        final_perceived_usefulness=last_step.get("perceived_usefulness", 0.5),
        final_perceived_ease_of_use=last_step.get("perceived_ease_of_use", 0.5),
        pages_visited=state["pages_visited"],
        unique_pages=len(set(state["pages_visited"])),
        total_back_navigations=state["back_nav_count"],
        total_hesitations=state["hesitation_count"],
        **state["big_five"],
        digital_literacy=state["digital_literacy"],
    )


def _build_step_logs(state: dict) -> list[StepLog]:
    """상태 파일의 steps → StepLog dataclass 리스트."""
    logs = []
    for s in state["steps"]:
        logs.append(StepLog(
            step_index=s["step_index"],
            url="",  # Claude 트랜스크립트에 있음
            action_type="",  # Claude 트랜스크립트에 있음
            action_target=None,
            action_reasoning="",
            pad_pleasure=s["pad_pleasure"],
            pad_arousal=s["pad_arousal"],
            pad_dominance=s["pad_dominance"],
            emotion_labels=[s.get("emotion_label", "")],
            emotion_reasoning="",
            abandonment_risk=0.0,
            cognitive_load=s.get("cognitive_load", 0.0),
            perceived_usefulness=s.get("perceived_usefulness", 0.5),
            perceived_ease_of_use=s.get("perceived_ease_of_use", 0.5),
            confidence=0.5,
            hesitation=False,
            elements_considered=0,
            should_abandon=s.get("should_abandon", False),
            abandon_reason=s.get("abandon_reason"),
        ))
    return logs


def main():
    parser = argparse.ArgumentParser(description="세션 종료")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--terminated-by", required=True,
                        choices=["abandoned", "goal_achieved", "max_steps", "error"])
    parser.add_argument("--state-dir", default="/tmp")
    parser.add_argument("--output-dir", default=None, help="JSONL 출력 디렉토리")
    parser.add_argument("--skip-review", action="store_true", help="리뷰 생성 건너뛰기")
    args = parser.parse_args()

    # 상태 파일 로드
    state_path = Path(args.state_dir) / f"shipcheck_{args.session_id}.json"
    if not state_path.exists():
        print(json.dumps({"error": f"세션 상태 파일 없음: {state_path}"}))
        sys.exit(1)

    state = json.loads(state_path.read_text())

    # 출력 디렉토리
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path("runs") / args.session_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # 이탈 스텝
    abandonment_step = None
    if args.terminated_by == "abandoned":
        for step in state["steps"]:
            if step.get("should_abandon"):
                abandonment_step = step["step_index"]
                break
        if abandonment_step is None:
            abandonment_step = state["step_count"]

    # SessionLog 구성 + JSONL 저장 (세션별 파일로 분리 → 동시 쓰기 안전)
    session_log = _build_session_log(state, args.terminated_by, abandonment_step)

    session_file = output_dir / f"session_{args.session_id}.json"
    session_file.write_text(
        json.dumps(asdict(session_log), ensure_ascii=False, indent=2)
    )

    steps_file = output_dir / f"steps_{args.session_id}.jsonl"
    with open(steps_file, "w", encoding="utf-8") as f:
        for step in state["steps"]:
            step["session_id"] = args.session_id
            f.write(json.dumps(step, ensure_ascii=False) + "\n")

    # 리뷰 생성
    review_data = None
    if not args.skip_review:
        persona_yaml_path = state.get("persona_yaml_path")
        if persona_yaml_path and Path(persona_yaml_path).exists():
            try:
                persona_data = yaml.safe_load(Path(persona_yaml_path).read_text())
                persona = PersonaProfile.from_dict(persona_data)
                step_logs = _build_step_logs(state)
                llm = ClaudeCli()

                review = generate_review(persona, session_log, step_logs, llm.complete_json)

                # 리뷰 저장
                reviews_dir = output_dir / "reviews"
                reviews_dir.mkdir(parents=True, exist_ok=True)
                safe_id = state["persona_id"].replace("/", "_")
                safe_product = state.get("product_name", "unknown").replace("/", "_").replace(" ", "_")
                review_path = reviews_dir / f"{safe_id}_{safe_product}.json"
                review_path.write_text(
                    json.dumps(asdict(review), ensure_ascii=False, indent=2)
                )
                review_data = {
                    "overall_rating": review.overall_rating,
                    "likes": review.likes[:200],
                    "dislikes": review.dislikes[:200],
                }
            except Exception as e:
                logger.warning("리뷰 생성 실패: %s", e)
                review_data = {"error": str(e)}

    # stdout
    result = {
        "session_id": args.session_id,
        "persona_id": state["persona_id"],
        "total_steps": state["step_count"],
        "terminated_by": args.terminated_by,
        "final_pad": state["pad"],
        "unique_pages": len(set(state["pages_visited"])),
    }
    if review_data:
        result["review"] = review_data
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
