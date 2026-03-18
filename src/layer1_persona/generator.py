"""페르소나 배치 생성기 — 역할×행동 매트릭스 기반.

G2 리뷰어 인구통계 분포를 반영하여 합성 페르소나를 생성한다.
기존 10개 행동 세그먼트 × 6개 역할 프로파일에서 가중치 기반 샘플링.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml
import numpy as np

from ..llm.claude_cli import ClaudeCli
from .models import (
    ROLE_PROFILES,
    RoleProfile,
    BudgetSensitivity,
)

logger = logging.getLogger(__name__)

# 10개 행동 세그먼트: Big Five 핵심 축을 기준으로 분산
SEGMENTS: list[dict[str, Any]] = [
    {"name": "explorer",           "label": "탐색가 (high O, low C)",     "O": (0.7, 0.95), "C": (0.1, 0.35), "E": (0.3, 0.7), "A": (0.3, 0.7), "N": (0.2, 0.5)},
    {"name": "power_user",         "label": "파워유저 (high O, high C)",   "O": (0.7, 0.95), "C": (0.7, 0.95), "E": (0.4, 0.8), "A": (0.3, 0.6), "N": (0.1, 0.4)},
    {"name": "cautious_methodical","label": "신중한 체계파 (low O, high C)","O": (0.1, 0.35), "C": (0.7, 0.95), "E": (0.2, 0.5), "A": (0.5, 0.8), "N": (0.3, 0.6)},
    {"name": "intuitive",          "label": "감 의존형 (low O, low C)",    "O": (0.1, 0.35), "C": (0.1, 0.35), "E": (0.4, 0.7), "A": (0.4, 0.7), "N": (0.3, 0.6)},
    {"name": "anxious",            "label": "불안형 (high N)",            "O": (0.3, 0.6),  "C": (0.3, 0.6),  "E": (0.2, 0.5), "A": (0.4, 0.7), "N": (0.75, 0.95)},
    {"name": "calm",               "label": "차분형 (low N)",             "O": (0.3, 0.6),  "C": (0.4, 0.7),  "E": (0.4, 0.7), "A": (0.4, 0.7), "N": (0.05, 0.25)},
    {"name": "agreeable",          "label": "관대형 (high A)",            "O": (0.3, 0.7),  "C": (0.3, 0.6),  "E": (0.4, 0.7), "A": (0.75, 0.95),"N": (0.2, 0.5)},
    {"name": "critical_vocal",     "label": "비판적 외향형 (low A, high E)","O": (0.4, 0.7), "C": (0.3, 0.6),  "E": (0.7, 0.95),"A": (0.05, 0.3), "N": (0.4, 0.7)},
    {"name": "tech_savvy",         "label": "기술 숙련 (digital_literacy=4)","O": (0.6, 0.9), "C": (0.5, 0.8), "E": (0.4, 0.7), "A": (0.3, 0.6), "N": (0.1, 0.4)},
    {"name": "tech_novice",        "label": "기술 미숙 (digital_literacy=1-2)","O": (0.1, 0.4),"C": (0.4, 0.7), "E": (0.3, 0.6), "A": (0.5, 0.8), "N": (0.4, 0.7)},
]

# 역할-행동 세그먼트 자연스러운 조합 가중치 (높을수록 현실에서 흔한 조합)
# 0이면 해당 조합을 생성하지 않음
ROLE_SEGMENT_AFFINITY: dict[str, dict[str, float]] = {
    "startup_founder": {
        "explorer": 0.8, "power_user": 1.0, "cautious_methodical": 0.3,
        "intuitive": 0.5, "anxious": 0.2, "calm": 0.7,
        "agreeable": 0.3, "critical_vocal": 0.8, "tech_savvy": 0.9, "tech_novice": 0.0,
    },
    "marketing_pro": {
        "explorer": 0.6, "power_user": 0.7, "cautious_methodical": 0.8,
        "intuitive": 0.4, "anxious": 0.3, "calm": 0.6,
        "agreeable": 0.5, "critical_vocal": 0.5, "tech_savvy": 0.4, "tech_novice": 0.2,
    },
    "small_biz_operator": {
        "explorer": 0.3, "power_user": 0.2, "cautious_methodical": 0.5,
        "intuitive": 0.8, "anxious": 0.6, "calm": 0.5,
        "agreeable": 0.8, "critical_vocal": 0.3, "tech_savvy": 0.1, "tech_novice": 0.7,
    },
    "tech_professional": {
        "explorer": 0.7, "power_user": 1.0, "cautious_methodical": 0.5,
        "intuitive": 0.2, "anxious": 0.1, "calm": 0.6,
        "agreeable": 0.2, "critical_vocal": 0.9, "tech_savvy": 1.0, "tech_novice": 0.0,
    },
    "educator_nonprofit": {
        "explorer": 0.3, "power_user": 0.2, "cautious_methodical": 0.7,
        "intuitive": 0.5, "anxious": 0.7, "calm": 0.5,
        "agreeable": 0.8, "critical_vocal": 0.2, "tech_savvy": 0.1, "tech_novice": 0.8,
    },
    "creative_freelancer": {
        "explorer": 0.9, "power_user": 0.5, "cautious_methodical": 0.2,
        "intuitive": 0.7, "anxious": 0.4, "calm": 0.5,
        "agreeable": 0.5, "critical_vocal": 0.6, "tech_savvy": 0.3, "tech_novice": 0.4,
    },
}


# 페르소나 생성 프롬프트 — 역할 맥락 포함 버전
PERSONA_GEN_SYSTEM = """당신은 다양한 배경의 사용자 페르소나를 생성하는 전문가입니다.
각 페르소나는 실제 사람처럼 구체적인 배경, 직업, 습관, 제품 사용 경험을 가져야 합니다.
G2에서 B2B SaaS 리뷰를 쓸 법한 실제 직장인 수준의 현실감을 목표로 합니다.
글로벌 사용자를 생성하십시오 (영어 이름 + 다양한 국적)."""


def _sample_big_five(segment: dict[str, Any], rng: np.random.Generator) -> dict[str, float]:
    """세그먼트 범위 내에서 Big Five 점수 샘플링."""
    result = {}
    for trait in ("O", "C", "E", "A", "N"):
        lo, hi = segment[trait]
        result[trait] = round(float(rng.uniform(lo, hi)), 2)
    return result


def _digital_literacy_from_segment(segment_name: str, rng: np.random.Generator) -> int:
    """세그먼트에 따른 디지털 리터러시 결정."""
    if segment_name == "tech_savvy":
        return 4
    elif segment_name == "tech_novice":
        return int(rng.choice([1, 2]))
    elif segment_name == "power_user":
        return int(rng.choice([3, 4]))
    elif segment_name in ("cautious_methodical", "intuitive"):
        return int(rng.choice([2, 3]))
    else:
        return int(rng.choice([2, 3, 3]))


def _select_role_segment_pairs(
    n_personas: int,
    rng: np.random.Generator,
) -> list[tuple[str, dict[str, Any]]]:
    """G2 가중치 × 역할-세그먼트 친화도 기반으로 (role_id, segment) 쌍 샘플링."""
    pairs: list[tuple[str, dict[str, Any], float]] = []

    for role_id, role in ROLE_PROFILES.items():
        affinities = ROLE_SEGMENT_AFFINITY[role_id]
        for seg in SEGMENTS:
            weight = role.g2_weight * affinities.get(seg["name"], 0.0)
            if weight > 0:
                pairs.append((role_id, seg, weight))

    # 가중치 정규화 후 샘플링
    weights = np.array([p[2] for p in pairs])
    weights = weights / weights.sum()

    indices = rng.choice(len(pairs), size=n_personas, replace=True, p=weights)
    return [(pairs[i][0], pairs[i][1]) for i in indices]


def _budget_sensitivity_to_wtp(bs: BudgetSensitivity, rng: np.random.Generator) -> float:
    """BudgetSensitivity → willingness_to_pay 수치 변환."""
    ranges = {
        BudgetSensitivity.VERY_HIGH: (0.0, 0.2),
        BudgetSensitivity.HIGH: (0.15, 0.45),
        BudgetSensitivity.MODERATE: (0.4, 0.7),
        BudgetSensitivity.LOW: (0.6, 0.95),
    }
    lo, hi = ranges[bs]
    return round(float(rng.uniform(lo, hi)), 2)


def generate_benchmark_personas(
    n_personas: int = 30,
    product_context: str = "Tally — 웹 기반 폼 빌더 (Notion 스타일 에디터, 무료 티어 제공)",
    output_dir: Path | None = None,
    llm_model: str = "sonnet",
    seed: int = 42,
) -> list[dict[str, Any]]:
    """벤치마크 비교용 페르소나 배치 생성.

    역할 프로파일 × 행동 세그먼트 매트릭스에서 G2 가중치 기반 샘플링.
    """
    output_dir = output_dir or Path("configs/personas/benchmark")
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed)
    llm = ClaudeCli(model=llm_model, timeout_seconds=180)

    # 역할×세그먼트 조합 샘플링
    role_seg_pairs = _select_role_segment_pairs(n_personas, rng)

    generated: list[dict[str, Any]] = []

    for idx, (role_id, seg) in enumerate(role_seg_pairs):
        persona_id = f"b{idx + 1:03d}"
        role = ROLE_PROFILES[role_id]

        # Big Five 샘플링
        b5 = _sample_big_five(seg, rng)
        dl = _digital_literacy_from_segment(seg["name"], rng)

        # 역할에서 구체적 값 샘플링
        use_context = str(rng.choice(role.use_contexts))
        jtbd_template = str(rng.choice(role.jtbd_templates))
        n_prior = int(rng.choice([1, 2, 3]))
        prior_tools = [str(t) for t in rng.choice(role.prior_tools, size=min(n_prior, len(role.prior_tools)), replace=False)]
        wtp = _budget_sensitivity_to_wtp(role.budget_sensitivity, rng)

        # LLM으로 서술적 프로필 생성
        prompt = f"""다음 조건의 사용자 페르소나를 생성하십시오.

[역할 맥락]
- 역할 유형: {role.label}
- 직업 풀: {', '.join(role.typical_occupations)}
- 회사 규모: {role.company_size}명
- 예산 민감도: {role.budget_sensitivity.value}
- 제품 사용 맥락: {use_context}
- 이전 사용 도구: {', '.join(prior_tools)}
- 핵심 JTBD: {jtbd_template}

[성격 점수 (Big Five, 0~1)]
- Openness(개방성): {b5['O']}
- Conscientiousness(성실성): {b5['C']}
- Extraversion(외향성): {b5['E']}
- Agreeableness(친화성): {b5['A']}
- Neuroticism(신경증): {b5['N']}

[디지털 리터러시]: {dl}/4
[행동 세그먼트]: {seg['label']}
[제품]: {product_context}

다음 JSON 형식으로 응답하십시오:
{{
  "name": "글로벌 이름 (예: Sarah K., Rohit B., Marie N.)",
  "age": 22~60,
  "occupation": "{role.label} 범주 내 구체적 직업",
  "background_narrative": "이 사람의 배경을 2-3문장으로. 기술 습관, 업무 맥락, 성격이 자연스럽게 드러나게. 제품(Tally)은 언급하지 말 것.",
  "jtbd": {{
    "primary_goal": "{jtbd_template}을 기반으로 더 구체적으로 작성",
    "success_criterion": "이 목표를 달성했다고 판단하는 구체적 기준 (시간, 결과물 등)",
    "prior_tools": {json.dumps(prior_tools)},
    "willingness_to_pay": {wtp}
  }}
}}"""

        try:
            result = llm.complete_json(prompt, system=PERSONA_GEN_SYSTEM)
        except Exception as e:
            logger.error("페르소나 %s 생성 실패: %s", persona_id, e)
            continue

        persona_data = {
            "persona_id": persona_id,
            "name": result.get("name", f"User_{idx + 1}"),
            "segment": seg["name"],
            "role_id": role_id,
            "big_five": {
                "openness": b5["O"],
                "conscientiousness": b5["C"],
                "extraversion": b5["E"],
                "agreeableness": b5["A"],
                "neuroticism": b5["N"],
            },
            "digital_literacy": dl,
            "demographics": {
                "age": result.get("age", 30),
                "occupation": result.get("occupation", ""),
                "company_size": role.company_size,
            },
            "background_narrative": result.get("background_narrative", ""),
            "prior_tools_detail": prior_tools,
            "budget_sensitivity": role.budget_sensitivity.value,
            "use_context": use_context,
            "jtbd": result.get("jtbd", {
                "primary_goal": jtbd_template,
                "success_criterion": "핵심 기능 확인",
                "prior_tools": prior_tools,
                "willingness_to_pay": wtp,
            }),
        }

        out_path = output_dir / f"{persona_id}.yaml"
        out_path.write_text(
            yaml.dump(persona_data, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )
        generated.append(persona_data)
        logger.info(
            "[%d/%d] %s (%s × %s) — %s",
            idx + 1, n_personas, persona_data["name"],
            role_id, seg["name"], persona_id,
        )

    logger.info("벤치마크 페르소나 생성 완료: %d명 → %s", len(generated), output_dir)
    return generated


# 하위 호환 — 기존 실험용 생성기 유지
def generate_experiment_personas(config_path: Path) -> None:
    """실험 설정에서 페르소나 50명 생성 (기존 방식 유지)."""
    config = yaml.safe_load(config_path.read_text())
    output_dir = Path(config.get("persona_dir", "configs/personas/generated"))
    output_dir.mkdir(parents=True, exist_ok=True)

    n_per_segment = config.get("personas_per_segment", 5)
    product_context = config.get("product_context", "웹 기반 SaaS 도구")
    llm_model = config.get("llm_model", "sonnet")
    seed = config.get("seed", 42)

    rng = np.random.default_rng(seed)
    llm = ClaudeCli(model=llm_model, timeout_seconds=180)

    persona_count = 0
    for seg in SEGMENTS:
        for i in range(n_per_segment):
            persona_count += 1
            persona_id = f"p{persona_count:03d}"

            b5 = _sample_big_five(seg, rng)
            dl = _digital_literacy_from_segment(seg["name"], rng)

            prompt = f"""다음 성격 특성을 가진 사용자 페르소나를 생성하십시오.

[성격 점수 (Big Five, 0~1)]
- Openness(개방성): {b5['O']}
- Conscientiousness(성실성): {b5['C']}
- Extraversion(외향성): {b5['E']}
- Agreeableness(친화성): {b5['A']}
- Neuroticism(신경증): {b5['N']}

[디지털 리터러시]: {dl}/4
[제품 맥락]: {product_context}
[세그먼트]: {seg['label']}

다음 JSON 형식으로 응답하십시오:
{{
  "name": "한국 이름 (예: 김민준)",
  "age": 20~65,
  "occupation": "직업",
  "background_narrative": "이 사람의 배경을 2-3문장으로 (기술 습관, 일상, 성격이 드러나게)",
  "jtbd": {{
    "primary_goal": "이 제품으로 달성하려는 구체적 목표",
    "success_criterion": "이 목표를 달성했다고 판단하는 기준",
    "prior_tools": ["이전에 사용한 유사 도구 1-3개"],
    "willingness_to_pay": 0.0~1.0
  }}
}}"""

            try:
                result = llm.complete_json(prompt, system=PERSONA_GEN_SYSTEM)
            except Exception as e:
                logger.error("페르소나 %s 생성 실패: %s", persona_id, e)
                continue

            persona_data = {
                "persona_id": persona_id,
                "name": result.get("name", f"User_{persona_count}"),
                "segment": seg["name"],
                "big_five": {
                    "openness": b5["O"],
                    "conscientiousness": b5["C"],
                    "extraversion": b5["E"],
                    "agreeableness": b5["A"],
                    "neuroticism": b5["N"],
                },
                "digital_literacy": dl,
                "demographics": {
                    "age": result.get("age", 30),
                    "occupation": result.get("occupation", ""),
                },
                "background_narrative": result.get("background_narrative", ""),
                "jtbd": result.get("jtbd", {
                    "primary_goal": "제품 탐색",
                    "success_criterion": "핵심 기능 확인",
                    "prior_tools": [],
                    "willingness_to_pay": 0.5,
                }),
            }

            out_path = output_dir / f"{persona_id}.yaml"
            out_path.write_text(
                yaml.dump(persona_data, allow_unicode=True, default_flow_style=False),
                encoding="utf-8",
            )
            logger.info(
                "[%d/50] %s (%s) — %s",
                persona_count, persona_data["name"], seg["name"], persona_id,
            )

    logger.info("페르소나 생성 완료: %d명 → %s", persona_count, output_dir)
