"""G2 비교 분석 — 합성 리뷰 vs G2 실제 리뷰 테마/감정 비교.

온보딩/첫인상 테마만 필터링하여 비교.
메트릭: Jaccard similarity, Kendall Tau, 감정 분포 비교.

사용법:
  python -m shipcheck compare-g2 runs/g2_validation_001
"""

from __future__ import annotations

import json
import logging
import re
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from scipy.stats import kendalltau

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 테마 매핑 — 키워드 → 테마
# ---------------------------------------------------------------------------

THEME_KEYWORDS: dict[str, list[str]] = {
    "ease_of_use": ["easy", "simple", "intuitive", "쉽", "간단", "직관", "편리", "편하"],
    "free_tier": ["free", "no cost", "generous", "무료", "공짜", "무료 티어", "비용 없"],
    "design_quality": ["beautiful", "clean", "design", "깔끔", "예쁘", "디자인", "세련", "미니멀"],
    "conditional_logic": ["conditional", "logic", "branching", "조건", "로직", "분기", "조건부"],
    "integrations": ["integration", "zapier", "webhook", "연동", "통합", "인테그레이션", "웹훅"],
    "notion_like_ui": ["notion", "notion-like", "노션", "블록", "문서처럼"],
    "templates": ["template", "템플릿", "양식", "서식"],
    "customization": ["customize", "branding", "커스터마이징", "브랜딩", "커스텀", "맞춤"],
    "no_signup_required": ["signup", "no signup", "가입", "회원가입", "로그인"],
    "language_barrier": ["english", "language", "영어", "한국어", "언어", "번역"],
    "learning_curve": ["confusing", "hard", "혼란", "어렵", "복잡", "헷갈", "막막", "당황", "불친절"],
    "pricing_wall": ["expensive", "paid", "paywall", "유료", "결제", "가격", "비싸", "Pro"],
}

# 역방향 매핑: 키워드 → 테마 (검색 최적화)
_KEYWORD_TO_THEME: dict[str, str] = {}
for _theme, _keywords in THEME_KEYWORDS.items():
    for _kw in _keywords:
        _KEYWORD_TO_THEME[_kw] = _theme


# ---------------------------------------------------------------------------
# 데이터 로드
# ---------------------------------------------------------------------------

def load_g2_reviews(g2_path: Path) -> list[dict[str, Any]]:
    """G2 리뷰 JSONL 로드."""
    reviews = []
    with open(g2_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            reviews.append(json.loads(line))
    logger.info("G2 리뷰 %d개 로드: %s", len(reviews), g2_path)
    return reviews


def load_synthetic_reviews(run_dir: Path) -> list[dict[str, Any]]:
    """합성 리뷰 로드 — runs/{id}/reviews/*.json"""
    reviews_dir = run_dir / "reviews"
    if not reviews_dir.exists():
        logger.warning("합성 리뷰 디렉토리 없음: %s", reviews_dir)
        return []

    reviews = []
    for path in sorted(reviews_dir.glob("*.json")):
        if path.name == "all_reviews.json":
            continue  # 집계 파일 스킵
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            reviews.extend(data)
        else:
            reviews.append(data)

    # JSONL 형태도 지원
    jsonl_path = reviews_dir / "synthetic_reviews.jsonl"
    if jsonl_path.exists():
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    reviews.append(json.loads(line))

    logger.info("합성 리뷰 %d개 로드: %s", len(reviews), reviews_dir)
    return reviews


# ---------------------------------------------------------------------------
# 테마 추출
# ---------------------------------------------------------------------------

def extract_themes(text: str) -> set[str]:
    """텍스트에서 테마 키워드를 매칭하여 테마 집합 반환."""
    text_lower = text.lower()
    themes = set()
    for keyword, theme in _KEYWORD_TO_THEME.items():
        # 단어 경계 기반 매칭 (부분 매칭 방지)
        if re.search(r"\b" + re.escape(keyword) + r"\b", text_lower):
            themes.add(theme)
    return themes


def extract_themes_from_g2(review: dict[str, Any]) -> set[str]:
    """G2 리뷰에서 테마 추출 (likes + dislikes)."""
    text = (review.get("likes", "") or "") + " " + (review.get("dislikes", "") or "")
    return extract_themes(text)


def extract_themes_from_synthetic(review: dict[str, Any]) -> set[str]:
    """합성 리뷰에서 테마 추출 (likes + dislikes)."""
    likes = review.get("likes", "")
    dislikes = review.get("dislikes", "")
    # 리스트면 join
    if isinstance(likes, list):
        likes = " ".join(str(x) for x in likes)
    if isinstance(dislikes, list):
        dislikes = " ".join(str(x) for x in dislikes)
    text = (likes or "") + " " + (dislikes or "") + " " + (review.get("review_text", "") or "")
    return extract_themes(text)


# ---------------------------------------------------------------------------
# 테마 빈도 (순위용)
# ---------------------------------------------------------------------------

def compute_theme_distribution(
    reviews: list[dict[str, Any]],
    extractor: callable,
) -> Counter:
    """리뷰 목록에서 테마 빈도 카운트."""
    counter: Counter = Counter()
    for review in reviews:
        themes = extractor(review)
        for theme in themes:
            counter[theme] += 1
    return counter


# ---------------------------------------------------------------------------
# 메트릭 A: Jaccard Similarity
# ---------------------------------------------------------------------------

def jaccard_similarity(set_a: set, set_b: set) -> float:
    """두 집합의 Jaccard 유사도."""
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# 메트릭 B: Kendall Tau (테마 순위 상관)
# ---------------------------------------------------------------------------

def kendall_tau_correlation(
    dist_a: Counter,
    dist_b: Counter,
) -> tuple[float, float]:
    """두 테마 분포의 Kendall Tau 순위 상관 계수.

    Returns:
        (tau, p_value) — 모든 테마가 동일하면 NaN 대신 (0.0, 1.0) 반환.
    """
    # 양쪽에 등장한 모든 테마의 합집합
    all_themes = sorted(set(dist_a.keys()) | set(dist_b.keys()))
    if len(all_themes) < 2:
        return (0.0, 1.0)

    ranks_a = [dist_a.get(t, 0) for t in all_themes]
    ranks_b = [dist_b.get(t, 0) for t in all_themes]

    tau, p_value = kendalltau(ranks_a, ranks_b)

    # NaN 처리 (모든 값이 동일할 때)
    if tau != tau:  # NaN check
        tau = 0.0
    if p_value != p_value:
        p_value = 1.0

    return (tau, p_value)


# ---------------------------------------------------------------------------
# 메트릭 C: 감정 분포 비교
# ---------------------------------------------------------------------------

@dataclass
class SentimentDistribution:
    """감정 분포: 긍정/혼합/부정 비율."""
    positive: float = 0.0   # rating >= 4.5
    mixed: float = 0.0      # 3.0 <= rating < 4.5
    negative: float = 0.0   # rating < 3.0
    count: int = 0


def compute_sentiment_distribution(
    reviews: list[dict[str, Any]],
    rating_key: str = "overall_rating",
) -> SentimentDistribution:
    """리뷰 목록의 감정 분포 계산."""
    if not reviews:
        return SentimentDistribution()

    positive = 0
    mixed = 0
    negative = 0

    for review in reviews:
        rating = _extract_rating(review, rating_key)
        if rating is None:
            continue
        if rating >= 4.5:
            positive += 1
        elif rating >= 3.0:
            mixed += 1
        else:
            negative += 1

    total = positive + mixed + negative
    if total == 0:
        return SentimentDistribution()

    return SentimentDistribution(
        positive=round(positive / total, 3),
        mixed=round(mixed / total, 3),
        negative=round(negative / total, 3),
        count=total,
    )


def _extract_rating(review: dict[str, Any], rating_key: str) -> float | None:
    """리뷰에서 rating 추출. G2는 nested, 합성은 flat."""
    # 합성 리뷰: flat key
    if rating_key in review:
        val = review[rating_key]
        if isinstance(val, (int, float)):
            return float(val)

    # G2 리뷰: ratings.overall
    ratings = review.get("ratings", {})
    if isinstance(ratings, dict):
        overall = ratings.get("overall")
        if isinstance(overall, (int, float)):
            return float(overall)

    return None


def sentiment_distance(a: SentimentDistribution, b: SentimentDistribution) -> float:
    """두 감정 분포 간 L1 거리 (0=동일, 2=최대 차이)."""
    return abs(a.positive - b.positive) + abs(a.mixed - b.mixed) + abs(a.negative - b.negative)


# ---------------------------------------------------------------------------
# 전체 비교 파이프라인
# ---------------------------------------------------------------------------

@dataclass
class G2ComparisonResult:
    """G2 비교 분석 결과."""
    # 메트릭 A: Jaccard
    jaccard_theme_similarity: float = 0.0
    g2_themes: list[str] = field(default_factory=list)
    synthetic_themes: list[str] = field(default_factory=list)
    common_themes: list[str] = field(default_factory=list)
    g2_only_themes: list[str] = field(default_factory=list)
    synthetic_only_themes: list[str] = field(default_factory=list)

    # 메트릭 B: Kendall Tau
    kendall_tau: float = 0.0
    kendall_p_value: float = 1.0
    g2_theme_ranks: dict[str, int] = field(default_factory=dict)
    synthetic_theme_ranks: dict[str, int] = field(default_factory=dict)

    # 메트릭 C: 감정 분포
    g2_sentiment: dict[str, float] = field(default_factory=dict)
    synthetic_sentiment: dict[str, float] = field(default_factory=dict)
    sentiment_l1_distance: float = 0.0

    # 메타
    g2_review_count: int = 0
    synthetic_review_count: int = 0
    product_name: str = ""


def run_comparison(
    run_dir: Path,
    g2_path: Path | None = None,
    product_name: str | None = None,
) -> G2ComparisonResult:
    """전체 비교 파이프라인 실행.

    Args:
        run_dir: 실험 결과 디렉토리 (runs/{experiment_id})
        g2_path: G2 JSONL 경로. None이면 자동 탐색.
        product_name: 비교 대상 제품명. None이면 합성 리뷰에서 추출.
    """
    # G2 리뷰 로드
    if g2_path is None:
        g2_path = _find_g2_reviews(run_dir, product_name)
    g2_reviews = load_g2_reviews(g2_path)

    # 합성 리뷰 로드
    synthetic_reviews = load_synthetic_reviews(run_dir)
    if not synthetic_reviews:
        logger.warning("합성 리뷰가 없습니다.")
        return G2ComparisonResult()

    # 제품명 결정
    if product_name is None:
        product_name = synthetic_reviews[0].get("product_name", "unknown")

    # 제품명으로 G2 리뷰 필터
    g2_filtered = [
        r for r in g2_reviews
        if r.get("product_name", "").lower() == product_name.lower()
    ]
    if not g2_filtered:
        g2_filtered = g2_reviews  # 필터 결과 없으면 전체 사용
        logger.warning("제품명 '%s' 필터 결과 없음 — G2 전체 %d개 사용", product_name, len(g2_filtered))

    # --- 메트릭 A: Jaccard Similarity ---
    g2_theme_set: set[str] = set()
    for r in g2_filtered:
        g2_theme_set |= extract_themes_from_g2(r)

    synthetic_theme_set: set[str] = set()
    for r in synthetic_reviews:
        synthetic_theme_set |= extract_themes_from_synthetic(r)

    jaccard = jaccard_similarity(g2_theme_set, synthetic_theme_set)
    common = sorted(g2_theme_set & synthetic_theme_set)
    g2_only = sorted(g2_theme_set - synthetic_theme_set)
    synth_only = sorted(synthetic_theme_set - g2_theme_set)

    # --- 메트릭 B: Kendall Tau ---
    g2_dist = compute_theme_distribution(g2_filtered, extract_themes_from_g2)
    synth_dist = compute_theme_distribution(synthetic_reviews, extract_themes_from_synthetic)
    tau, p_val = kendall_tau_correlation(g2_dist, synth_dist)

    # --- 메트릭 C: 감정 분포 ---
    g2_sent = compute_sentiment_distribution(g2_filtered, "overall_rating")
    synth_sent = compute_sentiment_distribution(synthetic_reviews, "rating")
    sent_dist = sentiment_distance(g2_sent, synth_sent)

    result = G2ComparisonResult(
        jaccard_theme_similarity=round(jaccard, 3),
        g2_themes=sorted(g2_theme_set),
        synthetic_themes=sorted(synthetic_theme_set),
        common_themes=common,
        g2_only_themes=g2_only,
        synthetic_only_themes=synth_only,
        kendall_tau=round(tau, 3),
        kendall_p_value=round(p_val, 4),
        g2_theme_ranks=dict(g2_dist.most_common()),
        synthetic_theme_ranks=dict(synth_dist.most_common()),
        g2_sentiment={
            "positive": g2_sent.positive,
            "mixed": g2_sent.mixed,
            "negative": g2_sent.negative,
        },
        synthetic_sentiment={
            "positive": synth_sent.positive,
            "mixed": synth_sent.mixed,
            "negative": synth_sent.negative,
        },
        sentiment_l1_distance=round(sent_dist, 3),
        g2_review_count=len(g2_filtered),
        synthetic_review_count=len(synthetic_reviews),
        product_name=product_name,
    )

    return result


def _find_g2_reviews(run_dir: Path, product_name: str | None) -> Path:
    """G2 리뷰 JSONL 자동 탐색.

    탐색 우선순위:
    1. run_dir 내 g2_*.jsonl
    2. engine/data/benchmarks/g2_{product}_reviews.jsonl
    """
    # 1. run_dir 내부
    for p in run_dir.glob("g2_*.jsonl"):
        return p

    # 2. 벤치마크 디렉토리
    benchmarks_dir = Path(__file__).parent.parent.parent / "data" / "benchmarks"
    if product_name:
        product_lower = product_name.lower().replace(" ", "_")
        candidate = benchmarks_dir / f"g2_{product_lower}_reviews.jsonl"
        if candidate.exists():
            return candidate

    # 아무거나 첫 번째
    for p in sorted(benchmarks_dir.glob("g2_*_reviews.jsonl")):
        return p

    raise FileNotFoundError(
        f"G2 리뷰 JSONL을 찾을 수 없습니다. "
        f"run_dir={run_dir}, benchmarks_dir={benchmarks_dir}"
    )


# ---------------------------------------------------------------------------
# 콘솔 출력 + JSON 저장
# ---------------------------------------------------------------------------

def print_summary(result: G2ComparisonResult) -> None:
    """비교 결과를 콘솔에 출력."""
    print("\n" + "=" * 60)
    print(f"  G2 비교 분석: {result.product_name}")
    print(f"  G2 리뷰 {result.g2_review_count}개 vs 합성 리뷰 {result.synthetic_review_count}개")
    print("=" * 60)

    # A. Jaccard
    print(f"\n[A] Jaccard Theme Similarity: {result.jaccard_theme_similarity:.3f}")
    print(f"    공통 테마:   {', '.join(result.common_themes) or '(없음)'}")
    print(f"    G2 only:     {', '.join(result.g2_only_themes) or '(없음)'}")
    print(f"    Synthetic:   {', '.join(result.synthetic_only_themes) or '(없음)'}")

    # B. Kendall Tau
    print(f"\n[B] Kendall Tau:  tau={result.kendall_tau:.3f}, p={result.kendall_p_value:.4f}")
    print(f"    G2 테마 순위:       {result.g2_theme_ranks}")
    print(f"    Synthetic 테마 순위: {result.synthetic_theme_ranks}")

    # C. 감정 분포
    print(f"\n[C] Sentiment Distribution (L1 distance: {result.sentiment_l1_distance:.3f})")
    g2s = result.g2_sentiment
    ss = result.synthetic_sentiment
    print(f"    G2:        positive={g2s.get('positive', 0):.1%}  mixed={g2s.get('mixed', 0):.1%}  negative={g2s.get('negative', 0):.1%}")
    print(f"    Synthetic: positive={ss.get('positive', 0):.1%}  mixed={ss.get('mixed', 0):.1%}  negative={ss.get('negative', 0):.1%}")

    print("\n" + "=" * 60)


def save_result(result: G2ComparisonResult, run_dir: Path) -> Path:
    """비교 결과를 JSON으로 저장."""
    output_path = run_dir / "g2_comparison.json"
    output_path.write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2)
    )
    logger.info("G2 비교 결과 저장: %s", output_path)
    return output_path


# ---------------------------------------------------------------------------
# CLI 진입점
# ---------------------------------------------------------------------------

def compare_g2_cli(run_dir_str: str, g2_path_str: str | None = None) -> None:
    """CLI에서 호출되는 비교 실행 함수."""
    run_dir = Path(run_dir_str)
    if not run_dir.exists():
        print(f"Error: 디렉토리가 존재하지 않습니다: {run_dir}")
        return

    g2_path = Path(g2_path_str) if g2_path_str else None

    result = run_comparison(run_dir, g2_path=g2_path)
    output_path = save_result(result, run_dir)
    print_summary(result)
    print(f"\n결과 저장: {output_path}")
