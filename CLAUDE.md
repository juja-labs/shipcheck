# Personica (페르소니카)

## Project Overview
Personica는 감정·인지·의사결정을 구조적으로 시뮬레이션하는 AI 합성 페르소나 플랫폼이다.

핵심 가치: 다양한 배경·감정·맥락을 가진 합성 페르소나가 **사람처럼 생각하고, 느끼고, 행동**하며 — 제품 체험, 서베이, A/B 테스트, 전문가 리뷰, 광고/퍼널 리서치 등 모든 사용자 리서치를 시뮬레이션한다.

## Current Status
- **단계**: Discovery — 핵심 가설 검증 중 (단일 세션 분화 검증 완료, 대규모 실험 준비)
- **핵심 가설**: "AI 페르소나 시뮬레이션의 충실도가 실제 의사결정에 쓸 만한 수준인가?" — (1) 분화: 페르소나들이 유의미하게 다른 행동을 보이는가, (2) 현실성: 그 패턴이 실제 인간과 방향 일치하는가
- **제품명 변경**: ShipCheck → **Personica** (2026-03-20)
- **포지셔닝 전환**: "웹앱 UX 테스팅 도구" → "합성 페르소나 시뮬레이션 플랫폼"
- **상세 계획**: `docs/discovery-plan.md` 참조

## Core Problem
기업과 창업자는 제품·서비스·마케팅에 대한 사용자 반응을 검증하고 싶지만, 기존 방법(설문, 베타테스터, FGI, 전문가 컨설팅)은 비용·시간·규모의 한계가 있다. AI 합성 페르소나를 활용한 제품들이 등장하고 있지만, 대부분 단순한 LLM 프롬프팅 수준으로 실제 인간의 감정·인지·의사결정 과정을 시뮬레이션하지 못한다.

Personica는 이 문제를 "5-Layer 시뮬레이션 엔진으로 사람처럼 생각·느끼·행동하는 AI 합성 페르소나"로 푼다.

## Tech Stack
- **Simulation Engine**: 5-Layer 페르소나 시뮬레이션 (핵심 IP)
- **Browser Automation**: Playwright — 제품 체험 모드에서 실제 제품 조작
- **LLM**: OpenAI / Anthropic / Google API — 페르소나 생성, 행동 결정, 감정 시뮬레이션, 리포트 생성
- **Backend**: Python (FastAPI)
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **Database**: PostgreSQL (서비스 데이터)
- **Memory/Data**: 검토 중 (Generative Agents 방식 기본, Zep/Graphiti/Mem0/A-Mem 옵션)

## Architecture

### 핵심 엔진: 5-Layer 페르소나 시뮬레이션
```
Layer 1: Persona Profile — Big Five → 행동 파라미터 수학적 매핑 (PRISM 차용)
Layer 2: Cognitive — Information Foraging, Cognitive Load, Mental Model, TAM
Layer 3: Emotion — OCC Appraisal + PAD 연속 상태 + SDE 확률적 감정 진화
Layer 4: Decision — BDI-E 모델 + Fogg Check + Satisficing Gate
Layer 5: Memory — Memory Stream + Reflection + Habit Strength + Drift Monitor
```
상세 설계: `docs/foundation/simulation-engine.md`

### 적용 범위 (Use Cases)
5-Layer 엔진은 특정 use case에 묶이지 않는 범용 합성 페르소나 플랫폼:

| 모드 | 설명 | 단계 |
|------|------|------|
| **제품 체험 시뮬레이션** | Playwright로 실제 제품을 사용하고 UX 피드백 | Phase 1 (beachhead) |
| **UI/UX 디자인 피드백** | Figma/프로토타입 기반 디자인 리뷰 | Phase 1 |
| **합성 서베이/인터뷰** | 설문, FGI, 인터뷰 시뮬레이션 | Phase 2 |
| **A/B 테스트** | 변형 간 선호도/행동 차이 시뮬레이션 | Phase 2 |
| **광고/마케팅 리서치** | 광고 크리에이티브, 메시지, 카피 테스트 | Phase 2 |
| **퍼널 분석** | 전환 퍼널 각 단계별 이탈/전환 시뮬레이션 | Phase 2 |
| **전문가 리뷰** | 도메인 전문가 페르소나의 제품/서비스 평가 | Phase 3 |

### 제품 체험 모드 플로우 (Phase 1 beachhead)
```
고객 입력 (스테이징 URL + 테스트 계정 + 타겟 유저 설명)
    │
    ▼
Step 1: 자동 분석
  ① Playwright로 제품 크롤링 → 페이지/기능/플로우 파악
  ② LLM이 Feature 온톨로지 자동 생성
  ③ 타겟 유저 기반 페르소나 N명 생성 (Big Five 수학적 매핑)
    │
    ▼
Step 2: 제품 체험 (개인 시뮬레이션)
  ① 각 페르소나가 Playwright로 실제 제품을 독립적으로 사용
  ② 매 상호작용마다 5-Layer 파이프라인 실행
  ③ 행동 로그 + 감성 로그 + 마이크로 행동 로그 수집
    │
    ▼
Step 3: 분석 및 리포트
  ① 세그먼트별 교차 분석
  ② 감정 궤적 타임라인, 이탈 지점, 개선 제안
  ③ 선택적 페르소나 인터뷰
```

## Key Differentiators
1. **페르소나 리얼리티 (핵심 해자)**: 5-Layer 아키텍처로 감정·인지·의사결정을 구조적으로 시뮬레이션. 다른 합성 페르소나 제품들이 단순 LLM 프롬프팅인 반면, Personica는 실제 사람과 유사한 반응을 생성. 모든 상용 경쟁사 중 유일
2. **범용 플랫폼**: 5-Layer 엔진이 제품 체험, 서베이, A/B 테스트, 전문가 리뷰, 광고/퍼널 리서치 등 다양한 리서치 모드에 적용 가능
3. **실제 제품 사용 (제품 체험 모드)**: 설문/Figma/데이터 기반이 아닌, Playwright로 실제 제품을 직접 조작. 경쟁사 전원이 이 접근을 회피함. 제품 체험 모드에서의 추가 차별화 포인트

## Thinking Principles
- **[CRITICAL] 문제 중심 사고**: 기술/도구를 먼저 정하고 문제에 끼워맞추지 말 것. 항상 "어떤 문제를 푸는가" → "그 문제를 가장 잘 푸는 방법은?" 순서로 사고할 것.
- **페르소나 리얼리티가 최우선 (핵심 해자)**: "개별 페르소나가 얼마나 사람처럼 생각·느끼·행동하는가"가 핵심 IP. 이 품질이 확보되지 않으면 위에 뭘 얹어도 무의미. 5-Layer 엔진의 시뮬레이션 충실도(fidelity)가 모든 use case의 전제.
- **QA 도구가 아님**: Personica는 기능 정상 동작 여부를 테스트하는 도구가 아님. "사용자가 어떻게 느끼고 반응하는가"를 시뮬레이션하는 도구.
- **Playwright는 인터페이스, 엔진이 핵심**: 브라우저 자동화는 "제품 체험" 모드에서 쓰는 하나의 인터페이스일 뿐. 전체 제품을 이것에만 묶지 말 것.

## 사업계획서 SOT (Source of Truth)
예비창업패키지 사업계획서 작성 시 아래 문서를 각 영역의 정본(SOT)으로 사용할 것. 수치·구조가 충돌하면 SOT가 우선.

| 영역 | SOT 문서 |
|------|----------|
| Unit Economics (원가·마진·가격) | `docs/scale/unit-economics.md` |
| 팀 구성 및 예산 | `docs/scale/team-budget-plan.md` |
| TAM / SAM / SOM 시장규모 | `docs/market-sizeing/market-sizing-yechangpae-appendix-software-first.md` |
| 수익 모델 | `docs/scale/revenue-model.md` |
| 시장진입 전략 | `docs/scale/market-entry-strategy.md` |

## Conventions
- 한국어 코멘트 사용
- 커밋 메시지는 영어 conventional commits (feat:, fix:, chore: 등)
- Python: Black formatter, type hints 필수
- Frontend: ESLint + Prettier

## Documentation
프로젝트 문서는 `docs/` 폴더에 정리:
- `docs/foundation/` — 제품 비전, 5-Layer 엔진 설계, 논문/레퍼런스
- `docs/research/` — 경쟁사 분석, 합성 페르소나 시장 조사, 피봇 리뷰
- `docs/strategy/` — 시장 규모, 경쟁사, SWOT, Lean Canvas, 유저리서치, VP, 인터뷰 스크립트
- `docs/plan/` — 기술 로드맵
- `docs/discovery-plan.md` — 전체 디스커버리 계획 (핵심 가설 + 실험 설계)

## References
- UXAgent (Amazon, CHI 2025): https://github.com/neuhai/UXAgent — 브라우저 자동화 기반 UX 테스팅
- PRISM (Fudan, 2025): https://arxiv.org/abs/2512.19933 — SDE 감정 진화, Big Five→행동 파라미터 매핑
- Concordia (Google DeepMind): https://github.com/google-deepmind/concordia — GM-Player 아키텍처
- Generative Agents (Stanford, 2023): https://arxiv.org/abs/2304.03442 — Memory Stream + Reflection
- 전체 레퍼런스: `docs/foundation/research-references.md` (논문 30+편, 데이터셋, 벤치마크)
