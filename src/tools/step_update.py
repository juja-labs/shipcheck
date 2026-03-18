#!/usr/bin/env python3
"""스텝 업데이트 — 매 행동 후 감정 파이프라인 실행.

Claude(페르소나)가 playwright-cli로 행동한 후 호출.
결정론적 계산(OCC → PAD → SDE → 이탈)만 수행하고 결과를 반환.
행동 로그(action-type, url, reasoning 등)는 Claude 트랜스크립트에 이미 있으므로 받지 않음.

사용법:
    python3 -m src.tools.step_update \
        --session-id abc123 \
        --action-succeeded true \
        --url-changed false \
        --element-count 45 \
        --error-detected false \
        --pu 0.4 --peou 0.6

출력 (stdout JSON):
    {
        "step": 3,
        "pad": {"pleasure": -0.12, "arousal": 0.35, "dominance": -0.08},
        "emotion_label": "frustrated",
        "occ_event": "action_failure",
        "cognitive_load": 0.42,
        "should_abandon": false,
        "abandon_reason": null,
        "consecutive_failures": 2
    }
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # repo root
from src.core.types import PADVector
from src.layer3_emotion.engine import (
    classify_event,
    compute_pad_delta,
    update_pad,
    compute_cognitive_load,
    check_abandonment,
    OCC_LABEL_MAPPING,
)


def str2bool(v: str) -> bool:
    return v.lower() in ("true", "1", "yes")


def main():
    parser = argparse.ArgumentParser(description="스텝 감정 업데이트")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--state-dir", default="/tmp")

    # OCC 분류에 필요한 관찰값 — Claude가 직전 행동 결과를 보고 넣음
    parser.add_argument("--action-succeeded", required=True, type=str2bool)
    parser.add_argument("--url-changed", required=True, type=str2bool)
    parser.add_argument("--element-count", type=int, default=30)
    parser.add_argument("--error-detected", type=str2bool, default=False)

    # ANOVA 종속변수 — Claude가 자기 판단으로 넣음
    parser.add_argument("--pu", type=float, required=True, help="Perceived Usefulness 0.0~1.0")
    parser.add_argument("--peou", type=float, required=True, help="Perceived Ease of Use 0.0~1.0")

    args = parser.parse_args()

    # 상태 파일 로드
    state_path = Path(args.state_dir) / f"shipcheck_{args.session_id}.json"
    if not state_path.exists():
        print(json.dumps({"error": f"세션 상태 파일 없음: {state_path}"}))
        sys.exit(1)

    state = json.loads(state_path.read_text())
    params = state["params"]
    step_idx = state["step_count"]

    # 현재 PAD 복원
    pad = PADVector(**state["pad"])

    # === 결정론적 파이프라인 ===

    # 1. OCC 이벤트 분류
    occ_event = classify_event(
        prev_action_succeeded=args.action_succeeded,
        url_changed=args.url_changed,
        error_in_dom=args.error_detected,
        page_element_count=args.element_count,
        consecutive_failures=state["consecutive_failures"],
        is_first_step=(step_idx == 0),
    )

    # 2. PAD delta 계산 (SDE noise 포함)
    rng = np.random.default_rng()
    pad_delta = compute_pad_delta(
        occ_event,
        params["emotional_volatility"],
        state["consecutive_failures"],
        rng,
    )

    # 3. PAD 업데이트
    pad = update_pad(pad, pad_delta, params["emotion_decay_rate"])
    emotion_label = OCC_LABEL_MAPPING[occ_event]

    # 4. 인지 부하
    text_length = args.element_count * 50  # 요소당 평균 50자 추정
    cognitive_load = compute_cognitive_load(
        args.element_count, text_length, state["digital_literacy"]
    )

    # 5. 이탈 판정
    should_abandon, abandon_reason = check_abandonment(
        pad,
        state["consecutive_failures"],
        params["error_tolerance"],
        params["pleasure_abandon_threshold"],
        cognitive_load,
        step_idx,
    )

    # === 상태 업데이트 ===

    if args.action_succeeded:
        state["consecutive_failures"] = 0
    else:
        state["consecutive_failures"] += 1

    state["step_count"] = step_idx + 1
    state["pad"] = pad.to_dict()

    # PU/PEOU 기록 (ANOVA용)
    state["steps"].append({
        "step_index": step_idx,
        "pad_pleasure": pad.pleasure,
        "pad_arousal": pad.arousal,
        "pad_dominance": pad.dominance,
        "emotion_label": emotion_label,
        "occ_event": occ_event.value,
        "cognitive_load": cognitive_load,
        "perceived_usefulness": args.pu,
        "perceived_ease_of_use": args.peou,
        "should_abandon": should_abandon,
        "abandon_reason": abandon_reason,
    })

    # 상태 파일 저장
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    # === stdout — Claude가 읽고 다음 행동 결정 ===
    result = {
        "step": step_idx,
        "pad": pad.to_dict(),
        "emotion_label": emotion_label,
        "occ_event": occ_event.value,
        "cognitive_load": round(cognitive_load, 2),
        "should_abandon": should_abandon,
        "abandon_reason": abandon_reason,
        "consecutive_failures": state["consecutive_failures"],
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
