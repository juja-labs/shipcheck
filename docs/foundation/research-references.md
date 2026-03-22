# Research References

Personica(이전 ShipCheck) 페르소나 시뮬레이션 엔진 설계에 참고한 논문, 프레임워크, 데이터셋, 제품.

## 핵심 논문

### Agent Architecture
| 논문 | 핵심 기여 | 관련도 |
|------|----------|--------|
| [Generative Agents](https://arxiv.org/abs/2304.03442) (Park et al., UIST 2023) | Memory Stream + Reflection + Planning → believable agents | 메모리 아키텍처 직접 차용 |
| [CoALA](https://arxiv.org/abs/2309.02427) (TMLR 2024) | Cognitive Architectures for Language Agents — 인지과학 기반 에이전트 분류 체계 | 전체 아키텍처 프레임워크 |
| [UXAgent](https://arxiv.org/abs/2502.12561) (Amazon, CHI 2025) | LLM + 브라우저 자동화 = 자동 사용성 테스트 | 브라우저 연동 직접 참고 |
| [AgentA/B](https://arxiv.org/abs/2504.09723) | 1,000 페르소나 에이전트로 웹사이트 A/B 테스트 | 대규모 시뮬레이션 아키텍처 |

### Persona Simulation Fidelity
| 논문 | 핵심 기여 | 관련도 |
|------|----------|--------|
| [Out of One, Many](https://arxiv.org/abs/2209.06899) (Argyle et al., 2023) | Silicon Sampling — LLM 인구통계 조건화 → 실제 설문 유사 분포 | 페르소나 생성 방법론 |
| [Stanford 1,000명 실험](https://www.syntheticusers.com/science-posts/generative-agent-simulations-of-1-000-people) | 2시간 인터뷰 기반 GPT-4 에이전트 → 85% 정확도, r=0.98 | 정확도 벤치마크 |
| [Stable Personas](https://arxiv.org/html/2601.22812) (2025) | 페르소나 행동 표현이 시간에 따라 감쇠 (Claude -1.6, GPT -5.5) | 시간적 안정성 한계 |
| [PersonaHub](https://arxiv.org/abs/2406.20094) (Tencent) | 10억 개 다양한 페르소나 자동 큐레이션 | 대규모 페르소나 생성 |
| [Polypersona](https://arxiv.org/abs/2512.14562) | LoRA 튜닝 + 433 페르소나 × 10 도메인 | 도메인별 페르소나 시뮬레이션 |
| [Customer-R1](https://arxiv.org/abs/2510.07230) | RL로 페르소나 행동 캘리브레이션 → 78.5% F1 | 행동 정밀도 향상 |

### Emotion & Cognition
| 논문 | 핵심 기여 | 관련도 |
|------|----------|--------|
| [Chain-of-Emotion](https://pmc.ncbi.nlm.nih.gov/articles/PMC11086867/) (PLOS One, 2024) | Appraisal 기반 감정 평가 → 행동 전 감정 선행 | 감정 레이어 핵심 패턴 |
| [Affective Computing in LLM Era](https://arxiv.org/pdf/2408.04638) (2024) | AU/AG 서베이, ECoT 프레임워크, EmotionPrompt | 감정 기술 총정리 |
| [OCC Model Revisited](https://people.idsia.ch/~steunebrink/Publications/KI09_OCC_revisited.pdf) | OCC 감정 모델 구현 가능 버전 | 감정 분류 체계 |
| [BDIPrompting](https://dl.acm.org/doi/10.1145/3623809.3623930) | BDI + LLM → 목표 지향적 계획 | 의사결정 아키텍처 |

### Social Simulation → 개별 에이전트 모델링 기법 차용
| 프레임워크 | 핵심 기여 | Personica 차용 |
|-----------|----------|---------------|
| [PRISM](https://arxiv.org/abs/2512.19933) (Fudan, 2025) | MBTI→행동 파라미터 매핑, SDE 감정 진화, PC-POMDP 의사결정 | Layer 1 성격 파라미터화, Layer 3 확률적 감정 모델, Layer 4 불완전 정보 의사결정 |
| [Concordia](https://github.com/google-deepmind/concordia) (Google DeepMind) | GM-Player 아키텍처, 조합형 컴포넌트 시스템 | 환경-에이전트 분리, 페르소나별 인지 사이클 분화 |
| [GenSim](https://arxiv.org/abs/2410.04360) (NAACL 2025) | 장기 시뮬레이션 오류 보정, 10만 에이전트 | 다중 세션 페르소나 드리프트 방지 |
| [Truman Platform](https://github.com/cornellsml/truman_2023) (Cornell) | 전수 활동 로깅 (마우스/스크롤/체류시간) | 마이크로 행동 로깅 패턴 |
| [S³/GA-S³](https://arxiv.org/abs/2307.14984) | 감정-태도-행동 3축 분리 모델 | 감정↔태도↔행동 상호 피드백 루프 |
| [MOSAIC](https://arxiv.org/abs/2504.07830) (EMNLP 2025) | 메모리+자기성찰+추론 기반 콘텐츠 평가 | 기능 평가 프레임 변용 |
| [AgentSociety](https://github.com/tsinghua-fib-lab/AgentSociety) (Tsinghua) | 1만+ 에이전트, 현실적 사회 환경 | 대규모 병렬 실행 아키텍처 참고 |

### Memory Systems
| 시스템 | 핵심 기여 | 관련도 |
|--------|----------|--------|
| [Mem0](https://arxiv.org/abs/2504.19413) | 그래프+시맨틱 듀얼 검색, 충돌 해결, 26% 정확도 향상 | 메모리 대안 |
| [Zep/Graphiti](https://arxiv.org/html/2501.13956v1) | 시간축 KG, bi-temporal model, 하이브리드 검색 | 데이터 구조화 핵심 |
| [A-Mem](https://arxiv.org/abs/2502.12110) (NeurIPS 2025) | Zettelkasten 방식, 양방향 링크, 다중 홉 추론 2× | 복잡한 추론 대안 |
| [CMA](https://arxiv.org/html/2601.09913) | Spreading activation, consolidation engine | 생물학적 메모리 모델 |

---

## 행동 이론 프레임워크

| 이론 | 핵심 | Personica 적용 |
|------|------|---------------|
| Information Foraging (Pirolli & Card) | 사용자는 "정보 냄새"를 따라 UI 탐색 | Layer 2: UI 요소 평가 |
| Cognitive Load Theory (Sweller, 1988) | 인지 부하 초과 → 에러, 이탈 | Layer 2: 누적 부하 추적 |
| TAM (Davis, 1989) | Perceived Usefulness × Ease of Use | Layer 2: PU/PEOU 실시간 갱신 |
| Fogg Behavior Model (B=MAP) | Motivation × Ability × Prompt | Layer 4: 행동 트리거 판단 |
| Bounded Rationality (Simon, Nobel 1978) | Satisficing vs Maximizing | Layer 4: 탐색 깊이 결정 |
| PAD Model (Mehrabian & Russell, 1974) | Pleasure-Arousal-Dominance 3차원 감정 | Layer 3: 연속 감정 추적 |
| OCC Model (Ortony, Clore, Collins, 1988) | 22개 감정 × 3종 자극 분류 | Layer 3: 이벤트별 감정 매핑 |
| Appraisal Theory | 이벤트 평가가 감정을 결정 | Layer 3: Chain-of-Emotion |

---

## 데이터셋

### 제품 리뷰 (페르소나 리뷰 스타일 학습)
| Dataset | 규모 | 소스 |
|---------|------|------|
| [Amazon Review Data (UCSD)](https://jmcauley.ucsd.edu/data/amazon/) | 1.42억 리뷰 | 무료, 연구용 |
| [Amazon Reviews Sentiment (Kaggle)](https://www.kaggle.com/datasets/bittlingmayer/amazonreviews) | ~400만 | 무료 |
| [G2 API](https://data.g2.com/api/docs) | B2B SaaS 리뷰 | API 키 필요 |

### 클릭스트림 (행동 패턴 캘리브레이션)
| Dataset | 내용 | 소스 |
|---------|------|------|
| [UCI Clickstream](https://archive.ics.uci.edu/dataset/553/clickstream+data+for+online+shopping) | 의류 쇼핑 5개월 | UCI ML Repository |
| [eCommerce Behavior (Kaggle)](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store) | view/cart/purchase | Kaggle |
| [Mobile Device Usage (Kaggle)](https://www.kaggle.com/datasets/valakhorasani/mobile-device-usage-and-user-behavior-dataset) | 앱 사용 패턴 | Kaggle |

### 시선/마우스 추적
| Dataset | 내용 |
|---------|------|
| [Attentive Cursor Dataset (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7701271/) | 마우스-주의력 상관관계 |
| [SERP Eye+Mouse (arXiv)](https://arxiv.org/html/2507.08003v1) | 47명, 2,776 검색 쿼리, 시선+마우스 |

### 웹 분석 벤치마크
- [Arvo Digital GA4 연구](https://arvo.digital/ga4-engagement-rates/) — 산업별 참여율
- [Databox 벤치마크](https://databox.com/website-traffic-benchmarks-by-industry) — 산업별 트래픽
- 평균 세션: 2분 38초 / 바운스율: 44-45% / 참여율: 62%

---

## 벤치마크 (에이전트 행동 현실성 측정)

| 벤치마크 | 내용 | 현 SOTA |
|----------|------|---------|
| [WebArena](https://webarena.dev/) | 812 태스크, 4 도메인 | Gemini 2.5 Pro: 54.8% |
| [Mind2Web](https://osu-nlp-group.github.io/Mind2Web/) | 137 사이트, 2,000+ 태스크 | MindAct 기반 |
| [WebChoreArena](https://arxiv.org/pdf/2504.01382) | 532 고난도 태스크 | 37.8% |

---

## 경쟁/참고 제품

| 제품 | 유형 | 핵심 | 링크 |
|------|------|------|------|
| UXAgent | 오픈소스 (학술) | LLM + Playwright 사용성 테스트 | [GitHub](https://github.com/neuhai/UXAgent) |
| Synthetic Users | 상용 SaaS | 인터뷰 기반 페르소나, 85% 정확도 | [syntheticusers.com](https://www.syntheticusers.com/) |
| Artificial Societies | YC W25, $5.35M | 300-5,000 페르소나 소셜 시뮬레이션 | [societies.io](https://societies.io/) |
| Blok | $7.5M | AI 제품 테스팅 | [joinblok.co](https://www.joinblok.co/) |
| Uxia | ~1M EUR | Think-aloud UX 테스트, 5분 | [uxia.app](https://www.uxia.app/) |
| OASIS | 오픈소스 | 1M 에이전트 소셜 시뮬레이션 | [GitHub](https://github.com/camel-ai/oasis) |
| MiroFish | 오픈소스 | OASIS+Zep 기반 AI 예측 엔진 | [GitHub](https://github.com/666ghj/MiroFish) |

---

## 검증 방법론

### Synthetic-Organic Parity (Synthetic Users 제안)
- 합성 응답이 인간 응답과 통계적으로 구분 불가능한지 측정
- Topic Consistency, Linguistic Pattern, Qualitative Alignment

### 정량적 비교 메트릭
- 페이지 체류 시간 분포 비교
- 클릭 순서 (task flow) 비교
- 감성 분포 KL-divergence
- 기능 우선순위 랭킹 Kendall Tau correlation

### NNGroup 평가 결론
- "AI for speed, humans for truth" — 합성 사용자는 조기 탐색용, 실제 검증은 인간
- 전체 트렌드 포착하지만 효과 크기와 분산을 과소평가
