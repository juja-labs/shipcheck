# Project Instructions

> Auto-generated from CLAUDE.md + Claude Code memory.
> Do not edit directly — run `codex-sync` to regenerate.

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

Personica는 이 문제를 "페르소나 리얼리티 엔진으로 사람처럼 생각·느끼·행동하는 AI 합성 페르소나"로 푼다.

## Tech Stack
- **Simulation Engine**: 페르소나 리얼리티 엔진 (핵심 IP)
- **Browser Automation**: Playwright — 제품 체험 모드에서 실제 제품 조작
- **LLM**: OpenAI / Anthropic / Google API — 페르소나 생성, 행동 결정, 감정 시뮬레이션, 리포트 생성
- **Backend**: Python (FastAPI)
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **Database**: PostgreSQL (서비스 데이터)
- **Memory/Data**: 검토 중 (Generative Agents 방식 기본, Zep/Graphiti/Mem0/A-Mem 옵션)

## Architecture

### 핵심 엔진: 페르소나 리얼리티 엔진
```
Layer 1: Persona Profile — Big Five → 행동 파라미터 수학적 매핑 (PRISM 차용)
Layer 2: Cognitive — Information Foraging, Cognitive Load, Mental Model, TAM
Layer 3: Emotion — OCC Appraisal + PAD 연속 상태 + SDE 확률적 감정 진화
Layer 4: Decision — BDI-E 모델 + Fogg Check + Satisficing Gate
Layer 5: Memory — Memory Stream + Reflection + Habit Strength + Drift Monitor
```
상세 설계: `docs/foundation/simulation-engine.md`

### 적용 범위 (Use Cases)
페르소나 리얼리티 엔진은 특정 use case에 묶이지 않는 범용 합성 페르소나 플랫폼:

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
  ② 매 상호작용마다 페르소나 리얼리티 엔진 파이프라인 실행
  ③ 행동 로그 + 감성 로그 + 마이크로 행동 로그 수집
    │
    ▼
Step 3: 분석 및 리포트
  ① 세그먼트별 교차 분석
  ② 감정 궤적 타임라인, 이탈 지점, 개선 제안
  ③ 선택적 페르소나 인터뷰
```

## Key Differentiators
1. **페르소나 리얼리티 (핵심 해자)**: 페르소나 리얼리티 엔진의 5개 레이어 아키텍처로 감정·인지·의사결정을 구조적으로 시뮬레이션. 다른 합성 페르소나 제품들이 단순 LLM 프롬프팅인 반면, Personica는 실제 사람과 유사한 반응을 생성. 모든 상용 경쟁사 중 유일
2. **범용 플랫폼**: 페르소나 리얼리티 엔진이 제품 체험, 서베이, A/B 테스트, 전문가 리뷰, 광고/퍼널 리서치 등 다양한 리서치 모드에 적용 가능
3. **실제 제품 사용 (제품 체험 모드)**: 설문/Figma/데이터 기반이 아닌, Playwright로 실제 제품을 직접 조작. 경쟁사 전원이 이 접근을 회피함. 제품 체험 모드에서의 추가 차별화 포인트

## Thinking Principles
- **[CRITICAL] 문제 중심 사고**: 기술/도구를 먼저 정하고 문제에 끼워맞추지 말 것. 항상 "어떤 문제를 푸는가" → "그 문제를 가장 잘 푸는 방법은?" 순서로 사고할 것.
- **페르소나 리얼리티가 최우선 (핵심 해자)**: "개별 페르소나가 얼마나 사람처럼 생각·느끼·행동하는가"가 핵심 IP. 이 품질이 확보되지 않으면 위에 뭘 얹어도 무의미. 페르소나 리얼리티 엔진의 시뮬레이션 충실도(fidelity)가 모든 use case의 전제.
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
- `docs/foundation/` — 제품 비전, 페르소나 리얼리티 엔진 설계, 논문/레퍼런스
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

---

## Project Memory (from Claude Code)

### 포지셔닝 피드백 — 속도 과장 금지 + URL만 넣으면 금지
> "5분 만에" 속도 과장 금지, "URL만 넣으면" 셀프서브 전제 금지, 페르소나 수 20명 고정 금지

1. "5분 만에 실사용자 수준의 리뷰" 같은 속도 중심 메시지는 과장이다.

2. "URL만 넣으면" 셀프서브 메시지 사용 금지. 제품 체험 모드에는 고객 협조(테스트 계정, 스테이징 URL)가 필수.

3. 페르소나 수 최소 100-500명이 기본 전제. 20명은 세그먼트당 통계적 의미 없음.

**Why:** Personica의 핵심 가치는 속도나 편의성이 아니라 **페르소나 리얼리티** — 시뮬레이션의 깊이와 충실도. 페르소나 리얼리티 엔진이 만드는 사람 같은 반응이 해자.

**How to apply:**
- 마케팅 메시지, 사업계획서 등에서 "URL만 넣으면", "5분 만에" 표현 제거
- 대신 "베타테스터 모집 2주 → 하루 이내" 수준의 현실적 시간 절감 강조
- 핵심 메시지는 "더 빠르다"가 아니라 "더 사람답다"

### feedback_skill_creation
> 스킬 생성 시 반드시 init_skill.py 사용하고 경로 이중 중첩 금지

스킬 생성 시 platform:claude-creator 가이드의 Step 3(init_skill.py 실행)을 반드시 따를 것. 수동으로 파일을 만들지 말 것.

**Why:** init_skill.py를 건너뛰고 수동 생성하다가 `codex-sync/codex-sync/` 이중 중첩 경로 실수가 발생함. hook 스크립트와 settings.json 모두 잘못된 경로가 들어가서 사용자가 직접 발견해야 했음.

**How to apply:** 스킬 생성 가이드가 로드되면 각 Step을 순서대로 실행할 것. 특히 init_skill.py로 디렉토리 구조를 먼저 잡고, 그 위에 커스터마이징하는 순서를 지킬 것. 경로를 하드코딩할 때는 항상 실제 파일 위치를 `ls`/`find`로 검증할 것.

### 템플릿 파일 직접 수정 금지
> 사업계획서 등 템플릿 파일에 바로 작성하지 말고, 별도 파일에 초안을 생성할 것

템플릿 파일(bizplan-template.md 등)에 직접 본문을 작성하면 안 된다. 템플릿은 구조/플레이스홀더로 유지하고, 작성한 초안은 별도 파일(예: `claudecode/bizplan-draft-*.md`)에 저장할 것.

**Why:** 템플릿은 반복 사용하는 틀이므로 원본을 보존해야 함. 직접 덮어쓰면 원본 복원이 어려움 (git에 커밋되지 않은 경우 특히).

**How to apply:** 사업계획서 등 문서 작성 시, 템플릿 참조하되 결과물은 항상 별도 경로에 생성. `docs/예창패 실제 제풀용/claudecode/` 또는 `codex/` 폴더 활용.

### 예비창업패키지 사업계획서 작업 현황
> 2026 예비창업패키지 사업계획서 — Personica 리브랜딩 + 플랫폼 포지셔닝 반영 (2026-03-20 대대적 수정)

**2026-03-20 대대적 수정 완료:**
- 제품명 ShipCheck → **Personica** 변경
- 포지셔닝: "UX 테스팅 도구" → "합성 페르소나 시뮬레이션 플랫폼"
- VC 피드백 반영: 시장 범위 확장 (제품 체험 + 합성 리서치 + 전문가 시뮬레이션)
- 경쟁 테이블: 2축(시뮬레이션 깊이 × 실제 사용) + UXAgent 포함
- 기술실사 리뷰 반영: 구현 상태 정직하게 표기 (Layer 1,3 완료 / 2,4,5 설계 완료)
- 스토리텔링 리뷰 반영: 시뮬레이션 로그로 오프닝
- 3단계 성장: Phase1 제품체험(비치헤드) → Phase2 합성리서치 → Phase3 전문가시뮬레이션

**2026-03-21 작업 방향:**
- `docs/예창패 실제 제출용/bizplan-template.md` 템플릿 기준으로 사업계획서 문서 작성 진행

**아직 미완료:**
- 팀 구성 섹션: 대표자 실제 경력/배경 정보 미기입
- MVP 스크린샷/목업 이미지 미삽입 (준비가이드에서 강력 권장)

**Why:** 예비창업패키지 자금으로 Personica MVP 개발 후 시드 투자 유치 계획.

**How to apply:** 사업계획서 작성 시 `docs/예창패 실제 제출용/bizplan-template.md` 템플릿 구조를 따를 것. 팀 구성 섹션은 사용자가 실제 정보 제공 필요. 공식 HWP 양식에 옮겨 적을 때 이미지/시각자료 삽입 권장.

### Personica Discovery Phase 현황
> Discovery 완료 — 30명 분화 검증 + G2 비교 완료, CLI 기반 아키텍처 확정, 사업계획서 준비 중 (2026-03-21)

## Discovery 현황 (2026-03-21 기준)

**Discovery Plan**: docs/discovery-plan.md
**검증 결과 보고서**: docs/engine-validation-report.md

### 핵심 결론

> "AI 페르소나 시뮬레이션의 충실도가 실제 의사결정에 쓸 만한 수준인가?"

- **(1) 분화**: ✅ **30명 검증 완료** — 9개 세그먼트별 다른 행동/감정/평점 패턴 확인
- **(2) 현실성**: ✅ **G2 비교 완료** — 긍정 테마 90% 일치, 불만 테마 71% 일치

### 실험 결과 요약 (n=30)
- 평균 평점: 3.80 (G2: ~4.5 — 합성이 더 솔직, G2는 인센티브 편향)
- 추천 비율: 90%
- 세그먼트별 평점 범위: 3.50 (비평형) ~ 4.33 (기술능숙형)
- Ablation: 감정 파이프라인 없으면 PU/PEOU가 0.2~0.3 더 높아짐 (sycophancy)

### 확정된 아키텍처
- Claude Code CLI (-p 모드) + playwright-cli + step_update 스킬
- 감정 시뮬레이션 엔진 (OCC → PAD → SDE noise → 이탈 판정) = 핵심 해자
- 브라우저 자동화는 인프라 (playwright-cli), 해자 아님

### 남은 과제
- 페르소나-실행 분리 (서브에이전트): 접근성 트리가 독백 오염 → 스크린샷 기반 분리 필요
- 다중 세션 미구현 (Day 1/2/3)
- 1개 제품(Tally)만 검증 → 다른 제품군 확대 필요
- 사업계획서 제출: 다음 주 수요일

**Why:** 사업계획서에 정량적 검증 결과를 포함해야 함
**How to apply:** docs/engine-validation-report.md를 근거자료로 참조. 실험 데이터는 runs/reviews/all_reviews.json에 있음.

### 다중 세션 시뮬레이션 — 추가 해자
> 다중 세션 시뮬레이션이 Personica의 추가 해자 — 단일 세션 분화 검증 완료 후 다음 단계

단일 세션에서 페르소나 분화가 유의미하게 동작하는 것은 검증 완료됨 (2026-03-17 기준).

다음 단계: **다중 세션 시뮬레이션**이 제품의 추가 해자(moat)로 결정됨.
- 실제 사용자 라이프사이클 시뮬레이션: 첫 방문 → 재방문 → 습관 형성 or 이탈
- 경쟁사 대비 차별점: "첫인상 리뷰"가 아닌 "3주 쓰면 누가 남고 누가 떠나는가"
- 이를 위해 세션 간 메모리 시스템이 기술적 핵심이 됨

**Why:** 고객에게 "첫인상"보다 "라이프사이클 예측"이 훨씬 가치 있는 질문이고, 이걸 하는 경쟁사가 없음
**How to apply:** 다중 세션 메모리 설계 시 이 맥락 참고. Generative Agents → Graph RAG 확장 경로를 염두에 둘 것. 단, 핵심 해자는 페르소나 리얼리티 엔진이고, 다중 세션은 추가 해자.

### Personica 제품 핵심 정의
> Personica = 합성 페르소나 시뮬레이션 플랫폼. 핵심 해자는 페르소나 리얼리티 엔진. 적용 범위 확장 (2026-03-21)

**제품명: Personica (페르소니카)** — 구 ShipCheck에서 2026-03-20 변경

**포지셔닝**: 합성 페르소나 시뮬레이션 플랫폼
- 기존: "웹앱 UX 테스팅 도구" → 시장이 좁아 보임
- 전환: "AI 합성 페르소나가 사람처럼 생각·느끼·행동하며 모든 사용자 리서치를 시뮬레이션하는 플랫폼"

**핵심 해자 = 페르소나 리얼리티**: 페르소나 리얼리티 엔진이 핵심 IP
- 다른 합성 페르소나 제품들은 단순 LLM 프롬프팅
- Personica는 감정·인지·의사결정을 구조적으로 시뮬레이션하여 실제 사람과 유사한 반응 생성
- 이 품질이 확보되지 않으면 위에 뭘 얹어도 무의미

**적용 범위** (Phase별 확장):
- Phase 1 (beachhead): 제품 체험 시뮬레이션 (Playwright), UI/UX 디자인 피드백
- Phase 2: 합성 서베이/인터뷰, A/B 테스트, 광고/마케팅 리서치, 퍼널 분석
- Phase 3: 전문가 리뷰 (도메인 특화 집단 토론/상담)

**핵심 원칙:**
- 페르소나 리얼리티 엔진은 특정 use case에 묶이지 않는 범용 플랫폼
- Playwright는 "제품 체험" 모드에서 쓰는 하나의 인터페이스일 뿐
- 피치 내러티브는 "합성 페르소나 플랫폼" (넓게), 실행은 beachhead 집중 (좁게)

**How to apply:** 모든 문서/코드/피치에서 Personica 사용. 포지셔닝은 "플랫폼"이지만, 실행은 Phase 1(제품 체험) 집중. 적용 범위를 설명할 때는 경쟁사들과 동일한 영역 + 우리만의 추가 차별점(실제 제품 사용) 프레이밍.

### 인증 장벽과 딜리버리 모델 재정립
> "URL만 넣으면" 메시지 폐기 — 제품 체험 모드에서 고객 협조 필수, 딜리버리 모델 재정립

## 핵심 결론 (2026-03-16)

### "URL만 넣으면"이 성립하지 않는 이유 (제품 체험 모드)
1. 랜딩페이지는 마케팅 카피 테스트이지 제품 체험 테스트가 아님
2. Personica 제품 체험 모드의 가치 = "제품이 사용자에게 가치를 주는가" → 제품의 핵심 가치는 로그인 후에 있음
3. 따라서 의미 있는 테스트에는 반드시 **고객 협조**가 필요

### 경쟁사 전원이 브라우저 자동화를 회피
- Blok, Aaru, Synthetic Users, Uxia 등 전부 Figma/설문/인지 시뮬레이션 방식
- 실제 제품을 브라우저로 조작하는 곳은 없음
- 비용 + 인증 문제가 회피 이유

### 딜리버리 모델 (제품 체험 모드)
- ~~셀프서브 SaaS ("URL만 넣으면")~~ → 고객 협조 기반 세팅
- 고객 제공: 테스트 계정, 스테이징/샌드박스 URL, 핵심 시나리오 안내
- 단, 서베이/인터뷰/A/B 테스트 등 다른 모드는 셀프서브 가능

**Why:** 비회원 퍼블릭 페이지만 테스트하는 것은 제품 체험 모드의 핵심 가치와 모순. 이 문제를 풀어야 Personica의 제품 체험 모드 차별화가 성립.
**How to apply:** 제품 메시징에서 "URL만 넣으면" 표현 사용 금지. 제품 체험 모드 온보딩에 테스트 환경 세팅 단계 포함.

### VC 미팅 피드백 — 시장 포지셔닝 확장
> 2026-03-20 VC 미팅 결과, 합성 페르소나 플랫폼으로 포지셔닝 확장 확정

VC 미팅(2026-03-20)에서 합성 페르소나 대규모 시뮬레이션 컨셉은 매우 긍정적 반응.

**제품명 변경**: ShipCheck → **Personica (페르소니카)**

**VC 제안 → 반영 완료:**
1. 합성 인터뷰/설문(Aaru/Synthetic Users 영역)도 적용 범위에 포함
2. 전문가 페르소나 집단 토론/시뮬레이션 (전문가 리뷰 모드)
3. A/B 테스트, 광고/마케팅 리서치, 퍼널 분석도 적용 범위에 포함
4. "실제 사용"은 디지털 프로덕트 체험 모드에서의 추가 차별화 포인트

**확정된 방향:**
- 포지셔닝: "합성 페르소나 시뮬레이션 플랫폼" (넓게)
- 핵심 해자: 페르소나 리얼리티 엔진 (감정·인지·의사결정 시뮬레이션)
- 실행: Phase 1 제품체험(beachhead) → Phase 2 합성리서치/A/B테스트/광고리서치 → Phase 3 전문가시뮬레이션
- Playwright는 하나의 인터페이스일 뿐

**Why:** 웹 UX 도구로만 한정하면 SAM이 작아 투자 유인 불충분. 엔진의 적용 범위를 보여줘야 VC 설득 가능.
**How to apply:** 전략 문서, 피치 자료에서 "합성 페르소나 시뮬레이션 플랫폼"으로 포지셔닝. 경쟁사들과 동일한 영역에서 페르소나 리얼리티 엔진의 깊이 차별화 + 제품 체험 모드의 추가 차별화.

### 사업계획서 작성 레퍼런스
> 사업계획서 작성 시 참조할 핵심 레퍼런스. TIPS 합격 사업계획서(마지막삼십분/잇차)가 유일한 참고 자료.

**유일한 레퍼런스 사업계획서:**
- `docs/strategy/reference-tips-bizplan-last30min.md` — TIPS 합격본 (마지막삼십분/잇차, 40페이지) 전체 분석
- 원본 PDF: `C:\Users\work\Documents\카카오톡 받은 파일\덕팔형네자료\20.05.20_마지막삼십분_팁스 사업계획서 최종본.pdf`

**이 레퍼런스에서 참고할 것:**
- 구조/흐름: 문제→기존한계→서비스→기술과제→솔루션→사업화→팀
- 시각자료 밀도: 모든 페이지에 차트/다이어그램/스크린샷/표/수식 포함
- 정량지표: 문제도 수치, 현황도 수치, 목표도 수치+측정방법+가중치, 매출도 수식
- 사업화 전략이 전체 45%로 가장 큰 비중 (TIPS는 사업화 가능성 중시)
- Personica 적용 매핑 표 포함 (잇차 패턴 → Personica 대응)

**기존 가이드라인 문서 (보조 참고):**
- `docs/strategy/bizplan-writing-guide.md`
- `docs/strategy/bizplan-preparation-guide.md`
- `docs/strategy/bizplan-template.md`

### Personica docs/ 문서 인덱스 — 언제 어떤 문서를 참고해야 하는가
> docs/ 폴더 전체 문서 맵 — 카테고리별 정리 + 각 문서의 용도/참고 시점 명시 (2026-03-21 현행화)

## docs/ 폴더 구조

```
docs/
├── foundation/         # 제품 기초 설계
├── research/           # 경쟁사/시장 조사
├── strategy/           # 전략 문서
├── plan/               # 기술 로드맵
├── charts/             # 시각자료
├── mockups/            # UI 프로토타입
└── [루트 마크다운]      # 디스커버리, 시장규모, VC 자료 등
```

---

### foundation/ — 제품 기초 설계

| 파일 | 이럴 때 참고 |
|------|------------|
| **product-vision.md** | 제품 방향/포지셔닝 논의 시 |
| **simulation-engine.md** | 엔진 구현/설계 시, 페르소나 리얼리티 엔진 아키텍처 참조 |
| **research-references.md** | 학술 근거, 새 논문 조사 시 기존 레퍼런스 확인 |

### research/ — 경쟁사/시장 조사

| 파일 | 이럴 때 참고 |
|------|------------|
| **uxagent-analysis.md** | 엔진 프로토타입 구현 시 |
| **blok-deep-dive.md** | 경쟁사 비교/포지셔닝 논의 시 |
| **auth-barrier-research.md** | 제품 체험 모드 온보딩 플로우 설계 시 |
| **pivot-review.md** | 제품 방향 재검토 시 |
| **synthetic-persona-market-landscape.md** | 전체 시장 지도, 30+ 경쟁사 비교 시 |

### strategy/ — 전략 문서

| 파일 | 이럴 때 참고 |
|------|------------|
| **market-scan.md** | SWOT/PESTLE/Porter 분석 시 |
| **competitive-analysis.md** | 경쟁사 심층 비교 시 |
| **lean-canvas.md** | 비즈니스 모델, 가격, COGS 논의 시 |
| **value-proposition.md** | 마케팅 카피, 세일즈 메시지 작성 시 |
| **user-research.md** | 페르소나/세그먼트/저니맵 논의 시 |
| **interview-script.md** | 고객 인터뷰 준비/실행 시 |
| **pre-mortem.md** | 리스크 체크, Go/No-Go 판단 시 |
| **vc-pitch-persona-agent.md** | 투자자 피칭 스크립트 |
| **bizplan-template.md** | 사업계획서 작성 시 (PSST 구조) |
| **bizplan-writing-guide.md** | 사업계획서 작성 실전 가이드 |

### scale/ — 사업계획서 핵심 SOT

| 파일 | 이럴 때 참고 | 비고 |
|------|------------|------|
| **unit-economics.md** | 원가·마진·가격 논의 시 | **SOT** — 수치 충돌 시 이 문서 우선 |
| **team-budget-plan.md** | 팀 구성·채용·예산 논의 시 | **SOT** — 인원/자금 충돌 시 이 문서 우선 |
| **revenue-model.md** | 수익 모델·과금 구조 논의 시 | |
| **market-entry-strategy.md** | 시장진입·채널 전략 논의 시 | |

### market-sizeing/ — 시장규모 SOT

| 파일 | 이럴 때 참고 | 비고 |
|------|------------|------|
| **market-sizing-yechangpae-appendix-software-first.md** | TAM/SAM/SOM 인용 시 | **SOT** — 시장규모 수치 충돌 시 이 문서 우선 |

### 루트

| 파일 | 이럴 때 참고 |
|------|------------|
| **discovery-plan.md** | 현재 위치/다음 단계 확인 시 |
| **user-stories.md** | 제품 플로우/스토리 맵 참조 시 |
| **engine-validation-report.md** | 엔진 검증 결과 데이터 인용 시 |
| **vc-meeting-handout*.md** | VC/예창패 자료 |

**How to apply:**
- 새 작업 시작 시 → `discovery-plan.md`에서 현재 위치 확인
- 기술 구현 시 → `foundation/simulation-engine.md`
- 전략/사업계획서 시 → `strategy/` 폴더 전체
- 경쟁사 질문 시 → `research/` + `strategy/competitive-analysis.md`

### 대표자 이력서 (유성)
> Personica 대표 유성의 이력서 정보 — 예창패 사업계획서 팀구성(T) 섹션 및 대표자 역량 작성 시 참조

## 기본 정보

- 이름: 유성
- 직함: AI Engineer
- 이메일: zoojaryu@gmail.com
- 총 경력: 11년 8개월 (2011.02~현재)

## 학력

- 중국 북경대학교(Peking University) 2008-2015
- 학사, Information Management and System 전공

## Technical Skills

- Languages: Python, Golang, SQL
- Cloud: Azure, AWS
- Agent Framework: Langgraph, SemanticKernel
- ML/DL: Pytorch, Tensorflow, Keras
- API: REST, GraphQL, gRPC
- Front-end: React
- Back-end: FastAPI, Flask, Spring
- Big Data: Spark

## 경력 상세

### 1. KT (2024.08~현재)

**AI엔지니어링팀 리딩 (약 20명 규모)**

| 프로젝트 | 설명 |
|---------|------|
| 보험 세일즈 Assistant | 보험 약관 및 세일즈 교육 자료 기반 영업 지원 Agent |
| 제조 도메인 Q&A봇 PoC | 멀티모달 RAG, 희소 도메인 LLM 파인튜닝 |
| 교육 Agent PoC | 멀티모달 교육 컨텐츠 및 개인화 기반 음성 교육 Agent |
| 팀즈 실시간 번역 미팅봇 PoC | MS팀즈 미팅 음성 번역 앱 개발 |
| AI은행원 PoC | 실시간 자연스러운 음성 은행업무 상담 AI |
| 기가지니 코파일럿 Agent PoC | 웹검색 Agent (Bing Search, Custom web search) |
| 법률문서 RAG Agent PoC | 공공기관 법령해석 및 판례 기반 RAG Agent |

### 2. SKT (2019.06~2024.08, 5년 2개월)

**Generative AI 개발 (2022.10~2024.08, 1년 10개월)**
- 생성형 이미지/비디오, AI 휴먼, LLM 기술 기반 뉴스 도메인 AI Studio 플랫폼 개발 **Tech PL**
- SKB AI 심재호 기자, 생성형 뉴스 이미지, AI 소년 최경주 POC
- AI 휴먼(lip-generation, faceswap, reenactment, super-resolution) 기술 R&D
- 이미지/비디오 생성 기술 R&D

**에이닷 큐피드 서비스 (2022.05~2022.10, 5개월)**
- 자연어 및 위치기반 검색 API 개발/운영 (Elasticsearch, Python, FastAPI, AWS)
- 큐피드 어시스턴트 봇 POC

**에이닷 메타버스 POC (2022.03~2022.05, 2개월)**
- 딥러닝 text summarization 리서치

**헬스케어 AI 서비스 (2021.10~2022.03, 5개월)**
- 멀티모달 기반 음성질환 예측 딥러닝 모델 개발
- CNN(ResNet, VGG16) 기반 멀티모달 모델 및 Spectrogram Autoencoder
- 음성/테뷸러 데이터 전처리 파이프라인 (Tensorflow)

**RPA Bot Builder**
- Dialog Manager (2021.02~2021.10, 8개월): FSM 기반 챗봇 DM 서버, 아키텍처 설계, Golang/gRPC
- Flow Builder (2020.08~2020.12, 4개월): Enterprise 챗봇 시나리오 low-code 웹앱, 아키텍처 설계, React/Django

**T월드 고객상담 챗봇**
- RCS Adapter (2020.11~2021.02, 4개월): GSMA RCC 규약 Adapter 서버, 아키텍처 설계
- Chatbot ADMIN (2020.05~2020.08, 3개월): FAQ/Mock 데이터 관리 (React, GraphQL, Flask)
- Backend Proxy (2020.02~2020.05, 3개월): Legacy API 기반 Proxy API (Java, Spring)

**T월드 다이렉트 세일즈봇 / 상담사 어시스턴트봇**
- Chatbot Server (2019.06~2020.02, 8개월): NLU/DM/백엔드 연동 서비스 플로우, **Scrum Master**, 아키텍처 설계

### 3. SSG.COM (2015.07~2019.06, 4년)

**AI 서비스 개발/운영 — 고객센터봇, 장보기봇**
- 딥러닝 NLP(LSTM, fasttext, w2v 등) 고객의도 분류 모델 개발
- Bot main server 개발 (메시지 템플릿, 채팅 플랫폼, 레거시 API, 3rd 파티 상담시스템 연동)
- Multi-turn Rule Based Dialog Manager 개발
- 클라우드 네이티브 개발 (Azure)

**빅데이터 플랫폼 및 서비스 개발/운영**
- Spark/Hadoop 기반 대용량 사용자 행위 데이터 → 상품 베스트 100 + 검색결과 랭킹 서비스
- 빅데이터 플랫폼 구축/운영 (Hadoop/Mesos/Spark)

**Machine Learning POC**
- Factorization Machines 기반 개인화 상품 추천
- BERT 기반 기계독해 및 챗봇 적용
- CNN 기반 상품이미지 카테고리 분류
- 사용자 검색 데이터 기반 구매예측 모델

### 4. 프리랜서 (2013.04~2013.07)
- SK 플래닛 내부 시스템 EAI 개발/운영 (Java, Spring)

### 5. (주)윌비솔루션 (2011.02~2013.04, 산업기능요원)
- 금융권 CRM 패키지 풀스택 개발/운영 (C# .NET, Java, Spring)

## Awards / Certifications

| 연도 | 내용 |
|------|------|
| 2025 | KT 부서간 협업 포상 |
| 2024 | KT인상 기관장 포상 |
| 2023 | SKT-B AI Challenge 해커톤 본선 진출 — "감성 AI 아바타를 활용한 AICC" 팀장 |
| 2023 | SKT SKADA Advanced Practitioner Vision Domain 자격 취득 |
| 2019 | SKT AI Center 우수사원상 |
| 2018 | SSG 해커톤 대상 (머신러닝 기반 상품 댓글 워드클라우드 서비스) |

## Community / 대외 활동

- 디지털플랫폼정부(DPG) AI 챌린지 멘토링 활동 (2024.09~2024.11)
- SK 개발자 커뮤니티 데보션 전문가 활동 (2024.02~2024.08)
- (사)한국인공지능연구소 자연어처리 Lab(SQUAD) 팀장 (2018.08~2019.02)

## 예창패 사업계획서 활용 포인트

Personica 대표자 역량 섹션에서 강조할 핵심:

1. **AI Agent 전문성**: KT에서 20명 규모 AI엔지니어링팀 리딩 — 보험/제조/교육/금융 등 다양한 도메인의 AI Agent 개발 경험
2. **LLM + 생성형 AI 실전 경험**: SKT에서 생성형 AI 플랫폼 Tech PL, AI 휴먼 기술 R&D — Personica의 페르소나 리얼리티 엔진 구현 역량 입증
3. **대화형 AI(챗봇) 아키텍처 설계 전문가**: SSG/SKT에서 Dialog Manager, NLU, 시나리오 엔진을 직접 설계/개발 — 페르소나의 인지/판단 시뮬레이션과 직결
4. **사용자 행동 데이터 분석**: SSG 빅데이터 플랫폼에서 대용량 사용자 행위 데이터 처리 → 구매예측, 추천, 랭킹 — 페르소나 행동 시뮬레이션의 데이터 기반
5. **풀스택 구현 능력**: Python/React/FastAPI/Cloud — 1인 MVP 개발 가능
6. **11년 8개월 경력 + 대기업(KT, SKT, SSG) 출신** — 실행 신뢰도
7. **"감성 AI 아바타"(2023 해커톤)**: Personica의 감정 시뮬레이션 방향과 일치하는 사이드 프로젝트 경험
