# 페르소나 시뮬레이션 엔진 — 기술 설계

Personica(이전 ShipCheck)의 핵심 IP. "다양한 배경의 AI 페르소나가 사람처럼 생각하고 반응하는 것"의 기술적 구현. 이 엔진은 제품 체험(Playwright), 서베이 응답, A/B 테스트, 광고/퍼널 리서치, 전문가 리뷰 등 다양한 리서치 모드에 범용 적용되는 **합성 페르소나 시뮬레이션 플랫폼**의 핵심이다.

## 페르소나 리얼리티 엔진 — 5개 레이어 아키텍처

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: Persona Profile                           │
│  ├── Demographics (나이, 직업, 소득)                  │
│  ├── Psychographics (가치관, 위험회피성향, 기술태도)     │
│  ├── Behavioral (인내심, 만족기준, 학습스타일)           │
│  ├── Prior Experience (써본 유사 제품 → 멘탈 모델)      │
│  └── JTBD (이 제품으로 달성하려는 구체적 목표)           │
├─────────────────────────────────────────────────────┤
│  Layer 2: Cognitive (매 상호작용마다 실행)               │
│  ├── Information Foraging — UI 요소의 "정보 냄새" 평가  │
│  ├── Cognitive Load Tracker — 복잡도 누적 추적          │
│  ├── Mental Model Matching — 기대 vs 실제 비교          │
│  └── TAM Score — Perceived Usefulness/Ease 실시간 갱신 │
├─────────────────────────────────────────────────────┤
│  Layer 3: Emotion (Chain-of-Emotion 패턴)             │
│  ├── OCC Appraisal — 이벤트 → 감정 유형 분류           │
│  ├── PAD State — Pleasure/Arousal/Dominance 연속 추적  │
│  ├── Emotion Decay — 지수적 감쇠 (반감기 적용)          │
│  └── Emotion History — 누적 감정 궤적                  │
├─────────────────────────────────────────────────────┤
│  Layer 4: Decision (BDI-E 모델)                       │
│  ├── Beliefs — 제품에 대한 현재 이해                    │
│  ├── Desires — JTBD에서 파생된 현재 목표                │
│  ├── Intentions — 다음 행동 선택                       │
│  ├── Fogg Check — Motivation × Ability × Prompt 충족?  │
│  └── Satisficing Gate — "충분히 좋은가?" 판단            │
├─────────────────────────────────────────────────────┤
│  Layer 5: Memory (장기/반복 사용)                      │
│  ├── Memory Stream — 관찰 + 중요도 점수 기록            │
│  ├── Reflection — 임계값 도달 시 상위 추상화 생성        │
│  ├── Habit Strength — 기능별 사용 빈도 (증가/감쇠)      │
│  ├── Novelty Factor — 세션마다 감쇠                    │
│  └── Satisfaction Trend — 누적 만족도 궤적              │
└─────────────────────────────────────────────────────┘
```

---

## Layer 1: Persona Profile

### 3-Layer 속성 모델

**Layer 1a — Demographics (기본 속성)**
- 나이, 성별, 직업, 교육, 지역, 소득
- 단독으로는 행동 예측력 낮지만 다른 레이어의 기초

**Layer 1b — Psychographics (심리적 속성)** — 행동 예측력 높음
- 가치관, 신념, 라이프스타일, 관심사
- 기술에 대한 태도 (early adopter vs. skeptic)
- 위험 회피 성향, 프라이버시 민감도

**Layer 1c — Behavioral (행동 속성)** — 시뮬레이션의 핵심
- 구매 의사결정 과정 (충동적 vs. 분석적)
- 정보 탐색 패턴 (검색 먼저 vs. 탐색 먼저)
- 학습 스타일 (tutorial 선호 vs. trial-and-error)

### JTBD (Jobs to Be Done) 통합
- Persona = Who (누가 사용하는가) — 감정, 맥락, 행동 패턴
- JTBD = Why (왜 사용하는가) — 달성하려는 결과(outcome)
- 예시:
  ```
  Persona(40대 비기술직 여성, 위험 회피적)
    + Job("팀 프로젝트 진행 상황을 한눈에 파악하고 싶다")
    = 예측 가능한 행동: 대시보드 우선 → 복잡한 설정 회피 → 직관적이지 않으면 빠른 포기
  ```

### Digital Literacy Spectrum
1. **Power User**: 키보드 단축키, 빠른 스캔, 에러 자체 해결
2. **Competent User**: 기본 패턴 이해, 가끔 혼란
3. **Novice User**: 모든 것을 읽음, 느린 탐색, 에러에 당황
4. **Low-literacy User**: 아이콘 의존, 텍스트 회피, 자주 포기

### 페르소나별 브라우징 프로파일
```python
class BrowsingProfile:
    scan_pattern: str         # "f_pattern" | "z_pattern" | "commitment"
    reading_ratio: float      # 0.15~0.80 (대부분 0.20)
    click_hesitation_ms: int  # 100~3000 (리터러시에 따라)
    back_button_freq: float   # 0.05~0.40 (시니어 높음)
    search_vs_browse: float   # 0~1 (시니어 = 검색 선호)
    error_tolerance: int      # 1~5 (포기까지 에러 허용 횟수)
    methodical_score: float   # 0~1 (단계적 vs 탐색적)
```

| 페르소나 유형 | click_hesitation | error_tolerance | methodical |
|--------------|-----------------|-----------------|------------|
| 20대 개발자 | 100-300ms | 5 | 0.2 |
| 40대 PM | 300-800ms | 3 | 0.5 |
| 65세 은퇴자 | 1000-3000ms | 1-2 | 0.95 |

---

## Layer 2: Cognitive

### Information Foraging Theory (정보 채집 이론)
- Pirolli & Card (PARC, 1990s), 동물 먹이 찾기 행동에서 차용
- 사용자는 UI에서 **"정보 냄새(information scent)"**를 따라감
- 링크/버튼의 텍스트가 목표와 관련 있어 보이면 클릭
- 냄새가 약하면 → 뒤로가기(patch-leave), 검색 시도, 또는 이탈
- 페르소나별로 같은 UI에서 다른 냄새를 맡음 (기술자는 "API" 인식, 비기술자는 못 봄)

### Cognitive Load Theory (인지 부하 이론)
- Sweller (1988), 3종 인지 부하:
  - **Intrinsic**: 태스크 자체의 복잡도
  - **Extraneous**: 나쁜 디자인이 부과하는 부하 (복잡한 메뉴, 혼란스러운 네비게이션)
  - **Germane**: 이해를 구축하는 생산적 노력
- 총 부하 > 작업 기억 용량 → 에러 증가, 속도 저하, 이탈
- 페르소나별 인지 용량이 다름 — 65세+는 태스크 수행 43% 느림 (NNGroup 연구)

### Mental Model Matching (멘탈 모델 매칭)
- 사용자는 기존 유사 제품 경험으로 멘탈 모델을 가지고 접근
- 제품이 기대와 일치하면 → 순조로운 탐색
- 기대와 불일치하면 → 혼란, 갭에 비례하는 인지 부하
- 예: Slack 경험 있는 사용자가 유사 메시징 앱을 쓸 때 vs 처음 쓰는 사용자

### TAM (Technology Acceptance Model)
- Davis (1989), 두 핵심 요인:
  - **Perceived Usefulness (PU)**: "이게 내 일에 도움이 되나?"
  - **Perceived Ease of Use (PEOU)**: "쓰는 데 얼마나 노력이 드나?"
- 각 페르소나가 사용 중 PU/PEOU 실시간 갱신
- 높은 PU + 낮은 PEOU = "유용하지만 어려움" — 특정 세그먼트의 전형적 반응

---

## Layer 3: Emotion

### OCC Model (Ortony, Clore, Collins)
- 22개 감정 카테고리, 3종 자극 기반:
  - **Events** → 목표 관련 평가 (joy, distress, hope, fear, relief, disappointment)
  - **Agent Actions** → 칭찬성 평가 (pride, shame, admiration, reproach)
  - **Objects** → 매력 평가 (love, hate)
- 제품 상호작용 매핑:
  - 버튼 못 찾음 → Event(goal-blocked) → distress/frustration
  - 깔끔한 온보딩 → Agent Action(well-designed) → admiration
  - 예쁜 UI → Object(appealing) → like

### PAD (Pleasure-Arousal-Dominance) 연속 상태
- 모든 감정을 3차원 연속값으로 표현:
  - **Pleasure** (-1 ~ +1): 즐거움 ↔ 불쾌
  - **Arousal** (-1 ~ +1): 각성 ↔ 차분
  - **Dominance** (-1 ~ +1): 통제감 ↔ 무력감
- 좌절 = 낮은 P + 높은 A + 낮은 D
- 만족 = 높은 P + 중간 A + 높은 D
- 지루함 = 낮은 P + 낮은 A + 중간 D
- **이탈 임계값**: P < -0.5 AND sessions > 1 → 이탈 확률 급증

### Chain-of-Emotion Architecture (PLOS One, 2024)
- 매 상호작용마다 **별도 LLM 콜**로 감정 평가 후 행동 결정
- 프롬프트 구성: system instruction + message history + **emotion history** + current input
- STEU(Situational Test of Emotional Understanding)에서 검증됨
- **Personica 핵심 패턴**: 행동 결정 전에 항상 감정 평가 선행

### Emotion Decay (감정 감쇠)
- 실제 인간 감정의 반감기 < 1시간
- 지수적 감쇠: `emotion_state[t] = emotion_state[t-1] * decay_factor + new_appraisal[t]`
- 좌절적 버그 → 즐거운 기능 발견 → 좌절이 시간에 따라 감쇠하며 새 긍정 경험으로 대체

---

## Layer 4: Decision

### BDI-E (Belief-Desire-Intention-Emotion)
- BDI 아키텍처에 Emotion 모듈 추가:
  - **Beliefs**: 제품에 대한 현재 이해 ("설정은 우측 상단에 있을 거다")
  - **Desires**: JTBD에서 파생 ("알림 설정을 바꾸고 싶다")
  - **Intentions**: 다음 행동 ("이 메뉴를 클릭하자")
  - **Emotions**: 현재 감정 상태 ("30초째 찾는 중이라 약간 짜증")
- 감정이 의도 선택에 피드백 — 짜증나면 탐색 포기하고 검색 시도

### Fogg Behavior Model (B = MAP)
- **B**ehavior = **M**otivation × **A**bility × **P**rompt
- 세 가지 모두 충족해야 행동 발생
- 동기 높지만 능력 낮으면 → 시도하되 실패 → 좌절
- 능력 높지만 동기 낮으면 → 기능이 있어도 사용 안 함
- 프롬프트 없으면 → 기능을 발견하지 못함

### Satisficing vs Maximizing
- Herbert Simon의 제한된 합리성:
  - **Satisficer**: 첫 번째 "충분히 좋은" 옵션 선택 (대부분의 사용자)
  - **Maximizer**: 모든 옵션을 비교 (소수, 더 오래 걸림, 자주 덜 만족)
- 페르소나 속성으로 설정 — 탐색 깊이와 속도에 직접 영향

---

## Layer 5: Memory

### Generative Agents 메모리 스트림 (Park et al., Stanford 2023)
- 핵심 검색 공식:
  ```
  score(M_i | Q) = α_rec × recency_i + α_imp × importance_i + α_rel × relevance_i
  ```
  - Recency: 지수적 감쇠 (factor 0.995)
  - Importance: LLM이 1-10 점수 부여
  - Relevance: 쿼리와 메모리의 코사인 유사도
- **Reflection**: 누적 중요도 > 임계값(150)일 때 트리거
  - 최근 100개 메모리에서 상위 질문 생성 → 관련 메모리 검색 → 상위 추상화 합성
  - "Klaus가 혼자 밥 먹고 위축된 것 같다" 수준의 인사이트
  - 반성이 없으면 48시간 내 행동 퇴화 (ablation study 실증)

### 반복 사용 시뮬레이션 (다중 세션)

**Session 1 (첫 사용)**:
- Novelty factor 높음 → 탐색적 행동 증가
- 멘탈 모델 형성 중 → 혼란 가능성 높음
- 감정 변동폭 큼

**Session 2-3 (학습 기간)**:
- 이전 세션 기억 기반 행동 (reflection 참조)
- 학습 곡선 → 익숙한 기능은 빠르게, 새 기능은 여전히 탐색
- "지난번에 막혔던 설정 메뉴, 이번엔 찾아보자"

**Session 4+ (습관 형성 or 이탈)**:
- Novelty 감쇠 → 실제 가치만 남음
- Habit strength에 따라 자동적 사용 vs 의식적 사용
- 만족도 누적 궤적이 이탈/잔존 결정

### 핵심 변수
- **Habit Strength**: 사용할수록 증가 (체감 감소), 안 쓰면 느리게 감쇠
- **Novelty Factor**: 세션마다 감쇠 — 4주 후 거의 0
- **Satisfaction Trend**: `S[t] = S[t-1] * decay + new_experience[t]`
- **Abandonment Risk**: pleasure < threshold AND sessions > 2 → 이탈 확률 급증

### 메모리 아키텍처 옵션

| 시스템 | 특징 | 적합도 |
|--------|------|--------|
| Generative Agents 방식 | 메모리 스트림 + 반성, 검증됨 | 기본 채택 |
| Zep/Graphiti | 시간축 Knowledge Graph, 하이브리드 검색 | 데이터 구조화에 사용 |
| Mem0 | 그래프+시맨틱 듀얼 검색, 충돌 해결 | 대안으로 검토 |
| A-Mem | Zettelkasten 방식, 양방향 링크 | 복잡한 다중 홉 추론에 강점 |

---

## 소셜 시뮬레이션 프레임워크에서 차용한 구현 방법론

소셜 미디어 시뮬레이션 프레임워크(PRISM, Concordia, GenSim, Truman 등)는 "소셜 네트워크를 시뮬레이션하는 것"이 목적이지만, 그 안에 들어 있는 **개별 에이전트 모델링 기법**은 Personica의 페르소나 시뮬레이션 충실도를 끌어올리는 데 직접 활용 가능함.

소셜 레이어(피드 추천, 팔로우 그래프, 바이럴 메트릭 등)는 Personica의 문제와 맞지 않으므로 전부 제외하고, **개별 에이전트의 감정·성격·의사결정·안정성 모델링 기법만** 선별 차용함.

### 1. SDE 기반 감정 진화 — PRISM (Fudan, 2025)

**문제**: 현재 감정 모델 `emotion[t] = emotion[t-1] * decay + appraisal[t]`은 결정론적(deterministic)임. 같은 자극을 받으면 같은 페르소나는 항상 같은 감정 궤적을 따름. 실제 인간은 그렇지 않음 — 같은 사람도 컨디션, 기분, 맥락에 따라 같은 버그에 대해 어떤 날은 짜증내고 어떤 날은 넘어감.

**PRISM의 접근**: 확률미분방정식(Stochastic Differential Equation)으로 감정 궤적을 모델링:

```
dE(t) = μ(E, t) dt + σ(E, t) dW(t)
```

- `μ(E, t)`: 드리프트 항 — 감정의 평균적 변화 방향 (OCC appraisal + decay)
- `σ(E, t)`: 확산 항 — 감정의 **확률적 변동폭** (성격에 따라 다름)
- `dW(t)`: Wiener process — 무작위 노이즈

**Personica 적용 (Layer 3 업그레이드)**:

```python
# 기존 (결정론적)
pad_state.pleasure = pad_state.pleasure * decay + appraisal.pleasure_delta

# SDE 적용 (확률적)
noise = persona.emotional_volatility * np.random.normal(0, 1)
pad_state.pleasure = (
    pad_state.pleasure * decay
    + appraisal.pleasure_delta
    + noise * dt**0.5  # 확산 항
)
```

- `emotional_volatility`는 페르소나 속성 (Layer 1b Psychographics)
  - 감정 기복이 큰 사람: σ = 0.3
  - 차분한 사람: σ = 0.05
- **효과**: 같은 제품을 20명이 써도, 같은 "좌절" 이벤트에 대해 **분포**가 생김. 실제 인간 반응의 분산과 유사해짐.
- **PRISM 결과**: 동질적 베이스라인 대비 반응 분포 발산(divergence) **66.7% 감소** — 즉 실제 인간 분포에 66.7% 더 가까워짐

**출처**: [PRISM](https://arxiv.org/abs/2512.19933), MBTI 기반 성격 유형 + SDE 감정 진화 + PC-POMDP 의사결정

---

### 2. 성격 유형 → 행동 파라미터 수학적 매핑 — PRISM

**문제**: 현재 페르소나 성격은 자연어 서술("꼼꼼하고 신중한 성격")이고, LLM이 이를 해석해서 행동에 반영함. 이 방식의 문제:
- **재현성 없음** — 같은 성격 서술을 줘도 LLM이 매번 다르게 해석
- **동질화** — LLM이 성격 차이를 축소시켜 비슷한 행동을 출력 (알려진 Homogeneity 한계)
- **제어 불가** — "이 페르소나는 저 페르소나보다 인내심이 정확히 2배" 같은 정밀 제어 불가

**PRISM의 접근**: MBTI 16유형을 **수치 파라미터 벡터로 변환**. 각 유형이 고유한 감정 반응 함수를 가짐.

**Personica 적용 (Layer 1 업그레이드)**: Big Five를 행동 파라미터로 매핑:

```python
class PersonalityParameters:
    """Big Five → 시뮬레이션 행동 파라미터"""

    # Big Five 원점수 (0~1)
    openness: float          # 개방성: 새 기능 탐색 의향
    conscientiousness: float # 성실성: 체계적 탐색 vs 충동적
    extraversion: float      # 외향성: 피드백 표현 강도
    agreeableness: float     # 친화성: 제품에 대한 관용도
    neuroticism: float       # 신경증: 감정 변동폭 (= SDE의 σ)

    # Big Five → 행동 파라미터 변환
    @property
    def error_tolerance(self) -> int:
        """포기까지 에러 허용 횟수"""
        base = 3
        return max(1, int(base + self.agreeableness * 3 - self.neuroticism * 2))

    @property
    def emotional_volatility(self) -> float:
        """SDE 확산 계수 σ"""
        return 0.05 + self.neuroticism * 0.25  # 0.05 ~ 0.30

    @property
    def exploration_tendency(self) -> float:
        """새 기능 탐색 확률"""
        return 0.2 + self.openness * 0.6  # 0.2 ~ 0.8

    @property
    def methodical_score(self) -> float:
        """단계적(1.0) vs 탐색적(0.0)"""
        return self.conscientiousness * 0.8 + (1 - self.openness) * 0.2

    @property
    def sycophancy_resistance(self) -> float:
        """제품 비판 성향 (LLM Sycophancy 대응)"""
        return (1 - self.agreeableness) * 0.7 + self.neuroticism * 0.3
```

- **효과**: 성격이 자연어 서술이 아닌 **수치**로 정의되므로, 행동 차이가 수학적으로 보장됨
- **LLM 동질화 방지**: LLM이 성격을 "해석"하는 게 아니라, 미리 계산된 파라미터가 행동을 **제어**함
- BrowsingProfile의 각 필드(click_hesitation, back_button_freq 등)도 이 파라미터에서 파생
- Big Five 외에 MBTI 매핑도 가능하나, Big Five가 학술적으로 더 신뢰성 높음 (MBTI의 test-retest reliability 이슈)

---

### 3. PC-POMDP 의사결정 — PRISM

**문제**: 현재 의사결정 모델(BDI-E + Fogg)은 에이전트가 **관찰 가능한 정보를 기반으로** 행동을 결정함. 그런데 실제 사용자는 불완전한 정보 하에서 의사결정을 함:
- "이 메뉴를 클릭하면 내가 원하는 게 나올까?" (모름)
- "가격 페이지가 어딘가에 있을 텐데..." (확실하지 않음)
- "이 기능이 내 문제를 해결해줄 것 같기는 한데..." (불확실)

**PRISM의 접근**: Personality-Conditioned Partially Observable Markov Decision Process (PC-POMDP)
- 에이전트가 환경의 **전체 상태를 모름** (partially observable)
- 관찰한 정보로 belief state(신념 상태)를 업데이트
- 성격 파라미터가 **탐색 vs 활용 트레이드오프**에 영향

**Personica 적용 (Layer 4 업그레이드)**:

```
상태 공간 S: 제품의 모든 페이지/기능/플로우
관찰 공간 O: 현재 보이는 페이지 + 과거 방문 기억
신념 상태 B: "아직 안 본 페이지에 뭐가 있을 것 같은지"에 대한 확률 분포

의사결정:
  - 높은 openness → 탐색(exploration) 선호: 안 가본 곳 방문
  - 높은 conscientiousness → 활용(exploitation) 선호: 알고 있는 경로 반복
  - 높은 neuroticism + 낮은 belief confidence → 이탈 확률 증가
```

- 핵심: **"잘 모르겠어서 불안하다"는 감정이 의사결정에 영향** — 이게 실제 사용자 행동
- "이 앱에서 가격표를 찾고 있는데, 아직 못 찾았고, 3페이지째 탐색 중" → belief confidence 하락 → neuroticism 높은 페르소나는 이탈, 낮은 페르소나는 계속 탐색

---

### 4. GM-Player 아키텍처 — Concordia (Google DeepMind)

**문제**: UXAgent는 모든 에이전트가 동일한 인지 사이클(perceive→feedback→plan→act)을 돎. 에이전트 유형에 따른 인지 과정의 차이를 표현할 수 없음.

**Concordia의 접근**: TRPG 스타일 Game Master + Player 분리
- **Game Master**: 환경을 서술하고, 행동의 결과를 판정
- **Player**: 자기 성격/목표/기억에 기반해 행동 결정
- 각 Player는 **다른 컴포넌트 조합**을 가질 수 있음

**Personica 적용 (전체 아키텍처)**:

```
┌──────────────────────────────────┐
│  Environment Master (= GM)       │
│  ├── Playwright → 페이지 상태     │
│  ├── DOM 파싱 → 구조화된 관찰     │
│  └── 액션 결과 판정               │
└──────────┬───────────────────────┘
           │ 관찰 (structured observation)
           ▼
┌──────────────────────────────────┐
│  Persona Agent (= Player)        │
│  ├── 컴포넌트 A: perceive         │  ← 모든 에이전트 필수
│  ├── 컴포넌트 B: emotion_eval     │  ← 모든 에이전트 필수
│  ├── 컴포넌트 C: reflect          │  ← Power User: 약함 / Novice: 강함
│  ├── 컴포넌트 D: wonder           │  ← 선택적 (현실감 추가)
│  ├── 컴포넌트 E: plan             │  ← 모든 에이전트 필수
│  └── 컴포넌트 F: act              │  ← 모든 에이전트 필수
└──────────────────────────────────┘
```

- **핵심 이점**: 페르소나 유형별로 인지 사이클을 분화할 수 있음
  - Power User: reflect 주기 길게, wonder 없음, plan 단순
  - Novice User: reflect 매 스텝, wonder 활성, plan 상세
  - Impatient User: perceive 빠르게 (스캔), reflect 없음, plan 최소
- UXAgent 대비: UXAgent는 하드코딩된 단일 사이클. Concordia 방식은 설정 기반 조합.
- Concordia의 연관 메모리 검색은 이미 Generative Agents 방식으로 커버됨

**출처**: [Concordia](https://github.com/google-deepmind/concordia), Google DeepMind, v2.0

---

### 5. 장기 시뮬레이션 오류 보정 — GenSim (NAACL 2025)

**문제**: 다중 세션 시뮬레이션에서 페르소나 특성이 시간에 따라 "평균 인간"으로 수렴함.
- Stable Personas 논문 결과: Claude는 -1.6, GPT는 -5.5 personality drift (10점 척도)
- Session 4 이후 모든 페르소나가 비슷하게 행동 → 시뮬레이션 무의미화

**GenSim의 접근**: 자동 오류 감지/보정 메커니즘 내장
- 에이전트 행동이 설정된 페르소나 프로필에서 벗어나면 자동 감지
- 보정 트리거 시 페르소나 원본을 re-injection하여 drift 복구

**Personica 적용 (Layer 5 + 전체 시스템)**:

```python
class PersonaDriftMonitor:
    """세션 간 페르소나 특성 드리프트 감지/보정"""

    def check_drift(self, session_log, original_persona):
        """
        현재 세션 행동과 원본 페르소나 프로필의 일관성 검증.
        - 행동 파라미터(error_tolerance, exploration 등) 실측값 vs 설정값 비교
        - 감정 반응 패턴이 neuroticism 설정과 일치하는지
        - 어휘/표현 스타일이 페르소나에서 벗어났는지
        """
        drift_score = self._compute_drift(session_log, original_persona)
        if drift_score > DRIFT_THRESHOLD:
            return self._generate_correction(original_persona)
        return None

    def _generate_correction(self, original_persona):
        """
        원본 페르소나의 핵심 특성을 re-inject하는 보정 메모리 생성.
        다음 세션 시작 시 메모리 스트림에 삽입.
        """
        return Reflection(
            content=f"나는 {original_persona.core_traits}인 사람이다. "
                    f"최근 내 행동이 내 성격답지 않았던 것 같다.",
            importance=10  # 최고 중요도
        )
```

- Session 간 checkpoint에서 drift 검사
- 보정이 필요하면, 다음 세션 시작 전에 **페르소나 원본 특성을 고중요도 reflection으로 주입**
- 이렇게 하면 메모리 검색 시 항상 상위에 랭크되어 행동에 영향

**출처**: [GenSim](https://arxiv.org/abs/2410.04360), NAACL 2025 Demo, 최대 10만 에이전트 지원

---

### 6. 마이크로 행동 로깅 — Truman Platform (Cornell)

**문제**: UXAgent는 매 스텝의 **액션**(click, type 등)과 **스크린샷**만 저장함. 실제 사용자 행동의 핵심인 **마이크로 행동**(체류 시간, 스크롤 속도, 망설임, 마우스 궤적)은 누락됨.

**Truman의 접근**: 모든 사용자 활동을 전수 로깅
- 페이지 방문, 버튼 클릭은 기본
- **마우스 움직임** (x, y 좌표 + 시간)
- **스크롤** (위치 + 속도 + 방향)
- **체류 시간** (요소별, 영역별)
- 이 데이터로 "사용자가 어디를 보고 있었는지" 추론 가능

**Personica 적용 (데이터 수집 레이어)**:

에이전트가 브라우저를 조작할 때 마이크로 행동을 **시뮬레이션하고 기록**:

```python
class MicroBehaviorLog:
    """에이전트의 마이크로 행동 로그"""

    # 각 스텝에서 기록
    dwell_time_ms: int           # 현재 페이지 체류 시간 (페르소나 속성에서 파생)
    scroll_depth: float          # 0.0~1.0 (어디까지 스크롤했나)
    hesitation_before_click: int # 클릭 전 망설임 시간 (ms)
    elements_scanned: list[str]  # 시선이 머문 요소들 (scan_pattern에 따라)
    back_navigation: bool        # 뒤로가기 했는지
    search_attempted: bool       # 검색을 시도했는지

    # 분석용 파생 메트릭
    confusion_signal: bool       # 같은 영역 반복 스크롤 = 혼란
    rage_click: bool             # 같은 요소 연속 클릭 = 좌절
    abandonment_signal: bool     # 긴 체류 + 무행동 = 이탈 고려 중
```

- **핵심**: 이 데이터가 있어야 "온보딩 3단계에서 7초간 멍하니 있었다"는 수준의 리포트가 가능
- Playwright에서 마우스 좌표/스크롤 이벤트 캡처 기술적으로 가능
- 페르소나의 BrowsingProfile(scan_pattern, click_hesitation 등)이 마이크로 행동을 결정
- UXAgent 대비: 행동 해상도가 "click" 수준에서 "3초 망설인 뒤 click" 수준으로 상승

**출처**: [Truman Platform](https://github.com/cornellsml/truman_2023), Cornell Social Media Lab

---

### 차용 기술 요약 — 우선순위별

| 우선순위 | 출처 | 차용 내용 | 적용 레이어 | 해결하는 문제 |
|---------|------|----------|-----------|-------------|
| **P0** | PRISM | 성격→행동 파라미터 수학적 매핑 | Layer 1 | LLM 동질화 방지, 재현성 확보 |
| **P0** | PRISM | SDE 기반 감정 진화 | Layer 3 | 결정론적 감정 궤적 → 확률적 분포 |
| **P1** | GenSim | 장기 시뮬레이션 오류 보정 | Layer 5 | 페르소나 드리프트 방지 |
| **P1** | Concordia | GM-Player 아키텍처 패턴 | 전체 | 에이전트 유형별 인지 사이클 분화 |
| **P1** | Truman | 마이크로 행동 로깅 | 데이터 수집 | 행동 해상도 향상 → 리포트 품질 |
| **P2** | PRISM | PC-POMDP 의사결정 | Layer 4 | 불완전 정보 하 탐색 모델링 |

### 명시적으로 차용하지 않는 것 (소셜 미디어 전용)

| 기술 | 출처 | 제외 이유 |
|------|------|----------|
| 추천 알고리즘 (RecSys) | OASIS | Personica의 문제와 무관 — 피드 추천이 없음 |
| 팔로우/팔로워 소셜 그래프 | OASIS, S³ | 개인 체험 시뮬레이션에 불필요 |
| 리포스트/좋아요 역학 | MOSAIC | 소셜 미디어 특화 행동 |
| 콘텐츠 바이럴리티 메트릭 | OASIS | 시장 동역학 시뮬레이션은 MVP 범위 밖 |
| 집단 극화/에코챔버 | PRISM, S³ | 개인 체험에 영향 없음 |

---

| LLM 시뮬레이션 한계 | 내용 | 대응 |
|---------------------|------|------|
| Sycophancy | 제품에 대해 너무 관대 | 명시적 비판 프롬프트, 페르소나별 비판 성향 |
| Homogeneity | 다양한 페르소나를 줘도 응답 유사 | temperature 조절, 인터뷰 기반 그라운딩 |
| Temporal Decay | 페르소나 특성이 "평균"으로 수렴 | Reflection 필수 (없으면 48h 내 퇴화) |
| 좁은 분산 | 실제 인간보다 반응 분포 좁음 | 극단적 페르소나 포함, 분산 비교 검증 |
| Item-level 실패 | 전체 패턴은 재현하나 개별 항목에서 오차 | 개별 행동 수준 캘리브레이션 필요 |

---

## 실제 인간 웹 행동 데이터 (시뮬레이션 캘리브레이션 기준)

NNGroup 연구 기반:
- 페이지 텍스트의 **~20%만 읽음** (79%는 스캔)
- 평균 세션 시간: **2분 38초**
- 바운스율: **44-45%** (모바일 58-60%)
- F-패턴/Z-패턴/Layer-cake 스캔
- 페이지 로드 **1초 이상**이면 "느리다" 인식
- 65세+: 태스크 수행 **43% 느림**, 95%가 단계적 행동 패턴
- **16%만** 기사를 전체 읽음
