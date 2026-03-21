#!/usr/bin/env python3
"""실험 실행기 — 여러 페르소나를 병렬로 돌리고 실시간 웹 대시보드 제공.

dryrun_runner.py의 로직을 내장하여, CLI 인자를 동일하게 유지한 채
여러 페르소나를 동시에 실행합니다.
"""

import argparse
import json
import subprocess
import sys
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
PERSONA_DIRS = [
    ROOT / "configs" / "personas" / "generated",
    ROOT / "configs" / "personas" / "benchmark",
]

DEFAULT_PERSONAS = [
    "b001","b002","b003","b004","b005","b006","b007","b008","b009","b010",
    "b011","b012","b013","b014","b015","b016","b017","b018","b019","b020",
    "b021","b022","b023","b024","b025","b026","b027","b028","b029","b030",
]
PRODUCT_URL = "https://tally.so"
PRODUCT_NAME = "Tally"
MAX_TURNS = 0
MODEL = "claude-opus-4-6[1m]"
MAX_STEPS = 999
MAX_DURATION_SEC = 3600  # 1시간 타임아웃


def parse_args():
    p = argparse.ArgumentParser(description="ShipCheck 실험 실행")
    p.add_argument("--personas", default=",".join(DEFAULT_PERSONAS),
                   help="콤마로 구분된 페르소나 ID (기본: b001,b002,b004,b020,b023)")
    p.add_argument("--max-steps", type=int, default=MAX_STEPS)
    p.add_argument("--port", type=int, default=8765, help="대시보드 포트")
    p.add_argument("--no-dashboard", action="store_true")
    return p.parse_args()


# ──────────────────────────────────────────────
# 상태 저장 (스레드 간 공유)
# ──────────────────────────────────────────────
status = {}  # persona_id → dict


def find_persona_path(persona_id: str) -> Path:
    for d in PERSONA_DIRS:
        p = d / f"{persona_id}.yaml"
        if p.exists():
            return p
    return None


def load_persona_meta(persona_id: str) -> dict:
    path = find_persona_path(persona_id)
    if not path:
        return {"persona_id": persona_id, "name": persona_id, "segment": "unknown"}
    data = yaml.safe_load(path.read_text())
    return {
        "persona_id": persona_id,
        "name": data.get("name", persona_id),
        "segment": data.get("segment", "unknown"),
        "age": data.get("demographics", {}).get("age", ""),
        "occupation": data.get("demographics", {}).get("occupation", ""),
    }


# ──────────────────────────────────────────────
# 페르소나 실행 (dryrun_runner.py 로직 내장)
# ──────────────────────────────────────────────
def run_persona(persona_id: str, max_steps: int):
    """단일 페르소나 실행 — dryrun_runner.py와 동일한 CLI 인자 사용."""
    persona_file = find_persona_path(persona_id)
    persona_path = str(persona_file) if persona_file else f"configs/personas/benchmark/{persona_id}.yaml"
    session_id = f"exp_{persona_id}_{int(time.time())}"
    meta = load_persona_meta(persona_id)
    output_dir = "runs/experiment"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    status[persona_id] = {
        **meta,
        "status": "running",
        "start_time": time.time(),
        "steps": [],
        "messages": [],  # 대화 히스토리
        "current_step": -1,
        "current_emotion": "",
        "current_pleasure": 0.0,
        "last_text": "",
        "cost": 0,
    }

    # 1. 세션 초기화
    subprocess.run(
        ["python3", "-m", "src.tools.session_init",
         "--persona", persona_path,
         "--product-url", PRODUCT_URL,
         "--product-name", PRODUCT_NAME,
         "--session-id", session_id],
        cwd=str(ROOT), capture_output=True, text=True,
    )

    # 2. 프롬프트 생성
    sys.path.insert(0, str(ROOT))
    from src.prompt_builder import build_system_prompt
    system_prompt = build_system_prompt(
        persona_yaml_path=persona_path,
        session_id=session_id,
        product_url=PRODUCT_URL,
        product_name=PRODUCT_NAME,
        engine_dir=str(ROOT),
        output_dir=output_dir,
        max_steps=max_steps,
    )

    # 3. Claude CLI — 원본과 동일한 인자
    user_msg = f"{PRODUCT_URL}을 사용하십시오. 세션 ID: {session_id}. playwright-cli open {PRODUCT_URL} 으로 시작하세요."
    stdin_json = json.dumps({
        "type": "user",
        "message": {"role": "user", "content": user_msg},
    })

    proc = subprocess.Popen(
        ["claude", "--print", "--verbose",
         "--append-system-prompt", system_prompt,
         "--allowedTools", "Bash",
         "--max-turns", str(MAX_TURNS),
         "--model", MODEL,
         "--dangerously-skip-permissions",
         "--input-format", "stream-json",
         "--output-format", "stream-json"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=str(ROOT),
        text=True,
    )

    proc.stdin.write(stdin_json + "\n")
    proc.stdin.close()

    # 4. stdout 파싱 + JSONL 로그
    name = meta["name"]
    log_path = Path(output_dir) / f"{persona_id}_{session_id}.jsonl"
    log_f = open(log_path, "a", encoding="utf-8", buffering=1)  # line-buffered
    log_f.write(json.dumps({"event": "session_start", "timestamp": time.time(),
                             "session_id": session_id, "persona_id": persona_id,
                             "persona_name": name, "segment": meta.get("segment", "")},
                            ensure_ascii=False) + "\n")

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        t = msg.get("type")

        if t == "assistant":
            for block in msg.get("message", {}).get("content", []):
                if block.get("type") == "text":
                    text = block["text"]
                    status[persona_id]["last_text"] = text[:150]
                    status[persona_id]["messages"].append({"type": "text", "content": text})
                    log_f.write(json.dumps({"event": "persona_text", "timestamp": time.time(),
                                            "session_id": session_id, "text": text},
                                           ensure_ascii=False) + "\n")
                    short = text[:120].replace("\n", " ")
                    print(f"  [{name:10s}] {short}")

                elif block.get("type") == "tool_use":
                    inp = block.get("input", {})
                    bname = block.get("name", "")
                    if bname == "Bash":
                        cmd = inp.get("command", "")
                        if "playwright-cli" in cmd:
                            pw = cmd.split("playwright-cli", 1)[-1].strip()[:80]
                            status[persona_id]["messages"].append({"type": "action", "content": f"🎭 {pw}"})
                            log_f.write(json.dumps({"event": "action", "timestamp": time.time(),
                                                    "session_id": session_id, "command": cmd},
                                                   ensure_ascii=False) + "\n")
                            print(f"  [{name:10s}] 🎭 {pw[:60]}")
                        elif "step_update" in cmd:
                            pass  # 결과에서 출력
                        elif "session_end" in cmd:
                            status[persona_id]["messages"].append({"type": "system", "content": "🏁 세션 종료"})
                            print(f"  [{name:10s}] 🏁 세션 종료")

        elif t == "user":
            for block in msg.get("message", {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    content = str(block.get("content", ""))
                    if "should_abandon" in content:
                        try:
                            result = json.loads(content)
                            step = result.get("step", 0)
                            pad = result.get("pad", {})
                            emotion = result.get("emotion_label", "")
                            load = result.get("cognitive_load", 0)
                            abandon = result.get("should_abandon", False)
                            p_val = pad.get("pleasure", 0)

                            status[persona_id]["current_step"] = step
                            status[persona_id]["current_emotion"] = emotion
                            status[persona_id]["current_pleasure"] = p_val
                            status[persona_id]["steps"].append({
                                "step": step, "emotion": emotion,
                                "pleasure": p_val, "cognitive_load": load,
                                "abandon": abandon,
                            })

                            status[persona_id]["messages"].append({
                                "type": "emotion",
                                "content": f"📊 step {step} | {emotion} | P={p_val:+.2f} | load={load:.2f}",
                            })
                            log_f.write(json.dumps({"event": "step_result", "timestamp": time.time(),
                                                    "session_id": session_id, "step": step,
                                                    "pad": pad, "emotion_label": emotion,
                                                    "cognitive_load": load, "should_abandon": abandon,
                                                    "raw": result},
                                                   ensure_ascii=False) + "\n")
                            print(f"  [{name:10s}] 📊 step {step:2d} | {emotion:12s} | P={p_val:+.2f} | load={load:.2f} | abandon={abandon}")
                        except (json.JSONDecodeError, TypeError):
                            pass

        elif t == "result":
            status[persona_id]["cost"] = msg.get("total_cost_usd", 0)
            status[persona_id]["status"] = "completed"
            status[persona_id]["end_time"] = time.time()
            cost = msg.get("total_cost_usd", 0)
            turns = msg.get("num_turns", 0)
            log_f.write(json.dumps({"event": "run_complete", "timestamp": time.time(),
                                    "session_id": session_id, "total_turns": turns,
                                    "total_cost_usd": cost},
                                   ensure_ascii=False) + "\n")
            print(f"  [{name:10s}] ✅ 완료 ({turns}턴, ${cost:.2f})")

    proc.wait()
    if status[persona_id]["status"] != "completed":
        status[persona_id]["status"] = "completed"
        status[persona_id]["end_time"] = time.time()
    log_f.close()
    print(f"  [{name:10s}] 📁 {log_path}")


# ──────────────────────────────────────────────
# 대시보드
# ──────────────────────────────────────────────
def dashboard_html(port):
    html_path = ROOT / "dashboard.html"
    return html_path.read_text(encoding="utf-8")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(status, ensure_ascii=False).encode())
        elif self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self._html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass


# ──────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────
def kill_all_subprocesses():
    """실행 중인 claude CLI 프로세스 모두 종료."""
    import signal
    for s in status.values():
        proc = s.get("proc")
        if proc and proc.poll() is None:
            try:
                proc.send_signal(signal.SIGTERM)
            except Exception:
                pass


def main():
    import signal
    args = parse_args()
    persona_ids = [p.strip() for p in args.personas.split(",")]

    start_time = time.time()

    print(f"ShipCheck 실험 — {len(persona_ids)}명 × {PRODUCT_NAME}")
    print(f"  페르소나: {', '.join(persona_ids[:5])}{'...' if len(persona_ids) > 5 else ''}")
    print(f"  max_steps: {args.max_steps}")
    print(f"  타임아웃: {MAX_DURATION_SEC//60}분")
    print(f"  Ctrl+C로 언제든 중단 가능 (로그는 보존)")

    # 대시보드
    if not args.no_dashboard:
        Handler._html = dashboard_html(args.port)
        server = HTTPServer(("0.0.0.0", args.port), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"  대시보드: http://localhost:{args.port}")

    print()

    # Ctrl+C 핸들러
    shutdown_flag = threading.Event()

    def signal_handler(sig, frame):
        print(f"\n⚠ 강제 종료 요청 — 프로세스 정리 중...")
        shutdown_flag.set()
        kill_all_subprocesses()

    signal.signal(signal.SIGINT, signal_handler)

    # 병렬 실행
    threads = []
    for pid in persona_ids:
        if shutdown_flag.is_set():
            break
        t = threading.Thread(target=run_persona, args=(pid, args.max_steps))
        t.start()
        threads.append(t)
        time.sleep(2)  # CLI 초기화 겹침 방지

    # 1시간 타임아웃 또는 모든 스레드 완료 대기
    while True:
        elapsed = time.time() - start_time
        alive = [t for t in threads if t.is_alive()]

        if not alive:
            break
        if elapsed >= MAX_DURATION_SEC:
            print(f"\n⏰ {MAX_DURATION_SEC//60}분 타임아웃 — 프로세스 정리 중...")
            shutdown_flag.set()
            kill_all_subprocesses()
            for t in alive:
                t.join(timeout=10)
            break
        if shutdown_flag.is_set():
            for t in alive:
                t.join(timeout=10)
            break

        time.sleep(5)

    # 요약
    elapsed = time.time() - start_time
    completed = sum(1 for s in status.values() if s.get("done"))
    print(f"\n{'='*60}")
    print(f"실험 {'완료' if not shutdown_flag.is_set() else '중단'} — {completed}/{len(persona_ids)}명 완료, {elapsed/60:.1f}분 소요")
    print(f"{'='*60}")
    print(f"  {'이름':12s} {'세그먼트':18s} {'스텝':>4s} {'Pleasure':>9s} {'감정':12s} {'비용':>6s}")
    print(f"  {'-'*12} {'-'*18} {'-'*4} {'-'*9} {'-'*12} {'-'*6}")
    for s in status.values():
        steps = len(s.get("steps", []))
        p = s.get("current_pleasure", 0)
        print(f"  {s['name']:12s} {s['segment']:18s} {steps:4d} {p:+9.2f} {s.get('current_emotion',''):12s} ${s.get('cost',0):.2f}")

    print(f"\n📁 로그: runs/experiment/")

    # 대시보드 유지 (강제종료 아닌 경우)
    if not args.no_dashboard and not shutdown_flag.is_set():
        print(f"대시보드: http://localhost:{args.port} (Ctrl+C로 종료)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n종료.")


if __name__ == "__main__":
    main()
