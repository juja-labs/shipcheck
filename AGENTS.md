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
- **Simulation Engine**: 페르소나 리얼리티 엔진 — 5개 레이어(인지→감정→판단→행동→기억) 시뮬레이션 (핵심 IP)
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
1. **페르소나 리얼리티 (핵심 해자)**: 페르소나 리얼리티 엔진이 감정·인지·의사결정을 5개 레이어로 구조적 시뮬레이션. 다른 합성 페르소나 제품들이 단순 LLM 프롬프팅인 반면, Personica는 실제 사람과 유사한 반응을 생성. 모든 상용 경쟁사 중 유일
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

## 사업계획서 작성 규칙

### 계위(depth) 규칙 — 3뎁스
- **Depth 1**: `1.`, `2.`, `3.`, `4.` — 대섹션 (문제 인식, 실현 가능성 등)
- **Depth 2**: `1-1.`, `1-2.`, `1-3.` — 중섹션 (기존 리서치의 구조적 한계 등)
- **Depth 3**: `•` 글머리 기호 — 모든 본문 내용 (+ 표도 이 레벨에 포함)

### 핵심 원칙
- 단락형 서술 전면 금지 — 모든 본문은 `•` 글머리 기호 사용
- 글머리 기호 내 문장은 자연스러운 서술체로 작성 (극단적 축약 금지)
- 표는 글머리 기호 레벨 안에 배치

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

### feedback_bizplan_no_daepyoja
> 사업계획서 본문에서 "대표자는 ~하였다" 식 3인칭 서술 금지

사업계획서 본문에서 "대표자는", "대표자가" 등으로 3인칭 서술하지 말 것.

**Why:** "대표자"는 양식 표/가이드의 라벨이지, 본문에서 자기를 지칭하는 용어가 아님. 본문에 쓰면 어색하다.
**How to apply:** 대표자 경력·역량은 4장(팀 구성)의 경력 표에서 정리. 1장 본문에서 굳이 언급해야 하면 "본 창업 아이템은 ~경험에서 출발하였다" 등 간접 서술로 처리.

### 사업계획서 작성 톤 지침
> 예창패 사업계획서는 AI/UX 비전문가인 고령 공무원 심사위원 대상으로 쉽고 평이하게 작성할 것

사업계획서 작성 시 어려운 전문 용어와 과장된 표현을 자제하고, 쉽게 읽히는 문장으로 작성할 것.

**Why:** 심사위원은 AI·UX 분야 비전문가이고 나이가 많은 공무원 성격의 평가자. 전문 용어나 영어 마케팅 투의 문장은 읽히지 않고 넘겨짐.

**How to apply:**
- 전문 용어는 처음 등장할 때 괄호로 쉬운 설명 병기
- 영어 마케팅 카피 직역체("사치가 아닌 일상 워크플로우로") 대신 자연스러운 한국어 사용
- 한 문장은 짧게, 한 문단에 한 가지 얘기만
- 과장 표현("수백 배", "역사상 가장", "폭발적") 지양 — 수치가 있으면 수치로, 없으면 담백하게
- 사업계획서 전체에 적용 (초안, 최종본 모두)

### feedback_bullet_format
> 사업계획서 개요(요약) 작성 시 글머리 기호(-) 형식으로 작성, 문장 나열 금지

사업계획서 개요(요약) 표 셀에 내용을 넣을 때 문장을 쭉 늘어놓지 말고, 글머리 기호(-)로 끊어서 작성할 것.

**Why:** 문장이 이어지면 읽기 힘들다는 사용자 피드백.
**How to apply:** 개요(요약) 표의 아이템 개요, 문제 인식, 실현 가능성, 성장전략, 팀 구성 셀 모두 `- 항목` 형식으로 작성.

### docs 편집 규칙
> docs/ 문서는 편집 전 최신 내용 재확인 + 편집 후 즉시 커밋 (여러 세션 동시 작업 충돌 방지)

### feedback_natural_korean
> 사업계획서 한국어 자연스러움 — 번역투/문어체 금지, 자연스러운 한국어 화자 관점에서 작성

사업계획서 작성 시 항상 자연스러운 한국어 화자 입장에서 읽어보고 작성할 것.

**Why:** "~인가" 반복, 번역투, 딱딱한 문어체 등이 그대로 나가서 사용자가 직접 수정해야 했음. 심사위원(비전문가·공무원)이 읽는 문서임.
**How to apply:** 작성 후 "한국어 원어민이 소리 내어 읽었을 때 어색하지 않은가" 기준으로 자체 검수. 번역투("~하는가", "~인 것이다"), 같은 어미 반복, 부자연스러운 한자어 나열 등 체크.

### feedback_no_lazy_repetition
> 표에서 같은 표현 반복 금지 — 각 항목의 맥락에 맞게 구체적으로 다르게 써야 함

표 작성 시 같은 표현을 여러 행에 반복하지 말 것. 각 행의 맥락에 맞게 구체적이고 다른 표현을 사용해야 한다.

**Why:** "실제 제품 미사용", "감정 없음" 같은 표현을 경쟁사 4곳에 반복하면 나이브하고 내용이 없어 보임. 사용자가 직접 수정해야 했음.
**How to apply:** 경쟁사 비교표 등에서 동일한 한계를 서술할 때, 각 경쟁사가 실제로 하는 방식을 기준으로 "왜 못 하는지"를 각각 다르게 설명. 예: "텍스트 인터뷰만 가능", "설문 응답만 가능", "기존 데이터 필수" 등.

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

### 예비창업패키지 사업계획서 작업 현황
> 2026 예비창업패키지 사업계획서 — 최종 파일 경로 및 워크플로우 (2026-03-23 정리)

**작업 파일:**
- **MD 원본 (SOT)**: `docs/예창패 실제 제풀용/claudecode/예창패_final.md` — 내용 수정은 여기서 진행
- **DOCX 최종본**: `docs/예창패 실제 제풀용/claudecode/2026년 예비창업패키지 사업계획서_final.docx` — MD 기반으로 생성하는 워드 제출본
- **워크플로우**: MD 원본 편집 → DOCX로 변환/반영

**다른 사업계획서 파일은 참조하지 않는다.** `예창패_초안_draft.md`, `bizplan-draft-p-s-*.md`, `codex/` 등 이전 초안·다른 버전은 무시할 것.

**Why:** 예비창업패키지 자금으로 Personica MVP 개발 후 시드 투자 유치 계획.

**How to apply:** 사업계획서 수정 요청 시 `예창패_final.md`만 읽고 편집. 워드 변환은 별도 요청 시 진행.

### Discovery 현황 (2026-03-21)
> 30명 분화 검증 + G2 비교 완료, CLI 아키텍처 확정. 상세: docs/discovery-plan.md, docs/engine-validation-report.md

- **분화**: ✅ 30명, 9개 세그먼트별 상이한 행동/감정/평점 패턴
- **현실성**: ✅ G2 대비 긍정 테마 90%, 불만 테마 71% 일치
- **결과**: 평균 평점 3.80, 추천 90%, Ablation에서 감정 파이프라인 제거 시 sycophancy 확인
- **아키텍처**: Claude Code CLI + playwright-cli, 감정 엔진(OCC→PAD→SDE) = 핵심 해자
- **남은 과제**: 페르소나-실행 분리, 다중 세션, 다제품 검증, 사업계획서 제출

### 다중 세션 시뮬레이션 — 추가 해자
> 첫 방문→재방문→습관 형성/이탈의 라이프사이클 시뮬레이션. 경쟁사 없음. 세션 간 메모리 시스템이 기술 핵심. 핵심 해자는 여전히 페르소나 리얼리티 엔진.

### Personica 핵심 정의
> **회사명**: 페르소닉 AI (2026-03-23 확정) | **제품명**: Personica (구 ShipCheck, 2026-03-20 변경)
> **포지셔닝**: 합성 페르소나 시뮬레이션 플랫폼. 피치는 "플랫폼"(넓게), 실행은 Phase 1 제품체험(좁게).
> **핵심 해자**: 페르소나 리얼리티 엔진 — 대외 브랜드명으로 사용, 내부에서만 "5개 레이어" 상세 설명.

### 딜리버리 모델 (제품 체험 모드)
> "URL만 넣으면" 폐기 → 고객 협조 기반 (테스트 계정 + 스테이징 URL + 시나리오 안내 필수). 서베이/인터뷰 등 다른 모드는 셀프서브 가능. 경쟁사 전원이 브라우저 자동화를 회피(Figma/설문 방식).

### VC 미팅 피드백 (2026-03-20)
> 합성 페르소나 플랫폼으로 포지셔닝 확장 확정. ShipCheck → Personica 제품명 변경.
> 적용 범위: 합성 인터뷰/설문, 전문가 시뮬레이션, A/B 테스트, 광고/퍼널 리서치까지 확장.

### 예창패 사업계획서 분량 제한
> 2026 예비창업패키지 사업계획서 본문 10페이지 이내 (목차 제외), 추가 이미지는 별첨 2 기타 증빙으로 제출

사업계획서는 **목차(1페이지)를 제외하고 본문 10페이지 이내**로 작성해야 한다.

- 사업 신청 시 작성 목차 페이지는 삭제하고 제출
- 사업계획 설명을 위한 추가 이미지 첨부가 필요한 경우, [별첨 2]의 기타 증빙서류로 제출
- 사업계획서 양식은 변경·삭제 불가
- 파일 용량 제한: 30MB
- 출처: `docs/예창패 실제 제풀용/claudecode/(붙임) 2026 예비창업패키지 예비창업자 모집 수정 공고(2026-143호).pdf` + 사업계획서 양식 docx

### reference_bizplan_template
> 예창패 사업계획서 양식 원본을 MD로 변환한 파일 위치 + 각 섹션별 작성 가이드 요약

예창패 사업계획서 양식 원본(DOCX)을 MD로 변환한 파일:
`docs/예창패 실제 제풀용/claudecode/양식.md`

## 각 섹션별 양식 가이드 (파란 글씨 안내 문구)

| 섹션 | 양식이 요구하는 내용 |
|------|---------------------|
| **아이템 개요** | 제품·서비스 개요(사용 용도, 사양, 가격), 핵심 기능·성능, 고객 제공 혜택. 예시: "가벼움(혜택)을 위해 용량 줄이는 재료(핵심 기능)" |
| **문제 인식** | 국내·외 시장 현황 및 문제점, 아이템 필요성 |
| **실현 가능성** | 사업기간 내 개발/구체화 계획(최종 산출물 형태·수량), 차별성 및 경쟁력 확보 전략, 정부지원사업비 집행 계획 |
| **성장전략** | 경쟁사 분석, 시장 진입 전략, 수익화 모델, 전체 로드맵, 투자유치 전략, 중장기 사회적 가치(ESG: 환경/사회/지배구조) |
| **팀 구성** | 대표자 역량(경영능력, 경력·학력, 기술력, 노하우, 네트워크), 팀원 역량, 채용 예정 인력, 협력 기관·파트너 |

## 주요 제약 규칙
- 본문 10페이지 이내 (목차 제외)
- 1단계/2단계 정부지원사업비 각 **20백만원 내외**
- 개인정보 마스킹 필수 (성명, 생년월일, 학교명, 직장명 → ○, * 처리)
- 파란 글씨 안내 문구는 삭제 후 검정 글씨로 작성

### docs/ 문서 인덱스
> 주요 문서 위치 가이드 (2026-03-21)

- `docs/foundation/` — 엔진 설계(`simulation-engine.md`), 제품 비전, 학술 레퍼런스
- `docs/research/` — 경쟁사 분석(`blok-deep-dive.md`, `synthetic-persona-market-landscape.md`), 피봇 리뷰
- `docs/strategy/` — SWOT/Porter(`market-scan.md`), 경쟁사 비교, Lean Canvas, VP, 사업계획서 가이드
- `docs/scale/` — **SOT**: unit-economics.md, team-budget-plan.md, revenue-model.md, market-entry-strategy.md
- `docs/market-sizeing/` — **SOT**: market-sizing-yechangpae-appendix-software-first.md (TAM/SAM/SOM)
- `docs/discovery-plan.md` — 현재 위치/다음 단계
- `docs/engine-validation-report.md` — 엔진 검증 결과 데이터

### 대표자 이력서 (유성)
> Personica 대표, AI Engineer 11년 8개월 경력

- **이름**: 유성 | **학력**: 북경대학교 Information Management and System
- **Skills**: Python, Golang, React, FastAPI, Pytorch, Langgraph, Azure/AWS
- **KT** (2024.08~현재): AI엔지니어링팀 리딩 (~20명), 보험/제조/교육/금융 도메인 AI Agent 다수 개발
- **SKT** (2019.06~2024.08): 생성형 AI 플랫폼 Tech PL, AI 휴먼 R&D, 챗봇 Dialog Manager/NLU 아키텍처 설계
- **SSG.COM** (2015.07~2019.06): 고객센터봇/장보기봇 NLP 모델, 빅데이터 플랫폼(Spark/Hadoop), ML 추천/예측
- **수상**: KT인상 기관장 포상(2024), SKT AI Challenge 해커톤 "감성 AI 아바타" 본선(2023), SSG 해커톤 대상(2018)
- **대외활동**: DPG AI 챌린지 멘토, SK 데보션 전문가, 한국AI연구소 NLP Lab 팀장
- **예창패 핵심**: AI Agent 전문성 + LLM/생성형AI 실전 + 챗봇 아키텍처 설계 + 풀스택 MVP 구현 가능 + 대기업 11년 실행 신뢰도
