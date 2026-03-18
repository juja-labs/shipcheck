"""공유 데이터 타입 — 모든 모듈이 참조하는 핵심 dataclass들."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Emotion
# ---------------------------------------------------------------------------

@dataclass
class PADVector:
    """Pleasure-Arousal-Dominance 3차원 감정 상태. 각 축 -1.0 ~ +1.0."""
    pleasure: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.0

    def clamp(self) -> PADVector:
        self.pleasure = max(-1.0, min(1.0, self.pleasure))
        self.arousal = max(-1.0, min(1.0, self.arousal))
        self.dominance = max(-1.0, min(1.0, self.dominance))
        return self

    def to_dict(self) -> dict[str, float]:
        return {"pleasure": self.pleasure, "arousal": self.arousal, "dominance": self.dominance}


@dataclass
class EmotionState:
    """Layer 3 출력. 감정 파이프라인의 최종 결과."""
    pad: PADVector = field(default_factory=PADVector)
    labels: list[str] = field(default_factory=list)  # ["frustrated", "confused"]
    chain_reasoning: str = ""  # LLM이 생성한 감정 추론
    abandonment_risk: float = 0.0  # 0.0 ~ 1.0


# ---------------------------------------------------------------------------
# Observation (BrowserEnv → Runner)
# ---------------------------------------------------------------------------

@dataclass
class UIElement:
    semantic_id: str
    tag: str
    text: str = ""
    element_type: str = ""  # "clickable" | "input" | "select"
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass
class Observation:
    """BrowserEnv.observe()의 반환값.

    html_summary는 이제 Playwright 접근성 스냅샷 YAML을 포함.
    """
    url: str
    page_title: str
    html_summary: str  # Playwright 접근성 스냅샷 (YAML 형태)
    element_count: int = 0  # 인터랙티브 요소 수 (cognitive load 계산용)
    text_length: int = 0  # 텍스트 길이 추정
    scroll_ratio: float = 0.0  # 현재 스크롤 위치 (0.0=최상단, 1.0=최하단)


# ---------------------------------------------------------------------------
# Action
# ---------------------------------------------------------------------------

class ActionType(str, Enum):
    CLICK = "click"
    TYPE = "type"
    FILL = "fill"
    SELECT = "select"
    HOVER = "hover"
    SCROLL = "scroll"
    GOTO_URL = "goto_url"
    BACK = "back"
    KEY_PRESS = "key_press"
    PRESS = "press"
    TERMINATE = "terminate"


@dataclass
class Action:
    action_type: ActionType
    target: str | None = None  # parser-semantic-id
    value: str | None = None  # type/select 시 입력값
    reasoning: str = ""


# ---------------------------------------------------------------------------
# Step & Session Logs
# ---------------------------------------------------------------------------

@dataclass
class StepLog:
    """한 스텝의 전체 기록. JSONL에 직렬화됨."""
    step_index: int
    url: str

    # Action
    action_type: str
    action_target: str | None
    action_reasoning: str

    # Emotion (ANOVA 종속변수)
    pad_pleasure: float
    pad_arousal: float
    pad_dominance: float
    emotion_labels: list[str]
    emotion_reasoning: str
    abandonment_risk: float

    # Cognitive (deterministic)
    cognitive_load: float

    # LLM 출력 메타데이터 (ANOVA 종속변수)
    perceived_usefulness: float
    perceived_ease_of_use: float
    confidence: float
    hesitation: bool
    elements_considered: int

    # 세션 제어
    should_abandon: bool = False
    abandon_reason: str | None = None


@dataclass
class SessionLog:
    """한 세션(1 페르소나 × 1 제품)의 집계."""
    session_id: str
    persona_id: str
    segment: str
    product_name: str
    product_url: str
    total_steps: int
    terminated_by: str  # "goal_achieved" | "abandoned" | "max_steps" | "error"
    abandonment_step: int | None

    # 최종 상태 (ANOVA 종속변수)
    final_pad_pleasure: float
    final_pad_arousal: float
    final_pad_dominance: float
    final_perceived_usefulness: float
    final_perceived_ease_of_use: float
    pages_visited: list[str]
    unique_pages: int
    total_back_navigations: int
    total_hesitations: int

    # Big Five (ANOVA 독립변수)
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float
    digital_literacy: int
