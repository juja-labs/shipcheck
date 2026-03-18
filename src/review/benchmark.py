"""벤치마크 비교 모듈 — 합성 리뷰 vs G2 리뷰 유사도 측정.

치팅 방지 원칙:
- G2 리뷰 내용을 페르소나 프롬프트에 주입하지 않음
- G2 리뷰어 인구통계 분포만 페르소나 생성에 반영 (동일 모집단 시뮬레이션)
- 비교는 사후적(post-hoc)으로만 수행
"""

from __future__ import annotations

import json
import logging
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 테마 추출
# ---------------------------------------------------------------------------

# G2 Tally 리뷰에서 관찰된 주요 테마 키워드 (구조적 패턴, 내용 아님)
THEME_KEYWORDS: dict[str, list[str]] = {
    "ease_of_use": [
        "easy to use", "user-friendly", "intuitive", "simple", "straightforward",
        "no coding", "effortless", "easy to set up", "easy setup",
    ],
    "free_tier": [
        "free", "free version", "free plan", "free tier", "freemium",
        "generous", "no cost", "without paying",
    ],
    "notion_like": [
        "notion", "notion-like", "notion style", "slash command",
        "like writing a document", "text-based",
    ],
    "conditional_logic": [
        "conditional logic", "logic", "conditional", "branching",
        "logic jumps", "conditional formatting",
    ],
    "integrations": [
        "integration", "zapier", "airtable", "notion", "google sheets",
        "slack", "webhook", "api", "make", "hubspot", "crm",
    ],
    "customer_support": [
        "support", "customer service", "responsive", "helpful",
        "support team", "jared",
    ],
    "design_quality": [
        "clean", "beautiful", "professional", "sleek", "minimalistic",
        "modern", "attractive", "looks amazing",
    ],
    "customization": [
        "customiz", "personali", "brand", "styling", "design flexibility",
        "fonts", "colors", "themes",
    ],
    "pricing_concern": [
        "expensive", "pricing", "cost", "price", "pay",
        "subscription", "affordable", "budget",
    ],
    "mobile_issues": [
        "mobile", "responsive", "phone", "screen size",
    ],
    "learning_curve": [
        "learning curve", "confusing", "complicated", "took a while",
        "hard to figure", "overwhelming",
    ],
    "comparison_google_forms": [
        "google forms", "google form", "g forms",
    ],
    "comparison_typeform": [
        "typeform", "type form",
    ],
}


@dataclass
class ThemeExtraction:
    """텍스트에서 추출한 테마와 빈도."""
    source: str  # "g2" | "synthetic"
    theme_counts: dict[str, int] = field(default_factory=dict)
    total_reviews: int = 0
    theme_rates: dict[str, float] = field(default_factory=dict)  # 비율 (0~1)


@dataclass
class ReviewComparison:
    """합성 vs G2 리뷰 비교 결과."""
    # 테마 비교
    g2_themes: ThemeExtraction
    synthetic_themes: ThemeExtraction
    theme_jaccard: float  # 테마 집합 Jaccard 유사도
    theme_correlation: float  # 테마 빈도 상관관계

    # 별점 비교
    g2_rating_mean: float
    g2_rating_std: float
    synthetic_rating_mean: float
    synthetic_rating_std: float
    rating_difference: float

    # 감정 톤 비교
    g2_sentiment_positive_rate: float  # likes가 dislikes보다 긴 비율
    synthetic_sentiment_positive_rate: float

    # 세그먼트별 비교 (있는 경우)
    segment_comparisons: dict[str, dict[str, Any]] = field(default_factory=dict)

    # 체리피킹 1:1 비교
    cherry_pick_comparisons: list[dict[str, Any]] = field(default_factory=list)


def extract_themes(
    reviews: list[dict[str, Any]],
    source: str,
    likes_field: str = "likes",
    dislikes_field: str = "dislikes",
) -> ThemeExtraction:
    """리뷰 텍스트에서 테마 추출.

    키워드 매칭 기반 — 각 리뷰에서 해당 테마 키워드가 1회 이상 등장하면 카운트.
    """
    theme_counts: dict[str, int] = defaultdict(int)
    total = len(reviews)

    for review in reviews:
        text = (
            (review.get(likes_field, "") or "")
            + " "
            + (review.get(dislikes_field, "") or "")
        ).lower()

        for theme, keywords in THEME_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                theme_counts[theme] += 1

    theme_rates = {
        theme: count / total if total > 0 else 0.0
        for theme, count in theme_counts.items()
    }

    return ThemeExtraction(
        source=source,
        theme_counts=dict(theme_counts),
        total_reviews=total,
        theme_rates=theme_rates,
    )


def _jaccard_similarity(set_a: set, set_b: set) -> float:
    """Jaccard 유사도."""
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def _pearson_correlation(x: list[float], y: list[float]) -> float:
    """Pearson 상관계수 (numpy 없이)."""
    n = len(x)
    if n < 2:
        return 0.0

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    std_x = (sum((xi - mean_x) ** 2 for xi in x)) ** 0.5
    std_y = (sum((yi - mean_y) ** 2 for yi in y)) ** 0.5

    if std_x * std_y == 0:
        return 0.0
    return cov / (std_x * std_y)


def compare_reviews(
    g2_reviews: list[dict[str, Any]],
    synthetic_reviews: list[dict[str, Any]],
    cherry_pick_pairs: list[dict[str, Any]] | None = None,
) -> ReviewComparison:
    """합성 리뷰와 G2 리뷰를 비교.

    Args:
        g2_reviews: G2에서 크롤링한 리뷰 목록
        synthetic_reviews: 합성 생성된 리뷰 목록
        cherry_pick_pairs: 1:1 비교 쌍 [{g2_review_id, synthetic_persona_id, match_reason}]
    """
    # 1. 테마 추출
    g2_themes = extract_themes(g2_reviews, "g2")
    syn_themes = extract_themes(synthetic_reviews, "synthetic")

    # 2. 테마 Jaccard 유사도 (등장한 테마 집합 비교)
    g2_present = {t for t, c in g2_themes.theme_counts.items() if c > 0}
    syn_present = {t for t, c in syn_themes.theme_counts.items() if c > 0}
    theme_jaccard = _jaccard_similarity(g2_present, syn_present)

    # 3. 테마 빈도 상관관계 (전체 테마에 대해 빈도 비교)
    all_themes = sorted(THEME_KEYWORDS.keys())
    g2_rates = [g2_themes.theme_rates.get(t, 0.0) for t in all_themes]
    syn_rates = [syn_themes.theme_rates.get(t, 0.0) for t in all_themes]
    theme_correlation = _pearson_correlation(g2_rates, syn_rates)

    # 4. 별점 비교
    g2_ratings = [r.get("ratings", {}).get("overall", 0) for r in g2_reviews if r.get("ratings", {}).get("overall")]
    syn_ratings = [r.get("overall_rating", 0) for r in synthetic_reviews if r.get("overall_rating")]

    g2_mean = sum(g2_ratings) / len(g2_ratings) if g2_ratings else 0.0
    g2_std = (sum((r - g2_mean) ** 2 for r in g2_ratings) / len(g2_ratings)) ** 0.5 if g2_ratings else 0.0
    syn_mean = sum(syn_ratings) / len(syn_ratings) if syn_ratings else 0.0
    syn_std = (sum((r - syn_mean) ** 2 for r in syn_ratings) / len(syn_ratings)) ** 0.5 if syn_ratings else 0.0

    # 5. 감정 톤 비교 (likes가 dislikes보다 긴 비율)
    g2_pos = sum(1 for r in g2_reviews if len(r.get("likes", "") or "") > len(r.get("dislikes", "") or ""))
    g2_pos_rate = g2_pos / len(g2_reviews) if g2_reviews else 0.0
    syn_pos = sum(1 for r in synthetic_reviews if len(r.get("likes", "") or "") > len(r.get("dislikes", "") or ""))
    syn_pos_rate = syn_pos / len(synthetic_reviews) if synthetic_reviews else 0.0

    # 6. 세그먼트별 비교
    segment_comparisons = _compare_by_segment(g2_reviews, synthetic_reviews)

    # 7. 체리피킹 1:1 비교
    cherry_results = []
    if cherry_pick_pairs:
        cherry_results = _cherry_pick_compare(g2_reviews, synthetic_reviews, cherry_pick_pairs)

    return ReviewComparison(
        g2_themes=g2_themes,
        synthetic_themes=syn_themes,
        theme_jaccard=round(theme_jaccard, 3),
        theme_correlation=round(theme_correlation, 3),
        g2_rating_mean=round(g2_mean, 2),
        g2_rating_std=round(g2_std, 2),
        synthetic_rating_mean=round(syn_mean, 2),
        synthetic_rating_std=round(syn_std, 2),
        rating_difference=round(abs(g2_mean - syn_mean), 2),
        g2_sentiment_positive_rate=round(g2_pos_rate, 3),
        synthetic_sentiment_positive_rate=round(syn_pos_rate, 3),
        segment_comparisons=segment_comparisons,
        cherry_pick_comparisons=cherry_results,
    )


def _compare_by_segment(
    g2_reviews: list[dict[str, Any]],
    synthetic_reviews: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """G2 리뷰어 역할과 합성 페르소나 역할별 테마 비교.

    G2 리뷰어 역할은 reviewer.role에서 추론 (heuristic).
    """
    # G2 역할 매핑 (heuristic)
    role_keywords = {
        "startup_founder": ["founder", "ceo", "co-founder", "cofounder", "owner"],
        "marketing_pro": ["marketing", "growth", "campaign"],
        "tech_professional": ["engineer", "developer", "it ", "product", "systems"],
        "educator_nonprofit": ["teacher", "professor", "education", "non-profit", "instructor"],
        "creative_freelancer": ["designer", "creator", "author", "coach", "freelance"],
    }

    def _classify_g2_role(reviewer: dict) -> str:
        role = (reviewer.get("role") or "").lower()
        for role_id, keywords in role_keywords.items():
            if any(kw in role for kw in keywords):
                return role_id
        return "small_biz_operator"  # 기본값

    g2_by_role: dict[str, list] = defaultdict(list)
    for r in g2_reviews:
        role_id = _classify_g2_role(r.get("reviewer", {}))
        g2_by_role[role_id].append(r)

    syn_by_role: dict[str, list] = defaultdict(list)
    for r in synthetic_reviews:
        syn_by_role[r.get("role_id", "unknown")].append(r)

    comparisons = {}
    for role_id in set(list(g2_by_role.keys()) + list(syn_by_role.keys())):
        g2_sub = g2_by_role.get(role_id, [])
        syn_sub = syn_by_role.get(role_id, [])

        if not g2_sub or not syn_sub:
            continue

        g2_th = extract_themes(g2_sub, f"g2_{role_id}")
        syn_th = extract_themes(syn_sub, f"syn_{role_id}")

        # 테마 상관
        all_themes = sorted(THEME_KEYWORDS.keys())
        g2_r = [g2_th.theme_rates.get(t, 0.0) for t in all_themes]
        syn_r = [syn_th.theme_rates.get(t, 0.0) for t in all_themes]

        comparisons[role_id] = {
            "g2_count": len(g2_sub),
            "synthetic_count": len(syn_sub),
            "g2_top_themes": sorted(g2_th.theme_rates.items(), key=lambda x: -x[1])[:5],
            "synthetic_top_themes": sorted(syn_th.theme_rates.items(), key=lambda x: -x[1])[:5],
            "theme_correlation": round(_pearson_correlation(g2_r, syn_r), 3),
        }

    return comparisons


def _cherry_pick_compare(
    g2_reviews: list[dict[str, Any]],
    synthetic_reviews: list[dict[str, Any]],
    pairs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """체리피킹 1:1 비교."""
    g2_by_id = {r.get("review_id"): r for r in g2_reviews}
    syn_by_id = {r.get("persona_id"): r for r in synthetic_reviews}

    results = []
    for pair in pairs:
        g2_r = g2_by_id.get(pair.get("g2_review_id"))
        syn_r = syn_by_id.get(pair.get("synthetic_persona_id"))
        if not g2_r or not syn_r:
            continue

        # 테마 비교
        g2_text = ((g2_r.get("likes", "") or "") + " " + (g2_r.get("dislikes", "") or "")).lower()
        syn_text = ((syn_r.get("likes", "") or "") + " " + (syn_r.get("dislikes", "") or "")).lower()

        g2_themes_set = set()
        syn_themes_set = set()
        for theme, keywords in THEME_KEYWORDS.items():
            if any(kw in g2_text for kw in keywords):
                g2_themes_set.add(theme)
            if any(kw in syn_text for kw in keywords):
                syn_themes_set.add(theme)

        results.append({
            "match_reason": pair.get("match_reason", ""),
            "g2_review_id": pair["g2_review_id"],
            "g2_reviewer": g2_r.get("reviewer", {}).get("name", ""),
            "g2_role": g2_r.get("reviewer", {}).get("role", ""),
            "synthetic_persona_id": pair["synthetic_persona_id"],
            "synthetic_role_id": syn_r.get("role_id", ""),
            "g2_rating": g2_r.get("ratings", {}).get("overall", 0),
            "synthetic_rating": syn_r.get("overall_rating", 0),
            "g2_themes": sorted(g2_themes_set),
            "synthetic_themes": sorted(syn_themes_set),
            "theme_overlap": sorted(g2_themes_set & syn_themes_set),
            "theme_jaccard": round(_jaccard_similarity(g2_themes_set, syn_themes_set), 3),
            "g2_likes_preview": (g2_r.get("likes", "") or "")[:200],
            "synthetic_likes_preview": (syn_r.get("likes", "") or "")[:200],
        })

    return results


# ---------------------------------------------------------------------------
# 체리피킹 매핑 — G2 리뷰어와 합성 페르소나의 프로필 매칭
# ---------------------------------------------------------------------------

CHERRY_PICK_PAIRS: list[dict[str, Any]] = [
    {
        "g2_review_id": "tally-review-12376444",
        "g2_reviewer_name": "Ashutosh J.",
        "g2_role": "Senior Manager",
        "synthetic_persona_id": "",  # 생성 후 매핑
        "target_role": "startup_founder",
        "target_segment": "cautious_methodical",
        "match_reason": "Senior Manager, Small-Biz, 체계적 평가 스타일",
    },
    {
        "g2_review_id": "tally-review-12414798",
        "g2_reviewer_name": "Martha F.",
        "g2_role": "Marketing Staff",
        "synthetic_persona_id": "",
        "target_role": "marketing_pro",
        "target_segment": "cautious_methodical",
        "match_reason": "Marketing Staff, Small-Biz, 기능 중심 상세 리뷰",
    },
    {
        "g2_review_id": "tally-review-11919921",
        "g2_reviewer_name": "Cole R.",
        "g2_role": "Member Systems Organizer",
        "synthetic_persona_id": "",
        "target_role": "tech_professional",
        "target_segment": "explorer",
        "match_reason": "Mid-Market IT, 매우 장문, 비교 기반 리뷰",
    },
    {
        "g2_review_id": "tally-review-11334694",
        "g2_reviewer_name": "Shamsul F.",
        "g2_role": "Assistant Professor",
        "synthetic_persona_id": "",
        "target_role": "tech_professional",
        "target_segment": "power_user",
        "match_reason": "Enterprise, 코더, 키보드 선호, 기술적 요구",
    },
    {
        "g2_review_id": "tally-review-11346363",
        "g2_reviewer_name": "Kareem E.",
        "g2_role": "Founder & Community Manager",
        "synthetic_persona_id": "",
        "target_role": "startup_founder",
        "target_segment": "agreeable",
        "match_reason": "가격 민감 Founder, 열정적이지만 가격 불만",
    },
    {
        "g2_review_id": "tally-review-12383941",
        "g2_reviewer_name": "Amanda M.",
        "g2_role": "(novice tone)",
        "synthetic_persona_id": "",
        "target_role": "small_biz_operator",
        "target_segment": "anxious",
        "match_reason": "Novice 톤, 서포트 의존, 학습곡선 언급",
    },
    {
        "g2_review_id": "tally-review-11861869",
        "g2_reviewer_name": "Frédéric C.",
        "g2_role": "Retired",
        "synthetic_persona_id": "",
        "target_role": "educator_nonprofit",
        "target_segment": "cautious_methodical",
        "match_reason": "비영리, 은퇴자, 예산 제약, Google Forms 대비",
    },
    {
        "g2_review_id": "tally-review-11337288",
        "g2_reviewer_name": "Brittany C.",
        "g2_role": "Founder and CEO",
        "synthetic_persona_id": "",
        "target_role": "creative_freelancer",
        "target_segment": "explorer",
        "match_reason": "CEO but creative use, Typeform 비교, 리드 생성",
    },
]


def load_g2_reviews(path: Path) -> list[dict[str, Any]]:
    """G2 리뷰 JSONL 로드."""
    reviews = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                reviews.append(json.loads(line))
    return reviews


def save_comparison_report(comparison: ReviewComparison, output_path: Path) -> None:
    """비교 결과를 JSON으로 저장."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = asdict(comparison)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    logger.info("비교 리포트 저장 → %s", output_path)


def print_comparison_summary(comp: ReviewComparison) -> str:
    """비교 결과 요약 텍스트."""
    lines = [
        "=" * 60,
        "  G2 vs Synthetic Review Benchmark Comparison",
        "=" * 60,
        "",
        f"  G2 Reviews: {comp.g2_themes.total_reviews}",
        f"  Synthetic Reviews: {comp.synthetic_themes.total_reviews}",
        "",
        "--- Theme Analysis ---",
        f"  Theme Jaccard Similarity: {comp.theme_jaccard:.3f}",
        f"  Theme Frequency Correlation: {comp.theme_correlation:.3f}",
        "",
        "  G2 Top Themes:",
    ]
    for theme, rate in sorted(comp.g2_themes.theme_rates.items(), key=lambda x: -x[1])[:7]:
        lines.append(f"    {theme}: {rate:.0%}")

    lines.append("")
    lines.append("  Synthetic Top Themes:")
    for theme, rate in sorted(comp.synthetic_themes.theme_rates.items(), key=lambda x: -x[1])[:7]:
        lines.append(f"    {theme}: {rate:.0%}")

    lines.extend([
        "",
        "--- Rating Analysis ---",
        f"  G2 Mean Rating: {comp.g2_rating_mean:.2f} (±{comp.g2_rating_std:.2f})",
        f"  Synthetic Mean Rating: {comp.synthetic_rating_mean:.2f} (±{comp.synthetic_rating_std:.2f})",
        f"  Rating Difference: {comp.rating_difference:.2f}",
        "",
        "--- Sentiment Tone ---",
        f"  G2 Positive Tone Rate: {comp.g2_sentiment_positive_rate:.0%}",
        f"  Synthetic Positive Tone Rate: {comp.synthetic_sentiment_positive_rate:.0%}",
    ])

    if comp.segment_comparisons:
        lines.extend(["", "--- Segment-level Comparison ---"])
        for role_id, data in comp.segment_comparisons.items():
            lines.append(f"  [{role_id}] G2: {data['g2_count']}, Syn: {data['synthetic_count']}, "
                         f"Corr: {data['theme_correlation']:.3f}")

    if comp.cherry_pick_comparisons:
        lines.extend(["", "--- Cherry-pick 1:1 Comparisons ---"])
        for cp in comp.cherry_pick_comparisons:
            lines.append(f"  {cp['g2_reviewer']} ({cp['g2_role']}) vs {cp['synthetic_persona_id']}")
            lines.append(f"    Rating: G2={cp['g2_rating']} vs Syn={cp['synthetic_rating']}")
            lines.append(f"    Theme Jaccard: {cp['theme_jaccard']:.3f}")
            lines.append(f"    Shared themes: {', '.join(cp['theme_overlap']) or 'none'}")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)
