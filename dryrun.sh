#!/bin/bash
set -e

cd "$(dirname "$0")"

SESSION_ID="dryrun_$(date +%s)"
PERSONA="configs/personas/benchmark/b001.yaml"
PRODUCT_URL="https://tally.so"
PRODUCT_NAME="Tally"
MAX_TURNS=50
MODEL="sonnet"

echo "=== 세션 초기화 ==="
python3 -m src.tools.session_init \
  --persona "$PERSONA" \
  --product-url "$PRODUCT_URL" \
  --product-name "$PRODUCT_NAME" \
  --session-id "$SESSION_ID"

echo ""
echo "=== 프롬프트 생성 ==="
PROMPT_FILE="/tmp/shipcheck_${SESSION_ID}_prompt.txt"
python3 -c "
from src.prompt_builder import build_system_prompt
import os
prompt = build_system_prompt(
    persona_yaml_path='$PERSONA',
    session_id='$SESSION_ID',
    product_url='$PRODUCT_URL',
    product_name='$PRODUCT_NAME',
    engine_dir=os.getcwd(),
    output_dir='runs/dryrun',
    max_steps=5,
)
with open('$PROMPT_FILE', 'w') as f:
    f.write(prompt)
print(f'프롬프트 저장: $PROMPT_FILE ({len(prompt)}자)')
"

echo ""
echo "=== 드라이런 시작: $SESSION_ID ==="

USER_MSG="${PRODUCT_URL}을 사용하십시오. 세션 ID: ${SESSION_ID}. playwright-cli open ${PRODUCT_URL} 으로 시작하세요."

echo "{\"type\":\"user\",\"message\":{\"role\":\"user\",\"content\":\"${USER_MSG}\"}}" | \
claude --print \
  --verbose \
  --append-system-prompt "$(cat "$PROMPT_FILE")" \
  --allowedTools Bash \
  --max-turns "$MAX_TURNS" \
  --model "$MODEL" \
  --dangerously-skip-permissions \
  --input-format stream-json \
  --output-format stream-json 2>/dev/null | \
python3 stream_filter.py
