# ShipCheck

## Project Overview
ShipCheck은 MVP/프로토타입을 실제 시장에 출시하기 전에, AI 페르소나가 실제 사람처럼 제품을 사용하고 리뷰해주는 SaaS 플랫폼이다.

핵심 가치: "만드는 건 끝났어. 이거 사람들이 원할까?" — 다양한 배경·감정·맥락을 가진 합성 페르소나가 제품을 직접 사용하고, 실제 사람의 리뷰와 유사한 수준의 피드백을 제공한다.

## Current Status
- **단계**: Discovery — 핵심 가설 검증 전 (실험 미실행)
- **핵심 가설**: "AI 페르소나 시뮬레이션의 충실도가 실제 의사결정에 쓸 만한 수준인가?" — (1) 분화: 페르소나들이 유의미하게 다른 행동을 보이는가, (2) 현실성: 그 패턴이 실제 인간과 방향 일치하는가
- **피봇 결정**: "URL만 넣으면 셀프서브"는 폐기됨 → 고객이 스테이징 URL + 테스트 계정 제공하는 모델로 전환
- **상세 계획**: `docs/discovery-plan.md` 참조

## Core Problem
제품을 만들 때 페르소나와 유저 저니맵을 기반으로 설계하지만, 실제 다양한 사용자가 쓸 때는 예상과 다르게 동작할 수 있다. 다양한 나이·환경·취향·기술 숙련도를 가진 개개인이 제품을 사용하면서 느끼는 감정과 가치를 실제 출시 전에 검증할 방법이 없다.

ShipCheck은 이 문제를 "사람처럼 제품을 사용하는 AI 페르소나 시뮬레이션"으로 푼다.

## Tech Stack
- **Browser Automation**: Playwright — 페르소나 에이전트가 실제 제품을 사용
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

### 제품 플로우
```
고객 입력 (스테이징 URL + 테스트 계정 + 타겟 유저 설명)
    │
    ▼
Phase 1: 자동 분석
  ① Playwright로 제품 크롤링 → 페이지/기능/플로우 파악
  ② LLM이 Feature 온톨로지 자동 생성
  ③ 타겟 유저 기반 페르소나 N명 생성 (Big Five 수학적 매핑)
  ④ 시뮬레이션 설정 자동 결정
    │
    ▼
Phase 2: 제품 체험 (개인 시뮬레이션)
  ① 각 페르소나가 Playwright로 실제 제품을 독립적으로 사용
  ② 매 상호작용마다 5-Layer 파이프라인 실행:
     인지 평가 → 감정 평가 → 의사결정 → 행동 실행
  ③ 행동 로그 + 감성 로그 + 마이크로 행동 로그 수집
    │
    ▼
Phase 3: 분석 및 리포트
  ① 세그먼트별 교차 분석 (기능별 × 세그먼트별)
  ② 감정 궤적 타임라인, 이탈 지점, 개선 제안
  ③ 선택적 페르소나 인터뷰 (체험 기반 후속 질문)
```

### 확장 아이디어: 시장 동역학 시뮬레이션 (MVP 이후)
- 개별 체험 후, 네트워크 기반 입소문/채택 시뮬레이션
- ※ 핵심 엔진(페르소나 시뮬레이션)이 충분히 성숙한 후 확장

## Key Differentiators
1. **시뮬레이션 충실도**: 5-Layer 아키텍처로 감정·인지·의사결정을 구조적으로 시뮬레이션. 모든 상용 경쟁사 중 유일
2. **실제 제품 사용**: 설문/Figma/데이터 기반이 아닌, Playwright로 실제 제품을 직접 조작. 경쟁사 전원이 이 접근을 회피함
3. **기존 데이터 불필요**: Amplitude/Mixpanel 등 기존 분석 데이터 없이, 스테이징 URL만으로 동작. Pre-launch MVP에 최적

## Thinking Principles
- **[CRITICAL] 문제 중심 사고**: 기술/도구를 먼저 정하고 문제에 끼워맞추지 말 것. 항상 "어떤 문제를 푸는가" → "그 문제를 가장 잘 푸는 방법은?" 순서로 사고할 것. 기술 스택은 문제 해결의 수단이지 전제가 아님. 특정 기술을 쓰기 위해 문제를 왜곡하거나 불필요한 복잡성을 추가하는 것은 금지.
- 설계/아키텍처 논의 시 "이 기술을 어떻게 적용할까?"가 아니라 "이 문제에 이 기술이 정말 필요한가?"를 먼저 물을 것.
- **페르소나 시뮬레이션 충실도가 최우선**: 소셜 시뮬레이션, KG 분석 등 부가 기능보다 "개별 페르소나가 얼마나 사람처럼 제품을 사용하고 반응하는가"가 핵심 IP. 이 품질이 확보되지 않으면 위에 뭘 얹어도 무의미.
- **QA 도구가 아님**: ShipCheck은 기능 정상 동작 여부를 테스트하는 도구가 아님. "이 제품이 사용자에게 가치와 만족을 주는가"를 검증하는 도구. 기술적으로 Playwright를 공유하지만 목적이 완전히 다름.

## Conventions
- 한국어 코멘트 사용
- 커밋 메시지는 영어 conventional commits (feat:, fix:, chore: 등)
- Python: Black formatter, type hints 필수
- Frontend: ESLint + Prettier

## Documentation
프로젝트 문서는 `docs/` 폴더에 정리:
- `docs/foundation/` — 제품 비전, 5-Layer 엔진 설계, 논문/레퍼런스
- `docs/research/` — UXAgent 분석, Blok 심층분석, 인증 장벽, 피봇 리뷰
- `docs/strategy/` — 시장 규모, 경쟁사, SWOT, Lean Canvas, 유저리서치, VP, 인터뷰 스크립트
- `docs/discovery-plan.md` — 전체 디스커버리 계획 (핵심 가설 + 실험 설계)

## References
- UXAgent (Amazon, CHI 2025): https://github.com/neuhai/UXAgent — 브라우저 자동화 기반 UX 테스팅 (parser.js, env.py 재사용 검토)
- PRISM (Fudan, 2025): https://arxiv.org/abs/2512.19933 — SDE 감정 진화, Big Five→행동 파라미터 매핑
- Concordia (Google DeepMind): https://github.com/google-deepmind/concordia — GM-Player 아키텍처
- Generative Agents (Stanford, 2023): https://arxiv.org/abs/2304.03442 — Memory Stream + Reflection
- 전체 레퍼런스: `docs/foundation/research-references.md` (논문 30+편, 데이터셋, 벤치마크)
