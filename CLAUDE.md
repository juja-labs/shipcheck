# ShipCheck

## Project Overview
ShipCheck은 MVP/프로토타입을 실제 시장에 출시하기 전에, AI 에이전트 기반 가상 시장 검증을 제공하는 SaaS 플랫폼이다.

핵심 가치: "만드는 건 끝났어. 이거 사람들이 원할까?" — 이 질문에 5분 만에 답한다.

## Tech Stack
- **Multi-Agent Simulation**: OASIS (Apache 2.0) 기반 소셜 시뮬레이션
- **Knowledge Graph**: Zep Cloud (GraphRAG) — 피드백 온톨로지, 시간별 변화 추적
- **Browser Automation**: Playwright — 에이전트가 실제 제품을 사용
- **LLM**: OpenAI / Anthropic API — 페르소나 생성, 행동 결정, 보고서 생성
- **Backend**: Python (FastAPI)
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **Database**: SQLite (OASIS 시뮬레이션), PostgreSQL (서비스 데이터)

## Architecture
```
사용자 입력 (MVP URL + 타겟 유저 설명 + 가설)
    │
    ▼
Phase 1: 자동 분석
  ① Playwright로 제품 크롤링 → 페이지/기능/플로우 파악
  ② LLM이 Feature 온톨로지 자동 생성
  ③ 타겟 유저 기반 페르소나 20~100명 생성
  ④ Zep Graph 초기화 (온톨로지 + 페르소나)
  ⑤ 시뮬레이션 설정 자동 결정
    │
    ▼
Phase 2: 제품 체험 + 소셜 시뮬레이션 (N 라운드)
  ① 에이전트가 Playwright로 실제 제품 사용
  ② OASIS 소셜 플랫폼에서 사용 경험 공유/토론
  ③ 행동 데이터 → Zep 그래프 실시간 업데이트
    │
    ▼
Phase 3: 분석 및 보고서
  ① ReportAgent가 Knowledge Graph 검색으로 구조화된 인사이트 도출
  ② Feature별 사용성 점수, 세그먼트별 반응, 핵심 이탈 지점
  ③ 선택적 에이전트 인터뷰
```

## Key Differentiators
1. **실제 제품 사용**: 설문/컨셉 설명이 아닌, 에이전트가 Playwright로 MVP를 직접 사용
2. **소셜 시뮬레이션**: 개별 피드백이 아닌, OASIS 기반 집단 토론/여론 형성
3. **Knowledge Graph**: 평면적 보고서가 아닌, "왜 이 세그먼트가 이탈했는가"를 구조적으로 추론

## Conventions
- 한국어 코멘트 사용
- 커밋 메시지는 영어 conventional commits (feat:, fix:, chore: 등)
- Python: Black formatter, type hints 필수
- Frontend: ESLint + Prettier

## References
- OASIS: https://github.com/camel-ai/oasis
- MiroFish (참고 구현): https://github.com/666ghj/MiroFish
- Zep Cloud: https://www.getzep.com/
