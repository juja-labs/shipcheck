#!/usr/bin/env python3
"""stream-json 출력에서 유의미한 내용만 실시간 출력."""

import json
import sys

for line in sys.stdin:
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
                    print(f"\n⚡ {inp.get('command', '')}")
                elif name == "Skill":
                    print(f"\n📦 Skill: {inp.get('skill', '')}")
                elif name == "Read":
                    print(f"\n📄 Read: {inp.get('file_path', '')}")
                else:
                    print(f"\n🔧 {name}: {json.dumps(inp, ensure_ascii=False)[:200]}")

    elif t == "user":
        for block in msg.get("message", {}).get("content", []):
            if isinstance(block, dict) and block.get("type") == "tool_result":
                content = block.get("content", "")
                if isinstance(content, str) and len(content) > 300:
                    content = content[:300] + "..."
                print(f"   → {content}")

    elif t == "result":
        cost = msg.get("total_cost_usd", 0)
        turns = msg.get("num_turns", 0)
        stop = msg.get("stop_reason", "")
        print(f"\n{'='*50}")
        print(f"완료: {turns}턴, ${cost:.2f}, stop={stop}")
