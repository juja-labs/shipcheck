"""Layer 3: 감정 엔진 — OCC 룰 매핑 + SDE noise + PAD decay.

LLM 외부에서 수학적으로 계산되어 LLM의 행동을 제약하는 핵심 모듈.
Chain-of-Emotion LLM 콜은 runner에서 별도 호출.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from enum import Enum

from ..core.types import PADVector, EmotionState


class OCCEvent(str, Enum):
    """단순화된 OCC 이벤트 타입. 22개 → 8개."""
    ACTION_SUCCESS = "action_success"  # 목표 진행 → joy
    ACTION_FAILURE = "action_failure"  # 목표 차단 → frustration
    PAGE_CHANGE = "page_change"  # 새 페이지 탐색 → curiosity/relief
    ERROR_DETECTED = "error_detected"  # 에러 메시지 → distress
    COMPLEX_PAGE = "complex_page"  # 복잡한 페이지 → anxiety
    SIMPLE_SUCCESS = "simple_success"  # 간단한 성공 → satisfaction
    STUCK = "stuck"  # 같은 페이지에서 반복 → frustration/boredom
    FIRST_IMPRESSION = "first_impression"  # 첫 페이지 로드 → neutral/curiosity


# OCC 이벤트 → PAD delta 결정론적 매핑
# 이 값은 LLM이 결정하지 않음 — 수학적으로 보장됨
OCC_PAD_MAPPING: dict[OCCEvent, tuple[float, float, float]] = {
    # (pleasure_delta, arousal_delta, dominance_delta)
    OCCEvent.ACTION_SUCCESS: (+0.10, -0.05, +0.10),
    OCCEvent.ACTION_FAILURE: (-0.15, +0.15, -0.15),
    OCCEvent.PAGE_CHANGE: (+0.05, +0.10, +0.05),
    OCCEvent.ERROR_DETECTED: (-0.20, +0.20, -0.20),
    OCCEvent.COMPLEX_PAGE: (-0.05, +0.15, -0.10),
    OCCEvent.SIMPLE_SUCCESS: (+0.12, -0.05, +0.08),
    OCCEvent.STUCK: (-0.12, -0.10, -0.15),
    OCCEvent.FIRST_IMPRESSION: (0.0, +0.15, 0.0),
}

# 이벤트 → 감정 라벨 매핑
OCC_LABEL_MAPPING: dict[OCCEvent, str] = {
    OCCEvent.ACTION_SUCCESS: "satisfied",
    OCCEvent.ACTION_FAILURE: "frustrated",
    OCCEvent.PAGE_CHANGE: "curious",
    OCCEvent.ERROR_DETECTED: "frustrated",
    OCCEvent.COMPLEX_PAGE: "anxious",
    OCCEvent.SIMPLE_SUCCESS: "satisfied",
    OCCEvent.STUCK: "bored",
    OCCEvent.FIRST_IMPRESSION: "neutral",
}


def classify_event(
    prev_action_succeeded: bool,
    url_changed: bool,
    error_in_dom: bool,
    page_element_count: int,
    consecutive_failures: int,
    is_first_step: bool,
) -> OCCEvent:
    """현재 상황에서 OCC 이벤트 타입을 결정론적으로 분류."""
    if is_first_step:
        return OCCEvent.FIRST_IMPRESSION
    if consecutive_failures >= 2:
        return OCCEvent.STUCK
    if not prev_action_succeeded:
        # 액션 실패 + DOM에 에러 메시지 → 더 심각한 에러
        if error_in_dom:
            return OCCEvent.ERROR_DETECTED
        return OCCEvent.ACTION_FAILURE
    # 아래부터는 액션 성공한 경우
    if url_changed and page_element_count > 30:
        return OCCEvent.COMPLEX_PAGE
    if url_changed:
        return OCCEvent.PAGE_CHANGE
    return OCCEvent.SIMPLE_SUCCESS


def compute_pad_delta(
    event: OCCEvent,
    emotional_volatility: float,
    consecutive_failures: int,
    rng: np.random.Generator | None = None,
) -> tuple[float, float, float]:
    """OCC 이벤트 → PAD delta 계산.

    1. 결정론적 OCC 매핑에서 기본 delta 가져옴
    2. 연속 실패 시 부정적 감정 증폭
    3. SDE noise 추가 (emotional_volatility = σ)

    Returns:
        (pleasure_delta, arousal_delta, dominance_delta)
    """
    if rng is None:
        rng = np.random.default_rng()

    base_p, base_a, base_d = OCC_PAD_MAPPING[event]

    # 첫 인상은 noise를 줄임 — 아직 충분한 자극이 없으므로
    noise_scale = 0.3 if event == OCCEvent.FIRST_IMPRESSION else 1.0

    # 연속 실패 증폭: 실패가 쌓일수록 부정 감정 강화
    failure_amplifier = 1.0 + consecutive_failures * 0.08
    if base_p < 0:
        base_p *= failure_amplifier
    if base_d < 0:
        base_d *= failure_amplifier

    # SDE noise: dE = μdt + σdW
    # σ = emotional_volatility (Big Five Neuroticism에서 파생, 0.05~0.30)
    # 중요: noise가 OCC delta(0.10~0.20)를 삼키면 안 됨
    # → noise를 delta의 ~30% 수준으로 제한 (σ * 0.4 스케일링)
    # noise_scale: 첫 인상에서는 추가로 0.3 적용
    scaled_vol = emotional_volatility * 0.4  # 0.02 ~ 0.12 범위
    noise_p = scaled_vol * noise_scale * rng.normal(0, 1)
    noise_a = scaled_vol * noise_scale * 0.5 * rng.normal(0, 1)
    noise_d = scaled_vol * noise_scale * 0.3 * rng.normal(0, 1)

    return (base_p + noise_p, base_a + noise_a, base_d + noise_d)


def update_pad(
    current: PADVector,
    delta: tuple[float, float, float],
    decay_rate: float,
) -> PADVector:
    """PAD 상태 업데이트: decay + delta + clamp.

    emotion[t] = emotion[t-1] * decay + delta[t]
    """
    new_p = current.pleasure * decay_rate + delta[0]
    new_a = current.arousal * decay_rate + delta[1]
    new_d = current.dominance * decay_rate + delta[2]
    return PADVector(pleasure=new_p, arousal=new_a, dominance=new_d).clamp()


def compute_cognitive_load(
    element_count: int,
    text_length: int,
    digital_literacy: int,
) -> float:
    """DOM 기반 인지 부하 heuristic.

    페이지 복잡도 / 페르소나 능력 = 상대적 인지 부하.
    NNGroup: 65세+는 태스크 수행 43% 느림 → digital_literacy로 반영.

    Returns: 0.0 (쉬움) ~ 1.0+ (과부하)
    """
    # 페이지 복잡도: 인터랙티브 요소 수 + 텍스트 양
    # 실제 웹페이지는 요소 100+, 텍스트 10000자+가 흔함 — 임계값을 현실적으로 설정
    page_complexity = (
        min(element_count, 150) / 150.0 * 0.5  # 요소 150개면 0.5
        + min(text_length, 15000) / 15000.0 * 0.3  # 텍스트 15000자면 0.3
    )
    # 디지털 리터러시로 나눔 (1=Low → 높은 부하, 4=Power → 낮은 부하)
    literacy_factor = 0.4 + digital_literacy * 0.2  # 0.6 ~ 1.2
    return min(1.0, page_complexity / literacy_factor)


def check_abandonment(
    pad: PADVector,
    consecutive_failures: int,
    error_tolerance: int,
    pleasure_threshold: float,
    cognitive_load: float,
    step_count: int,
) -> tuple[bool, str | None]:
    """결정론적 이탈 판정. LLM이 sycophancy로 무시할 수 없음.

    Returns:
        (should_abandon, reason)
    """
    if consecutive_failures >= error_tolerance:
        return True, f"연속 실패 {consecutive_failures}회 (허용: {error_tolerance})"

    if pad.pleasure < pleasure_threshold and step_count > 3:
        return True, f"pleasure={pad.pleasure:.2f} < threshold={pleasure_threshold:.2f}"

    if cognitive_load > 0.95 and pad.pleasure < -0.4 and step_count > 2:
        return True, f"인지 과부하 (load={cognitive_load:.2f}) + 부정 감정 (P={pad.pleasure:.2f})"

    return False, None
