# ShipCheck Market Sizing: TAM / SAM / SOM

**Date**: 2026-03-16
**Version**: 2.0 (심층 재작성)
**Methodology**: Top-down + Bottom-up 교차 검증, 경쟁사 펀딩/매출 간접 검증
**Sources**: 본문 내 인라인 + 하단 Sources 섹션 (22개 출처)

---

## 1. Market Definition

### 1.1 Problem Space

"출시 전/후 제품이 다양한 사용자에게 **가치를** 전달하는지 검증" — 기존 UX 리서치(인간 기반)와 AI 합성 사용자 테스팅의 교집합이되, 기능 QA가 아닌 **"사용자 경험의 질적 검증"**에 초점.

ShipCheck은 세 가지 시장 교차점에 위치한다:
1. **UX Research Software** — 사용자 리서치 도구
2. **AI-enabled Testing** — AI 기반 소프트웨어 테스팅
3. **Synthetic Research** — AI 합성 사용자/데이터 생성

기존 플레이어와의 핵심 차이: ShipCheck은 **Playwright로 실제 제품을 조작**하는 유일한 접근. 경쟁사 전원(Blok, Aaru, Simile, Synthetic Users, Uxia)은 Figma/설문/인지 시뮬레이션으로 브라우저 자동화를 회피.

### 1.2 Customer Segments

| 세그먼트 | 규모 추정 | ShipCheck 적합도 | 근거 |
|----------|----------|-----------------|------|
| 인디해커 / 솔로 파운더 | Micro SaaS $15.7B (2025)→$59.6B (2030), 39%가 솔로 파운더 [^1] | **비치헤드** | 베타테스터 모집 2주 → 하루 이내, 가격 민감 |
| 시드~시리즈A PM | 연간 ~450개 신규 funded SaaS [^2] | **2차 타겟** | UX 리서치 예산 $5K-$50K/년 |
| Product Hunt 런칭 제품 | 연간 ~5,000-8,000개 [^3] | **채널 겸 타겟** | 출시 전 검증 니즈 극대화 시점 |
| Growth/Product팀 (릴리즈별 UX) | 글로벌 SaaS 42,000+개사 [^2] | 확장 타겟 | 구독 모델, 높은 LTV |
| 엔터프라이즈 UX 리서치팀 | Fortune 500 | 장기 확장 | UserTesting.com 대체/보완 |

### 1.3 Geographic Scope
- **초기**: 글로벌 (영어권 우선, 웹 앱 한정)
- **제한**: 웹 앱만 (모바일/데스크톱/API 제외)
- 영어권이 글로벌 SaaS의 ~60%, 북미가 UX 리서치 소프트웨어 시장의 44% 점유 [^4]

---

## 2. 인접 시장 분석 (Adjacent Markets)

ShipCheck이 교차하는 인접 시장의 규모와 성장률을 개별적으로 정리한다. 이들의 교집합이 TAM의 근거가 된다.

### 2.1 UX Research Software

| 지표 | 수치 | 출처 |
|------|------|------|
| 2025 시장 규모 | $470M~$577M | Fortune Business Insights [^4], Business Research Insights [^5] |
| 2026 전망 | $520M~$630M | Fortune Business Insights [^4] |
| 2032-2034 전망 | $720M~$1,250M | MRFR [^6], Fortune Business Insights [^4] |
| CAGR | 9.1%~12.7% | 복수 리서치 펌 평균 |
| 북미 점유율 | 44% (2025) | Fortune Business Insights [^4] |
| SME 성장률 | 대기업 대비 높은 CAGR | Fortune Business Insights [^4] |

**시사점**: 시장이 연 10%+ 성장 중이며, **SME 세그먼트가 가장 빠르게 성장**. UX 리서치 민주화 트렌드(비연구자의 70%가 자체 리서치 수행 [^7])가 ShipCheck 같은 셀프서브형 도구의 수요를 키움.

### 2.2 Usability Testing Tools

| 지표 | 수치 | 출처 |
|------|------|------|
| 2025 시장 규모 | $1.28B~$1.54B | Business Research Insights [^8], Market.us [^9] |
| 2026 전망 | $1.84B | Business Research Insights [^8] |
| 2033-2034 전망 | $6.55B~$10.41B | Market Research Intellect [^10], Market.us [^9] |
| CAGR | 10.5%~26.3% | 범위가 넓음 — 정의에 따라 차이 |

**시사점**: UX Research Software보다 3배 큰 시장. 기존 도구(UserTesting, Maze, Hotjar)가 인간 기반 또는 행동 분석 중심인 반면, AI 합성 사용자는 아직 이 시장의 극초기 단계.

### 2.3 AI-enabled Testing

| 지표 | 수치 | 출처 |
|------|------|------|
| 2025 시장 규모 | $0.69B~$4.65B | Fortune Business Insights [^11], Grand View Research [^12] |
| 2026 전망 | $1.21B | Fortune Business Insights [^11] |
| 2034-2035 전망 | $3.8B~$10.0B | FMI [^13], Grand View Research [^12] |
| CAGR | 13.5%~18.7% | 복수 출처 |

**시사점**: 대부분 기능/성능/보안 테스팅(QA) 중심. ShipCheck이 속하는 "AI 기반 UX/사용성 테스팅"은 전체의 15-25% 추정. 그러나 CAGR이 높아 빠르게 성장하는 시장.

### 2.4 Synthetic Data Generation

| 지표 | 수치 | 출처 |
|------|------|------|
| 2025 시장 규모 | $486M~$580M | Coherent Market Insights [^14], Kings Research [^15] |
| 2026 전망 | $587M~$770M | Kings Research [^15] |
| 2030-2033 전망 | $2.67B~$7.22B | Next MSC [^16], Kings Research [^15] |
| CAGR | 30.6%~39.4% | 매우 높은 성장률 |

**시사점**: 가장 빠르게 성장하는 인접 시장. "합성 데이터"의 한 갈래인 "합성 사용자"가 UX/마케팅 리서치로 확산 중. Qualtrics가 합성 응답자를 자사 플랫폼에 내장한 것이 시장 신호 [^17].

### 2.5 AI Agents Market

| 지표 | 수치 | 출처 |
|------|------|------|
| 2025 시장 규모 | $7.6B~$8.0B | MarketsandMarkets [^18], Fortune Business Insights [^19] |
| 2026 전망 | $10.9B~$11.8B | Grand View Research [^20], Fortune Business Insights [^19] |
| 2030-2034 전망 | $52.6B~$251.4B | MarketsandMarkets [^18], Fortune Business Insights [^19] |
| CAGR | 40%~50% | 폭발적 성장 |

**시사점**: ShipCheck의 페르소나 에이전트는 기술적으로 AI Agent. 이 시장의 폭발적 성장은 기반 기술(LLM, 브라우저 자동화)의 비용 하락과 성능 향상을 의미 — ShipCheck의 유닛 이코노믹스에 긍정적.

### 2.6 Low-Code/No-Code Development

| 지표 | 수치 | 출처 |
|------|------|------|
| 2025 시장 규모 | $30.1B~$48.9B | Gartner/Kissflow [^21], Fortune Business Insights [^22] |
| 2026 전망 | $44.5B (Gartner) | Kissflow [^21] |
| 2034 전망 | $376.9B | Fortune Business Insights [^22] |
| CAGR | 19%~29% | |

**시사점**: 2026년 기준 새 앱의 75%가 로코드/노코드로 제작 전망 [^21]. 이는 "만드는 건 쉬워졌는데, 이걸 원하는 사람이 있을까?" 질문의 폭증을 의미 — ShipCheck의 핵심 가치 제안과 직결.

### 2.7 인접 시장 요약 도표

```
                        성장률(CAGR)
                            ↑
                  50% │      ● AI Agents
                      │             ● Synthetic Data
                  30% │  ● No-Code
                      │
                  20% │     ● AI Testing
                      │           ● Usability Testing
                  10% │  ● UX Research SW
                      │
                      └──────────────────────────→ 시장 규모 (2026)
                      $0.5B    $2B    $12B    $45B
```

---

## 3. 경쟁사 펀딩/매출 — 시장 규모의 간접 증거

VC 투자와 경쟁사 매출은 시장 존재의 가장 직접적인 증거다.

### 3.1 직접 경쟁사 (Synthetic User/AI UX)

| 회사 | 설립 | 펀딩 | 밸류에이션 | ARR | 접근법 | 출처 |
|------|------|------|-----------|-----|--------|------|
| **Simile** | 2025 (Stanford) | $100M Series A | 비공개 (추정 $500M+) | 비공개 | AI 디지털 트윈, 행동 예측 | TechCrunch, Bloomberg [^23] |
| **Aaru** | 2024.03 | $50M+ Series A | $1B (headline) | <$10M | AI 합성 설문/여론 시뮬레이션 | TechCrunch [^24] |
| **Blok** | — | $7.5M (Seed+Pre-seed) | 비공개 | "mid-single-digit M" 목표 (2025) | Figma + 인지 시뮬레이션 | TechCrunch [^25] |
| **Uxia** | 2025 | €1M Pre-seed | 비공개 | 초기 | Figma/와이어프레임 합성 테스터 | EU-Startups [^26] |
| **Synthetic Users** | — | 비공개 | 비공개 | $99/월 구독 | AI 인터뷰/설문 참가자 | — |
| **SYMAR (OpinioAI)** | — | 비공개 | 비공개 | €99/월~ | 합성 설문/포커스그룹 | — |
| **Ditto** | — | 비공개 | 비공개 | $50K-$75K/년/기업 | 인구통계 기반 합성 페르소나 | Ditto [^27] |
| **Lakmoos** | — | 비공개 | 비공개 | 비공개 | 뉴로심볼릭 AI, 98%+ 유사도 주장 | — |

### 3.2 인접 경쟁사 (UX Research Tools)

| 회사 | 펀딩/매출 | 밸류에이션 | 세그먼트 |
|------|----------|-----------|---------|
| **UserTesting** | 2021 매출 $147M, 2022 $1.3B에 PE 인수 | $1.3B (인수가) | 엔터프라이즈 인간 기반 UX 테스팅 [^28] |
| **Maze** | $60M 총 펀딩 (Series B $40M, Felicis 리드) | 비공개 | 프로덕트 디스커버리 플랫폼 [^29] |
| **Dovetail** | $69M 총 펀딩 (Series A $63M, Accel 리드) | ~$1B (2022) | 정성적 리서치 플랫폼 [^30] |
| **Contentsquare (Hotjar)** | Hotjar 인수, $500M Series E | $2.8B | 행동 분석 (히트맵, 세션 리플레이) [^31] |
| **Qualtrics** | Edge Audiences (합성 응답자) 출시 | $12.5B (Silver Lake 인수) | 설문 + 합성 리서치 통합 [^17] |

### 3.3 펀딩 데이터가 말하는 것

**2024-2026년 "합성 리서치" 카테고리에 최소 $1.5B+ VC 자금 유입** [^27]:
- Simile: $100M
- Aaru: $50M+
- Blok: $7.5M
- Uxia: €1M
- 기타 (Ditto, SYMAR, Lakmoos 등): 비공개

이 규모의 VC 투자는 다음을 시사한다:
1. **시장이 존재한다** — VC가 $1.5B+를 투자할 정도로 시장 기회가 검증됨
2. **아직 승자가 없다** — 다수의 초기 스타트업이 경쟁 중, 카테고리 형성기
3. **가격 포인트가 $50K+/년(엔터프라이즈)부터 $99/월(SMB)까지 분포** — 다양한 세그먼트가 존재
4. **실제 제품 브라우저 조작은 아무도 안 함** — ShipCheck의 차별화 공간이 열려 있음

---

## 4. TAM (Total Addressable Market)

### 4.1 Top-Down Approach

#### 방법: 인접 시장 교집합 추정

ShipCheck이 속하는 시장 = "AI 기반 사용자 시뮬레이션을 통한 UX/제품 검증"

```
UX Research Software ($520M, 2026)
    ∩ AI-enabled Testing ($1.21B, 2026)
    ∩ Synthetic Data/Research ($587M~$770M, 2026)
    = "AI Synthetic UX Validation" 교집합
```

**교집합 추정 근거**:

1. **AI 침투율 기반**: UX Research Software $520M × AI 활용률 24% (2025 기준, NNGroup [^32]) = **$125M**
   - 73%의 리서처가 합성 응답을 1회 이상 사용 [^17], 하지만 주력 도구로 채택한 비율은 아직 ~24%

2. **AI Testing 중 UX 비중**: AI-enabled Testing $1.21B × UX/사용성 비중 ~20% = **$242M**
   - AI 테스팅의 대부분은 기능/성능 QA. UX 비중은 보수적으로 20%

3. **Synthetic Research 시장 직접**: 합성 데이터 시장 $587M 중 "리서치/UX 검증" 비중 ~30% = **$176M**
   - Qualtrics, Simile, Aaru 등이 타겟하는 시장

4. **경쟁사 매출 기반 역추정**: Simile+Aaru+Blok+기타의 합산 ARR 추정 $20M~$50M (2026)
   - 초기 시장에서 선두 3-5개사가 전체의 15-25% 점유 → 전체 시장 $100M~$300M

**교차 검증**: 4가지 접근 모두 **$100M~$300M** 범위에 수렴.

#### Top-Down TAM 결론

> **TAM (Top-Down) = ~$150M~$300M** (2026, AI 기반 합성 사용자 UX 검증 전체)
>
> 2029년 전망: $400M~$700M (CAGR 25-30% 적용)

이 수치에는 엔터프라이즈(Simile, Aaru 타겟)부터 SMB/인디(ShipCheck 타겟)까지 전체가 포함됨.

### 4.2 Bottom-Up Approach

#### 방법: 테스트 가능한 제품 수 × 빈도 × 가격

**Step 1: 연간 테스트 가능 제품 수 산정**

| 채널 | 연간 신규 제품 | 웹 앱 비율 | 테스트 가능 비율 | 테스트 가능 수 | 근거 |
|------|--------------|-----------|----------------|-------------|------|
| Product Hunt | 5,000-8,000 | 65-70% | 75% (로그인 포함) | 2,400-4,200 | docs/20 리서치 [^3] |
| Show HN | ~2,000 | 70-80% | 80% | 1,120-1,280 | 오픈소스/무료 비율 높음 |
| BetaList | ~3,000 | 50-60% | 60% | 900-1,080 | 초기 베타, 대기목록 기반 |
| Indie Hackers / Reddit | ~5,000 | 60-70% | 50% | 1,500-1,750 | WIP/아이디어 단계 많음 |
| 직접 유입 (funded 스타트업) | ~450/년 | 80% | 80% | 288 | 시드~A 스타트업 [^2] |
| **소계 (신규 제품)** | **~15,500-18,450** | — | — | **~6,200-8,600** | |

| 채널 | 기존 SaaS 수 | 반복 테스트 참여율 | 연 테스트 횟수 | 연간 테스트 횟수 |
|------|-------------|------------------|-------------|---------------|
| 기존 SaaS (42,000+ 중) | 42,000+ | 1-3% (초기) | 4회/년 | 1,680-5,040회/년 |

**Step 2: 가격 시나리오**

| 가격 모델 | 1회 가격 | 월 구독 | 연 가치 |
|-----------|---------|--------|--------|
| Pay-per-test (인디해커) | $99-$199 | — | $149 (중간) |
| Monthly Lite | — | $99/월 | $1,188/년 |
| Monthly Pro (릴리즈별) | — | $299/월 | $3,588/년 |
| Enterprise | — | $2,000+/월 | $24,000+/년 |

**Step 3: Bottom-Up 계산**

**시나리오 A: 현재 (2026, 시장 극초기)**
```
신규 제품 테스트: 7,400 제품 × 5% 전환율 × $149/회 × 1.5회/년 = $82.7K
기존 SaaS 반복: 2,000회 × $199/회 = $398K
합계: ~$480K
```
→ 이것은 ShipCheck 혼자의 시장이 아니라, "이 세그먼트에서 모든 플레이어의 합산 수익" 개념.

**시나리오 B: 시장 인지 후 (2028, 카테고리 형성)**
```
신규 제품 테스트: 10,000 제품 × 15% 전환 × $149 × 2회 = $4.5M
기존 SaaS 반복: 5,000회 × $199 = $1.0M
구독 전환: 500개사 × $1,188/년 = $594K
합계: ~$6.1M
```

**시나리오 C: 시장 성숙 (2030, 구독 모델 일반화)**
```
신규 제품: 12,000 × 25% × $149 × 3회 = $13.4M
기존 SaaS 구독: 3,000개사 × $3,588/년 = $10.8M
엔터프라이즈: 200개사 × $24,000/년 = $4.8M
합계: ~$29M
```

#### Bottom-Up TAM 결론

> **Bottom-Up TAM = ~$0.5M (2026, 극초기) → ~$6M (2028) → ~$29M (2030)**
>
> 이것은 "인디/스타트업 웹 앱" 세그먼트만의 Bottom-Up. 엔터프라이즈 포함 시 $50M+ 가능.

### 4.3 Top-Down vs Bottom-Up 격차 분석

| 접근 | 2026 추정 | 2030 추정 | 포함 세그먼트 |
|------|----------|----------|-------------|
| Top-down | $150M~$300M | $400M~$700M | 엔터프라이즈 + SMB + 인디 전체 |
| Bottom-up (인디/스타트업만) | ~$0.5M | ~$29M | 인디해커 + 시드~A 스타트업만 |

**격차 해석**:

1. **Top-down의 $150M~$300M 중 인디/스타트업 비중은 5-15%** → ~$7.5M~$45M
   - 이는 Bottom-up 시나리오 C ($29M)와 정합

2. **나머지 85-95%는 엔터프라이즈** — Simile($100M 펀딩), Aaru($1B 밸류에이션)의 타겟
   - ShipCheck의 장기 확장 방향

3. **Bottom-up이 현재 극히 작은 이유**: 카테고리 자체가 2024-2025년에 막 형성. 대부분의 잠재 고객이 "AI 합성 사용자 테스팅"이라는 개념을 아직 모름.

### 4.4 TAM 최종 결론

> **TAM = ~$150M~$300M** (2026, AI 기반 합성 사용자 UX 검증 전체)
>
> 이 중 ShipCheck이 진입하는 **"프리런치~초기 제품, 인디/스타트업" 세그먼트 = ~$8M~$30M**
>
> 엔터프라이즈 포함 시 TAM의 전체가 타겟 가능 — 이것이 상방 확장 여지

---

## 5. SAM (Serviceable Addressable Market)

### 5.1 제약 조건 상세 분석

TAM에서 SAM으로 축소하는 각 제약의 근거를 명시한다.

| # | 제약 조건 | 축소율 | 상세 근거 |
|---|----------|--------|----------|
| 1 | **웹 앱만** (모바일/데스크톱/API/하드웨어 제외) | ×0.67 | PH 제품의 65-70%가 웹 앱 [^3], Playwright는 웹 전용 |
| 2 | **영어권 우선** | ×0.60 | 글로벌 SaaS의 ~60%가 영어. 미국 12,400개 + UK 1,700개 + 캐나다 1,100개 = 전체 42,000+ 중 ~60% [^2] |
| 3 | **로그인 가능 제품만** | ×0.75 | 고객이 스테이징 URL + 테스트 계정 제공 전제. 인디 SaaS의 75%가 이 방식 가능 [^3]. 노코드 플랫폼(Bubble 등)이 Test/Preview 환경 기본 제공 |
| 4 | **가격 수용** ($49-$299 범위) | ×0.25 | 인디해커의 지불 의향은 낮음. 70%가 $1K MRR 미만 [^1]. $49-$299 범위를 수용하는 비율은 전체 타겟의 25% 추정 (검증 필요) |
| 5 | **시뮬레이션 충실도 인식** | ×0.50 | NNGroup: "방향성은 맞지만 효과 크기를 과소평가" [^32]. 초기 시장에서 이를 수용하는 고객은 절반 수준. 카테고리 성숙 시 상승 예상 |

### 5.2 SAM 계산

**인디/스타트업 세그먼트 (비치헤드)**:
```
TAM 세그먼트: $8M~$30M
× 웹 앱: 0.67
× 영어권: 0.60
× 로그인 가능: 0.75
× 가격 수용: 0.25
× 충실도 수용: 0.50
= $0.3M~$1.1M
```

**중간값: ~$0.5M~$1.0M**

### 5.3 SAM 현실성 검증

경쟁사 매출과 비교하여 SAM의 현실성을 검증한다:

| 비교 기준 | 수치 | ShipCheck SAM 대비 |
|-----------|------|-------------------|
| Aaru ARR | <$10M (2025) [^24] | Aaru는 엔터프라이즈 타겟. ShipCheck SAM이 Aaru의 5-10% 수준은 합리적 |
| Blok 매출 목표 | "mid-single-digit M" (2025) [^25] | Blok은 금융/헬스케어 엔터프라이즈. ShipCheck은 인디 세그먼트로 더 작음 |
| Synthetic Users | $99/월 구독 | 연 $1.2K × 수백 고객 = $0.5M~$1M ARR 추정. 유사 규모 |
| Uxia | €1M 프리시드 | 초기 스타트업, 유사 규모감 |

**결론**: ShipCheck SAM $0.5M~$1.0M은 인디/스타트업 쐐기(wedge) 시장으로서 현실적이다.

### 5.4 SAM 확장 시나리오

| 시나리오 | SAM | 트리거 |
|---------|-----|--------|
| 현재 (인디/스타트업 웹 앱) | $0.5M~$1.0M | — |
| + 시장 교육 효과 (2028) | $2M~$5M | Simile/Aaru의 카테고리 인지도 상승, 충실도 수용률 50%→75% |
| + 엔터프라이즈 확장 (2029+) | $10M~$30M | 릴리즈별 구독 모델, Growth팀 타겟 |
| + 비영어권 확장 | $15M~$50M | 다국어 지원, 아시아/유럽 시장 |

---

## 6. SOM (Serviceable Obtainable Market)

### 6.1 연도별 시나리오 (보수적 / 기본 / 낙관)

#### Year 1 (2027) — Concierge MVP

| 시나리오 | 월 신규 고객 | 평균 가격 | 연간 테스트 횟수 | **연 매출** |
|---------|------------|---------|---------------|-----------|
| **보수적** | 3-5개 | $99 | 1.5회 | **$5K~$9K** |
| **기본** | 5-10개 | $149 | 2회 | **$18K~$36K** |
| **낙관** | 10-20개 | $199 | 2.5회 | **$60K~$120K** |

**근거**:
- Concierge 단계이므로 수동 온보딩, 고객 1:1 지원
- PH/IH 커뮤니티 초기 입소문 + 콘텐츠 마케팅
- 핵심 실험(시뮬레이션 충실도) 성공 전제
- SAM $0.5M 대비 점유율: 보수적 1%, 기본 4-7%, 낙관 12-24%

#### Year 2 (2028) — 셀프서브 전환기

| 시나리오 | 월 신규 고객 | 구독 전환 | 평균 ARPU | **ARR** |
|---------|------------|---------|----------|--------|
| **보수적** | 10-15개 | 20% | $149/회 × 3회 | **$65K~$100K** |
| **기본** | 20-40개 | 30% | $149/회 + $99/월 구독 | **$150K~$300K** |
| **낙관** | 40-60개 | 40% | $199/회 + $199/월 구독 | **$400K~$700K** |

**근거**:
- 셀프서브 전환으로 온보딩 자동화
- 반복 고객 증가 (구독 모델 도입)
- Simile/Aaru의 시장 교육 효과로 카테고리 인지도 상승
- SAM $2M~$5M (교육 효과 후) 대비 점유율: 보수적 2-5%, 기본 6-15%, 낙관 14-35%

#### Year 3 (2029) — 구독 + 엔터프라이즈 확장

| 시나리오 | 총 고객 수 | 구독 비율 | 엔터프라이즈 | **ARR** |
|---------|----------|---------|------------|--------|
| **보수적** | 200-300 | 40% | 0-2개 | **$200K~$400K** |
| **기본** | 400-600 | 50% | 5-10개 | **$500K~$1M** |
| **낙관** | 800-1,200 | 60% | 15-25개 | **$1.5M~$3M** |

**근거**:
- 구독형 전환 완료, MRR 기반 안정 성장
- 엔터프라이즈 파일럿 시작 ($2K+/월)
- SAM $10M~$30M (엔터프라이즈 포함) 대비 점유율: 보수적 1-4%, 기본 3-10%, 낙관 5-30%

### 6.2 SOM 근거 상세

| 벤치마크 | 수치 | 적용 |
|---------|------|------|
| Uxia (동일 규모 초기 스타트업) | €1M 프리시드, 초기 매출 | Year 1 기본 시나리오와 유사 규모 |
| 니치 SaaS 성장률 | MoM 10-20% (초기), 5-10% (성숙) | Year 2 기본: MoM ~12% |
| B2B SaaS 평균 전환율 | 무료→유료 2-5%, 방문→가입 3-7% | 기본 시나리오에 3% 적용 |
| CAC (인디 커뮤니티) | $30-$80 (콘텐츠/커뮤니티 마케팅) | PH/IH/Reddit 채널 |
| 니치 시장 점유율 성장 | 니치(~$5M 시장)에서는 3년 내 20-30% 가능 | Year 3 낙관과 정합 |

### 6.3 SOM 시각화

```
ARR ($)
$3M ─┐
     │                                          ╱ 낙관
     │                                        ╱
$1M ─┤                               ╱──────╱ 기본
     │                        ╱─────╱
$300K┤               ╱───────╱──────── 보수적
     │        ╱─────╱
$36K ┤───────╱
     │
$0   └──────┬──────────┬──────────┬──────
          Y1 (2027)  Y2 (2028)  Y3 (2029)
```

---

## 7. Market Summary Table

| Metric | 2026 (현재) | 2028 (카테고리 형성) | 2030 (시장 성숙) |
|--------|------------|-------------------|-----------------|
| **TAM** (AI 합성 UX 검증 전체) | $150M~$300M | $250M~$500M | $400M~$700M |
| **SAM** (인디/스타트업 웹 앱) | $0.5M~$1.0M | $2M~$5M | $10M~$30M |
| **SOM 보수적** | — | $65K~$100K | $200K~$400K |
| **SOM 기본** | — | $150K~$300K | $500K~$1M |
| **SOM 낙관** | — | $400K~$700K | $1.5M~$3M |

---

## 8. Growth Drivers & Risks

### 8.1 시장 확장 요인

| # | 드라이버 | 영향 | 시기 |
|---|---------|------|------|
| 1 | **AI 합성 사용자 채택 가속** | 2025년 기준 리서처의 73%가 1회+ 사용 [^17], 주력 채택률은 24%→2028년 50%+ 예상 | 2026-2028 |
| 2 | **Simile/Aaru의 카테고리 교육** | $150M+ 투자는 "합성 리서치" 카테고리 인지도를 급속히 높임. ShipCheck이 따로 시장 교육할 필요 감소 | 2026-2027 |
| 3 | **마이크로 SaaS 폭증** | $15.7B→$59.6B (2030), CAGR 30% [^1]. 노코드 확산으로 제품 제작 장벽 하락 → "이걸 원하는 사람이 있을까?" 질문 증가 | 지속 |
| 4 | **노코드/로코드 확산** | 2026년 새 앱의 75%가 로코드/노코드 [^21]. 기술 비전문가가 제품을 만드는 시대 → UX 검증 도구 수요 증가 | 지속 |
| 5 | **UX 리서치 민주화** | 비연구자의 70%가 자체 리서치 수행 [^7], PM/디자이너가 직접 사용할 수 있는 도구 선호 | 2026-2028 |
| 6 | **LLM 비용 하락** | GPT-4o 수준 모델의 API 비용이 연 40-50% 하락 추세. AI Agent 시장 CAGR 46% [^18] → 유닛 이코노믹스 개선 | 지속 |
| 7 | **UserTesting의 User Interviews 인수** | $1.3B 엔터프라이즈 플레이어의 움직임이 SMB 대안 수요를 키움 [^28] | 2026+ |

### 8.2 시장 축소 리스크

| # | 리스크 | 심각도 | 대응 |
|---|--------|--------|------|
| 1 | **LLM 범용화** — ChatGPT/Claude에 "내 제품 써본 척 해줘"로 대체 | **높음** | 차별점: 100-500명 병렬 + 실제 브라우저 조작 + 구조화된 리포트. 범용 LLM은 실제 제품을 사용하지 않음 |
| 2 | **Blok/Simile 하향 확장** — 저가 셀프서브 모델 출시 | **중간** | 경쟁사는 Figma/추론 기반. "실제 제품 사용"이라는 근본적 차이가 방어선 |
| 3 | **시뮬레이션 신뢰도 한계** — NNGroup: "효과 크기와 분산을 과소평가" [^32] | **높음** | 핵심 실험(discovery-plan)으로 검증. "방향성만 맞아도 가치 있다"로 포지셔닝 |
| 4 | **LLM API 비용 상승** — 특정 모델의 가격 인상 | **낮음** | 멀티 모델 전략, 오픈소스 LLM 활용, 하이브리드 시뮬레이션 |
| 5 | **인디해커 지불 의향 부족** — 70%가 $1K MRR 미만 [^1] | **중간** | Free tier + 유료 전환 모델, 또는 비치헤드를 시드~A PM으로 변경 검토 |
| 6 | **카테고리 정의 실패** — "합성 사용자"가 신뢰받지 못하는 기술로 인식 | **중간** | Qualtrics Edge, Simile의 대형 고객 사례가 카테고리 정당성을 확보해줄 것으로 기대 |

---

## 9. Key Assumptions & Confidence Levels

| # | 가정 | 신뢰도 | 출처/근거 | 검증 방법 |
|---|------|--------|----------|----------|
| 1 | AI 합성 사용자 테스팅 채택률이 연 5-10%p 증가 | **높음** | Qualtrics: 73% 리서처가 이미 사용 [^17], NNGroup 연구 시리즈 [^32] | 시장 리포트 추적 |
| 2 | Product Hunt 등 채널에서 연 8,000-12,000개 테스트 가능 제품 존재 | **높음** | docs/20 리서치 [^3]: PH 연 5K-8K, BetaList 3K, Show HN 2K | 플랫폼 데이터 크롤링 |
| 3 | 인디해커가 출시 전 검증에 $49-$299 지불 의향 | **중간** | Micro SaaS 평균 지출 <$1K/월, 하지만 70%가 $1K MRR 미만 [^1] | 인터뷰 WTP 조사 (미수행) |
| 4 | UX Research Software 시장이 CAGR 10%+ 성장 | **높음** | Fortune BI: 11.6%, Business Research: 12.7%, MRFR: 9.1% [^4][^5][^6] | 연간 리포트 갱신 |
| 5 | Blok/Simile가 인디해커 세그먼트로 하향 확장하지 않음 (2-3년) | **중간** | Blok: 금융/헬스케어 엔터프라이즈 집중 [^25], Simile: CVS Health 등 대기업 [^23] | 경쟁사 모니터링 |
| 6 | 시뮬레이션 충실도가 의사결정에 쓸 만한 수준 | **낮음** ⚠️ | NNGroup: "방향성 맞으나 효과 크기 과소평가" [^32], UXAgent: SUS 벤치마크 유사 결과 [^33] | **핵심 실험** (discovery-plan) |
| 7 | 100-500명 병렬 Playwright 실행 비용이 $20-$50/테스트로 유지 가능 | **중간** | Playwright Cloud 가격 하락 추세, 브라우저리스 옵션 확대 | 프로토타입 비용 측정 |
| 8 | $49-$299 가격이 유닛 이코노믹스상 성립 | **중간** | LLM API + Playwright 인프라 비용 추정 필요 | 프로토타입 비용 측정 |
| 9 | 인디 커뮤니티 입소문으로 CAC < $80 | **중간** | B2B SaaS 평균 CAC $200-$500, 인디 커뮤니티는 더 낮음 | 랜딩페이지 전환율 측정 |
| 10 | 글로벌 SaaS 수가 42,000+ → 2029년 50,000+ | **높음** | DemandSage: 42K+ (2025) [^2], 연 400-500개 신규 [^2] | Ascendix/DemandSage 추적 |

### 추정치를 크게 바꿀 수 있는 변수

| 방향 | 변수 | 영향 |
|------|------|------|
| **상방** | 엔터프라이즈 세그먼트 진출 시 | SAM $0.5M→$10M+ (20배). Blok과 다른 각도("실제 제품 사용") |
| **상방** | 릴리즈별 반복 테스트 구독 모델 | LTV 3-5× 증가. $149/회 → $1,188-$3,588/년 |
| **상방** | Simile/Aaru의 대규모 마케팅이 카테고리 전체를 키움 | SAM의 "가격 수용" 축소율 0.25→0.50으로 개선 |
| **하방** | 핵심 실험(시뮬레이션 충실도) 실패 | 전체 TAM 접근 불가 → 피봇 또는 중단 |
| **하방** | LLM API 비용 상승 또는 특정 모델 중단 | 유닛 이코노믹스 파괴 → 가격 인상 필요 |
| **하방** | Qualtrics Edge가 SMB까지 확장 | 카테고리 리더의 하향 확장은 니치 플레이어에게 치명적 |

---

## 10. Methodology Notes

### 10.1 데이터 신뢰도 등급

| 등급 | 설명 | 적용 |
|------|------|------|
| A (높음) | 복수의 시장 리서치 펌이 일관된 수치 제공 | UX Research SW, AI Testing 시장 규모 |
| B (중간) | 1-2개 출처 또는 간접 추정 | 경쟁사 매출, 인디해커 지불 의향 |
| C (낮음) | 가정 기반 추정, 검증 필요 | ShipCheck 전환율, 가격 수용률 |

### 10.2 추정의 한계

1. **"AI 합성 사용자 UX 검증" 시장은 시장 리서치 펌의 공식 카테고리가 아님** — 인접 시장의 교집합으로 간접 추정할 수밖에 없음
2. **경쟁사 매출 데이터가 대부분 비공개** — Aaru의 "<$10M ARR"과 Blok의 "mid-single-digit M 목표"만 공개
3. **인디해커 세그먼트의 WTP(지불 의향)은 미검증** — 가정 #3의 신뢰도가 낮음
4. **시뮬레이션 충실도(가정 #6)가 전체 추정의 전제** — 이것이 실패하면 모든 수치가 무의미

### 10.3 다음 갱신 시 반영할 사항

- [ ] 핵심 실험(시뮬레이션 충실도) 결과 반영
- [ ] 잠재 고객 인터뷰 WTP 데이터 반영
- [ ] Simile/Aaru의 2026 매출 데이터 공개 시 반영
- [ ] Qualtrics Edge Audiences의 SMB 확장 여부 모니터링
- [ ] 프로토타입 비용 측정 후 유닛 이코노믹스 재계산

---

## Sources

### 시장 규모 리포트

[^1]: [Micro SaaS Revenue Analysis 2025](https://www.rockingweb.com.au/micro-saas-revenue-analysis-2025/) — RockingWeb. 1,000 Micro SaaS 분석, 70%가 $1K MRR 미만. Micro SaaS 시장 $15.7B→$59.6B (2030).

[^2]: [Number of SaaS Companies Statistics](https://ascendixtech.com/number-saas-companies-statistics/) — Ascendix. 글로벌 SaaS 42,000+개, 미국 12,400개. 연 400-500개 신규. 또한 [SaaS Statistics 2026](https://www.demandsage.com/saas-statistics/) — DemandSage.

[^3]: docs/20-auth-barrier-research.md — 내부 리서치. Product Hunt 연간 5,000-8,000개, 65-75% 테스트 가능.

### UX Research & Testing

[^4]: [UX Research Software Market Size, 2032](https://www.fortunebusinessinsights.com/user-experience-ux-research-software-market-110632) — Fortune Business Insights. $470M (2025)→$520M (2026)→$1,248M (2034), CAGR 11.6%.

[^5]: [UX Research Software Market Report, 2035](https://www.businessresearchinsights.com/market-reports/user-experience-ux-research-software-market-111513) — Business Research Insights. $577M (2025), CAGR 12.8%.

[^6]: [UX Research Software Market Size Forecast 2035](https://www.marketresearchfuture.com/reports/user-experience-research-software-market-10405) — MRFR. CAGR 9.1%.

[^7]: [The Future of User Research Report 2026](https://maze.co/resources/user-research-report/) — Maze. 비연구자의 70%가 자체 리서치 수행, 88%가 AI 분석을 핵심 트렌드로 선정.

[^8]: [Usability Testing Tools Market Size & Growth](https://www.businessresearchinsights.com/market-reports/usability-testing-tools-market-102397) — Business Research Insights. $1.54B (2025)→$1.84B (2026).

[^9]: [Usability Testing Tools Market Size | CAGR 21.3%](https://market.us/report/usability-testing-tools-market/) — Market.us. $1.51B (2024)→$10.41B (2034).

[^10]: [Usability Testing Tools Market Size And Projections](https://www.marketresearchintellect.com/product/global-usability-testing-tools-market-size-and-forecast/) — Market Research Intellect. $1.28B (2025)→$6.55B (2033), CAGR 26.27%.

### AI Testing & Synthetic Data

[^11]: [AI-enabled Testing Market Size, 2034](https://www.fortunebusinessinsights.com/ai-enabled-testing-market-108825) — Fortune Business Insights. $1.01B (2025)→$1.21B (2026)→$4.64B (2034), CAGR 18.3%.

[^12]: [AI Enabled Testing Market Size & Outlook, 2030](https://www.grandviewresearch.com/horizon/outlook/ai-enabled-testing-market-size/global) — Grand View Research. $4.65B (2025)→$9.98B (2034), CAGR 13.5%.

[^13]: [AI-Enabled Testing Tools Market Size & Forecast 2025-2035](https://www.futuremarketinsights.com/reports/ai-enabled-testing-tools-market) — FMI. $687M (2025)→$3,826M (2035), CAGR 18.7%.

[^14]: [Synthetic Data Market Size & Opportunities, 2025-2032](https://www.coherentmarketinsights.com/industry-reports/synthetic-data-market) — Coherent Market Insights. $486M (2025)→$3,149M (2032), CAGR 30.6%.

[^15]: [Synthetic Data Generation Market to Reach $7.22B by 2033](https://www.kingsresearch.com/report/synthetic-data-generation-market-3032) — Kings Research. $580M (2025)→$7,220M (2033), CAGR 37.65%.

[^16]: [Synthetic Data Market Share, Size and Forecast 2024-2030](https://www.nextmsc.com/report/synthetic-data-market) — Next MSC. $510M (2025)→$2,670M (2030), CAGR 39.4%.

### 경쟁사 & 합성 리서치 카테고리

[^17]: [AI to Drive Massive Changes to Market Research in 2025](https://www.qualtrics.com/articles/news/ai-to-drive-massive-changes-to-market-research-in-2025-qualtrics-report-says/) — Qualtrics. 73% 리서처가 합성 응답 사용, 87% 만족도, 71%가 3년 내 주류화 예상.

[^18]: [AI Agents Market Size, Share & Trends](https://www.marketsandmarkets.com/Market-Reports/ai-agents-market-15761548.html) — MarketsandMarkets. $7.84B (2025)→$52.62B (2030), CAGR 46.3%.

[^19]: [AI Agents Market Share, Size, Trends, Forecast, 2034](https://www.fortunebusinessinsights.com/ai-agents-market-111574) — Fortune Business Insights. $8.03B (2025)→$11.78B (2026)→$251.38B (2034).

[^20]: [AI Agents Market Size And Share, 2033](https://www.grandviewresearch.com/industry-analysis/ai-agents-market-report) — Grand View Research. $7.63B (2025)→$10.91B (2026).

[^21]: [Gartner Forecasts for the Low-Code Development Market (2026)](https://kissflow.com/low-code/gartner-forecasts-on-low-code-development-market/) — Kissflow/Gartner. 2026년 $30B+, 새 앱의 75%가 로코드/노코드.

[^22]: [Low Code Development Platform Market Size, 2034](https://www.fortunebusinessinsights.com/low-code-development-platform-market-102972) — Fortune Business Insights. $48.91B (2026)→$376.92B (2034), CAGR 29.1%.

[^23]: [$100M for Stanford spinout Simile](https://techfundingnews.com/100m-for-stanford-spinout-simile-ai-that-simulates-human-decisions/) — TechFundingNews, Bloomberg. Simile $100M Series A, Index Ventures 리드, Fei-Fei Li/Andrej Karpathy 참여. 또한 [Bloomberg 보도](https://www.bloomberg.com/news/articles/2026-02-12/ai-startup-nabs-100-million-to-help-firms-predict-human-behavior).

[^24]: [AI synthetic research startup Aaru raised a Series A at a $1B 'headline' valuation](https://techcrunch.com/2025/12/05/ai-synthetic-research-startup-aaru-raised-a-series-a-at-a-1b-headline-valuation/) — TechCrunch. Aaru $50M+ Series A, Redpoint 리드, ARR <$10M.

[^25]: [Blok is using AI personas to simulate real-world app usage](https://techcrunch.com/2025/07/09/blok-is-using-ai-persons-to-simulate-real-world-app-usage/) — TechCrunch. Blok $7.5M, MaC Venture Capital 리드, 금융/헬스케어 집중.

[^26]: [Spanish startup Uxia lands €1M](https://www.eu-startups.com/2025/11/spanish-startup-uxia-lands-e1-million-to-develop-synthetic-user-technology-for-product-teams/) — EU-Startups. Uxia €1M Pre-seed, Abac Nest 리드.

[^27]: [Synthetic Research Platforms: The 2026 Market Map](https://askditto.io/news/synthetic-research-platforms-the-2026-market-map) — Ditto. "합성 리서치"에 $1.5B+ VC 유입. Ditto 가격 $50K-$75K/년.

### 학술/벤치마크

[^28]: [UserTesting Revenue](https://companiesmarketcap.com/usertesting/revenue/) — CompaniesMarketCap. 2021 $147M. [UserTesting to be acquired for $1.3B](https://siliconangle.com/2022/10/27/usertesting-acquired-1-3b-private-equity-firms/) — SiliconANGLE. 2026.01 User Interviews 인수.

[^29]: [Maze raises $40M to facilitate software product research](https://techcrunch.com/2022/06/09/2331513/) — TechCrunch. Maze $60M 총 펀딩, Felicis 리드 Series B.

[^30]: [Dovetail valuation soars to just under $1B following $87M Series A](https://www.businessnewsaustralia.com/articles/dovetail-valuation-soars-to-just-under--1-billion-following--87-million-series-a.html) — BusinessNewsAustralia. Dovetail $69M, ~$1B 밸류에이션. [Dovetail Revenue](https://getlatka.com/companies/dovetail) — GetLatka. $4.9M revenue (2024).

[^31]: [Contentsquare acquires Hotjar](https://contentsquare.com/press/contentsquare-acquires-hotjar/) — Contentsquare. Hotjar 인수, $500M Series E, $2.8B 밸류에이션.

[^32]: [Evaluating AI-Simulated Behavior: Insights from Three Studies](https://www.nngroup.com/articles/ai-simulations-studies/) — NNGroup. 합성 사용자의 분산이 인간보다 낮음, 방향성은 일치하나 효과 크기 과소평가. 또한 [Synthetic Users: If, When, and How](https://www.nngroup.com/articles/synthetic-users/).

[^33]: [UXAgent: An LLM-Agent-Based Usability Testing Framework](https://arxiv.org/abs/2502.12561) — Amazon Science / CHI '25. LLM 에이전트 기반 UX 테스팅, 브라우저 커넥터 모듈, 대규모 페르소나 생성.
