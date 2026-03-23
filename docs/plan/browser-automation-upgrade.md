# Browser Automation Upgrade Plan

## 배경

Personica의 "제품 체험" 모드에서 페르소나가 현실적인 리뷰를 생성하려면, 제품을 **에러 없이 충분히 사용**해야 한다. Playwright는 이 모드에서 쓰는 브라우저 자동화 인터페이스이며, 현재 접근성 스냅샷 기반으로 반복되는 엣지 케이스들이 리뷰 품질을 떨어뜨리고 있다.

## 현재 아키텍처

```
페르소나 LLM (스크린샷) → 감정 + 의도 ("파란 버튼 클릭")
액션 실행기 LLM (접근성 스냅샷 + 스크린샷) → Playwright 액션 실행
```

### 현재 스택
- `engine/shipcheck/browser/env.py` — BrowserEnv 클래스
- `page.locator('body').aria_snapshot()` — 접근성 트리 추출
- `page.get_by_role()` / `page.get_by_text()` — 요소 매칭
- `page.screenshot()` — 스크린샷 캡처

### parser.js → 접근성 스냅샷 전환 이력
- 초기: UXAgent의 parser.js 사용 → semantic-id가 `button1` 같은 무의미한 이름
- 1차 개선: Playwright 접근성 스냅샷으로 교체 → `button "Create a free form"` 같은 의미 있는 이름
- 효과: 클릭 실패가 세션당 3-5건 → 0-2건으로 감소

## 남은 문제들

### 1. contenteditable 타이핑 불가
Tally 에디터가 `<div contenteditable>` 사용 → 접근성 스냅샷에 input으로 안 잡힘 → `type` 액션 실패

### 2. LLM 출력의 role 파싱 에러
- `text "Form title"` → "text"는 유효한 ARIA role이 아님
- `textbox "≤"` → 특수문자가 selector parser에서 깨짐 (curly quotes는 수정 완료)

### 3. 이름 없는 요소 매칭
접근성 스냅샷에 `button` (이름 없음)만 있으면 → `.first`가 hidden file input을 잡는 문제 (필터링 로직 추가 완료, 하지만 근본적으로 이름 없는 요소 구분이 어려움)

### 4. SPA 페이지 전환 후 빈 스냅샷
React/Next.js 앱에서 라우팅 후 DOM이 아직 렌더되지 않은 시점에 스냅샷 → 빈 결과

### 5. 루프 감지 없음
같은 액션을 반복하다 이탈하는 패턴 → 현재 방지 메커니즘 없음

## browser-use 레퍼런스 분석

GitHub: https://github.com/browser-use/browser-use

### 핵심 아키텍처
```
CDP 4개 병렬 호출:
  1. DOM 스냅샷 (flattenedDocumentSnapshot)
  2. DOM 트리 (getDocument)
  3. 접근성 트리 (getFullAXTree)
  4. 레이아웃 메트릭스 (getLayoutTreeSnapshot)
      ↓
  Enhanced DOM Tree (병합)
      ↓
  DOMTreeSerializer (필터링 + 직렬화)
      ↓
  LLM에 전달
```

### 가져올 패턴 4가지

#### A. DOM + 접근성 트리 병합
- 접근성 트리에 없는 요소를 DOM에서 보완
- contenteditable, custom widget 등이 해결됨
- 구현 위치: `env.py`의 `_observe()`

#### B. ClickableElementDetector 5단계
```
1. CDP 이벤트 리스너 확인 (addEventListener)
2. 표준 태그 검사 (button, a, input, select, textarea)
3. 접근성 속성 확인 (role, tabindex, aria-*)
4. CSS cursor:pointer 확인
5. onclick 속성 확인
```
- 현재 접근성 스냅샷만으로 놓치는 클릭 가능 요소를 잡음
- 구현 위치: `env.py`에 새 메서드 `_detect_clickable_elements()`

#### C. 뷰포트 밖 요소 필터링
- bounding box로 화면 밖 요소 제거
- LLM 토큰 절약 + "보이지 않는 요소를 클릭하려는" 문제 방지
- 현재 `aria_snapshot()`은 전체 DOM의 접근성 트리를 반환 → 뷰포트 필터 없음
- 구현 위치: `_observe()`에서 직렬화 전 필터링

#### D. 루프 감지
- 최근 N개 액션을 비교하여 반복 패턴 감지
- 5/8/12회 반복 시 단계별 경고를 LLM 프롬프트에 주입
- 구현 위치: `session.py`에 `_detect_loop()` 추가

## 구현 계획

### Phase 1: CDP 직접 호출로 전환
```python
# 현재
snapshot = self._page.locator('body').aria_snapshot()

# 변경
cdp = self._page.context.new_cdp_session(self._page)
dom_snapshot = cdp.send("DOMSnapshot.captureSnapshot", {...})
ax_tree = cdp.send("Accessibility.getFullAXTree")
layout = cdp.send("DOMSnapshot.getLayoutTreeSnapshot", {...})
# → 병합하여 Enhanced DOM Tree 생성
```

### Phase 2: Enhanced DOM Tree 직렬화
- DOM 노드 + AX 노드를 backendNodeId로 병합
- 각 요소에 인덱스 부여: `[42] button "Create a free form" (visible, clickable)`
- 뷰포트 밖 요소 필터링
- 비가시 요소 (`display:none`, `visibility:hidden`, `opacity:0`) 제거

### Phase 3: 액션 실행 개선
```python
# 현재
locator = self._resolve_locator(target)  # get_by_role / get_by_text
locator.click()

# 변경
node = self._get_node_by_index(42)  # backendNodeId로 직접 접근
cdp.send("DOM.focus", {"backendNodeId": node.id})
cdp.send("Input.dispatchMouseEvent", {"x": node.center_x, "y": node.center_y, ...})
```

### Phase 4: 루프 감지 추가
- `session.py`에 최근 액션 히스토리 기반 반복 감지
- 반복 감지 시 실행기 프롬프트에 "이전과 다른 전략을 시도하라" 경고 주입

## 페르소나 파이프라인에 미치는 영향

**변경 없음.** 페르소나 LLM은 여전히 스크린샷만 보고 감정+의도를 생성. 액션 실행기 LLM의 입력이 접근성 스냅샷 YAML → Enhanced DOM Tree 텍스트로 바뀌지만, 역할은 동일.

```
[변경 없음] 페르소나: 스크린샷 → 감정 + "파란 버튼 클릭하고 싶다"
[변경됨]   실행기:   Enhanced DOM Tree + 스크린샷 → click [42]
[변경됨]   실행:     CDP Input.dispatchMouseEvent → 좌표 기반 클릭
```

## 검증 기준

1. Tally에서 "폼 생성 → 질문 추가 → 조건부 로직 설정 → 발행" 플로우를 1명이 에러 없이 완주
2. 30명 페르소나 실행 시 클릭 실패율 < 5%
3. G2 비교 지표: 테마 일치율 > 60%, Kendall Tau > 0.5

## 현재 완료된 것 (이 세션)

- [x] 페르소나 리얼리티 엔진 감정 파이프라인 (OCC + SDE + PAD)
- [x] parser.js → Playwright 접근성 스냅샷 전환
- [x] 스크린샷 VLM (페르소나: 스크린샷, 실행기: 스냅샷+스크린샷)
- [x] Ablation 테스트 (Full vs Naive — 파이프라인 가치 증명)
- [x] curly quotes 정규화 + file input 필터링
- [x] 페르소나 오염 정제 (b013, b030, b004)
- [x] G2 비교 스크립트 (Jaccard + Kendall Tau + 감정 분포)
- [x] 세션 종료 후 리뷰 생성 LLM 콜

## 다음 세션에서 할 것

- [ ] Phase 1: CDP 직접 호출 전환
- [ ] Phase 2: DOM + AX 병합 직렬화
- [ ] Phase 3: 인덱스 기반 액션 실행
- [ ] Phase 4: 루프 감지
- [ ] Tally 핵심 플로우 완주 테스트
- [ ] 30명 풀 실행 + G2 비교 → 정량 지표 도출

## 참고 파일

- `engine/shipcheck/browser/env.py` — BrowserEnv (수정 대상)
- `engine/shipcheck/runner/session.py` — SessionRunner
- `engine/shipcheck/prompts/action_executor.txt` — 실행기 프롬프트
- `engine/shipcheck/analysis/g2_compare.py` — G2 비교 스크립트
- `engine/data/benchmarks/g2_tally_reviews.jsonl` — G2 벤치마크 데이터
- `engine/data/benchmarks/nngroup_benchmarks.jsonl` — NNGroup 벤치마크
