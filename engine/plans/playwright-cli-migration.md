# playwright-cli Migration Plan

## 배경

CDP 직접 호출(cdp_dom.py + dom_tree.py + cdp_actions.py + async_env.py = 760줄)로
브라우저 자동화를 구현했으나, playwright-cli가 이 모든 것을 안정적으로 제공.

### playwright-cli가 이미 해결하는 것
- **스냅샷**: 접근성 트리 + ref(e1, e2) 기반 요소 참조
- **클릭/타이핑**: ref 기반으로 정확한 요소 조작
- **"/" 커맨드**: `type "/"` → keydown+keyup 자연 발생 → SPA 프레임워크 인식
- **contenteditable**: `fill` / `type` 명령으로 안정적 동작
- **세션 관리**: `-s=mysession`으로 브라우저 세션 유지
- **스크린샷**: `screenshot --filename=path`

### 교체 대상 (760줄 → ~50줄)
```
삭제:
  browser/cdp_dom.py      (150줄) — DOMSnapshot + AXTree 병합
  browser/dom_tree.py     (180줄) — 필터링 + 인덱싱 + 직렬화
  browser/cdp_actions.py  (200줄) — CDP 좌표 + Playwright 액션
  browser/async_env.py    (230줄) — 위 3개 조합

신규:
  browser/playwright_cli_env.py (~50줄) — playwright-cli subprocess 래퍼
```

## 아키텍처 변경

### 현재 (CDP 하이브리드)
```
CDP: DOMSnapshot + AXTree → backendNodeId → 인덱스 직렬화
     ↓
LLM: [42] button "Create" → {"target": "42"}
     ↓
CDP: backendNodeId → scrollIntoView → getContentQuads → (x,y)
Playwright: page.mouse.click(x, y)
```

### 변경 (playwright-cli)
```
playwright-cli snapshot → 접근성 트리 (ref 기반)
     ↓
LLM: button "Create" [ref=e15] → {"ref": "e15", "action": "click"}
     ↓
playwright-cli click e15 → 끝
```

## 구현

### PlaywrightCliEnv 클래스
```python
class PlaywrightCliEnv:
    """playwright-cli subprocess 래퍼."""

    def __init__(self, session_name: str, headless: bool = True):
        self.session = session_name
        self.headless = headless

    async def open(self, url: str) -> str:
        """브라우저 열기 + URL 이동. 스냅샷 반환."""
        cmd = f"playwright-cli -s={self.session} open {url}"
        if self.headless:
            cmd += " --headless"  # 또는 환경변수로 제어
        return await self._run(cmd)

    async def snapshot(self) -> str:
        """현재 접근성 트리 스냅샷."""
        return await self._run(f"playwright-cli -s={self.session} snapshot")

    async def screenshot(self, path: str) -> None:
        """스크린샷 저장."""
        await self._run(f"playwright-cli -s={self.session} screenshot --filename={path}")

    async def click(self, ref: str) -> str:
        """ref 기반 클릭. 스냅샷 반환."""
        return await self._run(f"playwright-cli -s={self.session} click {ref}")

    async def fill(self, ref: str, text: str) -> str:
        """ref 기반 텍스트 입력."""
        return await self._run(
            f"playwright-cli -s={self.session} fill {ref} {shlex.quote(text)}"
        )

    async def type_text(self, text: str) -> str:
        """현재 포커스 요소에 타이핑."""
        return await self._run(
            f"playwright-cli -s={self.session} type {shlex.quote(text)}"
        )

    async def press(self, key: str) -> str:
        """키 입력."""
        return await self._run(f"playwright-cli -s={self.session} press {key}")

    async def scroll(self, direction: str = "down") -> str:
        """스크롤."""
        delta = 400 if direction == "down" else -400
        return await self._run(
            f"playwright-cli -s={self.session} mousewheel 0 {delta}"
        )

    async def go_back(self) -> str:
        return await self._run(f"playwright-cli -s={self.session} go-back")

    async def close(self) -> None:
        await self._run(f"playwright-cli -s={self.session} close")

    async def _run(self, cmd: str) -> str:
        """subprocess 실행 + 결과 반환."""
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode()
```

### session.py 변경
```python
# 현재
obs = await self.env._observe()
succeeded = await self.env._execute_action(action)

# 변경
snapshot_text = await self.env.snapshot()
screenshot_path = await self.env.screenshot(f"step_{idx}.png")

# 액션 실행
if action_type == "click":
    result = await self.env.click(ref)
elif action_type == "type":
    result = await self.env.type_text(text)
elif action_type == "fill":
    result = await self.env.fill(ref, text)
elif action_type == "press":
    result = await self.env.press(key)
elif action_type == "scroll":
    result = await self.env.scroll(direction)
```

### action_executor 프롬프트 변경
```
현재: Enhanced DOM Tree의 인덱스([0], [1], ...)를 사용하여 target을 지정
변경: 스냅샷의 ref(e1, e2, ...)를 사용하여 action을 지정

예시:
  스냅샷: button "Create a free form" [ref=e15]
  출력: {"action": "click", "ref": "e15"}

  스냅샷: textbox "Type a question" [ref=e22]
  출력: {"action": "fill", "ref": "e22", "value": "제품 만족도는?"}

  "/"를 입력할 때:
  출력: {"action": "type", "value": "/"}

  Enter를 누를 때:
  출력: {"action": "press", "value": "Enter"}
```

## 주의사항

1. **subprocess 오버헤드**: 명령당 ~50-100ms. 15스텝 × 3명령 = ~2-5초 추가. 무시 가능.
2. **스냅샷 파싱**: playwright-cli 출력에서 스냅샷 텍스트를 추출하는 파서 필요.
3. **headless 모드**: playwright-cli의 headless 지원 확인 필요.
4. **에러 핸들링**: subprocess exit code + stderr로 실패 감지.
5. **기존 CDP 코드**: deprecated 처리. 당장 삭제하지 않고 유지 (rollback 가능하도록).

## 일정

| 일 | 할 것 |
|---|---|
| 수(오늘) | PlaywrightCliEnv 구현 + session.py 연동 |
| 목 | Tally dry run → "/" 커맨드 + 블록 팔레트 + 조건부 로직 완주 |
| 금 | 30명 실행 + 리뷰 생성 |
| 주말 | G2 비교 수치 확보 |
| 월 | 사업계획서 반영 |
| 화 | 최종 검토 + 제출 |
