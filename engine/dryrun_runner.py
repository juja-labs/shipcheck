#!/usr/bin/env python3
"""드라이런 실행기 — Claude CLI를 subprocess로 실행하고 실시간 파싱."""

import json
import subprocess
import sys
import time
from pathlib import Path

ENGINE_DIR = Path(__file__).parent
SESSION_ID = f"dryrun_{int(time.time())}"
PERSONA = "configs/personas/benchmark/b001.yaml"
PRODUCT_URL = "https://tally.so"
PRODUCT_NAME = "Tally"
MAX_TURNS = 50
MODEL = "sonnet"
MAX_STEPS = 5


def main():
    # 1. 세션 초기화
    print("=== 세션 초기화 ===")
    init = subprocess.run(
        ["python3", "-m", "shipcheck.tools.session_init",
         "--persona", PERSONA,
         "--product-url", PRODUCT_URL,
         "--product-name", PRODUCT_NAME,
         "--session-id", SESSION_ID],
        cwd=str(ENGINE_DIR), capture_output=True, text=True,
    )
    print(init.stdout.strip())

    # 2. 프롬프트 생성
    print("\n=== 프롬프트 생성 ===")
    from shipcheck.prompt_builder import build_system_prompt
    system_prompt = build_system_prompt(
        persona_yaml_path=PERSONA,
        session_id=SESSION_ID,
        product_url=PRODUCT_URL,
        product_name=PRODUCT_NAME,
        engine_dir=str(ENGINE_DIR),
        output_dir="runs/dryrun",
        max_steps=MAX_STEPS,
    )
    print(f"프롬프트 길이: {len(system_prompt)}자")

    # 3. Claude CLI subprocess 실행
    print(f"\n=== 드라이런 시작: {SESSION_ID} ===\n")

    user_msg = f"{PRODUCT_URL}을 사용하십시오. 세션 ID: {SESSION_ID}. playwright-cli open {PRODUCT_URL} 으로 시작하세요."
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
        cwd=str(ENGINE_DIR),
        text=True,
    )

    # stdin으로 유저 메시지 전송 후 닫기
    proc.stdin.write(stdin_json + "\n")
    proc.stdin.close()

    # 4. stdout 실시간 파싱
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
                    print(f"\n🗣️  {block['text']}")
                elif block.get("type") == "tool_use":
                    name = block.get("name", "")
                    inp = block.get("input", {})
                    if name == "Bash":
                        print(f"⚡ {inp.get('command', '')}")
                    elif name == "Skill":
                        print(f"📦 Skill: {inp.get('skill', '')}")
                    else:
                        print(f"🔧 {name}")

        elif t == "user":
            for block in msg.get("message", {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    content = str(block.get("content", ""))
                    # step_update 결과는 전체 표시
                    if "should_abandon" in content:
                        print(f"   → {content}")
                    elif len(content) > 200:
                        print(f"   → {content[:200]}...")
                    else:
                        print(f"   → {content}")

        elif t == "result":
            cost = msg.get("total_cost_usd", 0)
            turns = msg.get("num_turns", 0)
            stop = msg.get("stop_reason", "")
            print(f"\n{'='*50}")
            print(f"완료: {turns}턴, ${cost:.2f}, stop={stop}")

    proc.wait()


if __name__ == "__main__":
    main()
