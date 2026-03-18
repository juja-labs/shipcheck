# UXAgent 코드 레벨 분석

> UXAgent — Amazon Science / Northeastern University, CHI 2025
> GitHub: https://github.com/neuhai/UXAgent
> 로컬 클론: /home/work/Source/UXAgent

## 프로젝트 구조

```
UXAgent/
├── conf/
│   ├── base.yaml              # 글로벌 설정 (브라우저, LLM provider, tracing)
│   └── runConfig.yaml          # 배치 실행 설정 (페르소나, 인구통계, 설문)
├── experiment-ui/              # Vue.js 프론트엔드 (실험 위자드)
├── src/simulated_web_agent/
│   ├── agent/                  # 핵심 인지 에이전트
│   │   ├── agent.py            # Agent 클래스 (perceive/plan/act/reflect/wonder/feedback)
│   │   ├── memory.py           # 메모리 시스템 (임베딩 + 중요도 + 검색)
│   │   ├── gpt.py              # LLM 추상화 (LiteLLM, Anthropic Computer Use)
│   │   └── shop_prompts/       # 모든 프롬프트 (.txt 파일)
│   │       ├── perceive.txt    # HTML → 자연어 관찰
│   │       ├── planning.txt    # 다단계 계획 생성/갱신
│   │       ├── action.txt      # 계획 → 브라우저 액션 JSON
│   │       ├── reflect.txt     # 상위 인사이트 합성
│   │       ├── wonder.txt      # 랜덤 잡생각 생성
│   │       ├── feedback.txt    # 이전 액션 성공/실패 평가
│   │       ├── survey.txt      # 사후 설문 응답
│   │       └── memory_importance.txt  # 메모리 중요도 점수
│   ├── executor/               # 브라우저 자동화 레이어
│   │   ├── env.py              # WebAgentEnv (Playwright 래퍼, 1296줄)
│   │   └── parser/
│   │       ├── parser.js       # DOM 스트리퍼 + semantic-id 부여
│   │       └── initscript.js   # 네트워크 활동 트래커 + 호버 감지
│   └── main/                   # 진입점 및 오케스트레이션
│       ├── run.py              # 배치 오케스트레이터
│       ├── experiment.py       # 단일 실험 실행
│       ├── persona.py          # LLM 페르소나 생성
│       ├── survey.py           # 사후 설문
│       ├── model.py            # AgentPolicy (메인 루프)
│       └── app.py              # Flask API 서버
└── personas.json               # 생성된 페르소나 샘플 (20개)
```

## 아키텍처

### 3-Phase 파이프라인 (run.py)

**Phase 1: 페르소나 생성** → LLM이 인구통계 분포에서 N명 생성
**Phase 2: 에이전트 실행** → 페르소나별 독립 브라우저 세션
**Phase 3: 설문** → 메모리 트레이스 + 질문지 → LLM 응답

### 듀얼 프로세스 (System 1/2)

```python
# model.py — AgentPolicy.forward()
async def forward(self, playwright_env):
    observation = await playwright_env.observation()
    # System 1 (Fast): perceive → feedback → plan → act
    await asyncio.gather(
        self.agent.feedback(observation["html"]),
        self.agent.perceive(observation["html"]),
    )
    await self.agent.plan()
    action = await self.agent.act(observation)
    return json.dumps(action)

# 백그라운드 (System 2, Slow): reflect → wonder → memory update
async def slow_loop(self):
    while True:
        await self.agent.reflect()
        await self.agent.wonder()
        await asyncio.sleep(0.1)
```

## 페르소나 생성 상세

### 생성 방식 (persona.py)
- 인구통계를 가중치 분포에서 샘플링
- 이전 생성 페르소나를 예시로 제공 → 다양성 유도
- LLM이 풍부한 서사 생성

### 생성되는 속성 (personas.json 기준)
- Background: 나이, 성별, 위치, 교육, 직업, 소득, 취미, 기술 태도
- Financial Situation: 소득 안정성, 예산 습관, 지출 우선순위
- Shopping Habits: 빈도, 월 지출, 브랜드 선호, 리서치 습관
- Professional Life: 업무 스타일, 커리어 목표
- Personal Style: 의류 선호, 일상 루틴, 라이프스타일 가치

### 핵심 한계: Intent 공유
```python
# persona.py lines 116-129 — 개인화 intent 함수가 주석 처리됨
# 모든 페르소나가 동일한 general_intent를 받음
```

## 에이전트 의사결정 상세

### Perceive (HTML → 자연어)
- 스크린샷 사용하지 않음 — HTML 텍스트만 사용
- perceive.txt: "INCLUDE EVERY DETAIL ON THE WEB PAGE" 9회 반복
- parser.js가 DOM에서 비가시 요소 제거 + semantic-id 부여

### Plan (다단계 계획)
- `(next)` 마커로 현재 실행할 스텝 표시
- if-statement으로 미래 스텝 조건부 계획
- 현재 페이지에서 가능한 UI 액션만 계획에 포함

### Act (계획 → 브라우저 액션)
- 액션 스페이스: click, type, hover, select, clear, key_press, goto_url, back, forward, refresh, new_tab, switch_tab, close_tab, terminate
- 반복 방지: "DO NOT REPEAT A PREVIOUS ACTION"

### Feedback (액션 성공/실패 평가)
- 이전 계획 + 이전 액션 + 새 관찰 → 성공/실패 판단 + 생각 기록

## 브라우저 자동화 상세

### Universal Web Connector (parser.js)
핵심 혁신 — 임의의 웹사이트에서 작동하는 DOM 파서:
1. 비가시/비인터랙티브 요소 제거
2. 모든 인터랙티브 요소에 `parser-semantic-id` 부여 (텍스트 기반 slug)
3. 화이트리스트 속성만 보존 (id, type, name, value, placeholder, role 등)
4. 중첩 div 체인 플랫화
5. 클릭 가능 요소 자동 감지 (tag, role, cursor style, onclick)

### initscript.js
- addEventListener 후킹 → 호버 이벤트 리스너 추적
- XMLHttpRequest/fetch 후킹 → 네트워크 활동 모니터링 → 커스텀 idle 감지

### 타이밍
```python
# 현실성 낮음
pause = max(0.2 + normal(0, 0.05), 0)  # ~200ms 고정
sleep_after_action = 2  # 고정 2초
# 읽기 속도, 콘텐츠 비례 체류 시간, 망설임 등 없음
```

## 메모리 시스템 상세

### 5종 메모리 (memory.py)
| 유형 | 출처 | 설명 |
|------|------|------|
| Observation | perceive() | 현재 페이지 자연어 관찰 |
| Action | act() | 수행한 액션과 설명 |
| Plan | plan() | 현재 다단계 계획 |
| Thought | feedback(), wonder() | 평가, 잡생각, 근거 |
| Reflection | reflect() | 상위 인사이트 |

### 검색 공식
```python
scores = (similarities + recencies + importance) * kind_weights
# similarities: 코사인 유사도 (text-embedding-3-small)
# recencies: exp(timestamp - current_timestamp)
# importance: LLM 1-10 점수
# kind_weights: action=10, plan=10, thought=10, reflection=10
```

### 최근 윈도우
- 관찰: 3스텝 이내 항상 포함
- 액션/계획/생각: 5스텝 이내 항상 포함

## 출력물

에이전트별 `runs/<timestamp>/` 디렉토리:
- `basic_info.json` — 페르소나 + intent
- `screenshot/` — 매 스텝 스크린샷
- `simp_html/` — 파싱된 HTML
- `api_trace/` — 모든 LLM 호출 전문
- `action_trace.json` — 전체 액션 시퀀스
- `memory_trace.json` — 직렬화된 메모리 상태
- `survey_result.json` — SUS 설문 답변 + 근거 + 신뢰도

## ShipCheck 관점 — 가져올 것 vs 새로 만들 것

### 가져올 것
| 컴포넌트 | 품질 | 이유 |
|----------|------|------|
| parser.js (Universal Web Connector) | 우수 | 임의 웹사이트 DOM 파싱, semantic-id 부여 |
| initscript.js (네트워크/호버 감지) | 우수 | idle 감지, 인터랙티브 요소 자동 탐지 |
| env.py (Playwright 래퍼) | 우수 | 1296줄, 잘 구조화된 브라우저 자동화 |
| 메모리 검색 공식 | 좋음 | 3-score weighted retrieval 검증됨 |
| 듀얼 프로세스 패턴 | 좋음 | fast/slow loop 비동기 아키텍처 |
| 트레이싱 구조 | 좋음 | 스텝별 스크린샷/HTML/LLM콜 저장 |

### 새로 만들어야 할 것 (ShipCheck 핵심 IP)
| 컴포넌트 | UXAgent 상태 | ShipCheck 필요 |
|----------|-------------|---------------|
| 감정 시뮬레이션 | 없음 | OCC + PAD + Chain-of-Emotion |
| 인지 모델 | 없음 | Information Foraging + Cognitive Load |
| 시각 인식 | HTML만 (스크린샷 무시) | VLM 기반 시각적 판단 |
| 페르소나별 Intent | 전원 동일 intent | JTBD 기반 개인화 |
| 반복 사용 | 단일 세션 | 다중 세션 + 습관/이탈 모델링 |
| 현실적 타이밍 | 고정 200ms + 2초 | 페르소나별 BrowsingProfile |
| 교차 분석 | raw 트레이스만 | KG 기반 세그먼트/기능별 분석 |
| 도메인 범용성 | 쇼핑 전용 (shop_prompts/) | 도메인 무관 프롬프트 |
| 제품 자동 탐색 | 사람이 URL+intent 지정 | Phase 1 자동 크롤링/기능 발견 |

### 코드에서 발견된 기술적 이슈
1. `add_thought()` 메서드가 생각을 **6번 중복 저장** — 메모리 검색 가중치 해킹
2. Anthropic Computer Use 코드가 gpt.py에 있으나 실제 미사용
3. 막힘(stuck) 감지/복구 로직 없음 — 반복 방지 규칙만 있음
4. deny_list로 특정 단어(Crime, Security) 필터링 — 하드코딩
