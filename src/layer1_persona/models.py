"""Layer 1: Big Five → 수치 파라미터 매핑.

Personica의 핵심 IP. LLM이 성격을 "해석"하는 게 아니라,
미리 계산된 파라미터가 행동을 제어한다.

PRISM (Fudan, 2025) 방식 차용:
성격 유형을 수치 파라미터 벡터로 변환하여 재현성과 분화를 보장.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


@dataclass
class BigFive:
    """Big Five 성격 점수. 각 0.0 ~ 1.0."""
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

    def __post_init__(self):
        for name in ("openness", "conscientiousness", "extraversion",
                      "agreeableness", "neuroticism"):
            val = getattr(self, name)
            if not 0.0 <= val <= 1.0:
                raise ValueError(f"{name}={val} — 0.0~1.0 범위여야 합니다")


class PersonalityParameters:
    """Big Five → 시뮬레이션 행동 파라미터 수학적 매핑.

    모든 @property는 순수 함수 — Big Five 값이 같으면 결과도 같다.
    LLM에게는 이 수치가 하드 제약으로 전달된다.
    """

    def __init__(self, big_five: BigFive) -> None:
        self._b = big_five

    @property
    def error_tolerance(self) -> int:
        """포기까지 에러 허용 횟수.
        Agreeableness ↑ → 관대, Neuroticism ↑ → 참을성 ↓"""
        return max(1, round(3 + self._b.agreeableness * 3 - self._b.neuroticism * 2))

    @property
    def emotional_volatility(self) -> float:
        """SDE 확산 계수 σ. Neuroticism이 높을수록 감정 변동폭 큼.
        범위: 0.05 (차분) ~ 0.30 (감정 기복 큼)"""
        return 0.05 + self._b.neuroticism * 0.25

    @property
    def exploration_tendency(self) -> float:
        """새 기능 탐색 확률. Openness 주도.
        범위: 0.20 (보수적) ~ 0.80 (탐색적)"""
        return 0.20 + self._b.openness * 0.60

    @property
    def methodical_score(self) -> float:
        """단계적(1.0) vs 탐색적(0.0). Conscientiousness 주도.
        높으면 체계적 순서대로, 낮으면 이것저것 클릭."""
        return self._b.conscientiousness * 0.75 + (1 - self._b.openness) * 0.25

    @property
    def sycophancy_resistance(self) -> float:
        """제품 비판 성향. LLM Sycophancy 대응.
        낮은 Agreeableness + 높은 Neuroticism → 비판적."""
        return (1 - self._b.agreeableness) * 0.70 + self._b.neuroticism * 0.30

    @property
    def click_hesitation_range_ms(self) -> tuple[int, int]:
        """클릭 전 망설임 시간 범위(ms).
        Neuroticism ↑, Digital Literacy ↓ → 더 오래 망설임."""
        base_min = 100 + int(self._b.neuroticism * 400)
        base_max = base_min + int(self._b.conscientiousness * 600)
        return (base_min, max(base_min + 100, base_max))

    @property
    def reading_ratio(self) -> float:
        """페이지 텍스트 읽기 비율 (0.0~1.0).
        NNGroup: 대부분 ~20%만 읽음. Conscientiousness 높으면 더 읽음.
        범위: 0.10 ~ 0.65"""
        return min(0.65, 0.10 + (1 - self._b.openness) * 0.15
                   + self._b.conscientiousness * 0.30
                   + self._b.neuroticism * 0.10)

    @property
    def back_button_freq(self) -> float:
        """뒤로가기 빈도 (확률).
        Neuroticism ↑ → 불안해서 뒤로감."""
        return 0.05 + self._b.neuroticism * 0.15

    @property
    def satisficing_threshold(self) -> float:
        """Satisficer(낮음) vs Maximizer(높음).
        Conscientiousness ↑ → 더 꼼꼼히 비교."""
        return 0.40 + self._b.conscientiousness * 0.30 - self._b.openness * 0.10

    @property
    def pleasure_abandon_threshold(self) -> float:
        """PAD pleasure가 이 값 아래로 떨어지면 이탈 확률 급증.
        Neuroticism ↑ → 임계값이 높아짐 (더 쉽게 포기)."""
        return -0.6 + self._b.neuroticism * 0.3  # -0.6 ~ -0.3

    @property
    def emotion_decay_rate(self) -> float:
        """감정 감쇠율 (매 스텝 곱해짐). Agreeableness ↑ → 빠르게 회복."""
        return 0.75 + self._b.agreeableness * 0.15  # 0.75 ~ 0.90

    def to_dict(self) -> dict[str, Any]:
        """LLM 프롬프트 주입용 딕셔너리."""
        return {
            "error_tolerance": self.error_tolerance,
            "emotional_volatility": round(self.emotional_volatility, 3),
            "exploration_tendency": round(self.exploration_tendency, 2),
            "methodical_score": round(self.methodical_score, 2),
            "sycophancy_resistance": round(self.sycophancy_resistance, 2),
            "click_hesitation_range_ms": self.click_hesitation_range_ms,
            "reading_ratio": round(self.reading_ratio, 2),
            "back_button_freq": round(self.back_button_freq, 2),
            "satisficing_threshold": round(self.satisficing_threshold, 2),
            "pleasure_abandon_threshold": round(self.pleasure_abandon_threshold, 2),
            "emotion_decay_rate": round(self.emotion_decay_rate, 2),
        }


# ---------------------------------------------------------------------------
# Role Profile — G2 리뷰어 인구통계에서 도출한 역할 프로파일
# ---------------------------------------------------------------------------

class BudgetSensitivity(str, Enum):
    """예산 민감도. 리뷰 시 가격 관련 언급 빈도·톤에 영향."""
    VERY_HIGH = "very_high"  # 무료만 가능 (학생, 비영리, 개도국)
    HIGH = "high"            # 무료 선호, 유료는 ROI 증명 시
    MODERATE = "moderate"    # 부서 예산 있음, 합리적 가격이면 OK
    LOW = "low"              # 기능·생산성이 우선, 가격 부차적


@dataclass
class RoleProfile:
    """역할 기반 프로파일. G2 리뷰어 분포에서 도출.

    역할이 JTBD를 결정하고, JTBD가 제품 체험 시 주목하는 기능을 결정하고,
    그 기능 체험이 리뷰 내용을 결정하는 인과 체인의 시작점.
    """
    role_id: str                     # "startup_founder", "marketing_pro" 등
    label: str                       # 한글 표시명
    typical_occupations: list[str]   # 직업 샘플 풀
    company_size: str                # "1-10", "11-50", "51-200" 등
    budget_sensitivity: BudgetSensitivity
    prior_tools: list[str]           # 이전에 사용했을 도구 풀
    use_contexts: list[str]          # 제품 사용 맥락 풀
    jtbd_templates: list[str]        # JTBD primary_goal 템플릿 풀
    review_style_hints: dict[str, Any] = field(default_factory=dict)
    g2_weight: float = 0.0           # G2 리뷰에서 이 역할의 비율 (0.0~1.0)


# 6개 역할 프로파일 — G2 Tally 리뷰 97건 분석 기반
ROLE_PROFILES: dict[str, RoleProfile] = {
    "startup_founder": RoleProfile(
        role_id="startup_founder",
        label="스타트업 창업자/CEO",
        typical_occupations=["Founder", "CEO", "Co-founder", "CTO"],
        company_size="1-10",
        budget_sensitivity=BudgetSensitivity.HIGH,
        prior_tools=["Typeform", "Google Forms", "SurveyMonkey"],
        use_contexts=[
            "리드 캡처 및 고객 피드백 수집",
            "온보딩 설문 및 제품 검증",
            "투자자/파트너 데이터 수집",
        ],
        jtbd_templates=[
            "고객 피드백을 수집해서 제품-시장 적합성을 검증하고 싶다",
            "리드 제네레이션 폼을 만들어 웹사이트에 임베드하고 싶다",
            "고객 온보딩 프로세스를 자동화하고 싶다",
        ],
        review_style_hints={"verbosity": "concise", "focus": "business_value", "comparison": True},
        g2_weight=0.20,
    ),
    "marketing_pro": RoleProfile(
        role_id="marketing_pro",
        label="마케팅 전문가",
        typical_occupations=["Marketing Manager", "Marketing Coordinator", "Growth Marketer", "Marketing Staff"],
        company_size="11-50",
        budget_sensitivity=BudgetSensitivity.MODERATE,
        prior_tools=["Typeform", "HubSpot Forms", "Google Forms", "SurveyMonkey"],
        use_contexts=[
            "캠페인 등록 폼 및 전환 추적",
            "리드 퀄리피케이션 폼",
            "이벤트 등록 및 뉴스레터 구독",
        ],
        jtbd_templates=[
            "마케팅 캠페인용 등록 폼을 만들고 전환을 추적하고 싶다",
            "리드 스코어링을 위한 퀄리피케이션 폼이 필요하다",
            "CRM과 연동되는 리드 캡처 폼을 빠르게 만들고 싶다",
        ],
        review_style_hints={"verbosity": "detailed", "focus": "features_integrations", "comparison": True},
        g2_weight=0.15,
    ),
    "small_biz_operator": RoleProfile(
        role_id="small_biz_operator",
        label="소규모 비즈니스 운영자",
        typical_occupations=["Business Owner", "Sobriety Coach", "Fitness Coach", "Freelancer", "Consultant"],
        company_size="1-10",
        budget_sensitivity=BudgetSensitivity.VERY_HIGH,
        prior_tools=["Google Forms"],
        use_contexts=[
            "예약/등록 폼",
            "클라이언트 인테이크 설문",
            "내부 피드백 수집",
        ],
        jtbd_templates=[
            "클라이언트 상담 예약 폼을 무료로 만들고 싶다",
            "고객 정보를 체계적으로 수집하는 인테이크 폼이 필요하다",
            "이벤트 등록 폼을 만들어서 공유하고 싶다",
        ],
        review_style_hints={"verbosity": "enthusiastic", "focus": "ease_and_free_tier", "comparison": False},
        g2_weight=0.25,
    ),
    "tech_professional": RoleProfile(
        role_id="tech_professional",
        label="기술 전문가",
        typical_occupations=["Software Engineer", "IT Systems Admin", "Product Manager", "Developer"],
        company_size="11-50",
        budget_sensitivity=BudgetSensitivity.LOW,
        prior_tools=["Typeform", "JotForm", "custom code", "Airtable"],
        use_contexts=[
            "데이터 파이프라인 입력 폼",
            "내부 도구 및 워크플로우 자동화",
            "서포트 티켓 수집 및 웹훅 연동",
        ],
        jtbd_templates=[
            "웹훅과 API로 자동화할 수 있는 데이터 수집 폼을 구축하고 싶다",
            "기존 Typeform을 대체할 수 있는지 조건부 로직과 연동성을 평가하고 싶다",
            "내부 워크플로우에 임베드할 폼을 빠르게 만들고 싶다",
        ],
        review_style_hints={"verbosity": "technical", "focus": "architecture_and_api", "comparison": True},
        g2_weight=0.10,
    ),
    "educator_nonprofit": RoleProfile(
        role_id="educator_nonprofit",
        label="교육자/비영리",
        typical_occupations=["Teacher", "Professor", "Non-profit Manager", "Course Instructor", "Researcher"],
        company_size="1-50",
        budget_sensitivity=BudgetSensitivity.VERY_HIGH,
        prior_tools=["Google Forms", "Microsoft Forms", "네이버 폼"],
        use_contexts=[
            "학생/학부모 설문조사",
            "수업 등록 및 피드백 수집",
            "이벤트 참가 등록",
        ],
        jtbd_templates=[
            "학생 피드백 설문을 무료로 쉽게 만들어 배포하고 싶다",
            "수업 등록 폼에 조건부 로직을 넣어 복잡한 등록을 간소화하고 싶다",
            "예산 없이 Google Forms보다 보기 좋은 설문을 만들고 싶다",
        ],
        review_style_hints={"verbosity": "moderate", "focus": "ease_and_budget", "comparison": True},
        g2_weight=0.15,
    ),
    "creative_freelancer": RoleProfile(
        role_id="creative_freelancer",
        label="크리에이티브/프리랜서",
        typical_occupations=["Web Designer", "Content Creator", "Author", "Photographer", "Coach"],
        company_size="1-5",
        budget_sensitivity=BudgetSensitivity.HIGH,
        prior_tools=["Google Forms", "Canva", "Typeform"],
        use_contexts=[
            "리드 마그넷 (퀴즈, 스코어카드)",
            "클라이언트 프로젝트 브리프",
            "뉴스레터 구독 및 브랜딩 폼",
        ],
        jtbd_templates=[
            "내 브랜드에 맞는 세련된 리드 마그넷 퀴즈를 만들고 싶다",
            "클라이언트 프로젝트 의뢰 폼을 만들어 웹사이트에 넣고 싶다",
            "이메일 리스트를 늘리기 위한 구독 폼이 필요하다",
        ],
        review_style_hints={"verbosity": "enthusiastic", "focus": "design_and_branding", "comparison": True},
        g2_weight=0.15,
    ),
}


@dataclass
class JTBD:
    """Jobs to Be Done — 페르소나의 개인화된 사용 목적."""
    primary_goal: str  # "팀 프로젝트 마감 관리를 자동화하고 싶다"
    success_criterion: str  # "30분 내에 기존 Jira 워크플로우를 대체할 수 있는지 확인"
    prior_tools: list[str] = field(default_factory=list)  # ["Jira", "Notion"]
    willingness_to_pay: float = 0.5  # 0.0 ~ 1.0


@dataclass
class PersonaProfile:
    """완전한 페르소나 프로필. 실험의 독립변수."""
    persona_id: str
    name: str
    segment: str  # "explorer" 등 행동 세그먼트
    big_five: BigFive
    params: PersonalityParameters  # Big Five에서 파생
    jtbd: JTBD
    digital_literacy: int  # 1=Low, 2=Novice, 3=Competent, 4=Power
    demographics: dict[str, Any] = field(default_factory=dict)
    background_narrative: str = ""  # LLM이 생성한 배경 서술

    # 벤치마크 비교용 확장 필드 (G2 리뷰어 프로파일 매칭)
    role_id: str = ""               # RoleProfile.role_id 참조
    prior_tools_detail: list[str] = field(default_factory=list)
    budget_sensitivity: str = ""    # BudgetSensitivity 값
    use_context: str = ""           # 실제 할당된 사용 맥락

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PersonaProfile:
        """YAML/JSON에서 PersonaProfile 생성."""
        big_five = BigFive(**data["big_five"])
        jtbd = JTBD(**data["jtbd"])
        return cls(
            persona_id=data["persona_id"],
            name=data["name"],
            segment=data["segment"],
            big_five=big_five,
            params=PersonalityParameters(big_five),
            jtbd=jtbd,
            digital_literacy=data["digital_literacy"],
            demographics=data.get("demographics", {}),
            background_narrative=data.get("background_narrative", ""),
            role_id=data.get("role_id", ""),
            prior_tools_detail=data.get("prior_tools_detail", []),
            budget_sensitivity=data.get("budget_sensitivity", ""),
            use_context=data.get("use_context", ""),
        )
