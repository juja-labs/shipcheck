# Browser Automation Upgrade Plan (Updated)

## 현재 상태 (완료)

### 아키텍처
```
[스크린샷] + [페르소나 프롬프트]
    → LLM #1 (persona_react) → 감정 + 자연어 의도
         ↓
[의도] + [Enhanced DOM Tree (인덱스)] + [스크린샷]
    → LLM #2 (action_executor) → {"action": "click", "target": "42"}
         ↓
selector_map[42] → backendNodeId
    → CDP: scrollIntoView → getContentQuads → dispatchMouseEvent
```

### Phase 1-3 구현 완료 (CDP 기반)
- **cdp_dom.py**: DOMSnapshot + AXTree 병렬 추출, backendNodeId 병합
- **dom_tree.py**: 가시성/뷰포트 필터, 인터랙티브 감지, `[idx] role "name"` 직렬화
- **cdp_actions.py**: CDP Input.dispatchMouseEvent / Input.insertText 실행
- **async_env.py**: AsyncBrowserEnv (위 3개 조합)
- **session.py**: async 전환, 인덱스 기반 target 파싱

### dry run 결과 (Tally.so)
**이전 (접근성 스냅샷):**
- 클릭 실패: 3-5건/세션 (모달 오버레이, selector 파싱)
- contenteditable 타이핑: 불가
- 블록 팔레트: 열지 못함
- 조건부 로직: 한 번도 도달 못함

**CDP 전환 후:**
- 모달 내 템플릿 클릭: ✅
- contenteditable "/" 입력: ✅ (텍스트로 입력됨, 커맨드 메뉴 미트리거)
- 블록 팔레트 열기 ("+" 버튼): ✅
- Multiple Choice / Rating 블록 삽입: ✅
- "Type a question" contenteditable 입력: ✅
- "Delete this block" 클릭: ✅

## 남은 이슈 (다음 세션)

### 이슈 1: CDP → Playwright 하이브리드 전환 (우선순위 높음)
현재 `cdp_actions.py`가 CDP `Input.dispatchMouseEvent`와 `Input.insertText`를 직접 사용.

**문제**:
- `Input.insertText("/")`가 Tally 에디터에서 "/" 커맨드 메뉴를 트리거 못함
- CDP는 keydown/keyup 이벤트를 자연스럽게 발생시키지 않아서 SPA 프레임워크가 인식 못함

**해결**: CDP는 좌표 획득까지만, 실제 조작은 Playwright에 위임
```python
# 현재 (CDP 직접)
await cdp_session.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": cx, "y": cy, ...})

# 변경 (하이브리드)
cx, cy = await _get_element_center(cdp_session, backend_node_id)  # CDP로 좌표
await page.mouse.click(cx, cy)  # Playwright로 클릭

# 타이핑
await page.mouse.click(cx, cy)  # 포커스
await page.keyboard.type(text)   # Playwright 키보드 (keydown/keyup 자연 발생)
```

**장점**:
- `page.keyboard.type("/")` → keydown+keyup 발생 → Tally "/" 커맨드 메뉴 트리거
- Playwright의 auto-wait, 안정적 이벤트 시퀀스 활용
- cdp_actions.py가 훨씬 단순해짐

### 이슈 2: 페르소나 화면 인식 오류 (중간 우선순위)
step 4에서 이미 "Use this template" 클릭 성공 → step 5 스크린샷은 에디터인데,
페르소나가 "Use this template 버튼을 누르고 싶다"고 함 (이미 없는 버튼).

**원인**: LLM이 스크린샷보다 session_history의 감정 흐름에 끌려감
**해결**:
- 페르소나 프롬프트에 "스크린샷에 보이지 않는 요소를 클릭하려 하지 마십시오" 추가
- 또는 실행기에서 DOM에 없는 target → scroll fallback 대신 "대안 제시"

### 이슈 3: 루프 감지 (중간 우선순위)
같은 행동 반복 방지. 최근 5개 액션 비교 → 경고 주입.

### 이슈 4: rate limit 제어 (낮은 우선순위)
`asyncio.Semaphore`로 동시 LLM 호출 수 제한 (max 3).

## 파일 구조 (현재)

```
engine/shipcheck/browser/
├── env.py          ← 이전 (접근성 스냅샷 기반, deprecated)
├── async_env.py    ← 현재 (CDP Enhanced DOM Tree)
├── cdp_dom.py      ← DOMSnapshot + AXTree 병합
├── cdp_actions.py  ← CDP 액션 실행 → Playwright 하이브리드로 전환 예정
├── dom_tree.py     ← 필터링 + 인덱싱 + 직렬화
├── parser.js       ← deprecated (삭제 가능)
└── initscript.js   ← deprecated (삭제 가능)
```

## 일정 (사업계획서 제출: 다음주 수요일)

| 일 | 할 것 |
|---|---|
| 수 | cdp_actions.py → Playwright 하이브리드 전환 + "/" 커맨드 수정 |
| 목 | Tally 핵심 플로우 완주 검증 (폼 생성→질문→조건부 로직) |
| 금 | 30명 풀 실행 + 리뷰 생성 |
| 주말 | G2 비교 수치 확보 |
| 월 | 사업계획서 반영 |
| 화 | 최종 검토 + 제출 |

## 검증 기준

1. Tally.so에서 5명 페르소나가 각각 15스텝을 **클릭 실패 1건 이하**로 완주
2. "폼 생성 → 질문 추가 → 조건부 로직 탐색" 플로우를 최소 3명이 완주
3. G2 비교에서 테마 일치율 > 50%, 순위 상관 > 0.4
