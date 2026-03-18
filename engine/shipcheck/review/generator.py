"""리뷰 생성 파이프라인 — MOSAIC 스타일 체험→성찰→리뷰.

세션 완료 후 페르소나의 체험 데이터를 바탕으로 G2 구조의 리뷰를 생성한다.
치팅 방지: G2 리뷰 내용은 프롬프트에 포함되지 않음.
리뷰는 순수하게 시뮬레이션 체험에서 도출됨.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from ..core.types import StepLog, SessionLog
from ..layer1_persona.models import PersonaProfile, ROLE_PROFILES

logger = logging.getLogger(__name__)


@dataclass
class ExperienceSummary:
    """세션 체험 요약 — 리뷰 생성의 입력."""
    persona_id: str
    persona_name: str
    role_id: str
    segment: str
    product_name: str

    # 행동 요약
    total_steps: int
    pages_visited: list[str]
    unique_pages: int
    terminated_by: str  # "goal_achieved" | "abandoned" | "max_steps"
    abandonment_step: int | None

    # 감정 궤적 요약
    initial_pleasure: float
    final_pleasure: float
    min_pleasure: float
    max_pleasure: float
    emotion_trajectory: list[dict[str, float]]  # [{step, pleasure, arousal, dominance}]

    # 인지 메트릭
    final_perceived_usefulness: float
    final_perceived_ease_of_use: float
    total_hesitations: int
    total_back_navigations: int

    # 주요 이벤트 (좌절/성공/발견 순간)
    key_moments: list[dict[str, Any]]  # [{step, event, description}]

    # 페르소나 맥락 (리뷰 톤 결정용)
    prior_tools: list[str]
    budget_sensitivity: str
    use_context: str
    digital_literacy: int
    big_five_summary: dict[str, float]


@dataclass
class SyntheticReview:
    """G2 리뷰 구조와 동일한 합성 리뷰."""
    persona_id: str
    persona_name: str
    role_id: str
    segment: str
    product_name: str

    # G2 구조 필드
    likes: str
    dislikes: str
    problems_solved: str
    overall_rating: float  # 0.5 단위, 1.0~5.0

    # 메타데이터
    review_reasoning: str  # 리뷰 생성 근거 (자기성찰)
    experience_summary_hash: str  # 체험 요약 참조
    generation_method: str = "mosaic_pipeline"


def extract_experience_summary(
    persona: PersonaProfile,
    session_log: SessionLog,
    step_logs: list[StepLog],
) -> ExperienceSummary:
    """세션 데이터에서 체험 요약 추출."""
    # 감정 궤적
    emotion_trajectory = []
    min_p, max_p = 0.0, 0.0
    initial_p = step_logs[0].pad_pleasure if step_logs else 0.0

    for s in step_logs:
        emotion_trajectory.append({
            "step": s.step_index,
            "pleasure": s.pad_pleasure,
            "arousal": s.pad_arousal,
            "dominance": s.pad_dominance,
        })
        min_p = min(min_p, s.pad_pleasure)
        max_p = max(max_p, s.pad_pleasure)

    # 주요 순간 추출 (큰 감정 변화, 좌절, 성공)
    key_moments: list[dict[str, Any]] = []
    for i, s in enumerate(step_logs):
        # 좌절 순간: pleasure 급감 (-0.15 이상 하락)
        if i > 0 and s.pad_pleasure - step_logs[i - 1].pad_pleasure < -0.15:
            key_moments.append({
                "step": s.step_index,
                "event": "frustration_spike",
                "url": s.url,
                "description": s.emotion_reasoning,
                "pleasure_delta": round(s.pad_pleasure - step_logs[i - 1].pad_pleasure, 3),
            })
        # 이탈 결정
        if s.should_abandon:
            key_moments.append({
                "step": s.step_index,
                "event": "abandonment",
                "url": s.url,
                "description": s.abandon_reason or "abandoned",
            })
        # 높은 만족 순간
        if s.pad_pleasure > 0.3 and (i == 0 or step_logs[i - 1].pad_pleasure <= 0.3):
            key_moments.append({
                "step": s.step_index,
                "event": "satisfaction_peak",
                "url": s.url,
                "description": s.emotion_reasoning,
            })

    return ExperienceSummary(
        persona_id=persona.persona_id,
        persona_name=persona.name,
        role_id=persona.role_id,
        segment=persona.segment,
        product_name=session_log.product_name,
        total_steps=session_log.total_steps,
        pages_visited=session_log.pages_visited,
        unique_pages=session_log.unique_pages,
        terminated_by=session_log.terminated_by,
        abandonment_step=session_log.abandonment_step,
        initial_pleasure=round(initial_p, 3),
        final_pleasure=round(session_log.final_pad_pleasure, 3),
        min_pleasure=round(min_p, 3),
        max_pleasure=round(max_p, 3),
        emotion_trajectory=emotion_trajectory,
        final_perceived_usefulness=session_log.final_perceived_usefulness,
        final_perceived_ease_of_use=session_log.final_perceived_ease_of_use,
        total_hesitations=session_log.total_hesitations,
        total_back_navigations=session_log.total_back_navigations,
        key_moments=key_moments,
        prior_tools=persona.prior_tools_detail or persona.jtbd.prior_tools,
        budget_sensitivity=persona.budget_sensitivity,
        use_context=persona.use_context,
        digital_literacy=persona.digital_literacy,
        big_five_summary={
            "openness": persona.big_five.openness,
            "conscientiousness": persona.big_five.conscientiousness,
            "extraversion": persona.big_five.extraversion,
            "agreeableness": persona.big_five.agreeableness,
            "neuroticism": persona.big_five.neuroticism,
        },
    )


def _build_review_prompt(exp: ExperienceSummary) -> str:
    """체험 요약 → 리뷰 생성 프롬프트 구성.

    3단계 MOSAIC 파이프라인:
    1. 체험 회고 (어떤 기능을 썼고, 어디서 막혔고)
    2. 자기성찰 (나의 JTBD를 해결했는가?)
    3. 리뷰 작성 (G2 likes/dislikes/problems_solved 구조)
    """
    # 감정 궤적을 자연어로 변환
    emotion_narrative = _emotion_trajectory_to_narrative(exp)

    # 주요 순간 포매팅
    moments_text = ""
    for m in exp.key_moments[:8]:  # 최대 8개
        moments_text += f"- Step {m['step']}: [{m['event']}] {m.get('description', '')} (URL: {m.get('url', 'N/A')})\n"

    # 비교 프레임 (사전 도구 기반)
    comparison_frame = ""
    if exp.prior_tools:
        comparison_frame = f"이전에 사용해본 도구: {', '.join(exp.prior_tools)}. 이 도구들과 비교하여 평가할 것."

    # 예산 맥락
    budget_context = {
        "very_high": "무료 사용만 고려. 유료 기능은 평가 대상이 아님.",
        "high": "무료 사용 중심. 유료 전환은 확실한 ROI가 있을 때만.",
        "moderate": "합리적 가격이라면 유료 사용 가능. 기능 대비 가격 평가.",
        "low": "가격보다 기능과 생산성이 중요. 프로 플랜 적극 고려.",
    }.get(exp.budget_sensitivity, "")

    # 리뷰 스타일 가이드 (역할 기반)
    role = ROLE_PROFILES.get(exp.role_id)
    style_guide = ""
    if role and role.review_style_hints:
        hints = role.review_style_hints
        verbosity = hints.get("verbosity", "moderate")
        focus = hints.get("focus", "general")
        style_guide = f"리뷰 스타일: {verbosity} 수준의 상세함, {focus} 관점 중심."

    return f"""당신은 방금 웹 기반 SaaS 도구를 실제로 사용해본 사람입니다.
아래의 체험 데이터를 바탕으로, 실제 G2 리뷰처럼 자연스러운 리뷰를 작성하십시오.

=== 당신의 프로필 ===
- 이름: {exp.persona_name}
- 역할: {exp.role_id}
- 디지털 리터러시: {exp.digital_literacy}/4
- 사용 맥락: {exp.use_context}
- {comparison_frame}
- {budget_context}
- {style_guide}

=== 체험 데이터 ===
- 제품: {exp.product_name}
- 총 {exp.total_steps}단계 사용, {exp.unique_pages}개 고유 페이지 방문
- 결과: {exp.terminated_by} {"(Step " + str(exp.abandonment_step) + "에서 포기)" if exp.abandonment_step else ""}
- 뒤로가기: {exp.total_back_navigations}회, 망설임: {exp.total_hesitations}회

=== 감정 변화 ===
{emotion_narrative}

=== 주요 순간 ===
{moments_text if moments_text else "(특별한 이벤트 없음)"}

=== 최종 인지 평가 ===
- 유용성 인식 (Perceived Usefulness): {exp.final_perceived_usefulness:.2f}/1.0
- 사용 용이성 인식 (Perceived Ease of Use): {exp.final_perceived_ease_of_use:.2f}/1.0

=== 리뷰 작성 규칙 ===
1. **체험 기반**: 당신이 실제로 사용하면서 느낀 것만 작성. 사용하지 않은 기능은 언급하지 마세요.
2. **솔직함**: 좋은 점과 아쉬운 점 모두 구체적으로 작성. 만족도가 높아도 최소 1개 개선점 포함.
3. **비교 관점**: 이전 도구와 비교할 수 있으면 자연스럽게 비교. 없으면 제품 자체만 평가.
4. **1인칭 경험담**: "I found...", "What I love..." 등 개인 경험 톤으로 작성.
5. **영어로 작성**: G2 리뷰 스타일로 영어 작성.
6. **별점 근거**: 체험 만족도(pleasure), 유용성, 사용 용이성을 종합하여 0.5 단위 별점 결정.

다음 JSON 형식으로 응답하십시오:
{{
  "review_reasoning": "리뷰 작성 전 자기성찰 — 이 도구가 나의 목적을 해결했는가? 무엇이 좋았고 무엇이 아쉬웠는가? 2-3문장.",
  "likes": "제품의 좋은 점을 자세히. 구체적 기능, UI, 경험 언급. G2 'What do you like best?' 스타일.",
  "dislikes": "아쉬운 점, 개선 제안. G2 'What do you dislike?' 스타일. 체험 중 실제로 겪은 어려움 중심.",
  "problems_solved": "이 제품이 해결해준 문제. G2 'What problems is the product solving and how is that benefiting you?' 스타일.",
  "overall_rating": 1.0~5.0 (0.5 단위)
}}"""


def _emotion_trajectory_to_narrative(exp: ExperienceSummary) -> str:
    """감정 궤적을 자연어 서술로 변환."""
    if not exp.emotion_trajectory:
        return "감정 데이터 없음"

    parts = []
    parts.append(f"시작 시 감정: pleasure={exp.initial_pleasure:.2f}")

    # 전체 추세
    if exp.final_pleasure > exp.initial_pleasure + 0.1:
        parts.append("전반적으로 만족도가 상승했다.")
    elif exp.final_pleasure < exp.initial_pleasure - 0.1:
        parts.append("전반적으로 만족도가 하락했다.")
    else:
        parts.append("전반적으로 만족도가 비슷하게 유지되었다.")

    # 극단값
    if exp.min_pleasure < -0.3:
        parts.append(f"최저점: pleasure={exp.min_pleasure:.2f} (상당한 좌절 경험)")
    if exp.max_pleasure > 0.4:
        parts.append(f"최고점: pleasure={exp.max_pleasure:.2f} (높은 만족 경험)")

    parts.append(f"최종: pleasure={exp.final_pleasure:.2f}")
    return " ".join(parts)


def _compute_rating(exp: ExperienceSummary) -> float:
    """체험 데이터에서 별점 산출 — LLM에 참고용으로 제공.

    LLM이 최종 결정하지만, 체험 기반 가이드라인 제공.
    """
    pu = exp.final_perceived_usefulness
    pe = exp.final_perceived_ease_of_use
    fp = (exp.final_pleasure + 1.0) / 2.0  # -1~1 → 0~1 정규화

    # 가중 평균: 유용성 40%, 용이성 30%, 감정 30%
    raw = pu * 0.4 + pe * 0.3 + fp * 0.3

    # 1.0~5.0 매핑, 0.5 단위 반올림
    rating = max(1.0, min(5.0, 1.0 + raw * 4.0))
    return round(rating * 2) / 2  # 0.5 단위


def generate_review(
    persona: PersonaProfile,
    session_log: SessionLog,
    step_logs: list[StepLog],
    llm_complete_json: Any,  # callable: (prompt, system) → dict
) -> SyntheticReview:
    """세션 완료 후 합성 리뷰 생성.

    Args:
        persona: 페르소나 프로필
        session_log: 세션 집계 로그
        step_logs: 스텝별 상세 로그
        llm_complete_json: LLM JSON 완성 함수

    Returns:
        G2 구조의 합성 리뷰
    """
    # Step 1: 체험 요약 추출
    exp = extract_experience_summary(persona, session_log, step_logs)

    # Step 2: LLM 리뷰 생성 (MOSAIC 파이프라인 내장)
    prompt = _build_review_prompt(exp)
    system = (
        "당신은 제품 리뷰를 작성하는 실제 사용자입니다. "
        "G2.com의 리뷰 스타일로, 진솔하고 구체적인 리뷰를 작성하세요. "
        "리뷰는 반드시 체험 데이터에 근거해야 하며, 경험하지 않은 기능을 추측하지 마세요."
    )

    try:
        result = llm_complete_json(prompt, system)
    except Exception as e:
        logger.error("리뷰 생성 실패 (%s): %s", persona.persona_id, e)
        # 폴백: 체험 데이터 기반 최소 리뷰
        result = _fallback_review(exp)

    return SyntheticReview(
        persona_id=persona.persona_id,
        persona_name=persona.name,
        role_id=persona.role_id,
        segment=persona.segment,
        product_name=exp.product_name,
        likes=result.get("likes", ""),
        dislikes=result.get("dislikes", ""),
        problems_solved=result.get("problems_solved", ""),
        overall_rating=float(result.get("overall_rating", _compute_rating(exp))),
        review_reasoning=result.get("review_reasoning", ""),
        experience_summary_hash=f"{exp.persona_id}_{exp.total_steps}_{exp.terminated_by}",
    )


def _fallback_review(exp: ExperienceSummary) -> dict[str, Any]:
    """LLM 실패 시 폴백 리뷰 — 체험 데이터에서 직접 도출."""
    rating = _compute_rating(exp)

    if exp.terminated_by == "abandoned":
        likes = "The initial interface seemed clean."
        dislikes = f"I had difficulty completing my task and gave up at step {exp.abandonment_step}."
    else:
        likes = f"I was able to explore {exp.unique_pages} different pages and the overall experience was acceptable."
        dislikes = "Some areas could be more intuitive."

    return {
        "likes": likes,
        "dislikes": dislikes,
        "problems_solved": f"I was trying to use the product for {exp.use_context or 'my work'}.",
        "overall_rating": rating,
        "review_reasoning": "Fallback review generated from experience data.",
    }


def save_reviews(reviews: list[SyntheticReview], output_path: Path) -> None:
    """합성 리뷰를 JSONL로 저장."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in reviews:
            f.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")
    logger.info("%d개 합성 리뷰 저장 → %s", len(reviews), output_path)
