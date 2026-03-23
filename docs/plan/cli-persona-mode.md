# CLI Persona Mode — 구현 계획

## 배경

### 문제
Personica의 브라우저 자동화 계층을 4번 교체했지만 (parser.js → 접근성 스냅샷 → CDP+Playwright 하이브리드 → PlaywrightCliEnv), 여전히 엣지 케이스가 남아있다:
- "/" 커맨드 메뉴 트리거 실패 (Input.insertText vs 키보드 이벤트)
- contenteditable 타이핑 불안정
- SPA 페이지 전환 후 상태 인식 지연

### 발견
Claude Code CLI의 `-p` 모드 + `playwright-cli` 스킬 조합이 위 문제를 모두 해결한다:
- `playwright-cli type "/"` → Tally 에디터에서 블록 메뉴 정상 트리거
- `playwright-cli fill e5 "text"` → contenteditable 포함 안정적 입력
- `playwright-cli snapshot` → Microsoft가 관리하는 접근성 트리 (ref 기반)
- 실제 테스트에서 "52세 여교사" 롤플레이 + playwright-cli 조합으로 Tally 정상 사용 확인

### 핵심 결정
**브라우저 자동화는 해자가 아니다.** playwright-cli에 위임하고, Personica의 진짜 해자인 **페르소나 리얼리티**(페르소나 리얼리티 엔진의 감정·인지·의사결정 시뮬레이션의 깊이 + 페르소나 합성 방법론 + 정량 분석)에 집중한다. Playwright는 "제품 체험" 모드에서 쓰는 하나의 인터페이스일 뿐이다.

---

## 아키텍처

### 현재 (760줄+, 4개 모듈)
```
session.py → persona_react LLM → action_executor LLM → cdp_dom + cdp_actions + dom_tree + async_env
```

### 변경 후 (~100줄 오케스트레이터 + 프롬프트)
```
experiment.py (오케스트레이터)
  │
  ├─ 페르소나별 장수명 프로세스 생성:
  │   claude --print \
  │     --input-format stream-json \
  │     --output-format stream-json \
  │     --session-id <uuid> \
  │     --allowedTools "Bash(playwright-cli:*)"
  │
  ├─ stdin/stdout 스트림 루프:
  │   1. stdin write: 페르소나 프롬프트 + "tally.so 사용해봐"
  │   2. stdout read: 에이전트가 snapshot → 판단 → playwright-cli 실행 → 턴 완료
  │   3. emotion_update.py: 턴 결과 파싱 → OCC → PAD + SDE → 이탈 판정
  │   4. stdin write: "[감정 업데이트] pleasure=0.15, 이탈 위험 높음"
  │   5. 반복 (이탈 판정 or max_turns까지)
  │
  ├─ 세션 히스토리:
  │   ~/.claude/projects/{project}/{session-id}.jsonl 에 자동 저장
  │   (Claude Code가 관리, 우리가 별도 저장 불필요)
  │
  └─ 세션 종료 후:
      → 세션 JSONL 파싱 → 리뷰 생성
      → 실험 데이터 저장
      → G2 비교 스크립트 실행
```

### 핵심: 훅 불필요, stream-json으로 직접 제어
- 훅(PostToolUse)이 아닌 **stdin/stdout 스트림**으로 매 턴 감정 주입
- 오케스트레이터가 stdout을 읽으면서 "이번 턴에 뭘 했는지" 파악
- 파악한 결과로 PAD 계산 → 다음 턴에 stdin으로 주입
- 에이전트 입장에서는 "사용자가 감정 상태를 알려주는 것"처럼 보임

### 삭제 대상
- `browser/cdp_dom.py` (150줄)
- `browser/dom_tree.py` (180줄)
- `browser/cdp_actions.py` (200줄)
- `browser/async_env.py` (230줄)
- `browser/pw_cli_env.py`
- `browser/env.py`
- `browser/parser.js`, `browser/initscript.js`
- `prompts/action_executor.txt` (실행기 LLM 프롬프트)
- `prompts/action_decide.txt`
- `llm/claude_cli.py` (자체 CLI 래퍼 — Claude Code가 직접 LLM 역할)

### 유지 대상
- `layer1_persona/` — Big Five → 행동 파라미터 매핑
- `layer3_emotion/engine.py` — OCC + PAD + SDE noise 계산
- `data/exporter.py` — ANOVA CSV export
- `data/benchmarks/` — G2, NNGroup 데이터
- `analysis/g2_compare.py` — 테마 일치율, Kendall Tau, 감정 분포
- `review/generator.py` — 세션 종료 후 리뷰 생성
- `configs/personas/` — 30개 페르소나 YAML

---

## 구현 단계

### Phase 1: 페르소나 프롬프트 설계

페르소나 YAML → 시스템 프롬프트 텍스트 변환기 구현.

```
입력: configs/personas/benchmark/b005.yaml
출력: persona_prompts/b005.txt
```

프롬프트 구조:
```
당신은 {name}({age}세, {role})입니다.

[성격]
{Big Five 기반 성격 묘사}
탐색 성향: {exploration_tendency}/1.0
오류 허용: {error_tolerance}회
만족 기준: {satisficing_threshold}/1.0

[배경]
직업: {role}
디지털 능력: {digital_literacy}/4
이전 경험: {prior_tools}

[목표]
{jtbd.primary_goal}

[행동 규칙]
- playwright-cli를 사용해서 브라우저를 조작하세요
- 매 행동 전에 현재 감정 상태를 [감정: ...] 형식으로 먼저 말하세요
- 제품에 관대하지 마세요. 불편하면 솔직하게 표현하세요
- 너무 어렵거나 좌절하면 포기해도 됩니다
- 스크린샷 대신 snapshot을 사용하세요
- {prior_tools}와 항상 비교하면서 사용하세요
- 사용하지 않은 기능에 대해 추측하지 마세요

[현재 감정 상태]
pleasure: {pad.p}, arousal: {pad.a}, dominance: {pad.d}
(이 값은 매 행동 후 시스템이 업데이트합니다)

[시작]
{product_url}에 접속해서 {jtbd.primary_goal}을 달성해보세요.
playwright-cli open {product_url} 으로 시작하세요.
```

### Phase 2: 감정 파이프라인 (stream 주입)

훅 불필요. 오케스트레이터가 stdout을 읽고 stdin으로 감정 상태를 주입.

`emotion_engine.py` (기존 layer3_emotion/engine.py 재사용):
1. 에이전트 턴 출력에서 액션 성공/실패 파싱
2. OCC 이벤트 분류 → PAD delta 계산 → SDE noise 추가
3. 이탈 판정 (pleasure < threshold? error_count > tolerance?)
4. stdin에 감정 업데이트 메시지 write

### Phase 3: 실험 오케스트레이터 (stream-json)

`experiment.py` — 장수명 프로세스 + stdin/stdout 스트림:
```python
async def run_persona(persona_yaml, product_url):
    session_id = str(uuid.uuid4())
    prompt = generate_prompt(persona_yaml, product_url)

    # 장수명 프로세스 생성
    proc = await asyncio.create_subprocess_exec(
        "claude", "--print",
        "--input-format", "stream-json",
        "--output-format", "stream-json",
        "--session-id", session_id,
        "--allowedTools", "Bash(playwright-cli:*)",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )

    # 턴 1: 페르소나 프롬프트 전송
    send_message(proc.stdin, prompt)

    # 스트림 루프
    pad = PADState(0, 0, 0)
    error_count = 0
    for turn in range(max_turns):
        # stdout에서 에이전트 턴 완료까지 읽기
        turn_output = await read_until_turn_complete(proc.stdout)

        # 액션 결과 파싱 + 감정 업데이트
        event = classify_event(turn_output)
        pad = emotion_update(event, pad, persona_yaml.params)

        # 이탈 판정
        should_quit, reason = check_abandonment(pad, error_count, persona_yaml.params)
        if should_quit:
            send_message(proc.stdin, f"[시스템] 당신은 지금 너무 지쳤습니다. 세션을 마무리하세요. 이유: {reason}")
            break

        # 감정 상태 주입
        send_message(proc.stdin, f"[감정 업데이트] pleasure={pad.p:.2f}, arousal={pad.a:.2f}, dominance={pad.d:.2f}")

    # 세션 종료 → 리뷰 생성
    send_message(proc.stdin, "세션이 끝났습니다. 이 제품에 대한 리뷰를 작성해주세요.")
    review = await read_until_turn_complete(proc.stdout)
    save_review(review, session_id)

async def run_experiment(config):
    personas = load_personas(config)
    semaphore = asyncio.Semaphore(config.concurrency)
    async def limited(p):
        async with semaphore:
            return await run_persona(p, config.product_url)
    await asyncio.gather(*[limited(p) for p in personas])
```

### Phase 4: 데이터 수집 + 리뷰 생성

Claude CLI `-p`의 출력에서 추출할 것:
- 매 턴의 `[감정: ...]` 태그 → 감정 궤적
- playwright-cli 명령어 → 행동 로그
- 최종 발언 → 이탈 이유 또는 완료 평가

세션 종료 후 별도 LLM 콜로 G2 스타일 리뷰 생성:
```json
{
  "rating": 3.5,
  "likes": ["No signup required", "템플릿이 다양함"],
  "dislikes": ["전부 영어", "조건부 로직이 단순"],
  "review_text": "...",
  "would_recommend": false
}
```

### Phase 5: G2 비교 + 정량 지표

기존 `analysis/g2_compare.py` 재사용:
- 테마 일치율 (Jaccard)
- 테마 순위 상관 (Kendall Tau)
- 감정 분포 비교 (L1 distance)

필터: 온보딩/첫인상 테마만 비교 (단일 세션 한계)

---

## 대안: Agent SDK

CLI `-p` + 훅 대신 Anthropic Agent SDK를 쓰는 옵션도 있다:

```python
from claude_agent_sdk import Agent, Tool

agent = Agent(
    model="claude-sonnet-4-20250514",
    system_prompt=persona_prompt,  # 시스템 프롬프트 완전 교체 가능
    tools=[playwright_cli_tool, emotion_update_tool],
    max_turns=30,
)
```

| | CLI `-p` + 훅 | Agent SDK |
|---|---|---|
| 시스템 프롬프트 | append only | **완전 교체** |
| 턴별 감정 제어 | 훅으로 가능 | 콜백으로 가능 |
| playwright-cli | 네이티브 | 도구로 래핑 필요 |
| 구현 복잡도 | 낮음 | 중간 |
| 의존성 | Claude Code만 | SDK 추가 |

**결정**: 구현 시 CLI `-p` 먼저 시도. 시스템 프롬프트 append 제약이 문제가 되면 Agent SDK로 전환.

---

## 검증 계획

### 단계 1: 단일 페르소나 Tally 완주 (1일)
- 김도현(파워유저) → Tally에서 폼 생성 → 조건부 로직 설정 → 발행 시도
- 클릭 실패 0건, "/" 커맨드 메뉴 정상 작동 확인
- 감정 훅이 매 턴 PAD 업데이트하는지 확인

### 단계 2: 5명 병렬 실행 (0.5일)
- 5개 세그먼트 × 1명씩
- 분화 확인: PEOU/PU 분포, 이탈 스텝 차이

### 단계 3: 30명 실행 + G2 비교 (1일)
- 30명 × Tally × 15스텝
- 리뷰 생성 → G2 비교 스크립트
- 정량 지표 확보: Jaccard, Kendall Tau, 감정 분포

### 단계 4: 사업계획서 반영 (0.5일)
- 수치 삽입
- 데모 영상 캡처 (headless=false로 1명 실행)

---

## 일정 (D-8, 다음 주 수요일 제출)

| 날짜 | 작업 |
|---|---|
| 수 (오늘) | Phase 1-2: 프롬프트 생성기 + 감정 훅 |
| 목 | Phase 3: 오케스트레이터 + Phase 4: 데이터 수집 |
| 금 | 검증 단계 1-2: 단일 완주 + 5명 병렬 |
| 토-일 | 검증 단계 3: 30명 실행 + G2 비교 |
| 월 | 검증 단계 4: 사업계획서 수치 반영 |
| 화 | 최종 검토 + 제출 |

---

## 참고

### playwright-cli 핵심 명령어
```bash
playwright-cli open https://tally.so
playwright-cli snapshot                    # 접근성 트리 (ref 기반)
playwright-cli click e15                   # ref로 클릭
playwright-cli fill e5 "text"              # ref에 텍스트 입력
playwright-cli type "/"                    # 키보드 타이핑
playwright-cli press Enter                 # 키 입력
playwright-cli screenshot --filename=s.png # 스크린샷
playwright-cli close
```

### 해자 정리 — 핵심: 페르소나 리얼리티
| 계층 | 해자? | 설명 |
|---|---|---|
| 브라우저 자동화 | ❌ | playwright-cli에 위임. "제품 체험" 모드의 인프라일 뿐 |
| **페르소나 리얼리티 엔진** | **✅** | **OCC+SDE → PAD → LLM 제약. 감정·인지·의사결정 시뮬레이션의 깊이가 핵심 해자** |
| 페르소나 합성 방법론 | ✅ | Big Five → 15+ 파라미터, NNGroup 캘리브레이션 |
| 규모 + 자동화 | ✅ | 30명 병렬 실행 → 구조화된 데이터 |
| 정량 분석 | ✅ | G2 비교 (Jaccard, Kendall Tau, 감정 분포) |
| 적용 범위 확장성 | ✅ | 동일 엔진으로 서베이, A/B 테스트, 전문가 리뷰, 퍼널 분석 등 다양한 리서치 수행 |

### ablation 결과 요약
| 지표 | Full pipeline | Naive (단일 콜) |
|---|---|---|
| PU 범위 (박서연) | 0.3~0.5 | 0.6~0.8 |
| 이탈 위협 언급 | 4회 | 0회 |
| 매몰 비용 감정 | 자연 발생 | 없음 |
| sycophancy | 억제됨 | 제품에 관대 |
