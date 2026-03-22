# Pre-Mortem: Personica (합성 페르소나 시뮬레이션 플랫폼) 핵심 실험 + MVP 착수

**Date**: 2026-03-16
**Status**: Draft
**Scope**: 실험 1(분화 검증) + 실험 2(현실성 검증) 5주 타임라인 + MVP 착수 판단
**Team**: 1인

---

## Risk Summary

- **Tigers**: 9개 (Launch-blocking 3, Fast-follow 3, Track 3)
- **Paper Tigers**: 4개
- **Elephants**: 3개

---

## Launch-Blocking Tigers

실험 실패 = 프로젝트 전체 방향 전환. 이것들이 발생하면 5주 타임라인이 의미 없어진다.

| # | Risk | Likelihood | Impact | Mitigation | Deadline |
|---|------|-----------|--------|-----------|----------|
| T1 | **LLM 동질화를 극복 못함** — Big Five 수치 매핑 + SDE 감정 진화를 적용해도, 50명 페르소나가 비슷한 행동/감정을 보임. ANOVA p > 0.05 | 중간 (40%) | 치명적 | ① Week 1에 10명으로 빠른 파일럿 실행 → 분화 징후 없으면 즉시 프롬프트/파라미터 조정 ② temperature, 성격 파라미터 범위, sycophancy resistance 등 튜닝 가능한 변수 사전 목록화 ③ 최악: Claude vs GPT vs Gemini 크로스 모델 비교로 동질화가 모델 고유 한계인지 프롬프트 문제인지 진단 | Week 2 |
| T2 | **5주 내 Layer 1-4 프로토타입 완성 불가** — 1인 팀으로 Big Five 매핑 + OCC/PAD 감정 + BDI-E 의사결정 + Playwright 연동을 3주 안에 구현하기엔 스코프 과다 | 높음 (60%) | 높음 | ① 최소 구현 범위 재정의: Layer 3(감정)을 OCC 22개 → 6개 핵심 감정으로 축소, Layer 4(의사결정)를 BDI-E → 단순 규칙 기반으로 축소 ② UXAgent 코드(parser.js, env.py) 최대한 재사용 — 새로 쓰지 않음 ③ 리포트 생성 완전 제외 — raw 데이터(JSON)로 분석 ④ 비상: Layer 2(인지) 제외하고 Layer 1+3+4+Playwright만으로 실험 | Week 1 |
| T3 | **테스트 대상 웹 제품에서 Playwright가 차단됨** — 봇 감지(Cloudflare, reCAPTCHA), rate limiting, 동적 렌더링 실패로 크롤링/조작 불가 | 중간 (35%) | 높음 | ① 실험 대상 제품을 사전에 3-5개 후보 선정 → Week 1에 전부 Playwright 접근 테스트 ② Stealth 플러그인(playwright-extra) 적용 ③ 직접 만든 간단한 테스트용 웹앱을 대안으로 준비 (환경 완전 통제) ④ 로그인 불필요 제품 우선 (Tally, Draw.io 등 공개 도구) | Week 1 |

---

## Fast-Follow Tigers

실험은 성공했지만, MVP로 넘어갈 때 걸림돌이 되는 것들.

| # | Risk | Likelihood | Impact | Planned Response |
|---|------|-----------|--------|-----------------|
| T4 | **분화는 되지만 현실성이 없음** — 세그먼트 간 행동이 다르긴 한데, 실제 인간과 방향이 반대 (예: 시니어 페르소나가 더 빠르게 행동) | 중간 (30%) | 높음 | 실험 2 Option A(NNGroup 벤치마크)로 3개 이상 방향 확인. 불일치 시 특정 파라미터 캘리브레이션 (click_hesitation, error_tolerance 등 조정). 최악: 실험 2 Option B(실제 인간 비교)로 정밀 보정 |
| T5 | **컴퓨팅 비용이 예상보다 높음** — 50명 × 3제품 × 10분 시뮬레이션의 실제 LLM 토큰 + Playwright 비용이 $500+ | 중간 (40%) | 중간 | 실험 실행 전 1명 페르소나 × 1제품 비용 측정 → 50명 추정. 예산 상한 $300 설정. 초과 시 페르소나 수 30명으로 축소하거나 스텝 수 줄임 |
| T6 | **"좋은 리포트"를 만드는 방법을 모름** — 실험 raw 데이터는 있는데, 고객이 actionable하게 느끼는 리포트 포맷을 설계 못 함 | 중간 (35%) | 중간 | 실험 단계에서는 리포트 불필요 (raw 데이터로 분석). MVP 단계에서 Concierge 고객 5명에게 수동으로 리포트 작성 → 어떤 형식이 actionable한지 직접 학습. Uxia/Synthetic Users 샘플 리포트 참고 |

---

## Track Tigers

지금 당장은 아니지만 모니터링 필요.

| # | Risk | Trigger Condition | Monitoring |
|---|------|------------------|-----------|
| T7 | AgentA/B 상용화 | Amazon/Northeastern 팀의 스타트업 등록, PH 런칭 | arXiv, LinkedIn, PH 주 1회 체크 |
| T8 | Blok이 셀프서브 저가 플랜 출시 | Blok 가격 페이지 변경, IH/PH 광고 | joinblok.co 월 1회 체크 |
| T9 | EU AI Act 합성 콘텐츠 라벨링 의무가 Personica 리포트에 적용 (제품 체험, 서베이, A/B 테스트 등 모든 모드) | 2026.08 시행 가이드라인 발표 | artificialintelligenceact.eu 분기 1회 |

---

## Paper Tigers

무섭게 보이지만 실제로는 관리 가능한 것들.

| # | 우려 | 왜 Paper Tiger인가 | Real Tiger 전환 조건 |
|---|------|-------------------|-------------------|
| PT1 | "Playwright 브라우저 인스턴스 비용이 사업을 죽일 것" | LLM API 비용이 연 80% 하락 중. 2024년 $20/MTok → 2026년 $0.40/MTok. 이 트렌드가 지속되면 200명 시뮬레이션 COGS가 $10 이하로 떨어짐. Playwright 자체는 오픈소스 무료 | LLM 가격 하락 추세가 반전되거나, Playwright 클라우드 비용이 급등할 때 |
| PT2 | "인디해커가 $49도 안 쓸 것" | 인디해커는 "자기 제품에 도움되는 도구"에는 지불함 (Ship, Crisp, Plausible 등 $10-50/월 구독 다수). 1회 $49는 월 구독보다 심리적 장벽 낮음 | 인터뷰에서 10명 중 8명 이상이 "안 쓸 것"이라고 할 때 |
| PT3 | "1인 팀이라 경쟁사에 밀릴 것" | Blok($7.5M)과 직접 경쟁 아님 (다른 세그먼트, 다른 기술). 인디해커 시장은 1인 제품에 우호적. Uxia도 €1M pre-seed 초기 팀 | Blok이 정확히 같은 접근(Playwright + 감정 시뮬레이션)으로 인디 세그먼트 진출할 때 |
| PT4 | "테스트 계정 제공이 너무 큰 마찰" | Personica가 필요한 수준의 고객이라면 자기 제품의 테스트 계정을 만드는 건 5분 작업. 노코드 플랫폼(Bubble 등)은 Test 환경을 기본 제공. 이 마찰이 진지도 필터 역할 | 인터뷰/Concierge에서 "테스트 계정 만들기 귀찮아서 포기"가 50%+ 발생 시 |

---

## Elephants in the Room

팀(=자신)이 알고 있지만 직면하기 불편한 것들.

### E1: "실험이 실패하면 Personica 자체를 접어야 한다"

Discovery Plan에 "실험 실패 시 피봇 검토 (Figma 기반, 인터뷰 전용, 또는 중단)"이라고 적었지만, 실제로 수개월 투자한 프로젝트를 접는 결정을 할 수 있는가? Sunk cost fallacy에 빠져서 "한 번 더 해보자"를 반복할 위험.

**대응**: 실험 전에 Go/No-Go 기준을 **숫자로 확정**하고 기록. "ANOVA p < 0.05이고 NNGroup 벤치마크 3개 중 2개 이상 방향 일치"가 아니면 No-Go. 이 기준을 실험 후에 바꾸지 않겠다고 자신과 약속.

### E2: "5-Layer 아키텍처가 과도하게 복잡할 수 있다"

CLAUDE.md에 "페르소나 시뮬레이션 충실도가 최우선"이라고 적었고, 5-Layer 아키텍처를 설계했지만 — 이것이 고객이 원하는 것인가? 고객은 "OCC 감정 모델"을 원하는 게 아니라 "쓸만한 피드백"을 원한다. 3-Layer로도 "쓸만한 피드백"이 나올 수 있다면, 5-Layer는 over-engineering.

**대응**: 실험 1을 Layer 수를 줄여서도 실행해보기. 예: Layer 1+4+Playwright만으로 돌린 그룹 vs Layer 1+2+3+4+Playwright로 돌린 그룹 비교. 감정/인지 레이어가 실제로 결과 품질에 기여하는지 ablation study.

### E3: "예비창업패키지 일정에 쫓기고 있다"

사업계획서 마감이 있고, 전략 문서를 정비하는 것과 실제 엔진 프로토타입을 만드는 것 사이에서 시간 배분이 고민된다. 전략 문서가 아무리 완벽해도 제품이 안 돌아가면 의미 없고, 제품이 돌아가도 사업계획서가 없으면 지원금을 못 받는다.

**대응**: 전략 문서(Wave 0~2)는 현재 세션에서 최대한 완성. 엔진 프로토타입에 집중할 수 있는 시간 블록 확보. 사업계획서는 전략 문서를 재구성하는 수준이지 새로 쓸 필요 없음.

---

## Go/No-Go Checklist (실험 완료 후)

### Go 조건 (모두 충족):
- [ ] 실험 1: 세그먼트 간 ANOVA p < 0.05
- [ ] 실험 1: 같은 세그먼트 내 행동 일관성 > 0.6
- [ ] 실험 2: NNGroup 벤치마크 3개 중 2개 이상 방향 일치
- [ ] 시뮬레이션당 COGS < $25

### No-Go 시 옵션:
1. **파라미터 보정 후 재실험** (1회만) — T1 대응의 연장
2. **스코프 축소 피봇** — 서베이/인터뷰 모드만 유지하되 제품 체험 제거, "합성 페르소나 리서치" 포지셔닝
3. **근본 피봇** — Figma/스크린샷 기반 인지 시뮬레이션 (Blok/Uxia 유사)
4. **중단** — 학습 기록 후 다른 프로젝트로 이동

### Rollback Plan:
- 실험 인프라(Playwright 인스턴스, LLM API 키)는 사용량 기반 과금이므로 중단 시 비용 0
- 코드는 Git에 보존 — 추후 재개 가능
- 전략 문서(`docs/strategy/*`, `docs/market-sizeing/*`)는 피봇 시에도 부분 활용 가능

---

## Sources

- docs/discovery-plan.md — 실험 설계, Go/No-Go 매트릭스
- docs/strategy/market-scan.md — SWOT/Porter 위협 분석
- docs/strategy/lean-canvas.md — 비용 구조, 핵심 가정
- docs/strategy/user-research.md — 이탈 지점 분석
