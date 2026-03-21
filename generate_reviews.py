#!/usr/bin/env python3
"""JSONL 로그에서 G2 스타일 리뷰를 생성하는 스크립트."""

import json
import subprocess
import sys
import os
import glob
from pathlib import Path

REVIEW_PROMPT_TEMPLATE = """당신은 {persona_name}입니다. 방금 Tally.so라는 폼 빌더를 직접 사용해봤습니다.

아래는 당신이 제품을 사용하면서 느끼고 말한 것들입니다:

[당신의 경험]
{experience}

[감정 변화]
{emotion_trajectory}

이 경험을 바탕으로, G2(소프트웨어 리뷰 사이트)에 올릴 솔직한 리뷰를 작성하세요.

규칙:
- 직접 경험한 것만 쓰세요. 사용하지 않은 기능은 언급하지 마세요.
- 당신의 성격과 배경에 맞는 말투로 쓰세요.
- 과장하지 마세요. 솔직하게 쓰세요.
- AI가 쓴 티가 나지 않게, 실제 사용자처럼 자연스럽게 쓰세요.

아래 JSON 형식으로만 응답하세요. 다른 텍스트 없이 JSON만:
{{
  "rating": 3.5,
  "one_line": "한줄 요약",
  "likes": ["좋았던 점 1", "좋았던 점 2"],
  "dislikes": ["아쉬운 점 1", "아쉬운 점 2"],
  "review_text": "3~5문장의 전체 리뷰",
  "would_recommend": true,
  "switching_from": "이전에 쓰던 도구"
}}"""


def extract_experience(jsonl_path: str) -> dict:
    """JSONL에서 독백, 행동, 감정 변화를 추출."""
    persona_name = ""
    persona_id = ""
    segment = ""
    texts = []
    emotions = []
    actions = []

    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            event = entry.get("event", "")

            if event == "session_start":
                persona_name = entry.get("persona_name", "")
                persona_id = entry.get("persona_id", "")
                segment = entry.get("segment", "")

            elif event == "persona_text":
                texts.append(entry.get("text", ""))

            elif event == "action":
                cmd = entry.get("command", "")
                # playwright-cli 명령에서 핵심만 추출
                if "click" in cmd:
                    actions.append(f"클릭: {cmd.split('click ')[-1] if 'click ' in cmd else cmd}")
                elif "type" in cmd and "snapshot" not in cmd:
                    actions.append(f"입력: {cmd.split('type ')[-1] if 'type ' in cmd else cmd}")

            elif event == "step_result":
                pad = entry.get("pad", {})
                emotions.append({
                    "step": entry.get("step", "?"),
                    "pleasure": round(pad.get("pleasure", 0), 2),
                    "emotion": entry.get("emotion_label", "?"),
                    "load": entry.get("cognitive_load", 0),
                })

            elif event == "run_complete":
                pass  # 종료 정보

    return {
        "persona_name": persona_name,
        "persona_id": persona_id,
        "segment": segment,
        "texts": texts,
        "emotions": emotions,
        "actions": actions,
    }


def format_experience(data: dict) -> tuple[str, str]:
    """추출된 데이터를 프롬프트용 텍스트로 포맷."""
    # 독백 모음
    experience_lines = []
    for i, text in enumerate(data["texts"]):
        experience_lines.append(f"- {text}")

    experience = "\n".join(experience_lines)

    # 감정 궤적
    emotion_lines = []
    for e in data["emotions"]:
        emotion_lines.append(
            f"스텝 {e['step']}: pleasure={e['pleasure']}, "
            f"감정={e['emotion']}, 인지부하={e['load']}"
        )
    emotion_trajectory = "\n".join(emotion_lines) if emotion_lines else "감정 데이터 없음"

    return experience, emotion_trajectory


def generate_review(jsonl_path: str, output_dir: str) -> dict | None:
    """하나의 JSONL 파일에서 리뷰 생성."""
    data = extract_experience(jsonl_path)

    if not data["texts"]:
        print(f"  ⚠ {jsonl_path}: 독백 없음, 스킵")
        return None


    experience, emotion_trajectory = format_experience(data)

    prompt = REVIEW_PROMPT_TEMPLATE.format(
        persona_name=data["persona_name"],
        experience=experience,
        emotion_trajectory=emotion_trajectory,
    )

    print(f"  🔄 {data['persona_name']} ({data['segment']}) 리뷰 생성 중...")

    try:
        result = subprocess.run(
            ["claude", "--print", "--model", "claude-opus-4-6[1m]", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            print(f"  ❌ LLM 호출 실패: {result.stderr[:200]}")
            return None

        # JSON 추출
        output = result.stdout.strip()
        # JSON 블록 찾기
        start = output.find("{")
        end = output.rfind("}") + 1
        if start == -1 or end == 0:
            print(f"  ❌ JSON 파싱 실패: {output[:200]}")
            return None

        review = json.loads(output[start:end])
        review["persona_name"] = data["persona_name"]
        review["persona_id"] = data["persona_id"]
        review["segment"] = data["segment"]
        review["source_file"] = os.path.basename(jsonl_path)
        review["total_monologues"] = len(data["texts"])
        review["total_steps"] = len(data["emotions"])

        # 저장
        os.makedirs(output_dir, exist_ok=True)
        review_path = os.path.join(output_dir, f"{data['persona_id']}_review.json")
        with open(review_path, "w", encoding="utf-8") as f:
            json.dump(review, f, ensure_ascii=False, indent=2)

        print(f"  ✅ {data['persona_name']}: ★{review.get('rating', '?')} — {review.get('one_line', '')}")
        return review

    except subprocess.TimeoutExpired:
        print(f"  ❌ 타임아웃")
        return None
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON 파싱 에러: {e}")
        return None


def main():
    # 인자로 파일 지정 또는 최신 실험 자동 탐색
    if len(sys.argv) > 1:
        jsonl_files = sys.argv[1:]
    else:
        # 최근 실험 파일 자동 탐색 (b0XX_exp_ 패턴)
        jsonl_files = sorted(glob.glob("runs/experiment/b*_exp_*.jsonl"))
        if not jsonl_files:
            print("JSONL 파일을 찾을 수 없습니다. 경로를 인자로 지정하세요.")
            sys.exit(1)

        # 같은 페르소나의 가장 최신 파일만
        latest = {}
        for f in jsonl_files:
            pid = os.path.basename(f).split("_")[0]
            latest[pid] = f  # 정렬되어 있으므로 마지막이 최신
        jsonl_files = list(latest.values())

    output_dir = "runs/reviews"
    print(f"\n📝 리뷰 생성 — {len(jsonl_files)}명 (Opus, 병렬)")
    print(f"   출력: {output_dir}/\n")

    from concurrent.futures import ThreadPoolExecutor, as_completed
    reviews = []
    with ThreadPoolExecutor(max_workers=30) as pool:
        futures = {pool.submit(generate_review, f, output_dir): f for f in jsonl_files}
        for future in as_completed(futures):
            review = future.result()
            if review:
                reviews.append(review)

    # 요약
    print(f"\n{'='*60}")
    print(f"리뷰 생성 완료 — {len(reviews)}개")
    print(f"{'='*60}")
    for r in reviews:
        print(f"  {r['persona_name']:10s} ({r['segment']:8s}) ★{r.get('rating', '?'):4} | {r.get('one_line', '')}")

    # 전체 리뷰 요약 파일
    summary_path = os.path.join(output_dir, "all_reviews.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    print(f"\n📁 전체 리뷰: {summary_path}")


if __name__ == "__main__":
    main()
