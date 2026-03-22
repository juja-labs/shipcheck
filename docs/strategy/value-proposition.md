# Value Proposition: Personica

**Date**: 2026-03-17
**Version**: v2.0 — Wave 0 심층 재작성 반영 (커뮤니티 인용, 경쟁사 업데이트, 비용 기반 가격 정당화)
**Input**: user-research.md, lean-canvas.md, competitive-analysis.md, ../market-sizeing/market-sizing-yechangpae-appendix-software-first.md, market-scan.md

---

## Segment 1: 솔로 빌더 (민수) — 비치헤드

### 1. Who
혼자 또는 2-3명으로 SaaS/웹앱을 만드는 인디해커. Product Hunt 런칭을 앞두고 있거나, 방금 출시했는데 반응이 기대 이하. 개발은 잘 하지만 UX 리서치 경험/예산 없음. 주변 개발자 피드백만으로 의사결정.

### 2. Why
"런칭 전에, 내 타겟이 아닌 다양한 사용자가 내 제품을 썼을 때 어디서 막히고 뭘 느끼는지 알고 싶다. 개발자 친구 3명한테 보여줬더니 다 '좋다'고 하는데, 비기술직 40대가 써도 괜찮을까? Product Hunt Day 1이 골든타임인데 블라인드 스팟을 안고 가긴 싫다."

### 3. What Before (현재의 고통)

**지인 피드백 편향은 보편적 고통이다.** 커뮤니티에서 반복적으로 등장하는 패턴:

> *"I launched a habit tracker after three months of work on Product Hunt, Hacker News, and told people on LinkedIn about it. A few people signed up, but nobody was using it."*
> — Indie Hackers 포럼, 반복적으로 등장하는 패턴

> *"Build for weeks, hit 'launch,' post the tweet — then nothing. No users, no feedback, just crickets."*
> — DEV Community, 인디 파운더 실패 분석

> *"400 signups from Product Hunt, 1 paying customer. What 4 days taught me about launch vs traction."*
> — Indie Hackers 게시글 제목 그 자체

이 고통의 현재 대안과 한계:

- **지인 테스트 3-5명**: 다 개발자, 다 "좋다"고 함. 솔직한 피드백 없음. Indie Hackers: 80명에게 개인적으로 공유 후 **겨우 1명 가입** — *"Most people, even those close to you, don't care"*
- **커뮤니티 피드백**: "멋져요 :+1:" 문화. 구조화된 개선점 없음
- **ChatGPT "리뷰해줘"**: 제품을 써보지 않아서 "버튼이 직관적이에요" 수준의 일반론
- **안 함**: 가장 흔한 선택. 출시하고 데이터 보면서 개선. 하지만 첫인상에 실패하면 이탈 후 재방문 없음
- **UserTesting.com**: $49/명 x 5명 = $245 최소. 실제 연 계약 기준 ~$46K. 인구통계 제어 어렵고, 5명으로는 패턴 안 보임
- **베타 테스터 모집**: 솔로 파운더가 Reddit에서 테스터 모집하려면 커뮤니티 신뢰도 쌓는 데만 몇 주 소요. IH: *"Recruiting your first beta testers is hard"*

### 4. How (Personica의 해결)
- **실제 제품을 200명의 AI 페르소나가 직접 사용**: Playwright로 실제 DOM 조작 — 클릭, 스크롤, 입력, 탐색. ChatGPT처럼 "상상"이 아니라 실제로 써본 경험 기반
- **다양한 배경의 페르소나 자동 생성**: 20대 개발자, 40대 비기술직 PM, 60대 은퇴자까지. Big Five 성격 모델 + SDE 확률적 감정 모델 기반으로 행동이 실제로 다름 — 동일 자극에도 페르소나별 분산 생성
- **감정 궤적 리포트**: "온보딩 3단계에서 40대 비기술직 페르소나의 60%가 혼란 -> 이탈" — 이 수준의 구체적 인사이트
- **스테이징 URL + 테스트 계정만 제공하면 끝**: 복잡한 세팅 불필요. 기존 사용자 데이터(Amplitude/Mixpanel)도 불필요 — MVP/Pre-launch에서 바로 사용 가능

### 5. What After (달라지는 것)
- Product Hunt 런칭 전에 "40대 비기술직이 온보딩 3단계에서 막힌다"를 발견 -> 툴팁 추가 -> Day 1 이탈률 30% 감소
- "지인 테스트 3명"이 아닌 "200명 AI 테스트"로 의사결정 -> 자신감 있는 런칭
- 세그먼트별 반응 차이를 한눈에 파악 -> "누구를 위한 제품인가"가 명확해짐
- 런칭 후에도 릴리즈마다 반복 -> 지속적 UX 품질 관리

### 6. Alternatives (대안과 비교)

| 대안 | 한계 | Personica가 나은 이유 |
|------|------|---------------------|
| 지인 테스트 | 3-5명, 편향, 솔직하지 않음 | 200명, 다양한 배경, 페르소나 성격대로 솔직 반응 |
| ChatGPT "리뷰해줘" | 제품을 안 써봄. 일반론만 | 실제로 클릭하고 스크롤한 경험 기반 구체적 피드백 |
| UserTesting.com | $245+ / 5명 (연 계약 ~$46K). 인디해커에게 비현실적 | $49-99 / 200명. 세그먼트 자동 분화 |
| Uxia | Figma/프로토타입 기반, 실제 제품 미사용 | 실제 프로덕션 제품을 실제로 사용 |
| Synthetic Users | 제품을 써보지 않고 인터뷰 — "써본 후 말하기"가 아닌 "써본 척 말하기" | 실제 브라우저 조작 후 경험 기반 피드백 |
| Artificial Societies | $40/월이지만 PR/마케팅 전용. 제품 UX 체험 아님 | 실제 제품 사용 경험 기반 UX 인사이트 |
| 안 함 (출시하고 봄) | 첫인상 실패 -> 재방문 없음 | 출시 전 블라인드 스팟 제거 |

---

## Segment 2: 리서치-없는-PM (서연) — 2차 타겟

### 1. Who
시드~시리즈A 스타트업 PM. 팀 5-15명, UX 리서처 없음. Figma + Hotjar는 쓰지만 "왜 이탈하는가"에 대한 정성적 인사이트 부족. 분기 1회 ad-hoc 리서치를 하고 싶지만 시간/예산 부족.

### 2. Why
"온보딩을 개편하는데, 현재 온보딩에서 어떤 유형의 사용자가 어디서 왜 이탈하는지 구조적으로 파악하고 싶다. Hotjar 히트맵만으로는 '어디서'는 보이는데 '왜'는 모르겠다. 대표에게 데이터로 보여줘야 하는데 유저 인터뷰 5명으론 설득력 없다."

### 3. What Before

**UX 리서치의 민주화가 가속 중이나, 실행 인프라는 미비:**

> *"Hotjar answers the question every PM obsesses over: why did users bounce? But... the qualitative research layer is thin — teams that need to understand motivations, not just clicks, end up managing separate tools anyway."*
> — Hotjar vs FullStory 비교 리뷰들의 반복 패턴

> *"More researchers are struggling with the time it takes to find participants (61% vs. 45% previous year) and the cost of recruitment (32% vs. 25%)."*
> — User Interviews, State of User Research Report 2024

> *"42% of product managers already conduct user research — with companies citing business growth as a key objective fueling that research demand."*
> — Maze, Future of User Research Report 2025

**구조적 문제**: UX 리서처:개발자 비율 중앙값 = 1:100. 시드~시리즈A 스타트업의 71%가 디자이너:개발자 비율 1:20 미만 (NNGroup). PM이 8개 full-time job을 동시에 할 수 없다.

현재 대안과 한계:

- **Hotjar/FullStory**: 히트맵으로 "어디서 이탈"은 보이지만 "왜"는 모름
- **유저 인터뷰 5명**: 참가자 모집 2-3주, 비용 $500+. 다 얼리어답터. 일반 사용자 관점 부족. 대표 설득에 불충분
- **UserTesting.com**: 연 계약 ~$46K 기준이라 분기 1회 용도로 비효율
- **Blok**: Amplitude 데이터 연동 필수 -> 새 기능에는 데이터가 아직 없음. Demo 예약 기반 엔터프라이즈 세일즈 -> 셀프서브 불가

### 4. How
- **200명 AI 페르소나가 현재 제품을 실제로 사용**: 스테이징 환경에서 실행 -> 프로덕션 영향 없음
- **세그먼트별 교차 분석**: "비기술직 사용자의 60%가 온보딩 3단계에서 이탈, 기술직은 10%" — Hotjar가 못 주는 "왜"를 제공
- **감정 궤적 타임라인**: 각 페르소나가 언제 만족하고 언제 좌절했는지 시간순 시각화
- **페르소나 인터뷰**: 특정 페르소나에게 "왜 3단계에서 뒤로 갔어요?" 후속 질문 가능 — 실제로 써본 경험이 있기에 Synthetic Users의 "써보지 않고 인터뷰"와 질적으로 다름

### 5. What After
- "200명 AI 분석 결과, 비기술직 사용자의 60%가 온보딩 3단계에서 이탈" -> 대표에게 데이터 기반 제안 가능
- 유저 인터뷰 전에 "어디를 깊게 파야 하는지" 방향 설정 -> 리서치 효율 2x 향상
- 릴리즈마다 반복 -> "이번 개편으로 이탈률 60% -> 25% 개선" 추적 가능

### 6. Alternatives

| 대안 | 한계 | Personica가 나은 이유 |
|------|------|---------------------|
| Hotjar/FullStory | "어디서"는 보이지만 "왜"는 모름 | "왜"에 대한 정성적 인사이트 + 세그먼트별 분석 |
| 유저 인터뷰 5명 | 2주 소요, 편향, 대표 설득 불충분 | 200명 x 하루, 세그먼트별 정량 데이터 |
| Blok | Amplitude 데이터 필수, 새 기능엔 불가. 셀프서브 불가 | 데이터 없이도 동작, 실제 제품 사용. URL만으로 시작 |
| Synthetic Users | 제품을 안 써보고 인터뷰 | 실제 체험 후 인터뷰 — 경험 기반 구체성 |
| 안 함 | "감으로 결정" -> 팀 신뢰도 하락 | 데이터 기반 의사결정 문화 구축 |

---

## Segment 3: 데이터-드리븐 CPO (준혁) — 확장 타겟

### 1. Who
시리즈A+ 스타트업 CPO. 팀 15명+, Amplitude 붙어있고 MAU 5,000+. A/B 테스트는 하지만 세팅 2주 + 결과 4-6주. 출시 전 세그먼트별 예측 니즈.

### 2. Why
"새 기능 출시 전에, 다양한 사용자 세그먼트가 이 기능을 어떻게 경험할지 미리 시뮬레이션하고 싶다. A/B 테스트는 출시 후에나 가능하고 결과까지 한 달인데, 출시 전에 방향성이라도 알고 싶다."

### 3. What Before

**합성 사용자 리서치 시장은 형성 초기이며, VC가 검증 중:**

> *"Teams that have embraced a democratized research culture are 2x more likely to report that user research influences strategic decisions."*
> — Maze, Future of User Research Report 2026

> *"Blok officially launched on July 8, 2025, and announced the completion of a $7.5M seed funding round led by MaC Venture Capital."*
> — 합성 유저 리서치 시장에 VC 자금이 유입되고 있는 신호

> *"Digital twins work fairly well to replicate both individual-level and group-level human responses. However, synthetic personas are about gaining initial direction quickly, not replacing deep, human-centered research downstream."*
> — NNGroup, AI Simulations Studies

현재 대안과 한계:

- **A/B 테스트**: 세팅 2주 + 결과 4-6주. 출시 전엔 불가
- **Blok**: Figma + Amplitude 기반. 디자인 변형 비교는 되지만 "실제 사용 경험"은 아님. 기존 데이터 필수 -> 새 기능에 못 씀
- **Simile ($100M Series A)**: 디지털 트윈 + 행동 예측이지만 대기업 타겟. 인디/스타트업 접근 불가
- **PM 직감**: "이거 좋을 것 같아"로 결정 -> 출시 후 "왜 안 되지?" -> 3개월 뒤 롤백

### 4. How
- **출시 전 시뮬레이션**: 스테이징 환경에서 500명 AI 페르소나가 새 기능 사용
- **A/B 테스트 사전 시뮬레이션**: 현재 버전 vs 새 버전을 AI 페르소나로 먼저 비교
- **세그먼트별 예측**: "40대 비기술 사용자의 만족도가 20대 대비 40% 낮음. 온보딩 툴팁 추가 시 개선 예상"
- **반복 사용 시뮬레이션 (Day 1/7/30)**: Memory Stream + Persona Drift Monitor로 습관 형성/리텐션 예측 — 어떤 경쟁사도 미제공

### 5. What After
- A/B 테스트 전에 "방향이 맞는가"를 사전 확인 -> 실패 A/B 테스트 50% 감소
- 세그먼트별 영향 예측 -> 기능 출시 의사결정 가속 (4-6주 -> 하루)
- 비기술직 경영진에게 "정성적+정량적" 근거 제공

### 6. Alternatives

| 대안 | 한계 | Personica가 나은 이유 |
|------|------|---------------------|
| A/B 테스트 | 출시 후에만 가능, 4-6주 | 출시 전, 하루 내 결과 |
| Blok | Figma 기반, 실제 사용 아님. Amplitude 데이터 필수 | 실제 제품, 데이터 불필요 |
| Simile | $100M 펀딩이지만 대기업 전용. 접근 불가 | 셀프서브, $199/회로 접근 가능 |
| PM 직감 | 편향, 비구조적 | 200-500명 데이터 기반 |

---

## Value Proposition Statements

### Segment 1 (솔로 빌더)

> **For 인디해커/솔로 빌더** who need 출시 전 다양한 사용자 반응 확인,
> **Personica** is a 합성 페르소나 시뮬레이션 플랫폼 that **200명의 AI 페르소나가 제품 체험, 서베이, 인터뷰 등 다양한 방식으로 세그먼트별 피드백을 제공한다**.
> Unlike 지인 테스트나 ChatGPT, **5-Layer 감정/인지/의사결정 엔진이 페르소나 리얼리티를 보장하여 구체적 인사이트를 제공한다**.

### Segment 2 (리서치-없는-PM)

> **For UX 리서처 없는 스타트업 PM** who need 구조화된 사용성 인사이트,
> **Personica** is a 합성 페르소나 시뮬레이션 플랫폼 that **200명 AI 페르소나의 세그먼트별 이탈 원인과 감정 궤적을 제품 체험·서베이·A/B 테스트 등으로 제공한다**.
> Unlike Hotjar/FullStory, **"어디서"가 아니라 "왜" 이탈하는지를 알려준다**.

### Segment 3 (데이터-드리븐 CPO)

> **For 출시 전 세그먼트 영향을 예측하고 싶은 CPO** who need A/B 테스트보다 빠른 사전 검증,
> **Personica** is a 합성 페르소나 시뮬레이션 플랫폼 that **500명 AI 페르소나로 제품 체험, A/B 사전 시뮬레이션, 퍼널 분석 등을 통해 출시 전 세그먼트별 반응을 예측한다**.
> Unlike Blok, **기존 데이터 없이 실제 제품에서 바로 시뮬레이션 가능하다**.

---

## Reusable Messaging

### Marketing (랜딩페이지, 소셜)
- **헤드라인**: "200명의 합성 페르소나가 당신 제품을 체험하고 솔직히 말해준다"
- **서브**: "Product Hunt 런칭 전, 다양한 사용자가 어디서 막히고 뭘 느끼는지 — 제품 체험, 서베이, A/B 테스트, 퍼널 분석까지"
- **CTA**: "내 제품 Personica 분석 받기"
- **ChatGPT 차별화**: "ChatGPT는 URL만 읽습니다. Personica는 5-Layer 감정/인지/의사결정 엔진으로 사람처럼 느끼고 판단합니다 — 제품 체험, 서베이, 리서치 어디서든."

### Sales (PM/CPO 대상)
- "Hotjar는 '어디서 이탈'을 보여줍니다. Personica는 '왜 이탈'을 알려줍니다."
- "유저 인터뷰 5명 x 2주 대신, AI 200명 x 하루. 방향은 같고 속도는 다릅니다."
- "Amplitude 데이터 없이도 동작합니다. URL만 있으면 됩니다."

### Onboarding (가입 후)
- "스테이징 URL과 테스트 계정만 준비하세요. 나머지는 Personica가 합니다."
- "어떤 사용자 유형을 테스트하고 싶으세요? 타겟을 알려주시면 200명의 다양한 AI 페르소나를 생성합니다."

### Consideration 단계 — AI 신뢰 장벽 돌파 메시지

이탈 퍼널 분석에서 핵심 병목은 **Consideration (40-50% 이탈)** 단계의 "AI 피드백을 진짜 신뢰할 수 있나?" 장벽이다. 이를 넘기 위한 전용 메시지:

- **투명성 우선**: "Personica는 인간 리서치를 대체하지 않습니다. 인간 리서치 전에 '어디를 깊게 파야 하는지' 방향을 잡아줍니다."
- **구체적 증거**: "실제 공개 제품에 대한 샘플 리포트를 확인하세요. [링크]" — 추상적 약속이 아닌 실제 결과물로 신뢰 구축
- **학술 근거**: "NNGroup 연구: AI 합성 사용자는 '방향성은 맞지만 효과 크기를 과소평가'. 우리는 이 한계를 투명히 고지합니다."
- **비교 증명**: "같은 제품에 ChatGPT vs Personica를 돌린 결과를 비교해보세요." — side-by-side 데모
- **한계 선제 고지**: "100% 정확하지 않습니다. 하지만 지인 3명 피드백보다 구조적이고, ChatGPT 일반론보다 구체적입니다."

### Onboarding 세팅 마찰 완화 메시지

두 번째 병목인 **Onboarding (25-35% 이탈)** 단계의 세팅 마찰을 완화하기 위한 메시지:

- "스테이징 URL이 없으세요? Production URL도 괜찮아요. AI가 읽기 전용으로 제품을 탐색합니다."
- "Bubble/Softr를 쓰시나요? Test/Preview 환경 기본 제공 — 별도 세팅 필요 없습니다." [가이드 링크]
- "처음이시라면 저희가 직접 세팅을 도와드립니다. [Concierge 예약]"
- "예상 소요: 세팅 5-10분, 시뮬레이션 1-3시간, 리포트 자동 발송"

---

## "ChatGPT와 뭐가 달라?" — 최대 대체재에 대한 반론

### 왜 이 질문이 중요한가

Porter Five Forces 분석에서 대체재 위협 강도: **4/5 (High)**. ChatGPT/Claude는 무료이고, "이런 사용자인 척 하고 내 제품 리뷰해줘"가 점점 나아지고 있다. Computer Use/CUA로 스크린샷 기반 분석도 가능해지는 중. 이 질문에 명확히 답하지 못하면 Personica의 존재 이유가 사라진다.

### 구조적 차이

| 차원 | ChatGPT / Claude | Personica |
|------|------------------|-----------|
| **제품 사용** | URL만 읽거나 스크린샷 정적 분석. 실제로 클릭/스크롤/입력/탐색하지 않음 | Playwright로 실제 DOM 조작 — 클릭, 스크롤, 입력, 호버, 페이지 전환까지 실제 체험 |
| **페르소나 다양성** | 프롬프트에 "40대 비기술직인 척 해줘" -> 1명, LLM 동질화로 다양성 제한 | 200-500명 페르소나, Big Five 수학적 매핑 + SDE 확률적 감정 모델로 구조적 분화 보장 |
| **감정/인지** | "사용자가 불편할 수 있어요" 수준의 추측 | OCC 22개 감정 카테고리 + PAD 3차원 연속 상태 + 인지 부하 추적. "3단계에서 7초간 멍하니 있다가 뒤로가기" 수준의 구체성 |
| **세그먼트 분석** | 1명의 답변. 세그먼트 비교 불가 | 세그먼트별(기술자/비기술자/시니어) 교차 분석. "비기술직 60% 이탈, 기술직 10%" |
| **행동 데이터** | 없음. 텍스트 기반 의견만 | 클릭 위치, 체류 시간, 스크롤 깊이, 망설임, confusion/rage click 마이크로 행동 로깅 |
| **반복 사용** | 불가 | Day 1/7/30 반복 시뮬레이션으로 습관 형성/리텐션 예측 |
| **비용** | $0-20/월 | $49-199/회 |

### 핵심 반론 (고객 커뮤니케이션용)

**"ChatGPT한테 물어보면 되지 않아?"에 대한 한 줄 답변:**

> "ChatGPT는 당신의 제품을 써본 적이 없습니다. Personica의 200명은 실제로 클릭하고 스크롤하고 멍하니 있다가 뒤로 갔습니다."

**상세 반론:**

1. **"상상"과 "경험"의 차이**: ChatGPT에게 "맥주 맛이 어때?"라고 물으면 일반론을 말해줍니다. 실제로 마셔본 사람은 "이 맥주는 첫 모금에 시트러스가 강한데 뒷맛이 쓰다"라고 합니다. Personica는 제품을 "실제로 마셔본" AI입니다.

2. **1명 vs 200명**: ChatGPT는 1명의 관점입니다. 당신이 프롬프트를 바꿔도 LLM의 "평균적 인간" 응답 경향에서 벗어나기 어렵습니다. Personica의 200명은 SDE(확률미분방정식) 기반으로 같은 자극에도 수학적으로 다른 반응을 생성합니다.

3. **의견 vs 데이터**: ChatGPT는 "이 버튼이 직관적이에요"라는 의견을 줍니다. Personica는 "200명 중 47명이 이 버튼을 5초 이상 찾지 못했고, 그중 23명이 뒤로 갔다"는 데이터를 줍니다.

### Computer Use / CUA에 대한 추가 반론

Claude Computer Use (72.5% 인간 수준), OpenAI Operator/CUA가 발전하면서 "AI가 브라우저를 조작한다"는 것 자체는 더 이상 차별점이 아닐 수 있다.

Personica의 진짜 차별점은 **브라우저 조작 자체가 아니라, 5-Layer 엔진의 "페르소나 리얼리티" — 구조화된 감정/인지/의사결정 시뮬레이션**이다. Playwright를 통한 제품 체험은 여러 인터페이스 중 하나일 뿐이며, 서베이, A/B 테스트, 전문가 리뷰, 광고/마케팅 리서치, 퍼널 분석 등 다양한 모드에서도 동일한 페르소나 리얼리티가 적용된다:

- Computer Use는 범용 "작업 수행" 도구. "이 폼 작성해줘"를 잘 한다.
- Personica는 "이 폼을 작성하면서 65세 은퇴자가 어떤 감정을 느끼고, 어디서 인지 부하가 치솟으며, 어느 지점에서 포기 결정을 내리는가"를 시뮬레이션한다. 이 페르소나 리얼리티는 제품 체험뿐 아니라 서베이, A/B 테스트, 전문가 리뷰, 광고/마케팅 리서치 등 모든 모드에서 동일하게 작동한다.
- 범용 에이전트로는 200명의 구조적으로 분화된 페르소나를 병렬 실행하고 세그먼트별 교차 분석을 자동 생성할 수 없다.

---

## Simile/Aaru 대비 포지셔닝: 적이 아닌 카테고리 교육자

### 시장 현황

"AI 합성 사용자" 카테고리에 2024-2026년 최소 **$1.5B+ VC 자금**이 유입되었다:

| 회사 | 펀딩 | 밸류에이션 | 타겟 | 접근법 |
|------|------|-----------|------|--------|
| **Simile** | $100M Series A | $500M+ (추정) | 대기업 (CVS Health 등) | AI 디지털 트윈, 행동 예측 |
| **Aaru** | >$50M Series A | $1B (headline) | 대기업 (Accenture, EY, IPG) | 멀티 에이전트 설문/여론 시뮬레이션 |
| **Blok** | $7.5M Seed | 비공개 | 금융/헬스케어 PM, Growth팀 | Figma + Amplitude 데이터 기반 예측 |
| **Artificial Societies** | $5.35M | 비공개 | F100 마케팅/PR | 2.5M+ 페르소나 네트워크 시뮬레이션 |
| **Uxia** | EUR1M Pre-seed | 비공개 | PM, 디자이너 | Figma/프로토타입 합성 테스터 |
| **Personica** | $0 | — | 인디해커, 초기 스타트업 | **실제 제품 Playwright 조작 + 5-Layer 감정/인지** |

### 왜 "적"이 아닌 "카테고리 교육자"인가

1. **시장 세그먼트가 다르다**: Simile/Aaru는 대기업 대상 엔터프라이즈 세일즈. Personica는 인디해커 대상 셀프서브. 직접 경쟁하는 고객이 없다.

2. **JTBD가 다르다**: Simile은 "인간 행동 예측(디지털 트윈)", Aaru는 "설문/여론 시뮬레이션(포커스그룹 대체)". Personica는 "실제 제품 사용 경험 시뮬레이션(UX 체험 검증)". 풀고 있는 문제가 다르다.

3. **기술 접근이 다르다**: Simile/Aaru/Blok 모두 감정/인지/의사결정을 구조적으로 시뮬레이션하지 않는다. Personica의 5-Layer 엔진은 페르소나 리얼리티(감정·인지·의사결정 시뮬레이션)를 핵심 해자로 가지며, 이 엔진은 제품 체험(Playwright), 서베이, A/B 테스트, 전문가 리뷰, 광고/마케팅 리서치, 퍼널 분석 등 다양한 인터페이스에서 작동한다.

4. **$1.5B+가 카테고리를 교육해준다**: Simile의 $100M, Aaru의 $50M+가 "AI 합성 사용자"라는 카테고리를 빠르게 교육하고 있다. 48%의 UX 리서처가 합성 사용자를 "2026년 임팩트 있는 트렌드"로 선정 (Lyssna). Aaru의 EY 파트너십으로 90% 상관관계 결과가 공개되면서 시장 신뢰도가 상승. **Personica가 직접 시장을 교육할 필요가 줄어든다.**

5. **Personica는 교육된 시장 위에 올라탄다**: Aaru/Simile가 수억 달러를 들여 증명한 "합성 리서치가 된다"라는 전제 위에, Personica는 "그런데 실제로 써보는 건 우리뿐이다"를 얹는다.

### 포지셔닝 메시지

- **내부 전략**: "Simile/Aaru가 카테고리를 만들어준다. 우리는 그 카테고리 안에서 '5-Layer 페르소나 리얼리티'라는 고유한 포지션을 선점한다. 경쟁사들이 커버하는 서베이/설문 영역도 커버하면서, 실제 제품 체험 + 감정/인지/의사결정 깊이로 추가 차별화한다."
- **외부 커뮤니케이션**: "AI 합성 사용자 시장에서 $1.5B+가 투자되고 있습니다. Personica는 이 시장의 모든 유스케이스(서베이, A/B 테스트, 제품 체험, 전문가 리뷰, 광고/마케팅 리서치)를 커버하면서, 유일하게 5-Layer 감정/인지/의사결정 시뮬레이션으로 페르소나 리얼리티를 보장합니다."
- **투자자 피칭**: "Simile($100M), Aaru($1B 밸류에이션)가 검증한 시장입니다. 그러나 이들은 감정/인지/의사결정을 구조적으로 시뮬레이션하지 않습니다. Personica는 경쟁사 영역(서베이, 설문, 리서치)도 커버하면서, 실제 제품 체험 + 5-Layer 엔진의 페르소나 리얼리티로 차별화합니다."

---

## 비용 기반 가격 정당화: 왜 이 가격이 가능한가

### COGS 현실 — docs/33 실제 API 가격 기반 계산

Personica의 가격($49-199/회)은 "저렴한 느낌"이 아닌, 실제 원가 구조에서 도출된 건강한 마진 기반 가격이다.

**기본 시나리오 (GPT-4.1 mini + Browserless Usage-based):**

| 비용 항목 | 50명 (Starter $49) | 200명 (Standard $99) | 500명 (Pro $199) |
|----------|:---:|:---:|:---:|
| LLM API | $2.38 | $9.52 | $23.80 |
| Playwright 클라우드 | $1.20 | $4.80 | $12.00 |
| 서버 할당분 | $1.50 | $1.50 | $1.50 |
| **COGS 합계** | **$5.08** | **$15.82** | **$37.30** |
| **Gross Margin** | **89.6%** | **84.0%** | **81.3%** |

**어떤 시나리오에서든 Gross Margin 78-94%** — 건강한 SaaS 수준 (70%+ 기준).

### 가격이 가능한 3가지 이유

1. **LLM 비용 연 80% 하락**: 2024년 GPT-4급 $20/MTok -> 2026년 GPT-4.1 mini $0.40/MTok. 200명 시뮬레이션의 LLM 비용이 $10 수준. 이 비용 하락이 Personica의 비즈니스 모델을 가능하게 한다.

2. **브라우저 자동화 생태계 성숙**: Browserless Usage-based ($0.0048/분)로 200명 시뮬레이션 브라우저 비용이 $4.80. Playwright 1,350만 주간 npm 다운로드 — 인프라가 충분히 성숙.

3. **인간 리서치 대비 10-100x 가격 차이**: UserTesting.com 5명 = $245+ (연 계약 ~$46K/년). Personica 200명 = $99. 이 가격 갭이 가치 제안의 핵심.

### 가격 앵커링 전략

| 비교 대상 | 비용 | Personica | 배율 |
|-----------|------|-----------|------|
| 유저 인터뷰 10명 모집 + 진행 | $2,000-5,000 | $99 (200명) | **20-50x 저렴** |
| UserTesting.com 5명 | $245+ (1회) / $46K (연) | $99 (200명) | **2.5x 저렴, 40x 많은 참가자** |
| Synthetic Users 200명 RAG | $400-5,400 추정 | $99 (200명) | **4-54x 저렴** |
| Ditto 엔터프라이즈 | $50K-75K/년 | $99-199/회 | 완전히 다른 세그먼트 |

**핵심 메시지**: "인간 10명에 $5,000이면 받아들입니다. AI 200명에 $99면 왜 안 됩니까?"

### 손익분기: 월 2건

월 고정비 $55-125 / 공헌이익 $83 (Standard 기준) = **월 0.7-1.5건에 손익분기**. 보수적으로 **월 2건이면 흑자**. 이것이 1인 부트스트랩 SaaS로서 생존 가능한 구조를 만든다.

---

## Value Curve (경쟁사 대비) — 18개 Feature Matrix 반영

### 전체 Value Curve

```
                 Personica  Blok  Uxia  Synthetic  Aaru  Artificial  ChatGPT  UserTesting
                                       Users            Societies            (인간)
실제 제품 사용    *****      *     *     .         .     .           .        *****
감정 시뮬레이션   ****       *     .     **        .     .           *        *****
인지/의사결정    *****       **    .     .         .     .           .        *****
페르소나 규모     *****      ***   **    **        ****  *****       *        **
페르소나 분화     ****       **    *     ***       **    ***         *        *****
비용 효율        ****       **    ***   ***       *     ***         *****    *
속도             **         ***   ****  ****      ****  ****        *****    *
데이터 불필요     *****      .     **** ****      ****  ****        *****    *****
세팅 간편성       ***        **    **** ****      ****  *****       *****    ***
반복사용 시뮬     *****      .     .     .         .     .           .        .
세그먼트 교차분석 *****      ****  **    **        ***   ***         .        ***
실체험 후 인터뷰  *****      *     .     .         .     .           .        *****
A/B 사전 시뮬    ***        ****  ***   .         .     .           .        .
접근성 감사       **         .     **** .         .     .           .        .
행동 로그/스크린샷 *****     .     .     .         .     .           .        *****
네트워크 시뮬     .          .     .     .         *     *****       .        .
셀프서브          ****       .     **** **        .     ****        *****    ***
```

**범례**: 5=최고, 4=높음, 3=중간, 2=낮음, 1=최소, 0(.)=미지원

### Personica의 전략적 포지션

**압도적 우위 영역**: 5-Layer 페르소나 리얼리티(감정/인지/의사결정 시뮬레이션) + 실제 제품 체험 + 반복 사용 시뮬레이션 + 실체험 후 인터뷰 + 행동 로그/마이크로 행동. 이 페르소나 리얼리티는 제품 체험뿐 아니라 서베이, A/B 테스트, 전문가 리뷰, 광고/마케팅 리서치, 퍼널 분석 모드에서도 동일하게 적용된다.

**경쟁사 영역 커버 + 추가 차별화**: Aaru/Synthetic Users가 하는 서베이·인터뷰도 Personica에서 가능하되, 5-Layer 엔진의 페르소나 리얼리티가 더해져 더 현실적인 응답을 생성한다. Blok/Uxia가 하는 A/B 테스트·디자인 평가도 가능하되, 실제 제품 체험(Playwright) 모드를 추가로 제공한다.

**의도적 트레이드오프**: 제품 체험 모드에서는 속도(-) + 세팅 간편성(-)를 감수하고 **깊이**를 선택. Uxia가 5분 만에 결과를 주는 반면, Personica 제품 체험 모드는 1-3시간 걸리지만 "온보딩 3단계에서 65세 페르소나가 CTA를 3초간 못 찾고 뒤로가기를 눌렀다. 인지 부하 0.82, 좌절감 0.71" 수준의 리포트를 제공한다. 서베이/A/B 테스트 모드는 경쟁사와 유사한 속도 제공.

**유일한 포지션**: 5-Layer 감정/인지/의사결정 시뮬레이션을 상용 서비스로 제공하는 곳은 Personica뿐이다. Playwright 기반 실제 제품 체험은 학술(UXAgent, AgentA/B)에서만 유사하지만, 이들에게도 감정/인지 시뮬레이션은 없다.

**핵심 약점**: 네트워크/소셜 시뮬레이션은 미지원 (Artificial Societies 영역). 접근성 감사는 Uxia가 WCAG 자동 검사에서 우위.

---

## Sources

### 프로젝트 내부 문서
- docs/strategy/user-research.md — 페르소나 정의 (민수/서연/준혁), 커뮤니티 근거, 이탈 퍼널 분석
- docs/strategy/lean-canvas.md — 가격 모델, 비용 구조, 실제 API 가격 기반 COGS, 유닛 이코노믹스
- docs/strategy/competitive-analysis.md — 9개 경쟁사 + 학술 시스템 2개 + 간접 경쟁사 3개, 18개 Feature Matrix
- docs/market-sizeing/market-sizing-yechangpae-appendix-software-first.md — 보수적 TAM/SAM/SOM, 전략적 총기회, 1차 진입시장
- docs/strategy/market-scan.md — SWOT + PESTLE + Porter Five Forces + Ansoff Growth Matrix

### 핵심 외부 출처
- Indie Hackers — 런칭 실패 사례, 피드백 편향, 베타 테스터 모집 어려움
- Maze 2025/2026, Future of User Research Report — PM 42% 리서치 수행, 합성 사용자 48% 인지
- User Interviews 2024, State of User Research — 참가자 모집 시간 61% 증가, 비용 32% 증가
- NNGroup, AI Simulations Studies — 합성 사용자 방향성 일치, 효과 크기 과소평가
- TechCrunch/Bloomberg — Simile $100M, Aaru $1B, Blok $7.5M 보도
- Ditto 2026 Market Map — 합성 리서치에 $1.5B+ VC 유입
- Lyssna 2026 UX Research Trends — 48% 리서처가 합성 사용자를 임팩트 트렌드로 선정
