# Personica (페르소니카)

> AI 합성 페르소나가 사람처럼 생각·느끼·행동하며, 모든 사용자 리서치를 시뮬레이션하는 플랫폼

## Problem

제품·서비스·마케팅에 대한 사용자 반응을 검증하고 싶지만, 기존 방법은 한계가 있습니다:

- **설문/FGI**: 비용·시간·규모 제약 (건당 $25,000~$65,000, 6~12주)
- **베타테스터**: 모집 2주+, 다양성 부족
- **AI 합성 페르소나 (기존)**: 단순 LLM 프롬프팅으로 실제 인간의 감정·인지·의사결정 과정을 시뮬레이션하지 못함

## Solution

Personica는 **5-Layer 시뮬레이션 엔진**으로 감정·인지·의사결정을 구조적으로 시뮬레이션하는 합성 페르소나 플랫폼입니다.

### 핵심 해자: 페르소나 리얼리티

다른 합성 페르소나 제품들이 단순한 LLM 프롬프팅인 반면, Personica는 실제 사람과 유사한 반응을 생성합니다:

```
Layer 1: Persona Profile — Big Five → 행동 파라미터 수학적 매핑 (PRISM)
Layer 2: Cognitive — Information Foraging, Cognitive Load, Mental Model, TAM
Layer 3: Emotion — OCC Appraisal + PAD 연속 상태 + SDE 확률적 감정 진화
Layer 4: Decision — BDI-E 모델 + Fogg Check + Satisficing Gate
Layer 5: Memory — Memory Stream + Reflection + Habit Strength + Drift Monitor
```

### 적용 범위

5-Layer 엔진은 특정 use case에 묶이지 않는 범용 플랫폼:

| 모드 | 설명 | 단계 |
|------|------|------|
| **제품 체험 시뮬레이션** | Playwright로 실제 제품을 사용하고 UX 피드백 | Phase 1 (beachhead) |
| **UI/UX 디자인 피드백** | Figma/프로토타입 기반 디자인 리뷰 | Phase 1 |
| **합성 서베이/인터뷰** | 설문, FGI, 인터뷰 시뮬레이션 | Phase 2 |
| **A/B 테스트** | 변형 간 선호도/행동 차이 시뮬레이션 | Phase 2 |
| **광고/마케팅 리서치** | 광고 크리에이티브, 메시지, 카피 테스트 | Phase 2 |
| **퍼널 분석** | 전환 퍼널 각 단계별 이탈/전환 시뮬레이션 | Phase 2 |
| **전문가 리뷰** | 도메인 전문가 페르소나의 제품/서비스 평가 | Phase 3 |

### 기존 도구와의 차이

| | Aaru / Synthetic Users | Blok | **Personica** |
|---|---|---|---|
| 시뮬레이션 깊이 | LLM 프롬프팅 | 인지 모델 일부 | **5-Layer 감정·인지·의사결정** |
| 입력 | 설문/컨셉 설명 | Figma + 분석 데이터 | **실제 제품 URL + 서베이 + 디자인** |
| 적용 범위 | 설문/인터뷰 | UX 예측 | **제품 체험 + 서베이 + A/B + 전문가** |
| 기존 데이터 필요 | 부분적 | Amplitude 등 필수 | **불필요** |

## Validated Results

Tally.so(웹 폼 빌더) 대상 초기 검증 (2명 페르소나):

- **52세 교사 박서연** vs **31세 PM 김도현**: 동일 제품에서 이탈 시점 5스텝 차이
- 이탈 이유 완전히 다름 (심리적 불안 vs 기능 부족)
- 감정 파이프라인 on/off 시 행동 패턴이 유의미하게 달라짐

## Tech Stack

| 레이어 | 기술 |
|--------|------|
| Simulation Engine | 5-Layer (Profile → Cognitive → Emotion → Decision → Memory) |
| Browser Automation | Playwright (제품 체험 모드) |
| LLM | OpenAI / Anthropic / Google API |
| Backend | Python + FastAPI |
| Frontend | Next.js + TypeScript + Tailwind CSS |
| Database | PostgreSQL |

## Project Structure

```
src/
├── layer1_persona/    # Big Five → 행동 파라미터 매핑
├── layer3_emotion/    # OCC + PAD + SDE 감정 시뮬레이션
├── analysis/          # G2 리뷰 비교 분석
├── data/              # 벤치마크 데이터 크롤러
└── cli.py             # CLI 진입점

configs/               # 실험 설정 + 페르소나 YAML
docs/                  # 제품 비전, 엔진 설계, 전략, 시장 조사
```

## References

- [PRISM](https://arxiv.org/abs/2512.19933) — SDE 감정 진화, Big Five→행동 파라미터 매핑
- [UXAgent](https://github.com/neuhai/UXAgent) — 브라우저 자동화 기반 UX 테스팅 (CHI 2025)
- [Concordia](https://github.com/google-deepmind/concordia) — GM-Player 아키텍처
- [Generative Agents](https://arxiv.org/abs/2304.03442) — Memory Stream + Reflection
- 전체 레퍼런스: `docs/foundation/research-references.md` (논문 30+편)

## License

TBD
