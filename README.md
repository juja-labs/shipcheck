# ShipCheck

> 만드는 건 끝났어. 이거 사람들이 원할까?
>
> 100명의 AI 유저가 당신의 MVP를 실제로 써보고, 소셜 미디어에서 토론하고, 구조화된 시장 검증 보고서를 돌려줍니다.

## Problem

바이브 코딩 시대, **만드는 건 더 이상 병목이 아닙니다.**

- YC W25 배치의 25%가 코드의 95% 이상이 AI 생성
- 2025년 앱스토어 신규 앱 55.7만개 (+24% YoY)
- 미국 개발자 92%가 AI 코딩 도구를 매일 사용

하지만 **스타트업 실패 원인 1위는 여전히 "시장 수요 부재" (42%)** 입니다.

전통적 시장 검증은 건당 $25,000~$65,000, 6~12주 소요. 바이브 코딩으로 하루 만에 MVP를 만들 수 있는 시대에, 검증에 6주를 기다리는 건 말이 안 됩니다.

## Solution

ShipCheck은 **AI 에이전트 기반 가상 시장 검증 플랫폼**입니다.

```
MVP URL 입력 → AI 에이전트 100명이 실제로 사용 → 소셜 토론 → 구조화된 보고서
```

### 기존 도구와의 차이

| | Aaru / Synthetic Users | Blok | UXAgent (학술) | **ShipCheck** |
|---|---|---|---|---|
| 입력 | 설문/컨셉 설명 | Figma 디자인 | 실제 웹사이트 | **실제 MVP URL** |
| 에이전트 행동 | 설문 응답 | UI 시뮬레이션 | 웹 탐색 | **제품 사용 + 소셜 토론** |
| 사회적 역학 | 여론 전파 모델 | 없음 | 없음 | **집단 토론/여론 형성** |
| 지식 그래프 | 없음 | 없음 | 없음 | **피드백 온톨로지** |
| 출력 | 설문 결과 | UX 리포트 | 유저빌리티 이슈 | **시장 반응 종합 분석** |

## How It Works

### Phase 1: 자동 분석

1. **제품 크롤링** — Playwright로 MVP의 페이지 구조, 기능, 사용자 플로우를 자동 파악
2. **Feature 온톨로지 생성** — LLM이 제품 기능을 구조화된 스키마로 정리
3. **페르소나 생성** — 타겟 유저 설명을 기반으로 다양한 가상 유저 20~100명 생성
4. **Knowledge Graph 초기화** — Zep Cloud에 온톨로지 + 페르소나 그래프 구축

### Phase 2: 제품 체험 + 소셜 시뮬레이션

매 라운드:
1. **에이전트가 실제 제품 사용** — Playwright로 페이지 방문, 버튼 클릭, 폼 입력, 회원가입 시도
2. **OASIS 소셜 플랫폼에서 토론** — 사용 경험을 게시, 댓글, 좋아요, 팔로우 등 자연스러운 소셜 행동
3. **Knowledge Graph 실시간 업데이트** — 행동 데이터가 Zep 그래프에 즉시 반영

### Phase 3: 분석 및 보고서

- **Feature별 사용성 점수** — 어떤 기능이 잘 작동하고 어디서 이탈하는지
- **세그먼트별 반응 매트릭스** — 20대 직장인 vs 40대 주부의 반응 차이
- **핵심 이탈 지점 + 개선 제안** — 구체적으로 무엇을 바꿔야 하는지
- **에이전트 인터뷰** — 특정 에이전트에게 "왜 그렇게 행동했어?" 추가 질문 가능

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     ShipCheck Platform                  │
│                                                         │
│  ┌──────────────┐                  ┌────────────────┐   │
│  │  Playwright   │  제품 체험       │  Zep Cloud     │   │
│  │  Browser      │─────────────────│  Knowledge     │   │
│  │  Automation   │                 │  Graph         │   │
│  └──────────────┘                  └────────────────┘   │
│         │                                  │            │
│         ▼                                  ▼            │
│  ┌──────────────────────────────────────────────────┐   │
│  │              OASIS Social Simulation              │   │
│  │                                                   │   │
│  │  Agent ← LLM → create_post, like, comment, ...  │   │
│  │  Agent ← LLM → use_product, rate_feature, ...   │   │
│  │  Agent ← LLM → recommend, compare_product, ...  │   │
│  │                                                   │   │
│  │  Platform (SQLite) ← RecSys ← Channel (IPC)     │   │
│  └──────────────────────────────────────────────────┘   │
│         │                                               │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ ReportAgent  │  Graph 검색 → 구조화된 보고서          │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

## Knowledge Graph 활용

MiroFish의 접근 방식을 차용하되, 제품 검증에 맞게 재설계:

```
[UserSegment] ──사용한다──► [Feature]
     │                        │
  속한다                   발생시킨다
     │                        │
[Persona]  ──느꼈다──► [Sentiment]
     │                        │
  게시했다                  관련된다
     │                        │
[SocialPost] ──언급한다──► [PainPoint]
                              │
                        해결된다/미해결
                              │
                       [Competitor]
```

**왜 Knowledge Graph가 필요한가:**
- 기존 도구: "55%가 긍정적 반응" (숫자만)
- ShipCheck: **"왜 45%가 부정적이었는지"를 구조적으로 추론** 가능
- 반복 검증 시 이전 그래프와 비교하여 **개선 효과 추적**

## Market

| 지표 | 데이터 |
|------|--------|
| 글로벌 UX 리서치 시장 | $427M (2024) → $1B (2032) |
| Synthetic Data 시장 | $450~580M (2025) → $2.1B (2028) |
| 한국 연간 기술 창업 | 214,917건 (2024) |
| 스타트업 실패 #1 원인 | "시장 수요 부재" 42% |
| 전통 시장 조사 비용 | 건당 $25,000~$65,000 |
| Aaru (경쟁사) 밸류에이션 | $1B (Series A, 2025.12) |

### 경쟁 환경

"멀티 에이전트 + 실제 제품 사용 + 소셜 토론" 조합의 상용 제품은 **전무**합니다.

- **Aaru** ($1B) — 설문/여론 시뮬레이션 (제품 사용 안 함)
- **Artificial Societies** (YC W25) — 소셜 역학 시뮬레이션 (제품 사용 안 함)
- **Blok** ($7.5M seed) — Figma 디자인 시뮬레이션 (실제 제품 아님)
- **UXAgent** (CHI 2025, 학술) — 브라우저 사용 있으나 소셜 시뮬레이션 없음

## Roadmap

### Phase 1 (0~6개월): MVP
- 제품 URL 입력 → 에이전트 20명이 사용 + 토론
- 간단한 보고서 (감정 분석 + 핵심 피드백)
- 타겟: 예비창업자, 사이드 프로젝트 빌더
- 가격: 무료 / 건당 5만원

### Phase 2 (6~12개월): Knowledge Graph 통합
- Feature 온톨로지 자동 생성
- 구조화된 심층 보고서
- 반복 검증 + 변화 추적
- 가격: 월 구독 20~50만원

### Phase 3 (12~18개월): B2B 확장
- 액셀러레이터/VC 대상 포트폴리오 검증 도구
- 대기업 R&D 신제품 사전 검증
- API 제공 (CI/CD 파이프라인에 통합)
- 가격: 엔터프라이즈 연간 계약

## Tech Stack

| 레이어 | 기술 |
|--------|------|
| Multi-Agent Simulation | [OASIS](https://github.com/camel-ai/oasis) (Apache 2.0) |
| Knowledge Graph | [Zep Cloud](https://www.getzep.com/) (GraphRAG) |
| Browser Automation | [Playwright](https://playwright.dev/) |
| LLM | OpenAI / Anthropic API |
| Backend | Python + FastAPI |
| Frontend | Next.js + TypeScript + Tailwind CSS |
| Database | SQLite (시뮬레이션) + PostgreSQL (서비스) |

## References

- [OASIS: Open Agent Social Interaction Simulations](https://github.com/camel-ai/oasis)
- [MiroFish: GraphRAG + OASIS 통합 참고 구현](https://github.com/666ghj/MiroFish)
- [UXAgent: LLM Agents for Usability Testing (CHI 2025)](https://arxiv.org/abs/2504.09407)
- [AgentA/B: 1,000 LLM Agents on Live Amazon.com](https://arxiv.org/abs/2504.09723)
- [Harvard: Using LLMs for Market Research](https://www.hbs.edu/faculty/Pages/item.aspx?num=63859)

## License

TBD
