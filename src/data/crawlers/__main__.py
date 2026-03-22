"""크롤러 CLI 진입점.

사용법:
    # G2 리뷰 크롤링 (browser-operator 필요)
    python -m shipcheck.data.crawlers g2 --product tally
    python -m shipcheck.data.crawlers g2 --product typeform --max-pages 20

    # NNGroup 벤치마크 크롤링 (Playwright)
    python -m shipcheck.data.crawlers nngroup
    python -m shipcheck.data.crawlers nngroup --no-headless

    # 전체 크롤링
    python -m shipcheck.data.crawlers all
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path

from .g2_crawler import PRODUCT_NAMES, crawl_g2_reviews
from .nngroup_crawler import crawl_nngroup_benchmarks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

DEFAULT_OUTPUT = Path(__file__).resolve().parents[3] / "data" / "benchmarks"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shipcheck.data.crawlers",
        description="Personica 벤치마크 데이터 크롤러",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- g2 (browser-operator 기반) --
    g2 = sub.add_parser("g2", help="G2 리뷰 크롤링 (browser-operator 필요)")
    g2.add_argument(
        "--product", "-p",
        required=True,
        choices=list(PRODUCT_NAMES.keys()),
        help="크롤링할 제품",
    )
    g2.add_argument("--max-pages", type=int, default=10, help="최대 페이지 수 (기본: 10)")
    g2.add_argument("--server-url", default="http://127.0.0.1:9002", help="browser-operator 서버 URL")
    g2.add_argument("--output-dir", "-o", type=Path, default=DEFAULT_OUTPUT, help="출력 디렉토리")

    # -- nngroup (Playwright 기반) --
    nn = sub.add_parser("nngroup", help="NNGroup 벤치마크 크롤링 (Playwright)")
    nn.add_argument("--no-headless", action="store_true", help="브라우저 표시")
    nn.add_argument("--output-dir", "-o", type=Path, default=DEFAULT_OUTPUT, help="출력 디렉토리")

    # -- all --
    a = sub.add_parser("all", help="전체 크롤링 (G2 tally + typeform + NNGroup)")
    a.add_argument("--max-pages", type=int, default=10, help="G2 최대 페이지 수")
    a.add_argument("--server-url", default="http://127.0.0.1:9002", help="browser-operator 서버 URL")
    a.add_argument("--no-headless", action="store_true", help="NNGroup 브라우저 표시")
    a.add_argument("--output-dir", "-o", type=Path, default=DEFAULT_OUTPUT, help="출력 디렉토리")

    return parser


def _run_g2(args: argparse.Namespace) -> None:
    """G2 크롤링 (동기 — browser-operator 사용)."""
    reviews = crawl_g2_reviews(
        product=args.product,
        max_pages=args.max_pages,
        output_dir=args.output_dir,
        server_url=args.server_url,
    )
    logger.info(f"완료: {len(reviews)}개 G2 리뷰 수집")

    if reviews:
        verified_count = sum(1 for r in reviews if r.verified)
        with_role = sum(1 for r in reviews if r.reviewer.role)
        with_industry = sum(1 for r in reviews if r.reviewer.industry)
        with_company_size = sum(1 for r in reviews if r.reviewer.company_size)
        rated = [r for r in reviews if r.ratings.overall]
        avg_rating = sum(r.ratings.overall for r in rated) / len(rated) if rated else 0

        logger.info(f"  평균 평점: {avg_rating:.1f}/5")
        logger.info(f"  Verified: {verified_count}/{len(reviews)}")
        logger.info(f"  Role 있음: {with_role}/{len(reviews)}")
        logger.info(f"  Industry 있음: {with_industry}/{len(reviews)}")
        logger.info(f"  Company Size 있음: {with_company_size}/{len(reviews)}")


async def _run_nngroup(args: argparse.Namespace) -> None:
    """NNGroup 크롤링 (비동기 — Playwright 사용)."""
    benchmarks = await crawl_nngroup_benchmarks(
        headless=not args.no_headless,
        output_dir=args.output_dir,
    )
    logger.info(f"완료: {len(benchmarks)}개 NNGroup 벤치마크 수집")

    if benchmarks:
        categories: dict[str, int] = {}
        for b in benchmarks:
            categories[b.category] = categories.get(b.category, 0) + 1
        for cat, count in sorted(categories.items()):
            logger.info(f"  {cat}: {count}개")


def _run_all(args: argparse.Namespace) -> None:
    """전체 크롤링."""
    logger.info("=== 전체 크롤링 시작 ===")

    # G2: Tally (동기)
    logger.info("\n--- G2: Tally ---")
    tally_reviews = crawl_g2_reviews(
        product="tally",
        max_pages=args.max_pages,
        output_dir=args.output_dir,
        server_url=args.server_url,
    )
    logger.info(f"Tally: {len(tally_reviews)}개 리뷰")

    # G2: Typeform (동기)
    logger.info("\n--- G2: Typeform ---")
    typeform_reviews = crawl_g2_reviews(
        product="typeform",
        max_pages=args.max_pages,
        output_dir=args.output_dir,
        server_url=args.server_url,
    )
    logger.info(f"Typeform: {len(typeform_reviews)}개 리뷰")

    # NNGroup (비동기)
    logger.info("\n--- NNGroup ---")
    benchmarks = asyncio.run(crawl_nngroup_benchmarks(
        headless=not args.no_headless,
        output_dir=args.output_dir,
    ))
    logger.info(f"NNGroup: {len(benchmarks)}개 벤치마크")

    total_reviews = len(tally_reviews) + len(typeform_reviews)
    logger.info(f"\n=== 완료: G2 {total_reviews}개 리뷰 + NNGroup {len(benchmarks)}개 벤치마크 ===")


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "g2":
        _run_g2(args)
    elif args.command == "nngroup":
        asyncio.run(_run_nngroup(args))
    elif args.command == "all":
        _run_all(args)


if __name__ == "__main__":
    main()
