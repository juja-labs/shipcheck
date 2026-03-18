"""세션 로그에서 후처리로 리뷰를 생성하는 스크립트.

Usage:
    cd engine && python scripts/generate_reviews_post.py runs/g2_validation_001
"""
import json
import sys
import subprocess
import os
from pathlib import Path


def load_persona(persona_id: str) -> dict:
    """페르소나 YAML 로드"""
    import yaml
    persona_dir = Path(__file__).parent.parent / "data" / "personas"
    path = persona_dir / f"{persona_id}.yaml"
    if not path.exists():
        return {"name": persona_id, "segment": "unknown"}
    with open(path) as f:
        return yaml.safe_load(f)


def generate_review_via_cli(session: dict, persona: dict) -> dict | None:
    """Claude CLI로 리뷰 생성"""
    name = persona.get("name", session["persona_id"])
    segment = session.get("segment", "unknown")
    pu = session["final_perceived_usefulness"]
    peou = session["final_perceived_ease_of_use"]
    pleasure = session["final_pad_pleasure"]
    steps = session["total_steps"]
    terminated = session["terminated_by"]
    hesitations = session["total_hesitations"]
    pages = session.get("unique_pages", 1)

    # 이탈 정보
    if terminated == "abandoned":
        termination_desc = f"step {session['abandonment_step']}에서 자발적으로 이탈함"
    else:
        termination_desc = f"{steps}스텝을 모두 사용함 (시간 제한)"

    # 감정 상태 요약
    if pleasure > 0.4:
        mood = "전반적으로 만족스러운 경험"
    elif pleasure > 0.1:
        mood = "괜찮지만 아쉬운 점이 있는 경험"
    elif pleasure > -0.1:
        mood = "중립적이거나 혼합된 경험"
    else:
        mood = "부정적인 경험"

    prompt = f"""당신은 "{name}"이라는 사람입니다. 방금 Tally.so라는 폼 빌더를 {steps}스텝 동안 직접 사용해봤습니다.

## 당신의 프로필
- 세그먼트: {segment}
- 디지털 리터러시: {session.get('digital_literacy', 3)}/4
- 성격: O={session.get('openness', 0.5):.1f}, C={session.get('conscientiousness', 0.5):.1f}, E={session.get('extraversion', 0.5):.1f}, A={session.get('agreeableness', 0.5):.1f}, N={session.get('neuroticism', 0.5):.1f}

## 사용 경험 요약
- 방문 페이지 수: {pages}개
- 망설임 횟수: {hesitations}회 / {steps}스텝
- 최종 인식된 유용성(PU): {pu:.2f}/1.0
- 최종 인식된 사용 편의성(PEOU): {peou:.2f}/1.0
- 최종 감정: {mood} (pleasure={pleasure:.2f})
- 종료: {termination_desc}

## 지시사항
위 경험을 바탕으로 G2 리뷰 사이트에 올릴 제품 리뷰를 작성하세요.
- 실제 체험한 것만 기반으로 작성 (사용하지 않은 기능은 언급하지 마세요)
- 당신의 성격과 디지털 리터러시에 맞는 어조로 작성
- 솔직하게 작성 (좋은 점과 나쁜 점 모두)

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{{"rating": 1.0에서 5.0 사이 (0.5 단위), "likes": ["좋았던 점 1", "좋았던 점 2"], "dislikes": ["아쉬운 점 1", "아쉬운 점 2"], "review_text": "전체 리뷰 2-4문장", "would_recommend": true 또는 false}}"""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--model", "sonnet", "--output-format", "json"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"  ⚠ LLM 실패: {name}")
            return None

        # JSON 파싱
        stdout = result.stdout.strip()
        # claude --output-format json은 {"result": "..."} 형태
        outer = json.loads(stdout)
        text = outer.get("result", stdout)

        # JSON 블록 추출
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        # { } 추출
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            review = json.loads(text[start:end])
            review["persona_id"] = session["persona_id"]
            review["persona_name"] = name
            review["segment"] = segment
            return review

        print(f"  ⚠ JSON 파싱 실패: {name}")
        return None

    except Exception as e:
        print(f"  ⚠ 에러: {name} — {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_reviews_post.py runs/g2_validation_001")
        sys.exit(1)

    run_dir = Path(sys.argv[1])
    sessions_path = run_dir / "sessions.jsonl"

    if not sessions_path.exists():
        print(f"sessions.jsonl 없음: {sessions_path}")
        sys.exit(1)

    # 세션 로드
    sessions = []
    with open(sessions_path) as f:
        for line in f:
            line = line.strip()
            if line:
                sessions.append(json.loads(line))

    print(f"총 {len(sessions)}개 세션에서 리뷰 생성 시작\n")

    # 리뷰 폴더 생성
    reviews_dir = run_dir / "reviews"
    reviews_dir.mkdir(exist_ok=True)

    reviews = []
    for i, session in enumerate(sessions):
        persona_id = session["persona_id"]
        persona = load_persona(persona_id)
        name = persona.get("name", persona_id)

        print(f"[{i+1}/{len(sessions)}] {name} ({session['segment']})...", end=" ", flush=True)

        review = generate_review_via_cli(session, persona)
        if review:
            # 저장
            review_path = reviews_dir / f"{persona_id}_tally.json"
            with open(review_path, "w") as f:
                json.dump(review, f, ensure_ascii=False, indent=2)
            reviews.append(review)
            print(f"✅ rating={review.get('rating', '?')}")
        else:
            print("❌")

    print(f"\n완료: {len(reviews)}/{len(sessions)}개 리뷰 생성 → {reviews_dir}")

    # 요약
    if reviews:
        ratings = [r["rating"] for r in reviews if "rating" in r]
        print(f"평균 rating: {sum(ratings)/len(ratings):.1f}")
        print(f"추천 비율: {sum(1 for r in reviews if r.get('would_recommend'))/len(reviews)*100:.0f}%")


if __name__ == "__main__":
    main()
