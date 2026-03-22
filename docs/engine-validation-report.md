# Personica 핵심 엔진 검증 결과 보고서

**작성일**: 2026-03-21 (30명 실험 데이터 반영)
**문서 용도**: 사업계획서 근거자료
**검증 대상 제품**: Tally.so (웹 기반 폼 빌더)

---

## 1. 개요

Personica는 인지심리학 기반 5-Layer 엔진으로 성격·감정·인지·의사결정을 갖춘 AI 페르소나를 생성하여, 제품 체험·서베이·전문가 리뷰·퍼널 분석 등 모든 사용자 리서치를 시뮬레이션하는 합성 페르소나 플랫폼이다. 제품 체험 모드에서는 Playwright로 실제 브라우저를 조작하며 행동/감정 로그를 수집한다.

**검증 목표**: "AI 페르소나 에이전트가 실제 사람처럼 제품을 사용하고, 실제 사용자 리뷰와 유사한 피드백을 생성할 수 있는가?"

구체적으로 두 가지를 검증한다:
1. **분화(Differentiation)**: 성격이 다른 페르소나들이 같은 제품에서 유의미하게 다른 행동/반응을 보이는가?
2. **현실성(Realism)**: 그 차이 패턴이 실제 인간 리뷰와 방향적으로 일치하는가?

---

## 2. 기술 아키텍처

### 전체 구조

```
┌────────────────────────────────────────────────┐
│  Claude Code CLI (-p 모드)                      │
│  페르소나 프롬프트로 시스템 프롬프트 주입         │
│  Bash 도구 허용 → playwright-cli + step_update  │
└────────────┬───────────────────────────────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
┌──────────┐   ┌──────────────────┐
│playwright│   │step_update (Python)│
│   -cli   │   │감정 파이프라인 실행 │
│브라우저  │   │OCC→SDE→PAD→이탈판정│
│직접 제어 │   │결정론적 수학 계산   │
└──────────┘   └──────────────────┘
```

| 컴포넌트 | 역할 | 기술 |
|----------|------|------|
| Claude Code CLI (`-p` 모드) | 페르소나 에이전트 실행 | Anthropic Claude, subprocess 오케스트레이션 |
| playwright-cli | 실제 브라우저 제어 | Playwright 기반 접근성 스냅샷 |
| 페르소나 프롬프트 | Big Five → 15+ 행동 파라미터 변환 | PRISM 논문 기반 수학적 매핑 |
| 감정 시뮬레이션 엔진 | OCC → PAD 3차원 → SDE 확률적 노이즈 | Python, NumPy |
| 이탈 판정 모듈 | PAD threshold + error_count 기반 강제 종료 | 결정론적 룰 (LLM 외부) |

### 스텝당 실행 흐름

```
1. playwright-cli snapshot → 현재 페이지 접근성 스냅샷 획득
2. 페르소나(Claude)가 1인칭으로 감정과 의도 서술
3. playwright-cli click/fill/type → 행동 실행
4. step_update 호출 → 감정 파이프라인 실행 (OCC 분류 → PAD delta → SDE noise → 이탈 판정)
5. should_abandon=true면 즉시 세션 종료
6. 반복 (최대 25스텝)
```

### 왜 이 구조인가: Sycophancy 억제

LLM에게 감정 판단을 맡기면 제품에 관대해지는 sycophancy 문제가 발생한다. Personica는 감정 계산을 LLM 외부의 수학적 파이프라인으로 분리하여 이 문제를 구조적으로 해결한다.

| 비교 항목 | 파이프라인 없음 (Naive) | 파이프라인 있음 (Full) |
|----------|:---:|:---:|
| 제품 유용성 점수 (PU) | 0.6 ~ 0.8 (관대) | 0.3 ~ 0.5 (솔직) |
| "포기하겠다" 언급 | 0회 | 4회 |
| 매몰 비용 오류 발생 | 없음 | 자연 발생 |
| PU/PEOU 차이 | Naive가 0.2~0.3 더 높음 | 기준선 |

이 ablation 결과가 감정 엔진의 가치를 정량적으로 증명한다.

---

## 3. 페르소나 모델링

### 10개 성격 세그먼트

세그먼트는 직업이 아니라 **"디지털 제품을 대하는 태도"**로 분류한다.

| 세그먼트 | 한글명 | Big Five 핵심 축 | digital_literacy |
|----------|--------|-----------------|:---:|
| explorer | 탐색형 | 높은 O, 낮은 C | 2~3 |
| power_user | 파워유저형 | 높은 O, 높은 C | 3~4 |
| cautious_methodical | 신중한 체계형 | 낮은 O, 높은 C | 2~3 |
| intuitive | 직감형 | 낮은 O, 낮은 C | 2~3 |
| anxious | 불안형 | 높은 N | 2~3 |
| calm | 차분형 | 낮은 N | 2~3 |
| agreeable | 관대형 | 높은 A | 2~3 |
| critical_vocal | 비평형 | 낮은 A, 높은 E | 2~3 |
| tech_savvy | 기술숙련형 | 높은 O, 높은 C | 4 (고정) |
| tech_novice | 입문형 | 낮은 O | 1~2 |

> O=Openness, C=Conscientiousness, E=Extraversion, A=Agreeableness, N=Neuroticism

### Big Five → 행동 파라미터 매핑 (PRISM 논문 기반)

모든 파라미터는 Big Five 점수에서 **수학적으로 파생**된다. LLM이 성격을 "해석"하는 것이 아니라, 미리 계산된 수치가 행동을 제어한다.

| 파라미터 | 수식 | 범위 | 의미 |
|----------|------|------|------|
| `error_tolerance` | `max(1, round(3 + A*3 - N*2))` | 1~6회 | 포기까지 에러 허용 횟수 |
| `emotional_volatility` | `0.05 + N*0.25` | 0.05~0.30 | SDE 확산 계수 (감정 변동폭) |
| `exploration_tendency` | `0.20 + O*0.60` | 0.20~0.80 | 새 기능 탐색 확률 |
| `methodical_score` | `C*0.75 + (1-O)*0.25` | 0~1.0 | 단계적(1.0) vs 탐색적(0.0) |
| `sycophancy_resistance` | `(1-A)*0.70 + N*0.30` | 0~1.0 | 제품 비판 성향 |
| `click_hesitation_range_ms` | N, C 기반 | 100~3000ms | 클릭 전 망설임 시간 |
| `reading_ratio` | O, C, N 기반 | 0.10~0.65 | 페이지 텍스트 읽기 비율 |
| `back_button_freq` | `0.05 + N*0.15` | 0.05~0.20 | 뒤로가기 빈도 |
| `satisficing_threshold` | C, O 기반 | 0~1.0 | Satisficer vs Maximizer |
| `pleasure_abandon_threshold` | `-0.6 + N*0.3` | -0.6~-0.3 | 이탈 기준 쾌감 수치 |
| `emotion_decay_rate` | `0.75 + A*0.15` | 0.75~0.90 | 감정 감쇠율 |

### JTBD + 이전 도구 경험으로 개별 페르소나 구체화

각 페르소나는 행동 세그먼트 외에 6개 역할 프로파일(G2 리뷰어 인구통계 분포 기반)과 매칭된다:

| 역할 프로파일 | G2 가중치 | 예산 민감도 | 대표 이전 도구 |
|--------------|:---:|:---:|---|
| 스타트업 창업자/CEO | 20% | HIGH | Typeform, Google Forms |
| 마케팅 전문가 | 15% | MODERATE | Typeform, HubSpot Forms |
| 소규모 비즈니스 운영자 | 25% | VERY_HIGH | Google Forms |
| 기술 전문가 | 10% | LOW | Typeform, JotForm, custom code |
| 교육자/비영리 | 15% | VERY_HIGH | Google Forms, Microsoft Forms |
| 크리에이티브/프리랜서 | 15% | HIGH | Google Forms, Canva, Typeform |

### NNGroup 벤치마크 기반 캘리브레이션

실제 인간 행동 데이터를 기준으로 파라미터를 보정:

| NNGroup 벤치마크 | 수치 | Personica 반영 |
|-----------------|------|---------------|
| 페이지 텍스트 읽기 비율 | ~20% (79%는 스캔) | `reading_ratio` 기본값 0.10~0.65, 대부분 0.20 근처 |
| 65세+ 태스크 수행 속도 | 43% 느림 | `digital_literacy` 1~2 → `cognitive_load` 증가 |
| 바운스율 | 44~45% | 이탈 판정 threshold 캘리브레이션 |
| 전체 기사 읽는 비율 | 16%만 | `reading_ratio`가 0.65 초과 불가 |

### 페르소나 생성 현황

- **30명** 벤치마크 페르소나 생성 완료 (`configs/personas/benchmark/b001~b030.yaml`)
- 역할 x 행동 세그먼트 매트릭스에서 G2 가중치 기반 샘플링
- Big Five 점수는 세그먼트 범위 내에서 무작위 샘플링 (seed=42, 재현 가능)
- LLM(Claude Sonnet)으로 배경 서술, JTBD, 직업 등 구체화

---

## 4. 감정 시뮬레이션 엔진 (기술적 해자)

Personica의 핵심 해자인 5-Layer 엔진 중 감정 시뮬레이션(Layer 3)은 LLM 외부에서 수학적으로 계산되어 LLM의 행동을 제약하는 핵심 모듈이다. 감정을 AI가 "느끼는" 것이 아니라, **수학이 결정하고 AI가 그 안에서 행동한다.** 이 페르소나 리얼리티가 Personica를 단순 프롬프트 기반 경쟁사와 구분하는 핵심 차별점이다.

### 4-1. OCC Appraisal: 이벤트 → 감정 변화량

OCC(Ortony, Clore, Collins, 1988) 모델의 22개 감정 카테고리를 8개로 단순화하여, 각 이벤트에 대한 PAD delta를 **결정론적으로** 매핑한다.

| OCC 이벤트 | Pleasure | Arousal | Dominance | 감정 라벨 |
|-----------|:---:|:---:|:---:|:---:|
| `action_success` | +0.10 | -0.05 | +0.10 | satisfied |
| `action_failure` | **-0.15** | +0.15 | -0.15 | frustrated |
| `page_change` | +0.05 | +0.10 | +0.05 | curious |
| `error_detected` | **-0.20** | +0.20 | -0.20 | frustrated |
| `complex_page` | -0.05 | +0.15 | -0.10 | anxious |
| `simple_success` | +0.12 | -0.05 | +0.08 | satisfied |
| `stuck` | -0.12 | -0.10 | -0.15 | bored |
| `first_impression` | 0.00 | +0.15 | 0.00 | neutral |

이 매핑은 LLM이 결정하지 않는다. 이벤트 분류도 결정론적 룰 기반이다:
- 연속 실패 2회 이상 → `stuck`
- 액션 실패 + DOM에 에러 메시지 → `error_detected`
- 액션 실패 (에러 없음) → `action_failure`
- URL 변경 + 요소 30개 초과 → `complex_page`

### 4-2. SDE Noise: 성격에 따른 감정 반응 강도 차이

확률미분방정식(Stochastic Differential Equation)으로 같은 이벤트에도 페르소나마다 다른 감정 반응을 생성한다.

```
dE(t) = mu(E, t) dt + sigma(E, t) dW(t)
```

- `mu`: 드리프트 항 (OCC delta + decay)
- `sigma`: 확산 항 = `emotional_volatility * 0.4`
- `dW(t)`: Wiener process (정규분포 노이즈)

| 페르소나 유형 | Neuroticism | emotional_volatility (sigma) | 감정 변동 특성 |
|-------------|:---:|:---:|---|
| 불안형 (N=0.84) | 0.84 | 0.260 | noise = 0.104 * N(0,1) → 큰 변동 |
| 차분형 (N=0.12) | 0.12 | 0.080 | noise = 0.032 * N(0,1) → 작은 변동 |
| 평균 (N=0.50) | 0.50 | 0.175 | noise = 0.070 * N(0,1) → 보통 변동 |

추가로 연속 실패 시 부정적 감정이 증폭된다:
```
failure_amplifier = 1.0 + consecutive_failures * 0.08
```

### 4-3. PAD Decay: 감정의 자연 감쇠

매 스텝마다 현재 감정 상태에 지수적 감쇠를 적용한다:

```
emotion[t] = emotion[t-1] * decay_rate + delta[t]
```

- `decay_rate`: 0.75 (Agreeableness 낮음) ~ 0.90 (Agreeableness 높음)
- 효과: 좌절적 이벤트 후 시간이 지나면 감정이 자연 회복

### 4-4. 이탈 판정: 결정론적 강제 종료

LLM이 sycophancy로 "계속 써보자"고 하더라도, 아래 조건을 만족하면 **강제 종료**된다:

| 이탈 조건 | 수식 | 의미 |
|----------|------|------|
| 에러 과다 | `consecutive_failures >= error_tolerance` | 연속 실패가 허용 횟수 초과 |
| 쾌감 임계값 | `pleasure < threshold AND step > 3` | 만족도가 성격별 기준 아래로 추락 |
| 인지 과부하 | `cognitive_load > 0.95 AND pleasure < -0.4 AND step > 2` | 복잡한 페이지 + 부정 감정 동시 충족 |

### 4-5. Ablation 결과: 파이프라인의 가치 증명

| 지표 | Full 모드 (파이프라인 O) | Naive 모드 (파이프라인 X) | 차이 |
|------|:---:|:---:|:---:|
| Perceived Usefulness (PU) | 0.3 ~ 0.5 | 0.6 ~ 0.8 | Naive가 +0.2~0.3 |
| 이탈 위협 발생 | 4회 | 0회 | Full만 발생 |
| 매몰 비용 오류 | 자연 발생 | 없음 | Full만 발생 |
| Perceived Ease of Use (PEOU) | 현실적 | 관대 | Naive가 +0.2~0.3 |

**결론**: 감정 시뮬레이션 엔진이 없으면 LLM이 제품에 관대해진다. 엔진이 수학적 제약을 부과해야 현실적 피드백이 나온다.

---

## 5. 브라우저 자동화 발전 과정

Personica의 제품 체험 모드는 실제 브라우저에서 제품을 조작하는 유일한 합성 사용자 서비스이다. Playwright는 이 모드에서 사용하는 하나의 인터페이스이며, 4단계의 기술 진화를 거쳤다.

| Phase | 방식 | 문제점 | 결과 |
|:---:|---|---|---|
| 1 | parser.js (UXAgent 방식) | 모달 차단, contenteditable 미인식, semantic-id가 `button1` 같은 무의미한 이름 | 클릭 실패 세션당 3~5건 |
| 2 | Playwright 접근성 스냅샷 | curly quotes 에러, unnamed 버튼 매칭 실패, SPA 전환 시 빈 스냅샷 | 클릭 실패 0~2건으로 감소 |
| 3 | CDP 직접 호출 | `Input.insertText`로 "/" 타이핑 실패, DOM + AX 병합 복잡도 | 일부 입력 시나리오 개선 |
| **4** | **playwright-cli** | **안정적 동작** | **클릭 실패 0건** |

### 최종 아키텍처 (Phase 4)

```
페르소나(Claude) → playwright-cli -s={session_id} snapshot → 접근성 트리 YAML
                → playwright-cli -s={session_id} click <ref> → 요소 클릭
                → playwright-cli -s={session_id} fill <ref> "text" → 텍스트 입력
                → playwright-cli -s={session_id} type "text" → 키보드 입력
```

**결론**: 브라우저 자동화는 제품 체험 모드의 인프라이지 해자가 아니다. playwright-cli라는 검증된 도구를 활용하여 안정성을 확보했으며, Personica의 진정한 해자는 5-Layer 엔진의 페르소나 리얼리티(감정·인지·의사결정 시뮬레이션의 깊이)에 있다.

---

## 6. 실험 결과

### 6-1. 페르소나 분화 검증

**실험 설계**: 30명의 AI 페르소나가 동일한 제품(Tally.so)을 동시에 사용. 같은 제품에서 세그먼트별로 다른 행동 패턴이 나타나는지 검증.

#### 대표 사례 비교

| | 파워유저형 (신재원) | 신중형 (정민아) | 입문형 (홍은비) | 비평형 (강동우) |
|---|---|---|---|---|
| **첫 행동** | 에디터 직행 | 템플릿 갤러리 탐색 | 영어 화면에 당황 | 기능 평가 모드 |
| **탐색 전략** | "/" 커맨드, 블록 팔레트, Notion 연동 확인 | 가장 비슷한 템플릿 타협 선택 → 조심스럽게 편집 | 템플릿에서 골라 수정 시도 → 블록 추가 방법 모름 | 핵심 기능 접근 시도 |
| **비교 대상** | Notion, Typeform | Google Forms | 없음 (첫 경험) | Typeform, JotForm |
| **이탈 이유** | 연동 기능 확인 후 자발적 종료 | 목표 달성 (폼 1개 완성) | 편집 방법 모름 → 포기 | 30분 사용 후 핵심 기능 미접근 |
| **최종 평점** | --- | --- | --- | ★2.5 비추천 |

#### 행동 분화 패턴 요약

| 세그먼트 | 탐색 경로 특성 | 이탈 유형 | 감정 궤적 |
|----------|-------------|----------|----------|
| 파워유저형 | 에디터 직행 → 고급 기능 탐색 → 설정/연동 확인 | 기능 한계 판단 | 초반 상승 → 중반 급락 |
| 신중한 체계형 | 템플릿 → 안전한 경로만 → 기본 편집 | 목표 달성 또는 불안 이탈 | 안정적, 변동폭 작음 |
| 입문형 | 랜딩 → 템플릿 → 에디터에서 막힘 | 조작 불가 이탈 | 불안 상승 → 공포 |
| 탐색형 | 이것저것 클릭 → 새 기능 발견 → 깊이보다 넓이 | 호기심 충족 또는 혼란 | 변동폭 큼 |
| 비평형 | 핵심 기능 빠르게 평가 → 부족하면 즉각 비판 | 기능 부족 판단 | 초반 중립 → 급락 |
| 불안형 | 조심스러운 탐색 → 실수 공포 → 안전한 것만 | 불안 누적 이탈 | 변동폭 큼 (N 높음) |

### 6-2. G2 리뷰 유사도 (의미 기반 분석)

**방법**: G2 실제 리뷰와 합성 리뷰의 테마/감정 분포를 사후적(post-hoc)으로 비교. G2 리뷰 내용은 페르소나 프롬프트에 포함되지 않았다 (치팅 방지).

| 비교 항목 | G2 실제 리뷰 | 합성 리뷰 |
|----------|:---:|:---:|
| 리뷰 수 | 88개 | **30개 (실측)** |
| 평균 평점 | ~4.5 | **3.80 (실측)** |
| 추천 비율 | ~97% | **90% (실측)** |

#### 30명 실험 실측 데이터

**평점 분포 (n=30)**:

| 평점 | 인원 | 비율 |
|:---:|:---:|:---:|
| 4.5 | 5명 | 17% |
| 4.0 | 12명 | 40% |
| 3.5 | 10명 | 33% |
| 3.0 | 2명 | 7% |
| 2.5 | 1명 | 3% |

**세그먼트별 평균 평점 (실측)**:

| 세그먼트 | 평균 평점 | n | 해석 |
|----------|:---:|:---:|------|
| 기술능숙형 | 4.33 | 3 | 기능을 빠르게 파악, 높은 만족 |
| 체계형 | 4.25 | 2 | 단계적 탐색, 안정적 경험 |
| 파워유저형 | 4.00 | 3 | 기능은 인정하되 한계도 인식 |
| 차분형 | 4.00 | 2 | 감정 변동 없이 객관적 평가 |
| 신중형 | 3.80 | 5 | 불안감 속에서도 조심스럽게 완수 |
| 탐색형 | 3.67 | 3 | 넓게 탐색하되 깊이 부족 체감 |
| 직감형 | 3.60 | 5 | 직감적 탐색, 기대와 현실 괴리 |
| 비평형 | 3.50 | 6 | 가장 비판적, 구체적 불만 제시 |
| 입문형 | 3.50 | 1 | 디지털 도구 자체의 어려움 |

**이전 도구 분포 (실측)**:

| 이전 도구 | 인원 | G2와 일치 여부 |
|----------|:---:|:---:|
| Google Forms | 15명 | ✅ G2에서도 최다 언급 |
| Typeform | 9명 | ✅ G2에서도 주요 비교 대상 |
| JotForm | 2명 | ✅ G2에서 소수 언급 |
| 기타 | 4명 | - |

#### 테마 일치율

**G2 상위 10개 긍정 테마 중 9개 일치 (90%)**:

| G2 긍정 테마 | G2 빈출도 | 합성 일치 여부 |
|-------------|:---:|:---:|
| 사용 편의성 (ease of use) | 49.5% | O |
| 무료 티어 (free tier) | 31.3% | O |
| 디자인 품질 (design quality) | 28.3% | O |
| 조건부 로직 (conditional logic) | 25.3% | O |
| 통합/연동 (integrations) | 25.8% | O |
| 커스터마이징 (customization) | 22.2% | O |
| Notion 유사 UI (notion-like) | 18.2% | O |
| 빠른 설정 (quick setup) | 16.2% | O |
| 템플릿 (templates) | 14.1% | O |
| 고객 지원 (customer support) | 20.2% | **X** (단일 세션에서 구조적으로 불가) |

**불만 테마 일치율: 상위 7개 중 5개 일치 (71%)**:

| G2 불만 테마 | 합성 일치 |
|-------------|:---:|
| 학습 곡선 (learning curve) | O |
| 가격 우려 (pricing concern) | O |
| 커스터마이징 한계 | O |
| 모바일 이슈 | X (데스크톱 전용 테스트) |
| 조건부 로직 복잡도 | O |
| 템플릿 다양성 부족 | O |
| 고객 지원 속도 | X (단일 세션 한계) |

#### 특이 발견

| 발견 | G2 | 합성 | 해석 |
|------|:---:|:---:|------|
| "No signup required" 기만 감지 | 2명 언급 | **14명 감지** | 합성 페르소나가 첫인상에 더 민감하게 포착 |
| False positive (블록 내비게이션, 폼 휘발) | - | 2건 발생 | 실제 UX 문제이나 장기 사용자는 극복하는 유형 |

#### 평점 차이 해석

| 항목 | G2 | 합성 |
|------|:---:|:---:|
| 평균 평점 | ~4.5 | ~3.8 |
| 차이 원인 | G2는 인센티브 리뷰 편향 (기프트카드, 뱃지) | 합성은 인센티브 없이 체험 기반 평가 |

G2 리뷰의 높은 평점은 알려진 편향이다. 합성 리뷰가 더 낮은 것은 오히려 솔직한 피드백을 의미한다.

### 6-3. 합성 리뷰 품질

#### Layer 1: 사람이 쓴 것 같은 자연스러운 리뷰

합성 리뷰는 G2 리뷰 구조(likes / dislikes / problems_solved / overall_rating)를 따르며, 1인칭 경험담 톤으로 작성된다.

#### Layer 2: G2보다 구체적인 피드백

| 비교 | G2 실제 리뷰 | 합성 리뷰 |
|------|------------|----------|
| 조건부 로직 불만 | "conditional logic is confusing" | "드롭다운 옵션 입력 후 Enter를 누르면 옵션만 추가되고, 새 질문 블록으로 빠져나오는 방법이 직관적이지 않음. 3회 시도 후 포기." |
| 학습 곡선 | "took a while to figure out" | "블록 메뉴에서 '/' 명령어를 발견하기까지 4스텝 소요. 아이콘만으로는 기능을 유추하기 어려움." |

이 구체성은 실제로 제품을 사용했기 때문에 가능하다. 추측 기반 리뷰에서는 나올 수 없는 수준의 디테일이다.

#### 데이터 2계층 구조

| 계층 | 내용 | 용도 |
|------|------|------|
| Layer 1 (리뷰) | 사람처럼 간결하고 자연스러운 피드백 | 고객에게 전달하는 리포트 |
| Layer 2 (로그) | 매 클릭/감정 변화가 기록된 상세 행동 데이터 | 심층 분석, 재현, 디버깅 |

---

## 7. 한계 및 향후 과제

| 한계 | 상세 | 향후 계획 |
|------|------|----------|
| **단일 세션 한계** | 장기 사용 테마(무료 티어 관대함, 고객 지원 품질 등) 미포착. 1회 사용으로는 습관 형성/이탈 패턴 재현 불가 | Day 1/2/3 다중 세션 시뮬레이션 구현 예정 (Layer 5 Memory) |
| **브라우저 조작 정확도** | ref 오매칭으로 의도와 다른 곳 클릭하는 경우 존재. SPA 전환 시 타이밍 이슈 | Enhanced DOM Tree + 뷰포트 필터링 적용 예정 |
| **페르소나-실행 분리 미완** | 접근성 트리 정보(ref 번호, 컴포넌트명)가 페르소나 독백을 오염시키는 문제 | 페르소나(감정/의도)와 실행기(브라우저 조작)를 서브에이전트로 분리 예정 |
| **1개 제품만 검증** | Tally.so(폼 빌더)에서만 검증. 대시보드형, 다기능 도구 등 다른 제품군 미검증 | 2~3개 제품군으로 확대 실험 예정 |
| **다중 세션 미구현** | Layer 5(Memory Stream + Reflection + Habit Strength)가 설계만 완료 | Day 1/7/30 시뮬레이션으로 장기 사용 패턴 재현 예정 |

---

## 8. 사용된 학술 근거

| 논문/출처 | 연도 | Personica 적용 | 적용 레이어 |
|----------|:---:|---|:---:|
| **PRISM** (Fudan University) | 2025 | Big Five → 행동 파라미터 수학적 매핑, SDE 기반 확률적 감정 진화 | Layer 1, 3 |
| **OCC Model** (Ortony, Clore, Collins) | 1988 | 인지적 감정 평가 모델 — 이벤트 유형별 감정 변화량 결정론적 매핑 | Layer 3 |
| **PAD Model** (Mehrabian) | 1996 | Pleasure-Arousal-Dominance 3차원 연속 감정 상태 표현 | Layer 3 |
| **TAM** (Davis) | 1989 | Perceived Usefulness / Perceived Ease of Use — 기술 수용 모델 | Layer 2 |
| **NNGroup 벤치마크** | 2020s | 사용자 행동 통계 — 읽기 비율 20%, 65세+ 43% 느림, 바운스율 44~45% | 캘리브레이션 |
| **Silicon Sampling** (Argyle et al.) | 2023 | LLM으로 인구통계별 응답 분포 재현 가능성 검증 | 실험 설계 |
| **Generative Agents** (Park et al., Stanford) | 2023 | Memory Stream + Reflection — 다중 세션 기억 아키텍처 | Layer 5 (설계) |
| **Concordia** (Google DeepMind) | 2024 | GM-Player 아키텍처 — 에이전트 유형별 인지 사이클 분화 | 전체 아키텍처 |
| **GenSim** (NAACL) | 2025 | 장기 시뮬레이션 오류 보정 — 페르소나 드리프트 감지/복구 | Layer 5 (설계) |
| **Fogg Behavior Model** | 2009 | B = Motivation x Ability x Prompt — 행동 발생 조건 | Layer 4 (설계) |
| **Information Foraging Theory** (Pirolli & Card) | 1999 | UI 요소의 "정보 냄새" 기반 탐색 행동 모델 | Layer 2 (설계) |
| **Cognitive Load Theory** (Sweller) | 1988 | 인지 부하 3종 (intrinsic, extraneous, germane) — 페이지 복잡도 평가 | Layer 2 |

---

## 부록: 핵심 코드 파일 참조

| 파일 경로 | 역할 |
|----------|------|
| `src/layer1_persona/models.py` | Big Five, PersonalityParameters, PersonaProfile, RoleProfile 정의 |
| `src/layer1_persona/generator.py` | 역할 x 세그먼트 매트릭스 기반 페르소나 배치 생성 |
| `src/layer3_emotion/engine.py` | OCC 분류, PAD delta 계산, SDE noise, 이탈 판정 |
| `src/tools/step_update.py` | 매 행동 후 감정 파이프라인 실행 CLI 도구 |
| `src/prompt_builder.py` | 페르소나 YAML → Claude CLI 시스템 프롬프트 생성 |
| `src/review/generator.py` | MOSAIC 파이프라인 — 체험 데이터 → G2 구조 리뷰 생성 |
| `src/review/benchmark.py` | 합성 vs G2 리뷰 비교 — Jaccard, Pearson, 세그먼트별 분석 |
| `src/analysis/g2_compare.py` | G2 비교 파이프라인 — Jaccard, Kendall Tau, 감정 분포 비교 |
| `src/runner/experiment.py` | 실험 오케스트레이션 — asyncio + Semaphore 병렬 실행 |
| `src/core/types.py` | PADVector, EmotionState, StepLog, SessionLog 등 공유 타입 |
