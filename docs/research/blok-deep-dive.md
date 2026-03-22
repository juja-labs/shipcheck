# Blok Deep Dive: Personica의 가장 직접적 경쟁자 심층 분석

**Date**: 2026-03-16
**Version**: 1.0
**목적**: Blok이 Personica의 비전을 이미 실현했는지, Personica만의 차별화 여지가 있는지 팩트 기반으로 판단

---

## 1. 회사 기본 정보

### 설립 및 팀

| 항목 | 내용 |
|------|------|
| **회사명** | Blok Intelligence Inc. |
| **설립** | 2024년 |
| **본사** | 미확인 (미국 추정, MaC VC가 LA 기반) |
| **공식 사이트** | [joinblok.co](https://www.joinblok.co/) |
| **스텔스 탈출** | 2025년 7월 8-9일 |
| **팀 규모** | "small, high-caliber team" (구체적 인원 미공개) |
| **채용 중** | engineers, researchers, product thinkers |

### 창업자

**Tom Charman** (Co-founder & CEO)
- 10년간 3개 스타트업 창업 경력 (시리얼 앙트러프리너)
- 첫 번째 스타트업 (2016): 조직 내 직원 니즈 분석 → 인수 합병으로 엑싯
- KOMPAS: 여행 테크 ML 추천 회사 CEO (2017년 Greater Birmingham's Future Face of Innovation and Technology 수상)
- Rassa: Co-founder/CEO
- 두 번째 스타트업 (2021): 호스피탈리티 분야, 팬데믹 중 중단
- 이전 경력: 국가 안보/국방 데이터 사이언티스트
- 23세에 TEDx 강연 (AI와 기술의 미래)
- "20 young entrepreneurs to watch" 선정 (2017)
- 영국 정부 및 EU 의회에 데이터 정책 자문
- 교육: Ludwig-Maximilians Universitat Munchen (뮌헨 대학)
- Angel investor로도 활동 중

**Olivia Higgs** (Co-founder)
- 시리얼 앙트러프리너 (여행 및 학습 분야 경험)
- Blok 블로그의 주요 저자 (8편 중 6편 작성)
- 구체적 이전 경력 정보는 미확인

### 팀 구성 (자체 설명)
- "exited founders, Stanford/Harvard/Berkeley researchers, and AI engineers"
- 국가 안보 행동 모델링, 수백만 사용자 소비자 앱 런칭, 행동과학/헬스케어/금융 분야 연구 경력 보유

### 펀딩 히스토리

| 라운드 | 금액 | 리드 투자자 | 기타 투자자 |
|--------|------|-----------|-----------|
| **Pre-seed** | ~$2.5M (추정) | Protagonist | Rackhouse, Weekend Fund (Ryan Hoover), Blank Ventures, Correlation, Karman |
| **Seed** | $5M | MaC Venture Capital | 위와 동일 + 추가 엔젤 |
| **합계** | **$7.5M** | | |

**엔젤 투자자 출신 회사**: Discord, Google, Meta, Apple, Snapchat, Pinterest, Airbnb

**밸류에이션**: 미공개

### 현재 단계

- 2025년 7월: 스텔스 탈출 발표
- 현재(2026년 3월 기준): **"Book Demo" 기반 선별적 온보딩** (순수 웨이트리스트에서 데모 예약 모델로 전환된 것으로 보임)
- 웹사이트에 "Selective team approval -> Dashboard access -> Data integration -> Tailored simulation setup" 프로세스 명시
- 일부 금융/헬스케어 고객이 이미 사용 중 (early adopters)
- 매출 목표: "mid-single-digit millions" (2025년 기준)
- **GA(General Availability) 여부**: 미확인. 선별적 접근 단계로 판단

---

## 2. 제품 분석

### 핵심 제품 포지셔닝

Blok은 스스로를 **"product experimentation platform"** 으로 정의한다. 핵심 가치 제안:

> "4-6주 걸리는 A/B 테스트를 몇 시간으로 압축"

### 제품 워크플로우 (확인된 내용 기반)

```
Step 1: 데이터 통합
  ├── Amplitude, Mixpanel, Segment에서 이벤트 로그 업로드
  └── 실제 제품 사용 데이터 기반으로 행동 패턴 추출

Step 2: 페르소나 생성
  ├── 행동 모델링으로 사용자 유형별 클러스터링
  ├── "high-intent, skeptics, risk-averse" 등 행동 기반 세그먼트
  └── 실제 사용자 데이터 기반 합성 사용자 프로필 생성

Step 3: 실험 설정
  ├── Figma 디자인 파일 업로드
  ├── 실험 가설 및 파라미터 입력
  └── 사용자 목표(user goals) 정의

Step 4: 시뮬레이션 실행
  ├── AI 페르소나가 제출된 디자인에 대해 시뮬레이션
  ├── 여러 시뮬레이션을 병렬 실행
  └── 제어군 vs 변형군 비교

Step 5: 결과 분석
  ├── 페르소나별 상세 분석 리포트
  ├── 챗봇 인터페이스로 실험 데이터 질의
  └── 전환율/성과 예측 ("directionally accurate")
```

### AI가 실제로 제품을 "사용"하는가?

**핵심 발견: Blok은 실제 프로덕션 제품을 브라우저로 조작하지 않는다.**

확인된 사실:
- Blok은 **Figma 디자인 파일**과 **이벤트 로그 데이터**를 입력으로 받음
- AI 에이전트가 **디자인 목업에 대해** 시뮬레이션을 실행
- "simulate how different user types explore products" - 여기서 "explore"는 실제 브라우저 조작이 아닌 **행동 모델링 기반 예측**
- 공식 사이트에서 "directionally accurate, explainable insights"라고 표현 - 정확한 예측이 아닌 **방향성 제시**
- 어떤 기사/공식 자료에서도 Playwright, Selenium, Puppeteer 등 브라우저 자동화 기술 언급 없음

**결론: Blok은 "실제 제품을 브라우저로 사용하는" 방식이 아니라, "데이터 + 디자인 기반으로 사용자 행동을 예측하는" 방식이다.**

이는 Personica의 접근 방식과 **근본적으로 다르다**:
- **Personica**: 합성 페르소나 시뮬레이션 플랫폼. 제품 체험 모드에서는 Playwright로 실제 프로덕션 MVP를 브라우저에서 조작하고, 서베이·A/B 테스트·전문가 리뷰·광고/퍼널 리서치 등 다양한 모드도 지원. 모든 모드에서 5-Layer 페르소나 리얼리티(감정·인지·의사결정 시뮬레이션)가 핵심 해자.
- **Blok**: Figma 디자인 + 이벤트 로그 데이터로 행동을 **예측**. 실제 제품이 아닌 디자인 아티팩트 기반.

### 페르소나 시뮬레이션 깊이

**확인된 내용:**
- "behavioral modeling, decision heuristics, and interaction priors" 기반 에이전트 생성
- "behavioral science frameworks (cognitive biases, decision styles, attention patterns)" 통합
- "curious, imperfect and full of nuance, just like people are" - 인간적 불완전성 시뮬레이션 추구
- "messy realities of human decision making" 기반
- 행동 클러스터: high-intent, skeptics, risk-averse 등
- OCEAN 심리학 기반 디지털 성격 유형 분류 (웹사이트 퀴즈에서 확인)

**미확인 내용 (공개 자료에 없음):**
- 감정 시뮬레이션 (OCC, PAD 등) 존재 여부
- 인지 부하 모델링 여부
- 멘탈 모델 매칭 여부
- BDI 의사결정 모델 여부
- 메모리/반성 시스템 여부
- 반복 사용 시뮬레이션 여부
- 구체적인 LLM 사용 방식

### 브라우저 자동화 기술

**미확인.** 어떤 공개 자료에서도 브라우저 자동화 프레임워크(Playwright, Selenium 등) 언급 없음. Figma 디자인 기반 시뮬레이션으로 판단되므로, 전통적 의미의 브라우저 자동화가 아닌 **디자인 파일 분석 + 행동 모델링** 접근으로 추정.

### 리포트/아웃풋 형식

확인된 리포트 요소:
- 페르소나별 상세 분석 및 추천사항
- 제어군 vs 변형군 성과 비교
- 전환율/행동 예측
- 챗봇 인터페이스로 실험 데이터에 대한 자유 질의 가능
- "directionally accurate, explainable insights" - 방향성 인사이트 + 설명 가능성 강조

미확인:
- 1인칭 사용기 형태 리포트 여부
- 감정 궤적 시각화 여부
- 마이크로 행동 로그 여부

### 반복 사용 시뮬레이션

**미확인.** Day 1/7/30 시뮬레이션이나 습관 형성, 리텐션 예측에 대한 언급 없음.

### 기술적 접근 요약

```
Blok의 기술 스택 (확인/추정):

입력:
  ├── 이벤트 로그 데이터 (Amplitude, Mixpanel, Segment)
  ├── Figma 디자인 파일
  └── 실험 가설 및 파라미터

처리:
  ├── 행동 모델링 (behavioral science + deep learning)
  ├── GenAI (LLM) + 행동 프레임워크 결합
  ├── 0파티/1파티 데이터 기반 학습
  └── 지속적 백테스팅으로 캘리브레이션

출력:
  ├── 실험 결과 리포트
  ├── 페르소나별 분석
  ├── 전환율/성과 예측
  └── 챗봇 질의 인터페이스
```

---

## 3. 타겟 시장

### 타겟 고객

**현재 (초기 집중):**
- 금융 서비스 (financial services) - 규제로 인해 라이브 A/B 테스트가 어려운 도메인
- 소비자 헬스케어 (consumer health) - 개인정보 민감, 공개 실험 부담
- SaaS 기업
- 이커머스

**타겟 구매자 페르소나:**
- Product Managers
- Growth Teams
- UX Researchers
- Design Leads
- Marketing Teams (카피 테스트)

**주요 고객 증언 출처 (웹사이트 리더십 인용):**
- Meta Product Lead
- Spotify Senior Data Scientist
- Hex CEO
- Uber Eats Head of Growth
- Booking.com ex-Group Product Manager

> 참고: 이들은 "증언"이 아니라 실험 문화에 대한 일반적 관점을 인용한 것. Blok 제품을 실제 사용한 고객 증언인지는 불분명.

**지원 배경:**
- Meta, Uber, Pinterest, Twilio, Square, Strava, Discord, Pleo, Google, Lyft, Airbnb, Slack 출신 리더십이 "backed by"로 표시됨

### 가격 모델

- **SaaS 기반** (구체적 가격 미공개)
- 데모 예약 기반 세일즈 프로세스
- 컴퓨트 비용 최적화에 집중 (자체 언급)
- 매출 목표: "mid-single-digit millions" (2025년)

### 현재 고객/사용자 규모

- 미공개
- "early adopters in financial services and consumer health" 확인
- 선별적 온보딩 프로세스 운영 중

### Personica 타겟과의 비교

| 항목 | Blok | Personica |
|------|------|-----------|
| **비치헤드 세그먼트** | 금융/헬스케어 PM | 인디해커/1인 개발자 |
| **가격대** | 미공개 (엔터프라이즈 추정) | $20-50/시뮬레이션 목표 |
| **세일즈 모델** | Demo-led, 선별적 | Self-serve |
| **기존 데이터 필요** | 필수 (Amplitude/Mixpanel 로그) | 불필요 (URL만 입력) |
| **기존 사용자 필요** | 필수 (행동 데이터 기반) | 불필요 (AI가 처음부터 시뮬레이션) |

**핵심 차이**: Blok은 **기존 제품 데이터가 있는 팀**을 타겟한다. Personica는 **아직 사용자가 없는 MVP/프로토타입**을 타겟한다. 이는 제품 라이프사이클에서 완전히 다른 시점이다.

---

## 4. Personica 5-Layer 아키텍처 대비 비교

### Layer별 상세 비교

#### Layer 1: Persona Profile

| 요소 | Personica | Blok | 비교 |
|------|-----------|------|------|
| Demographics | O (나이, 직업, 소득) | △ (행동 클러스터 기반, 개별 인구통계 불명확) | Personica 우위 |
| Psychographics | O (가치관, 위험회피, 기술태도) | △ (OCEAN 심리학 언급, 깊이 미확인) | 비교 불가 |
| Behavioral | O (인내심, 만족기준, 학습스타일) | O (decision heuristics, interaction priors) | **동등 또는 Blok 우위** (실데이터 기반) |
| Prior Experience | O (유사 제품 경험 -> 멘탈 모델) | △ (미확인) | Personica 우위 |
| JTBD | O (구체적 사용 목표) | O (user goals 입력) | 동등 |
| **Big Five -> 수치 매핑** | O (PRISM 방식) | △ (OCEAN 언급은 있으나 수치 매핑 여부 미확인) | **비교 불가** |
| **실데이터 기반 생성** | X (AI 생성) | **O** (Amplitude/Mixpanel 실데이터) | **Blok 우위** |

**Layer 1 판정**: Blok은 실제 사용자 데이터에서 페르소나를 생성하므로 **데이터 기반 정확도**에서 우위. Personica는 **속성의 구조적 깊이와 다양성**에서 우위. 그러나 Blok의 "실데이터 기반"은 기존 사용자가 있어야 한다는 전제조건이 있음.

---

#### Layer 2: Cognitive

| 요소 | Personica | Blok | 비교 |
|------|-----------|------|------|
| Information Foraging | O | X (미확인) | Personica 우위 |
| Cognitive Load Tracker | O | △ ("cognitive biases" 언급) | Personica 우위 |
| Mental Model Matching | O | X (미확인) | Personica 우위 |
| TAM Score | O | X (미확인) | Personica 우위 |

**Layer 2 판정**: Blok은 "cognitive biases"와 "attention patterns"을 언급하지만, 구조화된 인지 모델이 있는지는 공개 자료에서 확인 불가. Personica의 4가지 인지 이론(Information Foraging, Cognitive Load, Mental Model, TAM) 기반 구조와는 차원이 다를 가능성 높음. **Personica 명확히 우위.**

---

#### Layer 3: Emotion

| 요소 | Personica | Blok | 비교 |
|------|-----------|------|------|
| OCC Appraisal | O (22개 감정 카테고리) | X (미확인) | Personica 우위 |
| PAD State | O (3차원 연속 감정 추적) | X (미확인) | Personica 우위 |
| Emotion Decay | O (지수적 감쇠) | X (미확인) | Personica 우위 |
| SDE 확률적 감정 진화 | O (PRISM 차용) | X (미확인) | Personica 우위 |
| Chain-of-Emotion | O (별도 LLM 콜) | X (미확인) | Personica 우위 |

**Layer 3 판정**: Blok의 어떤 공개 자료에서도 감정 시뮬레이션에 대한 언급을 찾을 수 없음. "curious, imperfect and full of nuance"라는 표현은 있으나, 이는 마케팅 언어이지 감정 모델 존재의 증거가 아님. **Personica 명확히 우위.**

---

#### Layer 4: Decision

| 요소 | Personica | Blok | 비교 |
|------|-----------|------|------|
| BDI-E Model | O | X (미확인) | Personica 우위 |
| Fogg Check (B=MAP) | O | X (미확인) | Personica 우위 |
| Satisficing Gate | O | X (미확인) | Personica 우위 |
| Decision Heuristics | O | O ("decision heuristics" 명시) | **동등** |
| PC-POMDP | O (PRISM 차용) | X (미확인) | Personica 우위 |

**Layer 4 판정**: Blok은 "decision heuristics"를 명시적으로 언급하므로 어떤 형태의 의사결정 모델이 있음. 그러나 BDI-E, Fogg, Satisficing 등 구조화된 프레임워크 사용 여부는 미확인. **Personica가 구조적 깊이에서 우위.**

---

#### Layer 5: Memory

| 요소 | Personica | Blok | 비교 |
|------|-----------|------|------|
| Memory Stream | O (Generative Agents 방식) | X (미확인) | Personica 우위 |
| Reflection | O (임계값 기반 추상화) | X (미확인) | Personica 우위 |
| Habit Strength | O (반복 사용 추적) | X (미확인) | Personica 우위 |
| Persona Drift Monitor | O (GenSim 차용) | X (미확인) | Personica 우위 |
| Multi-session | O (Day 1/7/30) | X (미확인) | Personica 우위 |

**Layer 5 판정**: 반복 사용 시뮬레이션이나 메모리 시스템에 대한 언급이 Blok에서는 전혀 없음. **Personica 명확히 우위.**

---

### 5-Layer 종합 비교

```
                    Personica                 Blok
Layer 1: Profile    ████████░░ (구조적)       ██████████ (실데이터 기반)
Layer 2: Cognitive  ████████░░                ██░░░░░░░░
Layer 3: Emotion    █████████░                ░░░░░░░░░░ (미확인)
Layer 4: Decision   ████████░░                ███░░░░░░░
Layer 5: Memory     ████████░░                ░░░░░░░░░░ (미확인)

총 시뮬레이션 깊이:  █████████░ (9/10)         ███░░░░░░░ (3/10, 확인 가능한 기준)
```

**중요 한정**: Blok이 내부적으로 더 깊은 시뮬레이션을 구현했을 수 있으나, 공개 자료에서는 확인 불가. 위 비교는 **공개된 정보 기준**이다.

---

## 5. 기술적 차이점

### 근본적 접근 방식의 차이

| 차원 | Personica | Blok |
|------|-----------|------|
| **포지셔닝** | 합성 페르소나 시뮬레이션 플랫폼 | 제품 실험 플랫폼 |
| **입력** | 모드별 상이 (제품 체험: URL, 서베이/리뷰: 시나리오 설정) | 이벤트 로그 + Figma 디자인 |
| **시뮬레이션 대상** | 제품 체험 + 서베이 + A/B 테스트 + 전문가 리뷰 + 광고/퍼널 리서치 | 디자인 목업 + 데이터 모델 |
| **실행 방식** | 5-Layer 페르소나 리얼리티 엔진 (제품 체험 모드에서 Playwright 활용) | 행동 모델링 + GenAI 예측 |
| **사용자 데이터 필요** | 불필요 | **필수** |
| **기존 제품 필요** | 제품 체험 모드에서만 필수 (동작하는 MVP) | 불필요 (Figma만으로 가능) |
| **시뮬레이션 범위** | 전체 사용자 경험 (탐색 ~ 이탈) + 다양한 리서치 모드 | 특정 실험/변형 비교 |
| **산출물 성격** | 경험 리포트 ("왜 이탈하는가") + 리서치 인사이트 | 실험 결과 ("어떤 변형이 더 나은가") |
| **핵심 해자** | 페르소나 리얼리티 — 감정·인지·의사결정 시뮬레이션의 깊이 | 실데이터 기반 행동 예측 |

### LLM 사용 방식

**Personica (설계):**
- 페르소나 생성: LLM으로 프로필 생성 + Big Five 수치 매핑
- 매 인터랙션: 인지 평가 -> 감정 평가(별도 LLM 콜) -> 의사결정
- 리포트 생성: 메모리 스트림 + 감정 궤적 기반 1인칭 사용기

**Blok (추정):**
- "GenAI with underlying behavioral frameworks and deep learning models"
- 0파티/1파티 데이터로 훈련된 모델
- LLM + 행동 모델링 하이브리드
- 구체적 아키텍처 미공개

### 브라우저 자동화

**Personica**: 제품 체험 모드에서 Playwright 기반 실제 브라우저 조작. DOM 파싱, 스크린샷, 마이크로 행동 시뮬레이션 (체류 시간, 스크롤, 망설임). Playwright는 제품 체험 모드에서 쓰는 하나의 인터페이스이며, 서베이·전문가 리뷰 등 다른 모드에서는 브라우저 자동화 없이 5-Layer 엔진만으로 동작.

**Blok**: 브라우저 자동화 사용 증거 없음. Figma 디자인 분석 + 이벤트 로그 기반 행동 예측 모델.

### 데이터 통합

**Personica**: 입력 데이터 최소 (URL만). AI가 자체적으로 제품을 크롤링하고 분석.

**Blok**: 풍부한 입력 데이터 필요. Amplitude, Mixpanel, Segment 이벤트 로그 + Figma 디자인. 이 데이터가 시뮬레이션 품질의 핵심 기반.

---

## 6. 결론

### Q1: Blok이 Personica의 비전을 이미 실현했는가?

**아니다.** Blok과 Personica는 비슷해 보이지만 근본적으로 다른 문제를 풀고 있다.

| 질문 | Blok의 답 | Personica의 답 |
|------|----------|---------------|
| "A와 B 중 어느 디자인이 더 나은가?" | **이것을 풀려고 함** | 직접 풀지 않음 |
| "이 사용자는 왜 이탈하는가?" | 직접 풀지 않음 | **이것을 풀려고 함** |
| "60대 사용자가 온보딩에서 어떤 감정을 느끼는가?" | 풀지 않음 | **이것을 풀려고 함** |
| "이 기능 변경이 전환율에 어떤 영향을 미치는가?" | **이것을 풀려고 함** | 부수적으로 답 가능 |
| "사용자가 없는 새 MVP에 대한 피드백을 받고 싶다" | **불가** (기존 데이터 필요) | **이것을 풀려고 함** |

**핵심 차이점 정리:**

1. **Blok은 "실험 관리 플랫폼"이다.** A/B 테스트를 AI로 가속하는 것이 핵심. 기존 사용자 데이터가 있어야 하고, 디자인 변형 간 성과 비교가 목적.

2. **Personica는 "합성 페르소나 시뮬레이션 플랫폼"이다.** 5-Layer 페르소나 리얼리티 엔진으로 감정/인지/의사결정을 구조적으로 시뮬레이션하는 것이 핵심 해자. 제품 체험(Playwright), 서베이, A/B 테스트, 전문가 리뷰, 광고/퍼널 리서치 등 다양한 적용 모드를 지원하며, "왜" 특정 경험이 발생하는지를 답하는 것이 목적.

3. **제품 라이프사이클 시점이 다르다:**
   - Blok: 이미 사용자가 있는 제품의 기능 최적화 (Growth 단계)
   - Personica: 아직 사용자가 없는 MVP의 출시 전 검증 (Pre-launch 단계)

### Q2: Blok이 있는데도 Personica를 만들 필요가 있는가?

**있다.** 다음 이유로:

1. **다른 고객, 다른 시점**: Blok의 고객은 Amplitude 데이터가 있는 Growth 팀. Personica의 고객은 아직 첫 사용자가 없는 인디해커. 두 제품은 제품 라이프사이클의 다른 시점을 서빙한다.

2. **다른 질문에 답한다**: Blok은 "어떤 변형이 더 나은가?" Personica는 "이 제품을 쓰면 사람들이 어떤 경험을 하는가?" 전자는 최적화, 후자는 이해.

3. **다른 기술적 접근**: Blok은 데이터 기반 예측 모델. Personica는 5-Layer 페르소나 리얼리티 엔진(감정·인지·의사결정 시뮬레이션의 깊이)이 핵심이며, 제품 체험 모드에서는 Playwright를 인터페이스로 활용. 기술 스택이 근본적으로 다르다.

4. **입력 요구사항이 다르다**: Blok은 이벤트 로그 + Figma가 필수. Personica는 URL만. 인디해커의 MVP에는 Amplitude가 붙어있지 않다.

5. **시뮬레이션 깊이가 다르다**: Blok은 행동 예측 수준. Personica는 감정/인지/의사결정까지 시뮬레이션. "왜 이탈하는가"에 대한 답의 깊이가 다르다.

### Q3: "Blok이 있으니 Personica는 필요 없다"가 맞는 판단인가?

**아니다.** 이 판단이 틀린 이유:

1. **Blok은 Personica가 풀려는 문제를 풀지 않는다.** "사용자 데이터가 없는 MVP를 출시 전에 다양한 페르소나로 검증"하는 것은 Blok이 할 수 없다.

2. **Blok의 타겟 세그먼트와 Personica의 비치헤드는 겹치지 않는다.** Blok은 금융/헬스케어 엔터프라이즈. Personica는 인디해커/1인 개발자.

3. **Blok이 증명하는 것은 오히려 Personica에 긍정적이다.** "AI 합성 사용자로 제품을 테스트하는 것"에 $7.5M이 투자되었다는 것은 이 시장에 진짜 수요가 있다는 시장 검증 신호다.

4. **Blok이 해결하지 않는 "페르소나 리얼리티" 갭이 여전히 존재한다.** 어떤 경쟁자도 5-Layer 수준의 감정·인지·의사결정 시뮬레이션 깊이를 구현하지 않고 있다. Personica는 다른 합성 페르소나 제품들(Synthetic Users, Aaru 등)이 커버하는 설문/인터뷰 영역도 포함하면서, 시뮬레이션 깊이에서 추가 차별화된다.

### Q4: Personica가 Blok 대비 취할 수 있는 전략

#### 전략 1: 제품 라이프사이클 시점 차별화

```
제품 라이프사이클:

아이디어 → 디자인 → MVP → 첫 사용자 → 성장 → 최적화
              │         │                      │
           Blok 가능   Personica 최적          Blok 최적
           (Figma)     (URL 기반)             (데이터 기반)
```

Personica는 "MVP -> 첫 사용자" 구간에 집중. 이 구간에서 Blok은 작동하지 않음 (데이터 없으므로).

#### 전략 2: 시뮬레이션 깊이 차별화

Blok이 "어떤 변형이 10% 더 나은가"를 답한다면, Personica는 "65세 은퇴자 김 씨가 온보딩 3단계에서 7초간 멍하니 있다가 뒤로가기를 누른 이유"를 답한다. 이 페르소나 리얼리티(감정·인지·의사결정 시뮬레이션의 깊이)는 기술적으로 모방하기 어렵다.

#### 전략 3: 접근성 차별화

| 차원 | Blok | Personica |
|------|------|-----------|
| 시작하려면 필요한 것 | 이벤트 로그 + Figma + Demo 예약 | URL 입력 |
| 가격 | 미공개 (엔터프라이즈 추정) | $20-50 |
| 결과까지 시간 | 미공개 | 목표 30분-1시간 |
| 기술적 전제조건 | Amplitude/Mixpanel 설정 필요 | 없음 |

#### 전략 4: Blok을 경쟁자가 아닌 시장 검증자로 활용

Blok의 존재와 $7.5M 펀딩은 "AI 합성 사용자" 카테고리의 시장 검증으로 활용 가능:
- 투자자 설득 시: "Blok은 $7.5M 투자받았으나, 기존 데이터 있는 Growth 팀만 서빙. Pre-launch MVP 검증 시장은 비어있음"
- 고객 설득 시: "이미 Blok, Aaru 등이 AI 합성 사용자의 유효성을 증명. Personica는 이를 아직 사용자가 없는 MVP에 적용"

#### 전략 5: Blok이 확장할 수 없는 영역 선점

Blok이 "실데이터 기반 행동 예측"에서 "5-Layer 수준 페르소나 리얼리티"로 확장하려면:
- 감정·인지·의사결정 시뮬레이션 엔진을 처음부터 구축해야 함
- 기존 "데이터 기반 예측" DNA와 충돌
- 기존 고객(엔터프라이즈)의 니즈와 다른 방향
- 가격 모델 재설계 필요 (Self-serve)

이 전환은 Blok에게 쉽지 않다. 반대로 Personica가 "데이터 기반 A/B 테스트 가속"으로 확장하는 것도 어렵지만, Personica는 그럴 필요가 없다 — Personica는 서베이, 전문가 리뷰, 광고/퍼널 리서치 등 다른 합성 페르소나 제품들과 같은 영역도 커버하면서, 5-Layer 페르소나 리얼리티로 차별화되는 방향으로 확장한다.

---

## 7. 위험 요인과 모니터링 항목

### Blok이 Personica 방향으로 확장할 가능성

| 시나리오 | 가능성 | 영향 | 대응 |
|----------|--------|------|------|
| Blok이 URL 기반 시뮬레이션 추가 | 중간 (기술적 전환 비용 높음) | 높음 | 시뮬레이션 충실도에서 선점 |
| Blok이 감정/인지 시뮬레이션 추가 | 낮음 (핵심 DNA와 다름) | 매우 높음 | 5-Layer 아키텍처로 깊이 차별화 |
| Blok이 인디해커 세그먼트 진출 | 낮음 (엔터프라이즈 DNA) | 중간 | 가격/접근성으로 방어 |
| Blok이 "데이터 없이도 가능" 모드 추가 | 중간 | 높음 | 시뮬레이션 깊이 + 1인칭 리포트로 차별화 |

### 모니터링 항목

1. **Blok의 제품 업데이트**: 브라우저 자동화 추가 여부, URL 입력 지원 여부
2. **Blok의 세그먼트 확장**: 인디해커/스타트업 대상 Self-serve 출시 여부
3. **Blok의 기술 블로그**: 감정/인지 모델링 관련 기술적 발표 여부
4. **Blok의 채용**: Playwright/브라우저 자동화 엔지니어 채용 여부
5. **Blok의 추가 펀딩**: Series A 진행 시 사업 방향 변화 여부

---

## 8. 최종 요약

### 한 줄 요약

> **Blok은 "기존 데이터 기반 A/B 테스트 가속 플랫폼"이고, Personica는 "합성 페르소나 시뮬레이션 플랫폼"이다. Personica의 핵심 해자는 5-Layer 페르소나 리얼리티(감정·인지·의사결정 시뮬레이션의 깊이)이며, 제품 체험·서베이·A/B 테스트·전문가 리뷰·광고/퍼널 리서치 등 다양한 모드를 지원한다. 비슷해 보이지만 다른 고객, 다른 시점, 다른 질문, 다른 기술로 다른 문제를 푼다.**

### 팩트 기반 판정표

| 판정 항목 | 결론 |
|-----------|------|
| Blok이 Personica 비전을 이미 실현? | **아니다** - 다른 문제를 풀고 있음 |
| Blok이 실제 제품을 브라우저로 사용? | **아니다** - Figma + 데이터 기반 예측 |
| Blok에 감정/인지 시뮬레이션 있음? | **미확인** - 공개 자료에 증거 없음 |
| Blok이 데이터 없이 작동? | **아니다** - Amplitude/Mixpanel 로그 필수 |
| Blok이 인디해커를 타겟? | **아니다** - 금융/헬스케어 엔터프라이즈 |
| Personica만의 차별화 여지 있음? | **있다** - 페르소나 리얼리티 + 적용 범위 확장으로 차별화 |
| Blok의 존재가 Personica에 위협? | **부분적** - 장기적 확장 시 경쟁 가능성 |
| Blok의 존재가 Personica에 긍정적? | **그렇다** - 시장 검증, 카테고리 교육 효과 |

---

## Sources

### 공식 자료
- [Blok 공식 사이트](https://www.joinblok.co/) - 제품 설명, 워크플로우, Use cases
- [Blok 스텔스 탈출 발표](https://www.joinblok.co/insights/meet-blok-future-of-product-development) - 2025.07.08
- [Blok 블로그: Agentic AI & Experimentation](https://www.joinblok.co/insights/) - 기술 접근 방식
- [Blok 성격 퀴즈](https://www.joinblok.co/quiz) - OCEAN 기반 디지털 성격 분류

### 뉴스 보도
- [TechCrunch: "Blok is using AI personas to simulate real-world app usage"](https://techcrunch.com/2025/07/09/blok-is-using-ai-persons-to-simulate-real-world-app-usage/) - 2025.07.09
- [SiliconANGLE: "Blok raises $7.5M to build AI agents that simulate human behavior"](https://siliconangle.com/2025/07/09/blok-raises-7-5m-build-ai-agents-simulate-human-behavior-accelerate-software-testing/) - 2025.07.09
- [FutureTekNow: Blok AI agents funding](https://futureteknow.com/blok-ai-agents-software-testing-raise/) - 2025.07.10
- [Technology.org: "Blok's AI Personas Test Apps Before Users Ever See Them"](https://technology.org/2025/07/10/bloks-ai-personas-test-apps-before-users-ever-see-them/) - 2025.07.10
- [OpenTools.ai: "Blok Revolutionizes App Testing with AI Personas"](https://opentools.ai/news/blok-revolutionizes-app-testing-with-ai-personas)
- [StartupHub.ai: "Blok Secures $7.5M for AI App Testing Platform"](https://startuphub.ai/ai-news/funding-round/2025/blok-secures-7-5m-for-ai-app-testing-platform/)
- [CompleteAITraining: "Blok's AI Personas Let Developers Test Apps Before Writing Code"](https://completeaitraining.com/news/bloks-ai-personas-let-developers-test-apps-before-writing/)

### 창업자 정보
- [Tom Charman LinkedIn](https://www.linkedin.com/in/tcharman/) - Co-founder & CEO
- Brave Search 결과: Tom Charman 경력 상세 (KOMPAS, Rassa, 국방 데이터 사이언스)

### 조사 한계
- Blok의 내부 기술 아키텍처 미공개 (감정/인지 시뮬레이션 유무 확인 불가)
- Olivia Higgs의 상세 경력 미확인
- 구체적 가격 정보 미공개
- 현재 고객 수/매출 미공개
- Crunchbase 접근 불가 (403)
- Product Hunt 접근 불가 (403)
- X/Twitter 검색 제한
