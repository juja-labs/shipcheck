#!/usr/bin/env python3
"""세션 초기화 — 페르소나 YAML을 로드하고 세션 상태 파일을 생성.

사용법:
    python3 -m src.tools.session_init \
        --persona configs/personas/benchmark/b005.yaml \
        --product-url "https://tally.so" \
        --session-id abc123

출력 (stdout JSON):
    {
        "session_id": "abc123",
        "persona_id": "b005",
        "persona_name": "김도현",
        "segment": "power_user",
        "pad": {"pleasure": 0.1, "arousal": 0.1, "dominance": 0.1},
        "params": {
            "error_tolerance": 5,
            "emotional_volatility": 0.12,
            "exploration_tendency": 0.68,
            ...
        },
        "state_file": "/tmp/shipcheck_abc123.json"
    }
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

# 엔진 모듈 임포트
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # repo root
from src.layer1_persona.models import PersonaProfile


def main():
    parser = argparse.ArgumentParser(description="세션 초기화")
    parser.add_argument("--persona", required=True, help="페르소나 YAML 경로")
    parser.add_argument("--product-url", required=True, help="제품 URL")
    parser.add_argument("--product-name", default="", help="제품 이름")
    parser.add_argument("--session-id", required=True, help="세션 ID")
    parser.add_argument("--state-dir", default="/tmp", help="상태 파일 디렉토리")
    args = parser.parse_args()

    # 페르소나 로드
    data = yaml.safe_load(Path(args.persona).read_text())
    profile = PersonaProfile.from_dict(data)
    params = profile.params

    # 초기 상태
    state = {
        "session_id": args.session_id,
        "persona_id": profile.persona_id,
        "persona_name": profile.name,
        "segment": profile.segment,
        "persona_yaml_path": str(Path(args.persona).resolve()),
        "product_url": args.product_url,
        "product_name": args.product_name,
        # PAD 초기값 — 자발적으로 제품을 열어본 사람 → 살짝 긍정적
        "pad": {"pleasure": 0.1, "arousal": 0.1, "dominance": 0.1},
        # 누적 상태
        "step_count": 0,
        "consecutive_failures": 0,
        "pages_visited": [],
        "back_nav_count": 0,
        "hesitation_count": 0,
        # 페르소나 파라미터 (결정론적 계산에 사용)
        "params": {
            "error_tolerance": params.error_tolerance,
            "emotional_volatility": params.emotional_volatility,
            "exploration_tendency": params.exploration_tendency,
            "satisficing_threshold": params.satisficing_threshold,
            "pleasure_abandon_threshold": params.pleasure_abandon_threshold,
            "emotion_decay_rate": params.emotion_decay_rate,
            "sycophancy_resistance": params.sycophancy_resistance,
        },
        # Big Five (ANOVA 독립변수)
        "big_five": {
            "openness": profile.big_five.openness,
            "conscientiousness": profile.big_five.conscientiousness,
            "extraversion": profile.big_five.extraversion,
            "agreeableness": profile.big_five.agreeableness,
            "neuroticism": profile.big_five.neuroticism,
        },
        "digital_literacy": profile.digital_literacy,
        # 로그
        "steps": [],
    }

    # 상태 파일 저장
    state_path = Path(args.state_dir) / f"shipcheck_{args.session_id}.json"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    # stdout에 결과 출력 — Claude가 읽음
    result = {
        "session_id": args.session_id,
        "persona_id": profile.persona_id,
        "persona_name": profile.name,
        "segment": profile.segment,
        "pad": state["pad"],
        "params": state["params"],
        "state_file": str(state_path),
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
