# Competitive Analysis: AI 합성 사용자 테스팅 시장 — 심층 분석

**Date**: 2026-03-16
**Version**: 2.0 (전면 재작성)
**Analyzed**: 직접 경쟁사 6개 + 학술 시스템 2개 + 간접 경쟁사 3개
**Lens**: 기술 접근, 포지셔닝, 시뮬레이션 깊이, 타겟 세그먼트, 펀딩/트랙션, 가격, 위협도

---

## 1. Market Overview

### 1.1 카테고리 정의

"AI 합성 사용자(Synthetic Users)"는 AI가 생성한 가상의 사용자 프로필이 실제 사람을 대신하여 제품/서비스에 대한 피드백을 제공하는 기술이다. 2025년부터 본격적으로 상용 시장이 형성되었으며, 2026년 현재 접근 방식에 따라 크게 4가지 하위 카테고리로 분화되고 있다:

| 하위 카테고리 | 접근법 | 대표 플레이어 |
|---|---|---|
| **예측 기반 실험** | 기존 데이터 + Figma 디자인 → 행동 예측 | Blok |
| **설문/인터뷰 시뮬레이션** | AI 페르소나에게 질문 → 답변 생성 | Aaru, Synthetic Users, Custovia |
| **네트워크/여론 시뮬레이션** | 수천 페르소나 간 사회적 상호작용 시뮬레이션 | Artificial Societies |
| **실제 제품 조작 시뮬레이션** | 브라우저 자동화로 실제 제품 사용 + 감정/인지 시뮬레이션 | **ShipCheck** (유일) |

### 1.2 시장 규모와 성장

- **UX 서비스 시장**: 2025년 $6.4B → 2034년 $77.2B (CAGR 31.2%) — Fortune Business Insights
- **합성 사용자 채택률**: UX 리서처의 48%가 2026년 가장 임팩트 있는 트렌드로 "합성 사용자/AI 참가자"를 꼽음 — Maze 2026 리포트
- **시장 예측**: 3년 내 시장조사의 절반 이상이 AI 합성 페르소나로 수행될 것 — Qualtrics 2025 리포트

### 1.3 핵심 시장 신호

| 이벤트 | 시기 | 의미 |
|---|---|---|
| Aaru $1B 밸류에이션 (Series A) | 2025.12 | "합성 리서치" 카테고리의 대형 벤처 검증 |
| Blok $7.5M 시드 | 2025.07 | AI 합성 사용자 + 제품 실험의 수요 확인 |
| Artificial Societies $5.35M (YC W25) | 2025 | 네트워크 시뮬레이션 접근의 투자 유치 |
| UserTesting, User Interviews 인수 | 2026.01 | 전통 리서치 플랫폼의 AI 통합 가속화 |
| Accenture → Aaru 전략 투자 | 2025 | 엔터프라이즈의 합성 리서치 채택 시작 |

### 1.4 모든 상용 경쟁사가 실제 브라우저 조작을 회피

이 시장의 가장 중요한 구조적 특징: **어떤 상용 서비스도 Playwright/Selenium으로 실제 프로덕션 제품을 조작하지 않는다.** 전부 Figma/설문/데이터 기반으로 우회. 이유:
1. 컴퓨팅 비용 (브라우저 인스턴스 × 페르소나 수)
2. 인증/계정 문제 (로그인 벽)
3. 기술적 복잡도 (임의 웹사이트에서 안정적 자동화)
4. 속도 제약 (실제 조작은 설문 대비 수십 배 느림)

학술에서만 UXAgent와 AgentA/B가 실제 웹 조작을 시도했으며, 상용 서비스로는 ShipCheck이 유일하다.

---

## 2. Direct Competitors — 상세 분석

### 2.1 Blok — $7.5M, 가장 직접적 경쟁자

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **회사명** | Blok Intelligence Inc. |
| **설립** | 2024년 |
| **본사** | 미국 (Sacramento 추정, MaC VC가 LA 기반) |
| **사이트** | [joinblok.co](https://www.joinblok.co/) |
| **스텔스 탈출** | 2025.07.08 |
| **팀** | "small, high-caliber team" — exited founders, Stanford/Harvard/Berkeley researchers |

#### 창업자
- **Tom Charman** (Co-founder & CEO): 10년간 3개 스타트업 창업. 국가 안보/국방 데이터 사이언티스트 출신. 23세에 TEDx 강연. 영국 정부 및 EU 의회에 데이터 정책 자문. Ludwig-Maximilians-Universitat Munchen 교육
- **Olivia Higgs** (Co-founder): 시리얼 앙트러프리너 (여행 및 학습 분야)

#### 펀딩

| 라운드 | 금액 | 리드 | 참여 |
|---|---|---|---|
| Pre-seed | ~$2.5M | Protagonist | Rackhouse, Weekend Fund (Ryan Hoover), Blank Ventures, Correlation, Karman |
| Seed | $5M | MaC Venture Capital | 위 + 추가 엔젤 (Discord, Google, Meta, Apple, Snapchat, Pinterest, Airbnb 출신) |
| **합계** | **$7.5M** | | |

#### 포지셔닝 + 타겟 고객 + 핵심 메시지

- **포지셔닝**: "Product experimentation platform" — 4-6주 A/B 테스트를 몇 시간으로 압축
- **핵심 메시지**: "Simulate before you ship" — directionally accurate, explainable insights
- **타겟**: 금융/헬스케어 PM, Growth Team, UX Researcher. 규제 산업에서 라이브 A/B 테스트가 어려운 팀
- **증언 출처**: Meta Product Lead, Spotify Senior Data Scientist, Hex CEO, Uber Eats Head of Growth, Booking.com ex-Group PM (단, Blok 사용 증언인지 일반 관점 인용인지 불분명)

#### 기술 접근

```
입력: 이벤트 로그 (Amplitude/Mixpanel/Segment) + Figma 디자인 + 실험 가설
  ↓
처리: 행동 모델링 (behavioral science + deep learning + GenAI)
     - OCEAN 심리학 기반 디지털 성격 유형 분류
     - 행동 클러스터: high-intent, skeptics, risk-averse 등
     - "cognitive biases, decision styles, attention patterns" 통합
     - 0파티/1파티 데이터 기반 지속적 백테스팅
  ↓
출력: 페르소나별 분석 리포트, 전환율/성과 예측, 챗봇 질의 인터페이스
```

**핵심: 실제 제품을 브라우저로 조작하지 않음.** Figma 디자인 파일 + 이벤트 로그 데이터 기반 행동 예측.

#### 강점 (구체적 근거)
1. **실데이터 기반 정확도**: Amplitude/Mixpanel 실사용 데이터에서 페르소나 생성 → 행동 예측의 데이터 기반 신뢰성
2. **$7.5M 펀딩 + 강력한 투자자**: MaC VC 리드, FAANG 출신 엔젤 다수 → 채용/BD 여력
3. **"Directionally accurate" 포지셔닝**: 과장 없이 "방향성 정확도"를 약속 → 엔터프라이즈 신뢰 구축
4. **규제 산업 집중**: 금융/헬스케어처럼 라이브 테스트가 위험한 도메인에서 강력한 PMF 잠재력
5. **행동과학 기반 프레임워크**: "cognitive biases, decision heuristics, interaction priors" 명시 → 학술적 기반

#### 약점 (구체적 근거)
1. **기존 사용자 데이터 필수**: Amplitude/Mixpanel 데이터가 없으면 사용 불가 → MVP/신규 제품 불가
2. **실제 제품 미사용**: Figma 디자인 위에서만 시뮬레이션 → 실제 DOM 인터랙션, 응답시간, 실시간 상태 반영 불가
3. **감정/인지 시뮬레이션 미확인**: 어떤 공개 자료에서도 OCC, PAD 등 감정 모델 언급 없음
4. **선별적 온보딩**: Demo 예약 기반 → 셀프서브 불가, 진입 장벽 높음
5. **반복 사용 시뮬레이션 없음**: Day 1/7/30 습관 형성/리텐션 예측에 대한 언급 없음

#### 가격 모델
- **SaaS 기반** — 구체적 가격 미공개
- Demo 예약 기반 세일즈. 엔터프라이즈 가격대 추정
- 매출 목표: "mid-single-digit millions" (2025년)

#### 최근 동향 (6개월 이내)
- 2026.03 기준: Demo 예약 기반 선별적 온보딩 유지 (GA 여부 미확인)
- PitchBook에 2026 Company Profile 등록, 추가 펀딩 소식 없음
- 금융/헬스케어 early adopters 유지 중

#### 위협도 평가: **중간-높음**
가장 유사한 카테고리에 있고, $7.5M 자금력 보유. 단, 기술 접근이 근본적으로 달라 단기 직접 경쟁보다는 카테고리 내 다른 포지션에 위치.

---

### 2.2 Aaru — $1B 밸류에이션, 카테고리 교육자

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **회사명** | Aaru |
| **설립** | 2024.03 |
| **본사** | 미국 |
| **사이트** | [aaru.com](https://aaru.com/) |
| **핵심 제품** | Lumen (프라이빗 섹터용 예측 엔진) |
| **팀 규모** | 미공개 |

#### 창업자
- **Cameron Fink** (Co-founder & CEO): 창업 당시 18세. 선거 예측으로 기술 검증 시작. 2020년 선거에서 실제 결과 대비 0.5% 이내 예측 정확도
- **Ned Koh** (Co-founder): 창업 당시 19세
- **John Kessler** (Co-founder): 창업 당시 15세. 테크 프로디지
- **어드바이저**: Dave Burwick (Boston Beer 전 CEO), Frank Luntz (저명한 여론조사 전문가)

#### 펀딩

| 라운드 | 금액 | 리드 | 비고 |
|---|---|---|---|
| Series A | >$50M | Redpoint Ventures | 멀티-티어 밸류에이션: 일부 $1B, 블렌디드 < $1B |
| Accenture 전략 투자 | 미공개 | Accenture Ventures | Lumen 통합 협약 |
| **합계** | **>$50M** | | **헤드라인 밸류에이션 $1B** |

#### 포지셔닝 + 타겟 고객 + 핵심 메시지

- **포지셔닝**: "Rethinking the science of prediction" — 멀티 에이전트 AI로 인간 행동 예측
- **핵심 메시지**: "Near-instant customer research" — 수분 내 행동 예측 결과
- **타겟**: 대기업 (Accenture, EY, IPG), 컨설팅, 정치 캠페인, 금융/자산관리
- **유스케이스**: 신제품 개발, 마케팅, 고객 전략, 고객 서비스, 선거 예측

#### 기술 접근

```
입력: 타겟 인구통계/지역 정의 + 연구 질문
  ↓
처리: 멀티 에이전트 AI 시스템
     - 고유 + 공개 데이터 기반 행동 시뮬레이션
     - 수천 개 에이전트 동시 배포
     - 설문/포커스그룹 대체 예측 엔진
  ↓
출력: 행동 예측 결과 (90%+ 실제 설문 상관관계)
```

**핵심: 실제 제품을 사용하지 않음.** 설문/여론 기반 예측 엔진. 제품 UX 테스팅이 아닌 리서치/예측에 가까움.

#### 강점 (구체적 근거)
1. **$1B 밸류에이션 + >$50M 자금**: 시장에서 가장 큰 자금력. 카테고리 인지도 확산 역할
2. **검증된 예측 정확도**: NY 민주당 프라이머리 예측 성공. 90%+ 설문 상관관계
3. **대형 고객 확보**: Accenture (Lumen 통합), EY, IPG → 엔터프라이즈 신뢰
4. **Accenture Song 통합**: Lumen이 Accenture의 AI 제품/서비스에 직접 통합 → 대규모 배포 채널
5. **10대 창업자 화제성**: 18-19세 창업자 스토리 → 미디어 주목도 높음

#### 약점 (구체적 근거)
1. **ARR < $10M**: $1B 밸류에이션 대비 매출 극히 낮음 (100x+ revenue multiple)
2. **실제 제품 미사용**: 설문/여론 시뮬레이션 — "제품을 써보고 어떤 경험을 하는가"에 답할 수 없음
3. **멀티-티어 밸류에이션 논란**: 블렌디드 밸류에이션은 $1B 미만 — 밸류에이션 과장 가능성
4. **제품 UX 테스팅과 JTBD 다름**: 마케팅/여론/리서치 → UX 사용성 테스트와는 본질적으로 다른 문제

#### 가격 모델
- 미공개. 엔터프라이즈 세일즈
- 대형 고객 위주 계약 구조 추정

#### 최근 동향 (6개월 이내)
- 2026.03: "Teens, AI, and Billions: The Startup That Replaces Focus Groups" 기사 — 지속적 미디어 노출
- Accenture Song과의 Lumen 통합 진행 중
- 부동산/자산관리 분야로 확장 (EY 협업)

#### 위협도 평가: **낮음 (직접 경쟁), 중간 (간접 영향)**
다른 JTBD를 풀고 있어 직접 경쟁 위험은 낮음. 단, "AI 합성 사용자" 카테고리의 기대치와 정의를 형성하는 데 영향력이 크므로 간접적으로 모니터링 필요.

---

### 2.3 Synthetic Users — Unfunded, 가장 성숙한 인터뷰 플랫폼

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **회사명** | Synthetic Users |
| **설립** | 2023년 |
| **본사** | Lisbon, Portugal |
| **사이트** | [syntheticusers.com](https://www.syntheticusers.com/) |
| **팀** | 소규모 (Kwame Ferreira + 엔지니어링 팀) |
| **펀딩** | Unfunded |

#### 창업자
- **Kwame Ferreira** (Founder & CEO): 앙골라 출생, 브라질/포르투갈 성장. Lisbon 미술 아카데미 5년, Berlin 미디어 아트, Boston Sociable Media 연구. Kwamecorp 창업 (Intel, Samsung, Google 협업). Impossible (Lily Cole와 공동 창업) 플랫폼 운영 경험. 디자인 + 기술 + 사회적 미디어의 교차점에서 커리어 구축

#### 포지셔닝 + 타겟 고객 + 핵심 메시지

- **포지셔닝**: "User research without the headaches" — AI 인터뷰/설문 참가자 플랫폼
- **핵심 메시지**: 실제 사용자 리서치의 시간/비용 문제를 AI로 해결
- **타겟**: PM, UX 리서처, 제품 팀
- **고객 채널**: Comcast NBCUniversal LIFT Labs와 파트너십, Product Hunt 활성

#### 기술 접근

```
입력: 연구 질문/시나리오 + (선택적) 독자 데이터로 페르소나 enrichment
  ↓
처리: 멀티 에이전트 아키텍처
     - Planner → Interviewer → Critic/Reviewer 에이전트 체인
     - FFM (Big Five) 성격 모델 기반 페르소나 생성
     - "Chain-of-Feeling" — 감정 상태 + OCEAN 성격 특성 결합
     - Shuffle v2 — 복수 LLM 간 라우팅으로 다양성/현실성 향상
     - RAG — 도메인 특화 지식 통합
     - 이론적 샘플링 (theoretical sampling) → 포화 점수(saturation score)로 품질 관리
  ↓
출력: 인터뷰 결과 (Problem Exploration, Solution Feedback, Custom Script 등 4가지 유형)
```

**핵심: 실제 제품 미사용.** AI 인터뷰/설문 방식. 단, "Chain-of-Feeling"으로 감정 시뮬레이션을 시도하는 유일한 경쟁사.

#### 강점 (구체적 근거)
1. **Chain-of-Feeling**: 감정 상태 + OCEAN 성격 특성을 결합한 감정 시뮬레이션 — 경쟁사 중 유일하게 감정 레이어를 명시적으로 구현
2. **Shuffle v2**: 복수 LLM 라우팅으로 페르소나 다양성과 현실성(Synthetic Organic Parity) 향상
3. **학술적 방법론 기반**: 이론적 샘플링, 포화 점수, 유기적 인터뷰 벤치마킹 등 리서치 방법론 엄격
4. **FFM (Big Five) 성격 모델**: 심리학 기반 페르소나 생성 체계화
5. **4가지 인터뷰 유형**: Problem Exploration, Solution Feedback, Custom Script 등 다양한 리서치 모드
6. **Gartner 인정**: AI-powered synthetic user research 분야 리더로 인용
7. **RAG 통합**: 독자 데이터로 페르소나 맞춤화 가능

#### 약점 (구체적 근거)
1. **Unfunded**: 성장 속도 및 엔지니어링 투자에 구조적 제한
2. **실제 제품 미사용**: 순수 인터뷰/설문 — "제품을 사용해 본 후의 피드백"이 아닌 "제품에 대해 이야기한 것"
3. **합성 응답의 구체성 부족**: 연구에 따르면 "합성 답변이 실제 답변보다 덜 구체적(less concrete)"
4. **가격 미공개**: 영업팀 접촉 필요 → 셀프서브 진입 장벽

#### 가격 모델
- 미공개 — 영업팀 접촉 필요
- 팀 규모에 따라 스케일하는 구조 시사 ("designed to evolve with your team")

#### 최근 동향 (6개월 이내)
- Chain-of-Feeling, Shuffle v2 등 기술적 진화 지속 공개
- Gartner AI-powered synthetic user research 리더 인용
- 2026.01 Medium 기사: "From static personas to emergent dynamic behavior"
- 펀딩 없이 제품 개발 지속 — 부트스트랩 모드

#### 위협도 평가: **중간**
인터뷰/설문 영역에서 가장 성숙. ShipCheck의 "체험 후 인터뷰" 기능과 비교될 수 있음. Chain-of-Feeling은 감정 시뮬레이션을 먼저 시도한 사례로 주목. 다만 Unfunded 상태로 성장 제한.

---

### 2.4 Uxia — €1M Pre-seed, 가장 유사한 초기 스타트업

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **회사명** | Uxia |
| **설립** | 2025년 |
| **본사** | Barcelona, Spain (Barcelona Activa Startup Lab) |
| **사이트** | [uxia.app](https://www.uxia.app/) |
| **팀** | 소규모 (Google, Gopuff, Shiji, TransferGo 출신) |

#### 창업자
- **Borja Diaz-Roig** (Co-founder & CEO): TransferGo Product Growth Lead 출신. Gopuff, Founderz 경력. Harvard University Program on Negotiation (2019)
- **Victor Perdiguer** (Co-founder & CTO): Shiji Group 기술 통합 리드. Vonzu, NTT Data에서 AI 역할

#### 펀딩

| 라운드 | 금액 | 리드 | 참여 |
|---|---|---|---|
| Pre-seed | ~€1M | Abac Nest Ventures | Encomenda VC, Javier Darriba (UserZoom 공동창업자), Marsal Gavalda (Clarity AI CTO), William Leppard (Oracle AI Director) |

#### 포지셔닝 + 타겟 고객 + 핵심 메시지

- **포지셔닝**: "UX Testing in Minutes with AI Synthetic Testers" — 빠른 합성 사용자 UX 테스팅
- **핵심 메시지**: "Actionable insights in ~5 minutes" — 속도 최우선
- **타겟**: PM, 디자이너, 제품 팀 (유럽, 한국, 미국 고객 보유)
- **트랙션**: 700+ 제품 팀이 사용. Product Hunt Product of the Day/Week/Month 달성

#### 기술 접근

```
입력: Figma/Sketch/Adobe XD 프로토타입 + 타겟 페르소나 정의
  ↓
처리: 독자 AI 파이프라인 + 데이터 프로세싱 모델
     - 인구통계(나이, 국가, 성별, 기술 리터러시) + 행동 프레임워크
     - 공개 온라인 정보 + 업로드된 페르소나 문서 결합
     - Think-aloud 프로토콜 — 합성 사용자가 "생각하며 말하기" 수행
     - 자동 분석: 사용성, 네비게이션, 카피, 접근성 이슈 플래깅
  ↓
출력: Think-aloud 트랜스크립트, AI 히트맵, WCAG 접근성 리포트, A/B 테스트 결과
```

**핵심: 프로토타입/와이어프레임 기반.** 실제 프로덕션 제품이 아닌 디자인 아티팩트 위에서 시뮬레이션.

#### 강점 (구체적 근거)
1. **속도**: ~5분 내 결과 → 시장에서 가장 빠른 피드백 루프
2. **Think-aloud 프로토콜**: 합성 사용자의 사고 과정을 자연어로 출력 → 정성적 인사이트
3. **히트맵 + WCAG 접근성**: 시각적 리포트 + 접근성 자동 검사 → 테이블 스테이크 기능 잘 갖춤
4. **700+ 팀 사용**: Pre-seed 단계 치고 빠른 트랙션
5. **UserZoom 공동창업자 엔젤**: UX 리서치 도메인 전문 엔젤 네트워크
6. **Unmoderated + A/B 테스트**: 다양한 테스트 유형 지원
7. **월 정액 무제한 테스트 + 무료 플랜**: 접근성 높은 가격 모델

#### 약점 (구체적 근거)
1. **프로토타입 기반**: 실제 제품이 아닌 Figma/Sketch 위에서만 동작 → 실시간 인터랙션, 백엔드 상태 반영 불가
2. **€1M Pre-seed**: 극초기 자금 — 기술 깊이와 팀 확장에 제한
3. **감정 시뮬레이션 없음**: Think-aloud는 있으나 구조화된 감정/인지 모델 부재
4. **반복 사용 시뮬레이션 없음**: 단일 세션 테스트만 지원
5. **페르소나 깊이 제한**: 인구통계 + 기술 리터러시 수준 — 의사결정 모델, 인내심 임계값 등 없음

#### 가격 모델
- **Free**: 3 테스트까지
- **Pro**: 월 정액, 무제한 테스트 + 무제한 사용자 (구체적 금액 미공개)
- **Custom**: 팀용 — 내보내기, 통합, 우선 지원

#### 최근 동향 (6개월 이내)
- 2025.11: €1M Pre-seed 클로즈
- 유럽/한국/미국으로 글로벌 확장 중
- 테스트 유형 추가, 페르소나 충실도 향상, 리포트 기능 강화 로드맵 공개
- Barcelona Activa Startup Lab 입주

#### 위협도 평가: **중간**
가장 유사한 포지셔닝("합성 사용자 UX 테스팅")이지만 기술 접근이 다름 (Figma vs Playwright). 속도와 접근성에서 ShipCheck보다 유리. ShipCheck이 "실제 제품 조작의 가치"를 증명하지 못하면 Uxia의 Figma 기반 접근이 "충분히 좋은" 대안이 될 수 있음.

---

### 2.5 Artificial Societies — $5.35M, YC W25, 네트워크 시뮬레이션

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **회사명** | Artificial Societies |
| **설립** | 2024.10 |
| **본사** | London, UK |
| **사이트** | [societies.io](https://societies.io/) |
| **핵심 제품** | Radiant (마케팅/커뮤니케이션 시뮬레이션 플랫폼) |
| **팀** | 9명 |

#### 창업자
- **James He** (Co-founder): YC W25 졸업
- **Patrick Sharpe** (Co-founder)

#### 펀딩

| 라운드 | 금액 | 리드 | 참여 |
|---|---|---|---|
| Pre-seed | 미공개 | Kindred Capital | YC, Pioneer Fund, Ventures Together, Icehouse Ventures, Multimodal Ventures |
| Seed | 미공개 | Point72 Ventures | Sequoia Capital Scout, Figma, Prolific, Google DeepMind 엔젤 |
| **합계** | **$5.35M** | | |

#### 포지셔닝 + 타겟 고객 + 핵심 메시지

- **포지셔닝**: "AI simulations of your target audience" — 네트워크 기반 오디언스 시뮬레이션
- **핵심 메시지**: 실제 오디언스의 반응을 시뮬레이션으로 미리 테스트. "Marketers waste half their spending — simulate to find the best version"
- **타겟**: 마케팅, PR, 전략 커뮤니케이션 팀. F100 기업
- **유스케이스**: 투자자 관계, 고가치 광고, 위기 커뮤니케이션, 평판 관리, 기업 전략 포지셔닝

#### 기술 접근

```
입력: 타겟 오디언스 정의 (또는 소셜 그래프 연결) + 테스트할 콘텐츠/메시지
  ↓
처리: 2.5M+ AI 페르소나 풀
     - 실세계 소셜 행동 데이터 기반 페르소나 구축
     - 행동 분석 엔진으로 학습/정제
     - 300-5,000 페르소나 네트워크 구성
     - 개별 피드백이 아닌 페르소나 간 사회적 상호작용 시뮬레이션
     - 네트워크 내 영향력 맵핑
     - 메시지 변형 자동 생성 + 결과 비교
  ↓
출력: 정량 점수 + 정성 피드백, 영향력 맵, 메시지 변형별 성과 비교
```

**핵심: 실제 제품 미사용.** 의견/반응 네트워크 시뮬레이션. 개별 제품 UX 체험이 아닌 콘텐츠/메시지 반응 테스트.

#### 강점 (구체적 근거)
1. **네트워크 효과 시뮬레이션**: 개별 피드백이 아닌 페르소나 간 사회적 상호작용 — 입소문, 영향력 전파 시뮬레이션 가능
2. **YC W25 졸업 + Point72 Ventures**: 강력한 투자자 신호
3. **$990K 매출 (9명 팀)**: 팀 대비 높은 매출 효율. F100 고객으로 엔터프라이즈 검증
4. **2.5M+ 페르소나 풀**: 실세계 소셜 행동 데이터 기반 대규모 페르소나
5. **Radiant**: 18M+ 응답 전달, $100M+ 의사결정에 영향 → 검증된 트랙션
6. **Pulsar 파트너십**: 오디언스 인텔리전스 플랫폼과 통합 → 배포 채널 확보

#### 약점 (구체적 근거)
1. **실제 제품 미사용**: 콘텐츠/메시지 반응 시뮬레이션이지 제품 체험 시뮬레이션이 아님
2. **UX 테스팅과 다른 JTBD**: 마케팅/PR/커뮤니케이션 → 제품 사용성과는 별개 영역
3. **네트워크 시뮬레이션의 한계**: "온보딩 3단계에서 막혔다"를 네트워크로 시뮬레이션할 수 없음
4. **9명 팀**: 소규모 → 다중 영역 확장 어려움

#### 가격 모델
- **Free**: 3 크레딧 무료 + 2주 트라이얼
- **Pro**: $40/월 — 무제한 시뮬레이션
- **Enterprise**: 맞춤형 오디언스 구축 — 가격 별도

#### 최근 동향 (6개월 이내)
- Radiant 글로벌 출시 — 마케팅/커뮤니케이션 팀 대상
- Product Hunt에서 "Reach by Artificial Societies" 런칭 (LinkedIn 오디언스 시뮬레이션)
- Pulsar와 파트너십 — 오디언스 인텔리전스 연계
- F100 고객 확보, 18M+ 응답 전달

#### 위협도 평가: **낮음**
완전히 다른 JTBD (마케팅/PR vs 제품 UX). ShipCheck의 미래 확장(시장 동역학 시뮬레이션)에서만 간접 경쟁 가능.

---

### 2.6 Custovia AI — 극초기, 파일럿 모집 중

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **회사명** | Custovia AI |
| **설립** | 미확인 (2024-2025 추정) |
| **본사** | 미확인 |
| **사이트** | [custovia.ai](https://custovia.ai/) |
| **팀** | 미공개 |
| **펀딩** | 미확인 (극초기) |

#### 포지셔닝 + 타겟 고객 + 핵심 메시지

- **포지셔닝**: "AI-Powered Customer Intelligence on-demand" — 고객 데이터 기반 합성 페르소나
- **핵심 메시지**: "Hyper-realistic synthetic personas from your customer data"
- **타겟**: Product Team, Founder, Marketing Team. 규제 산업(금융/헬스케어) 강조

#### 기술 접근

```
입력: 고객 데이터 (보안 연결) 또는 큐레이션된 AI 페르소나
  ↓
처리: 데이터 기반 합성 페르소나 생성
     - 프라이버시 퍼스트 — 사용자 데이터 비침해 시뮬레이션
     - 행동 인사이트 기반 검증
  ↓
출력: 기능 검증 결과, 아이디어 킬/투자 판단, 캠페인 세그먼트별 테스트
```

**핵심: 실제 제품 미사용.** 고객 데이터 기반 페르소나 생성 후 질의/검증 방식.

#### 강점
1. **프라이버시 퍼스트**: 규제 산업 타겟에 적합한 포지셔닝
2. **고객 데이터 기반**: 자체 데이터에서 페르소나 생성 → 맞춤 정확도
3. **데이터 없이도 시작 가능**: 큐레이션된 AI 페르소나 옵션 제공
4. **무료 6개월 파일럿**: Q1 2026 코호트 — 적극적 시장 학습

#### 약점
1. **극초기**: 20사 파일럿 모집 단계 — 제품 성숙도 미확인
2. **고객 데이터 의존**: 풍부한 데이터가 있어야 차별화 가능
3. **실제 제품 미사용**: 페르소나 기반 질의 방식
4. **팀/펀딩/트랙션 정보 부재**: 공개 정보 극히 제한적

#### 가격 모델
- 무료 6개월 파일럿 + 파운딩 고객 가격 (20사 한정)
- 정식 가격 미공개

#### 위협도 평가: **낮음**
극초기 + 다른 접근. 단, 고객 데이터 기반 페르소나 생성이 성숙하면 Blok과 유사한 포지션으로 성장할 가능성.

---

## 3. Academic / Open-Source Systems — 상세 분석

### 3.1 UXAgent — Amazon/Northeastern, CHI 2025

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **출처** | Amazon Science + Northeastern University HAI Lab |
| **발표** | CHI EA '25 (2025.04-05, 요코하마) |
| **논문** | [arXiv:2502.12561](https://arxiv.org/abs/2502.12561), [arXiv:2504.09407](https://arxiv.org/abs/2504.09407) |
| **코드** | [github.com/neuhai/UXAgent](https://github.com/neuhai/UXAgent) (오픈소스) |
| **데모** | [uxagent.hailab.io](https://uxagent.hailab.io/) |

#### 기술 접근

```
Phase 1: 페르소나 생성 → LLM이 인구통계 분포에서 N명 생성
Phase 2: 에이전트 실행 → 페르소나별 독립 브라우저 세션 (Playwright)
Phase 3: 설문 → 메모리 트레이스 + 질문지 → LLM 응답

핵심 아키텍처:
- 듀얼 프로세스: System 1 (perceive→feedback→plan→act) + System 2 (reflect→wonder)
- Universal Browser Connector (parser.js): 임의 웹사이트 DOM 파싱 + semantic-id 부여
- 5종 메모리: Observation, Action, Plan, Thought, Reflection
- 메모리 검색: 유사도 + 최근성 + 중요도 가중 점수
```

**핵심: 실제 웹사이트를 Playwright로 조작.** ShipCheck과 가장 유사한 기술 접근. 단, 쇼핑 도메인 전용.

#### 강점
1. **실제 브라우저 조작**: Playwright + Universal Web Connector → 임의 웹사이트에서 작동
2. **듀얼 프로세스 아키텍처**: fast/slow loop 비동기 구조 → 계획+반성 동시 수행
3. **5종 메모리 시스템**: Generative Agents 스타일 메모리 + 중요도 기반 검색
4. **오픈소스**: 전체 코드 공개 → 커뮤니티 기여 가능
5. **CHI 학회 발표**: 학술적 검증, 16명 UX 연구자 평가

#### 약점 (코드 레벨 분석 기반)
1. **감정 시뮬레이션 없음**: OCC, PAD 등 감정 모델 전혀 없음
2. **인지 모델 없음**: Information Foraging, Cognitive Load 등 인지 이론 미적용
3. **쇼핑 전용**: shop_prompts/ 디렉토리 — 도메인 범용성 없음
4. **모든 페르소나 동일 Intent**: `general_intent`만 사용, 개인화 intent 주석 처리됨
5. **비현실적 타이밍**: 고정 ~200ms 대기 + 2초 sleep — 읽기 속도, 망설임 등 미반영
6. **단일 세션**: 반복 사용(Day 1/7/30) 미지원
7. **시각 인식 없음**: HTML 텍스트만 사용, 스크린샷 미활용 (VLM 미사용)
8. **코드 버그**: add_thought() 6번 중복 저장, stuck 감지 로직 없음

#### ShipCheck에 가져올 것 vs 새로 만들 것

**가져올 것 (검증된 컴포넌트)**:
- parser.js (Universal Web Connector) — DOM 파싱, semantic-id
- initscript.js — 네트워크/호버 감지, idle 감지
- env.py (Playwright 래퍼) — 1296줄, 잘 구조화
- 메모리 검색 공식 — 3-score weighted retrieval
- 듀얼 프로세스 패턴 — fast/slow loop
- 트레이싱 구조 — 스텝별 스크린샷/HTML/LLM콜

**새로 만들 것 (ShipCheck 핵심 IP)**:
- 감정 시뮬레이션 (OCC + PAD + Chain-of-Emotion)
- 인지 모델 (Information Foraging + Cognitive Load + Mental Model)
- VLM 기반 시각 인식
- 페르소나별 개인화 Intent (JTBD 기반)
- 반복 사용 (다중 세션 + 습관/이탈)
- 현실적 타이밍 (페르소나별 BrowsingProfile)
- 도메인 범용 프롬프트
- KG 기반 교차 분석

#### 위협도 평가: **중간-높음**
기술적으로 ShipCheck에 가장 가까운 시스템. 오픈소스이므로 누구나 기반으로 상용화 가능. 단, Amazon이 직접 상용 서비스로 출시할 가능성은 낮음 (Amazon Science 연구 프로젝트 성격). 위협은 "UXAgent를 기반으로 하는 새 스타트업"에서 올 수 있음.

---

### 3.2 AgentA/B — Northeastern/Penn State/Amazon, 2025

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **출처** | Northeastern University + Penn State + Amazon |
| **발표** | 2025.04 |
| **논문** | [arXiv:2504.09723](https://arxiv.org/abs/2504.09723) |

#### 기술 접근

```
4개 모듈:
(i) LLM Agent Generation — 100,000 페르소나 풀에서 에이전트 인스턴스화
(ii) Testing Preparation — 실험 설정, 디자인 조건 배치
(iii) Autonomous A/B Simulation — 실제 웹사이트에서 자율 탐색
(iv) Post-Testing Analysis — 결과 집계, 서브그룹 패턴 분석

핵심:
- Environment Parsing Module + LLM Agent + Action Execution Module
- 페르소나: 나이, 교육, 기술 숙련도, 쇼핑 선호 등
- 100,000 페르소나 → 1,000 에이전트 선택 → 실제 웹사이트 A/B 테스트
```

**핵심: 실제 웹사이트에서 A/B 테스트.** 대규모 페르소나 기반 자동화된 비교 실험.

#### 강점
1. **실제 웹사이트 조작**: 라이브 웹 플랫폼에서 에이전트가 직접 상호작용
2. **대규모**: 100,000 페르소나 풀 → 1,000 에이전트 동시 실행
3. **검증된 결과**: Amazon.com에서 실험, 1M 실제 사용자 데이터와 방향 일치 확인
4. **서브그룹 분석**: 인구통계별, 행동별 패턴 자동 분석
5. **효율성**: 실제 사용자 대비 더 적은 액션으로 태스크 완료 → 목적 지향적

#### 약점
1. **감정/인지 시뮬레이션 없음**: 순수 행동 + 태스크 완료 중심
2. **A/B 테스트 전용**: "어떤 변형이 나은가"에 답하지만, "왜 이탈하는가"에는 답하지 않음
3. **학술 프로젝트**: 상용화 계획 미확인
4. **쇼핑 도메인 중심**: Amazon.com 사례 연구 — 범용성 미검증
5. **단일 세션**: 반복 사용 시뮬레이션 없음

#### 위협도 평가: **중간-높음**
100,000 페르소나 + 실제 웹 조작 + Amazon 연구 역량. 상용화되면 직접 경쟁. 다만 감정/인지 시뮬레이션 없으므로 ShipCheck의 핵심 차별점(5-Layer)은 유지됨.

---

### 3.3 [참고] SimAB — 2026.03 신규 논문

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **논문** | [arXiv:2603.01024](https://arxiv.org/html/2603.01024v1) |
| **발표** | 2026.03 (약 2주 전) |

#### 기술 접근

웹페이지 디자인 스크린샷 + 전환 목표를 입력받아, 페르소나 조건화된 AI 에이전트가 A/B 테스트를 시뮬레이션. 실제 브라우저 조작이 아닌 **스크린샷 기반 선호 표명** 방식.

#### 결과
- 47개 히스토리컬 A/B 테스트 대비 **67% 전체 정확도, 고신뢰 케이스 83% 정확도**
- LLM 체계적 편향 완화를 위한 counterbalancing + neutral naming 기법 적용

#### 의의
AgentA/B의 "실제 웹 조작" 접근과 달리, 스크린샷만으로 방향성 예측이 가능함을 보여줌. Blok/Uxia의 "디자인 기반 예측"의 학술적 뒷받침이 될 수 있음.

---

## 4. Indirect Competitors — 간접 경쟁사 분석

### 4.1 UserTesting.com — 전통 UX 리서치의 대표

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **매출** | ~$180M TTM (2026.03) |
| **펀딩** | $441M (Sunstone Partners, Thoma Bravo) |
| **핵심** | 실제 인간 참가자 리크루팅 + 비디오 리뷰 |
| **사이트** | [usertesting.com](https://www.usertesting.com/) |

#### JTBD 겹침: "다양한 사용자 피드백 수집"

#### 최근 동향 (6개월 이내)
- **2026.01**: User Interviews 인수 → 리서치 파이프라인 통합 강화
- **2026.01**: UserTesting for Figma 출시 — AI 기반 고객 인사이트를 Figma 디자인 워크플로우에 직접 임베드
- **AI 기능 확장**: AI 기반 리크루팅 최적화, AI 요약, AI 사기 방지, Results API
- ML 투자 2019년부터 지속 — 인사이트 도출 속도/품질 개선

#### ShipCheck과의 비교

| 차원 | UserTesting | ShipCheck |
|---|---|---|
| **참가자** | 실제 인간 | AI 페르소나 |
| **속도** | 시간~일 | 분~시간 |
| **비용** | $49+/테스트 (수백 달러 이상) | 목표 $20-50 |
| **규모** | 1-50명 (비용 비례) | 20-500 AI 페르소나 |
| **피드백 품질** | 최고 (실제 인간) | 검증 필요 (AI 시뮬레이션) |
| **감정 진실성** | 실제 감정 | 시뮬레이션된 감정 |

#### 위협/기회
- **위협**: UserTesting이 AI 합성 사용자 기능을 추가하면 (예: Figma 통합 + 합성 사용자) 강력한 하이브리드 제공 가능. User Interviews 인수로 리크루팅 파이프라인까지 소유 → AI 대체 동기 감소 가능성도
- **기회**: UserTesting의 가격/시간은 인디해커에게 접근 불가. ShipCheck은 이 가격/속도 갭에 포지셔닝

---

### 4.2 Maze — $60M 펀딩, 프로토타입 기반 unmoderated 테스팅

#### 기본 정보

| 항목 | 내용 |
|---|---|
| **펀딩** | $60M (4 라운드 — Amplify Partners, Seedcamp, Emergence Capital, Cherry Ventures, Theory Ventures) |
| **팀** | 162명 (2026.01) |
| **핵심** | 프로토타입 기반 unmoderated 테스트 + AI 모더레이터 |
| **사이트** | [maze.co](https://maze.co/) |
| **트랙션** | 60,000+ 제품 팀, 6M+ 참가자 패널 |

#### JTBD 겹침: "빠른 사용성 검증"

#### 최근 동향 (6개월 이내)
- **AI Moderator 출시**: 자율 인터뷰 수행 — 연구 목표 기반 동적 후속 질문, 자동 전사/태깅/요약
- 다국어 지원 + 시간대 무관 24/7 인터뷰
- 라이브 웹사이트 테스팅 + 모바일 테스팅 지원
- Maze AI: 바이어스 감지, 맥락 제안, 동적 팔로업
- 2025 Q2 매출 YoY 1,134% 증가 (절대 금액 미공개)

#### ShipCheck과의 비교

| 차원 | Maze | ShipCheck |
|---|---|---|
| **참가자** | 실제 인간 (6M+ 패널) + AI 모더레이터 | AI 페르소나 |
| **테스트 대상** | 프로토타입 + 라이브 사이트 | 라이브 사이트 |
| **AI 역할** | 인터뷰 모더레이션/분석 보조 | 페르소나 = AI (사용 + 감정 + 인지 전체) |
| **규모** | 인간 참가자 수 × 비용 | AI 페르소나 무제한 (컴퓨팅 비용) |
| **속도** | 인간 리크루팅 소요 | 즉시 (세팅 후) |

#### 위협/기회
- **위협**: Maze가 AI 합성 참가자를 자체 패널에 추가하면 ("실제 인간 + AI 합성 하이브리드") 강력한 포지션
- **위협**: 라이브 웹사이트 테스팅을 이미 지원 — Playwright 기반 에이전트 추가 시 직접 경쟁
- **기회**: Maze는 인간 참가자 기반 비즈니스 모델 — AI 전환은 자기 잠식(cannibalization)

---

### 4.3 Hotjar / FullStory — 세션 리코딩 + 행동 분석

#### Hotjar (Contentsquare 소속)

| 항목 | 내용 |
|---|---|
| **매출** | 추정 $25-100M (Contentsquare 인수 후 비공개) |
| **핵심** | 히트맵, 세션 리플레이, 설문, 피드백 위젯 |
| **최근** | Contentsquare 합병 완료 (2025.07), AI 설문 생성, 감성 분석 |
| **사이트** | [hotjar.com](https://www.hotjar.com/) |

#### FullStory

| 항목 | 내용 |
|---|---|
| **핵심** | Digital Experience Intelligence (DXI) — 세션 리플레이, rage click/dead click 감지, AI 분석 |
| **최근** | StoryAI (자연어 질의, 예측 분석, 자동 이상 감지), Usetiful 인수 (2025.11) |
| **사이트** | [fullstory.com](https://www.fullstory.com/) |

#### JTBD 겹침: "사용자가 어디서 막히는가"

#### ShipCheck과의 비교

| 차원 | Hotjar/FullStory | ShipCheck |
|---|---|---|
| **데이터 소스** | 실제 사용자 세션 (사후) | AI 페르소나 시뮬레이션 (사전) |
| **타이밍** | 출시 후 — 실제 사용자 필요 | 출시 전 — 사용자 없이 시뮬레이션 |
| **인사이트** | "어디서" 막히는가 (행동 데이터) | "왜" 막히는가 (감정/인지 시뮬레이션) |
| **스케일** | 트래픽 비례 | 페르소나 수 설정 |

#### 위협/기회
- **위협**: 매우 낮음. 완전히 다른 타이밍 (사후 vs 사전)과 방법론 (관찰 vs 시뮬레이션)
- **기회**: ShipCheck의 시뮬레이션 결과를 Hotjar/FullStory 리포트 형태로 표현하면 친숙한 UX → 도입 저항 감소

---

## 5. Feature Comparison Matrix (18개 항목)

| # | Capability | **ShipCheck** | Blok | Aaru | Synthetic Users | Uxia | Artificial Societies | Custovia | UXAgent | AgentA/B |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **실제 제품 브라우저 조작** | **O** | X | X | X | X | X | X | **O** | **O** |
| 2 | Figma/프로토타입 기반 | X | **O** | X | X | **O** | X | X | X | X |
| 3 | 기존 사용자 데이터 불필요 | **O** | X | **O** | **O** | **O** | **O** | △ | **O** | **O** |
| 4 | 대규모 페르소나 (100+) | **O** | △ | **O** | △ | △ | **O** | △ | **O** | **O** |
| 5 | 감정 시뮬레이션 (OCC/PAD) | **O** | X | X | △ (CoF) | X | X | X | X | X |
| 6 | 인지 모델 (Cognitive Load 등) | **O** | △ | X | X | X | X | X | X | X |
| 7 | 의사결정 모델 (BDI-E) | **O** | △ | X | X | X | X | X | X | X |
| 8 | 반복 사용 (Day 1/7/30) | **O** | X | X | X | X | X | X | X | X |
| 9 | 인터뷰/후속 대화 | **O** | △ | X | **O** | X | X | △ | X | X |
| 10 | A/B 테스트 | △ | **O** | X | X | **O** | X | X | X | **O** |
| 11 | 설문/여론 조사 | X | X | **O** | **O** | X | **O** | **O** | △ | X |
| 12 | 히트맵/접근성 | X | X | X | X | **O** | X | X | X | X |
| 13 | 스크린샷/행동 로그 | **O** | X | X | X | X | X | X | **O** | △ |
| 14 | Big Five 성격 모델 | **O** | △ | X | **O** | △ | X | X | X | X |
| 15 | Think-aloud 프로토콜 | **O** | X | X | X | **O** | X | X | X | X |
| 16 | 네트워크/소셜 시뮬레이션 | X | X | △ | X | X | **O** | X | X | X |
| 17 | 셀프서브 가능 | **O** | X | X | △ | **O** | **O** | △ | **O** | X |
| 18 | Chain-of-Feeling / 감정 체인 | **O** | X | X | **O** | X | X | X | X | X |

**범례**: O = 지원/구현, △ = 부분적/미확인, X = 미지원, CoF = Chain-of-Feeling

---

## 6. Positioning Maps

### 6.1 Map 1: 시뮬레이션 깊이 vs 제품 조작 수준

```
           시뮬레이션 깊이 (감정/인지/의사결정 충실도)
           ▲
           │
     높음  │                              ★ ShipCheck
           │                              (실제 제품 + 5-Layer 시뮬레이션)
           │
           │
     중간  │        Blok                  UXAgent ◇
           │     (데이터+행동예측)         (브라우저+메모리)
           │
           │  Synthetic Users
           │  (CoF + FFM)     Uxia        AgentA/B ◇
     낮음  │                (Think-aloud)  (대규모 A/B)
           │
           │  Aaru         Artificial
           │  (여론예측)   Societies
           │              (네트워크)  Custovia
           │
           └──────────────────────────────────────────► 제품 조작 수준
             설문/디자인      프로토타입      실제 제품
             기반              기반           브라우저 조작

★ = ShipCheck    ◇ = 학술 시스템
```

### 6.2 Map 2: 제품 라이프사이클 시점 vs 타겟 고객 규모

```
           타겟 고객 규모
           ▲
           │
  엔터프    │  Aaru ($1B)       Blok ($7.5M)
  라이즈    │  (대기업 리서치)   (Growth팀 A/B)
           │
           │       Artificial Societies
           │       (F100 마케팅)
  스타트업/ │                    Custovia
  SMB      │  Synthetic Users   (데이터있는팀)
           │  (PM/리서처)
           │                           ★ ShipCheck
           │       Uxia                (인디해커/초기)
  인디      │    (PM/디자이너)
  해커      │
           │
           └──────────────────────────────────────────► 제품 라이프사이클
             아이디어/     디자인/       MVP/        성장/
             컨셉         프로토타입     첫 사용자    최적화
```

### 6.3 Map 3: 속도 vs 인사이트 깊이

```
           인사이트 깊이
           ▲
           │
     높음  │                              ★ ShipCheck
           │                              (2시간, 1인칭 경험 리포트)
           │
           │            Blok
     중간  │         (수 시간, 전환율 예측)
           │
           │  Synthetic Users              UXAgent ◇
           │  (수 분, 인터뷰)
     낮음  │                Uxia           AgentA/B ◇
           │             (5분, Think-aloud)
           │  Aaru
           │  (수 분, 여론)  Artificial Societies
           │
           └──────────────────────────────────────────► 속도
             시간~일        수십분~시간      수분
```

---

## 7. Differentiation Opportunities (6개)

### 7.1 "유일한 실제 제품 조작" — 기술적 해자

**설명**: 모든 상용 경쟁사가 Figma/설문/데이터 기반으로 우회하는 상황에서, Playwright로 실제 DOM을 조작하여 제품을 체험하는 것은 ShipCheck만의 접근.

**방어 가능성**: **높음**
- Blok이 전환하려면 기술 스택 완전 재구축 + 데이터 기반 DNA와 충돌
- Uxia가 전환하려면 Figma 기반 워크플로우 포기 + 컴퓨팅 비용 구조 변경
- Aaru/Artificial Societies는 아예 다른 JTBD → 전환 동기 없음
- 경쟁사가 진입하더라도 "실제 조작의 안정성/범용성" 엔지니어링에 12-18개월 소요 추정

**핵심 리스크**: "실제 조작 vs Figma 시뮬레이션"의 품질 차이를 정량적으로 증명해야 함. 차이가 미미하면 비용/속도 우위인 Figma 접근이 승리.

---

### 7.2 "5-Layer 감정/인지/의사결정 시뮬레이션" — 시뮬레이션 충실도

**설명**: OCC 감정 모델(22개 카테고리) + PAD 3차원 감정 상태 + Cognitive Load + Information Foraging + BDI-E 의사결정 + Memory Stream + Persona Drift Monitor. 어떤 경쟁사도 이 깊이의 통합 구현을 공개하지 않음.

**방어 가능성**: **중간-높음**
- 이론 자체는 공개(학술 논문)지만, 통합 구현 + 캘리브레이션에 상당한 R&D 시간 필요
- Synthetic Users의 Chain-of-Feeling이 유일하게 유사한 시도이나, 감정 + 인지 + 의사결정 + 메모리의 통합은 없음
- 경쟁사가 모방하려면 6-12개월 R&D 필요 (통합 + 튜닝)

**핵심 가치**: "온보딩 3단계에서 7초간 멍하니 있다가 뒤로가기를 누른 이유: 인지 부하 점수 0.82, 좌절감 0.71, 이전 경험 앱과의 멘탈 모델 불일치" 수준의 리포트 품질.

---

### 7.3 "데이터 없이 동작" — Pre-launch MVP 시장

**설명**: Blok은 Amplitude/Mixpanel 필수, Custovia는 고객 데이터 필수. ShipCheck은 URL + 테스트 계정만으로 동작. 아직 사용자가 없는 MVP에 적용 가능한 유일한 "실제 체험" 방식.

**방어 가능성**: **높음**
- 데이터 기반 경쟁사가 "데이터 없이도 가능" 모드를 추가해도, 데이터 없는 시뮬레이션이 핵심 역량이 아님
- 해당 경쟁사의 가치 제안이 "실데이터 기반 정확도"이므로, 데이터 없는 모드는 열등 제품으로 인식될 가능성

**핵심 가치**: 인디해커/초기 스타트업의 유일한 선택지. "Amplitude도 붙이지 않은 MVP를 AI가 써보고 피드백을 준다"는 메시지.

---

### 7.4 "반복 사용 시뮬레이션 (Day 1/7/30)" — 리텐션 예측

**설명**: 어떤 경쟁사/학술 시스템도 다중 세션 시뮬레이션을 제공하지 않음. Memory Stream + Reflection + Habit Strength + Persona Drift Monitor 조합으로 습관 형성/리텐션 예측.

**방어 가능성**: **높음**
- 기술적 복잡도 높음: 세션 간 메모리 유지, 감정 누적, 습관 강도 모델링, 페르소나 드리프트 모니터링
- 기존 경쟁사가 추가하려면 메모리 시스템부터 재구축 필요

**핵심 가치**: "첫인상은 좋은데 3일 후 안 쓸 제품" vs "처음은 어렵지만 습관이 형성되는 제품" — 이 구분은 시장에서 유일하게 ShipCheck만 제공 가능.

---

### 7.5 "실제 체험 기반 인터뷰" — 가상 인터뷰와의 질적 차이

**설명**: Synthetic Users는 "제품에 대해 이야기하기(설문/인터뷰)", ShipCheck은 "제품을 써본 후 이야기하기(체험 후 인터뷰)". 경험 기반 피드백과 가설 기반 피드백의 질적 차이.

**방어 가능성**: **높음**
- 실제 브라우저 조작 + 메모리 스트림 + 감정 궤적을 기반으로 한 인터뷰는 "써보지 않고 답하는" 인터뷰와 구조적으로 다름
- Synthetic Users가 이 방향으로 전환하려면 브라우저 자동화 + 메모리 시스템 전면 구축 필요

**핵심 가치**: "이 화면에서 어떤 느낌이 들었어요?" → "3단계에서 결제 버튼을 찾지 못해서 15초간 스크롤했고, 점점 짜증이 났어요. 비슷한 앱에서는 상단에 있었거든요." — 경험 기반 구체성.

---

### 7.6 "시뮬레이션 리포트의 감정 궤적 시각화" — 리포트 형태 차별화

**설명**: 기존 경쟁사의 리포트는 텍스트 요약 + 정량 지표(전환율 예측 등). ShipCheck은 페르소나별 감정 궤적 타임라인 + 인지 부하 그래프 + 이탈 지점 시각화 + 1인칭 사용기를 결합한 새로운 리포트 포맷.

**방어 가능성**: **중간**
- 리포트 포맷 자체는 모방 가능하나, 기반 데이터(감정/인지 시뮬레이션)가 없으면 내용물이 빈약
- 5-Layer 시뮬레이션과 결합된 리포트는 형식과 내용이 동시에 차별화

**핵심 가치**: Uxia의 히트맵, Blok의 전환율 예측과 다른 차원의 리포트. "이 사용자의 감정이 어떻게 변했는가"를 시각적으로 보여주는 것은 시장에 없음.

---

## 8. Competitive Threats — 시나리오별 분석

### 8.1 위협 시나리오 1: Blok의 하향 확장

**시나리오**: Blok이 "데이터 없이도 사용 가능한 모드"를 추가하거나, URL 기반 시뮬레이션으로 확장
**가능성**: 중간 (12-18개월)
**영향도**: 높음

| 세부 시나리오 | 가능성 | 대응 |
|---|---|---|
| Blok이 Figma 없이 URL 입력 추가 | 중간 | 시뮬레이션 충실도(감정/인지)로 차별화. Blok의 URL 모드는 데이터 없는 "열등 버전"이 될 가능성 |
| Blok이 셀프서브 저가 플랜 출시 | 중간 | 인디해커 세그먼트 선점 + 가격 경쟁력 유지 ($20-50) |
| Blok이 브라우저 자동화 추가 | 낮음 | 기술 스택 완전 재구축 필요. Playwright 엔지니어링 12개월+ 소요 |

**모니터링**: Blok 제품 업데이트, 가격 페이지, Playwright/Selenium 엔지니어 채용, 인디해커 커뮤니티 마케팅

---

### 8.2 위협 시나리오 2: LLM 범용화 — "ChatGPT로 충분한가?"

**시나리오**: GPT-5/Claude 4 등 차세대 LLM이 "이런 사용자인 척 하고 내 제품 리뷰해줘"에 충분히 좋은 답변 제공
**가능성**: 높음 (이미 진행 중)
**영향도**: 높음

| 세부 시나리오 | 대응 |
|---|---|
| "ChatGPT에 URL 주고 리뷰해달라" → 텍스트만 기반 피드백 | ShipCheck은 실제로 써본 경험 기반. "ChatGPT는 버튼을 클릭해보지 않았다" |
| LLM에 스크린샷 주고 UX 리뷰 | ShipCheck은 동적 인터랙션(호버, 스크롤, 입력, 전환)까지 체험. 스크린샷은 정적 단면 |
| AI 코딩 도구(Cursor 등)가 UX 리뷰 기능 추가 | 개발자 워크플로우 통합 시 위협. 다만 "다양한 페르소나 × 감정/인지 시뮬레이션"은 별도 엔지니어링 |

**핵심 방어**: "실제 제품을 조작한 경험 기반 피드백"이어야 함. ChatGPT는 제품을 써보지 않았으므로 구체적 피드백 불가. 이 차이를 증명하는 것이 ShipCheck의 핵심 가설.

---

### 8.3 위협 시나리오 3: UXAgent/AgentA/B의 상용화

**시나리오**: Amazon/대학 연구팀의 학술 시스템이 스타트업으로 스핀오프, 또는 누군가가 오픈소스를 기반으로 상용 서비스 출시
**가능성**: 중간 (6-12개월)
**영향도**: 높음

| 세부 시나리오 | 대응 |
|---|---|
| UXAgent 기반 SaaS 등장 | 감정/인지/반복 사용 시뮬레이션으로 차별화 (UXAgent에는 없음) |
| AgentA/B 기반 A/B 테스트 서비스 등장 | ShipCheck은 A/B 비교가 아닌 "경험 이해" — 다른 JTBD |
| Amazon이 직접 상용 서비스 출시 | 가능성 낮음 (Amazon Science 연구 성격). 단, AWS Marketplace 통해 출시 시 위협 |

**모니터링**: UXAgent GitHub 활동, 관련 논문 저자의 스타트업 활동, Amazon Science 상용화 움직임

---

### 8.4 위협 시나리오 4: 대형 플랫폼의 합성 사용자 기능 추가

**시나리오**: Maze, UserTesting, Figma, 또는 Hotjar/Contentsquare가 자체 합성 사용자 기능을 제품에 통합
**가능성**: 높음 (12-24개월)
**영향도**: 중간-높음

| 세부 시나리오 | 대응 |
|---|---|
| Maze가 AI 합성 참가자 추가 | Maze의 핵심은 인간 참가자 → AI 전환은 자기 잠식. 합성 참가자는 보조 기능 |
| Figma가 합성 사용자 테스팅 내장 | Figma 생태계 내 디자인 기반 테스팅만 → 실제 프로덕션 체험과 다른 레벨 |
| UserTesting이 AI 합성 모드 추가 | User Interviews 인수 + AI 기능 확장 중 → 가능성 높음. 단, "인간 품질" 브랜드와 충돌 |

**모니터링**: Maze/UserTesting AI 기능 로드맵, Figma Dev Mode 확장, Contentsquare AI 전략

---

### 8.5 위협 시나리오 5: Aaru의 제품 UX 영역 확장

**시나리오**: Aaru가 $1B 밸류에이션 자금력으로 "설문/여론"에서 "제품 체험 시뮬레이션"으로 확장
**가능성**: 낮음 (18-24개월)
**영향도**: 매우 높음 (자금력 + 브랜드 + 고객 채널)

| 세부 시나리오 | 대응 |
|---|---|
| Aaru가 브라우저 자동화 팀 구축 | 기술 전환에 12-18개월+ 소요. ShipCheck이 이 기간 내 PMF 확보 필요 |
| Aaru가 Blok/Uxia 인수 | 가격 + 기술 결합 → 강력한 경쟁자. ShipCheck은 감정/인지 깊이로 차별화 유지 |

**모니터링**: Aaru 채용 (브라우저 자동화, Playwright), 인수 뉴스, 제품 로드맵

---

## 9. 전략적 권고

### Double Down (핵심 우위 강화)
1. **실제 제품 조작 + 감정/인지 시뮬레이션 통합**: 유일한 차별점. 이 조합의 가치를 정량적으로 증명하는 것이 최우선
2. **"써본 후 인터뷰" 경험**: Synthetic Users의 "가상 인터뷰"와 질적으로 다른 경험 기반 인터뷰
3. **Day 1/7/30 반복 사용**: 시장에서 유일한 기능. 리텐션 예측이라는 고가치 인사이트 제공

### Close the Gap (테이블 스테이크)
1. **리포트 품질**: Uxia의 히트맵/접근성, Blok의 전환율 예측 수준 참고. 감정 궤적 + 세그먼트 분석으로 차별화된 리포트
2. **속도**: Uxia "5분", Synthetic Users "수 분". ShipCheck은 실제 브라우저 조작이라 구조적으로 느리지만, "2시간 내" 목표 유지
3. **접근성**: Uxia의 무료 플랜 + 월 정액 모델 참고. ShipCheck도 셀프서브 진입 경험 확보 필요

### Ignore (대응 불필요)
1. Aaru의 여론/설문 시뮬레이션 — 다른 JTBD
2. Artificial Societies의 네트워크/PR 시뮬레이션 — 다른 유스케이스
3. Blok의 엔터프라이즈 A/B 테스트 가속 — 다른 시장 시점

---

## 10. Competitive Intelligence 모니터링 체크리스트

### 월간 모니터링

| 대상 | 체크 항목 | 소스 |
|---|---|---|
| **Blok** | 제품 업데이트, 가격 페이지, URL 입력 지원 여부, 채용 (Playwright) | joinblok.co/insights, LinkedIn, TechCrunch |
| **Aaru** | 제품 UX 확장 여부, 인수, 채용 (브라우저 자동화) | aaru.com, LinkedIn, Accenture 뉴스 |
| **Synthetic Users** | 펀딩, Chain-of-Feeling 발전, 브라우저 통합 여부 | syntheticusers.com/science, Product Hunt |
| **Uxia** | Seed 라운드, 실제 제품 테스팅 확장 여부, 가격 변경 | uxia.app, EU-Startups |
| **Artificial Societies** | 제품 UX 확장 여부, 엔터프라이즈 고객 확대 | societies.io, YC updates |
| **UXAgent** | GitHub 커밋, 새 논문, 상용화 움직임 | github.com/neuhai/UXAgent, arXiv |
| **Maze** | AI 합성 참가자 추가 여부, 가격 변경 | maze.co/ai, G2 reviews |
| **UserTesting** | AI 합성 모드, 인수, Figma 통합 확장 | usertesting.com/resources |

### 분기별 분석
- Feature Comparison Matrix 업데이트
- Positioning Map 재평가
- 신규 진입자 스캔 (Product Hunt, YC Demo Day, arXiv)

---

## Sources

### 경쟁사 공식 사이트
- [Blok — joinblok.co](https://www.joinblok.co/)
- [Aaru — aaru.com](https://aaru.com/)
- [Aaru About — aaru.com/about](https://aaru.com/about)
- [Synthetic Users — syntheticusers.com](https://www.syntheticusers.com/)
- [Synthetic Users Science — syntheticusers.com/science](https://www.syntheticusers.com/science)
- [Synthetic Users System Architecture](https://www.syntheticusers.com/science-posts/synthetic-users-system-architecture-the-simplified-version)
- [Synthetic Users Chain-of-Feeling](https://www.syntheticusers.com/science-posts/chain-of-feeling)
- [Synthetic Users Pricing — syntheticusers.com/pricing](https://www.syntheticusers.com/pricing)
- [Uxia — uxia.app](https://www.uxia.app/)
- [Artificial Societies — societies.io](https://societies.io/)
- [Artificial Societies — artificialsocieties.com](https://www.artificialsocieties.com/)
- [Artificial Societies Radiant — radiant.societies.io](https://radiant.societies.io/)
- [Custovia AI — custovia.ai](https://custovia.ai/)
- [UserTesting — usertesting.com](https://www.usertesting.com/)
- [Maze — maze.co](https://maze.co/)
- [Maze AI — maze.co/ai](https://maze.co/ai/)
- [Maze AI Moderator — maze.co/features/ai-moderator](https://maze.co/features/ai-moderator/)
- [Hotjar — hotjar.com](https://www.hotjar.com/)
- [FullStory — fullstory.com](https://www.fullstory.com/)

### 뉴스/펀딩 보도
- [Blok TechCrunch — 2025.07.09](https://techcrunch.com/2025/07/09/blok-is-using-ai-persons-to-simulate-real-world-app-usage/)
- [Blok SiliconANGLE — 2025.07.09](https://siliconangle.com/2025/07/09/blok-raises-7-5m-build-ai-agents-simulate-human-behavior-accelerate-software-testing/)
- [Blok MaC VC](https://macventurecapital.com/blok-is-using-ai-personas-to-simulate-real-world-app-usage/)
- [Blok Technology.org — 2025.07.10](https://www.technology.org/2025/07/10/bloks-ai-personas-test-apps-before-users-ever-see-them/)
- [Aaru Series A — TechCrunch 2025.12.05](https://techcrunch.com/2025/12/05/ai-synthetic-research-startup-aaru-raised-a-series-a-at-a-1b-headline-valuation/)
- [Aaru TechBuzz — Multi-tier Series A](https://www.techbuzz.ai/articles/aaru-hits-1b-valuation-with-multi-tier-series-a-funding)
- [Aaru — La Voce di New York 2026.03.11](https://lavocedinewyork.com/en/news/2026/03/11/teens-ai-and-billions-the-startup-that-replaces-focus-groups/)
- [Accenture → Aaru 투자](https://newsroom.accenture.com/news/2025/accenture-invests-in-and-collaborates-with-ai-powered-agentic-prediction-engine-aaru)
- [EY × Aaru Wealth Management](https://www.ey.com/en_us/insights/wealth-asset-management/how-ai-simulation-accelerates-growth-in-wealth-and-asset-management)
- [Aaru × Accenture — The Drum](https://www.thedrum.com/news/accenture-s-bet-aaru-why-synthetic-data-the-future-marketing-intelligence)
- [Uxia €1M — EU-Startups 2025.11](https://www.eu-startups.com/2025/11/spanish-startup-uxia-lands-e1-million-to-develop-synthetic-user-technology-for-product-teams/)
- [Uxia Pre-seed — The SaaS News](https://www.thesaasnews.com/news/uxia-secures-1m-pre-seed-round)
- [Artificial Societies — Silicon Canals](https://siliconcanals.com/yc-backed-artificial-societies-bags-e4-5m/)
- [Artificial Societies — EU-Startups 2025.08](https://www.eu-startups.com/2025/08/british-ai-startup-artificial-societies-raises-e4-5-million-to-simulate-human-behaviour-at-scale/)
- [Artificial Societies — SiliconANGLE 2025.07.30](https://siliconangle.com/2025/07/30/ai-startup-artificial-societies-simulates-behavior-target-audiences-speed-market-research/)
- [Artificial Societies Revenue — GetLatka](https://getlatka.com/companies/societies.io)
- [Artificial Societies HN Launch](https://news.ycombinator.com/item?id=44755654)
- [UserTesting acquires User Interviews — 2026.01](https://www.usertesting.com/blog/usertesting-acquires-user-interviews)
- [UserTesting for Figma — 2026.01](https://www.usertesting.com/company/newsroom/press-releases/navigating-future-experience-research-usertesting-unveils-new)
- [FullStory StoryAI — 2025.04](https://www.globenewswire.com/news-release/2025/04/02/3054288/0/en/Fullstory-Unveils-AI-Agent-Powered-Behavioral-Data-Solutions-To-Transform-Customer-And-Employee-Experiences.html)
- [FullStory acquires Usetiful — 2025.11](https://www.cmswire.com/digital-experience/fullstory-acquires-usetiful-to-connect-analytics-action/)
- [Hotjar × Contentsquare](https://www.hotjar.com/)

### 학술 논문
- [UXAgent — Amazon Science / CHI 2025](https://www.amazon.science/publications/uxagent-an-llm-agent-based-usability-testing-framework-for-web-design)
- [UXAgent Paper — arXiv:2502.12561](https://arxiv.org/abs/2502.12561)
- [UXAgent System Paper — arXiv:2504.09407](https://arxiv.org/abs/2504.09407)
- [UXAgent GitHub](https://github.com/neuhai/UXAgent)
- [AgentA/B — arXiv:2504.09723](https://arxiv.org/abs/2504.09723)
- [AgentA/B MarkTechPost 해설](https://www.marktechpost.com/2025/04/25/agenta-b-a-scalable-ai-system-using-llm-agents-that-simulate-real-user-behavior-to-transform-traditional-a-b-testing-on-live-web-platforms/)
- [SimAB — arXiv:2603.01024](https://arxiv.org/html/2603.01024v1)

### 시장 리포트/분석
- [Synthetic Users Explained: Top 7 — AIMultiple](https://aimultiple.com/synthetic-users)
- [Maze Future of User Research Report 2026](https://maze.co/resources/user-research-report/)
- [UX Services Market Size — Fortune Business Insights](https://www.fortunebusinessinsights.com/ux-services-market-108780)
- [Qualtrics 2025 Market Research Trends](https://www.qualtrics.com/articles/news/ai-to-drive-massive-changes-to-market-research-in-2025-qualtrics-report-says/)
- [UserTesting Revenue — CompaniesMarketCap](https://companiesmarketcap.com/usertesting/revenue/)
- [Synthetic Users — Making Science](https://www.makingscience.co.uk/blog/synthetic-users/)
- [Comcast LIFT Labs × Synthetic Users](https://lift.comcast.com/smart-insights-less-friction-synthetic-users-is-simplifying-research-w-ai-personas/)

### 내부 문서
- docs/18-blok-deep-dive.md — Blok 심층 분석
- docs/21-pivot-review.md — 경쟁 지형 요약 + 피봇 검토
- docs/01-product-vision.md — ShipCheck 포지셔닝
- docs/03-uxagent-analysis.md — UXAgent 코드 레벨 분석
