"""NNGroup 벤치마크 크롤러.

NNGroup 공개 기사에서 UX 벤치마크 수치를 추출한다.
합성 페르소나 행동 패턴 검증 근거로 활용:
  - 연령별 사용성 차이
  - 바운스율/이탈 벤치마크
  - 텍스트 읽기 패턴
  - 온보딩/학습곡선 통계

사용법:
    python -m shipcheck.data.crawlers nngroup
"""

from __future__ import annotations

import asyncio
import logging
import random
import re
from pathlib import Path

from playwright.async_api import Page, async_playwright

from .models import NNGroupBenchmark, save_jsonl

logger = logging.getLogger(__name__)

# 크롤링 대상 기사 목록 — 무료 공개 기사 중 벤치마크 수치가 포함된 것
TARGET_ARTICLES: list[dict[str, str]] = [
    {
        "url": "https://www.nngroup.com/articles/usability-for-senior-citizens/",
        "category": "age_usability",
        "title": "Usability for Seniors",
    },
    {
        "url": "https://www.nngroup.com/articles/how-long-do-users-stay-on-web-pages/",
        "category": "bounce_rate",
        "title": "How Long Do Users Stay on Web Pages?",
    },
    {
        "url": "https://www.nngroup.com/articles/how-users-read-on-the-web/",
        "category": "reading_pattern",
        "title": "How Users Read on the Web",
    },
    {
        "url": "https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/",
        "category": "reading_pattern",
        "title": "F-Shaped Pattern For Reading Web Content",
    },
    {
        "url": "https://www.nngroup.com/articles/response-times-3-important-limits/",
        "category": "response_time",
        "title": "Response Times: The 3 Important Limits",
    },
    {
        "url": "https://www.nngroup.com/articles/how-little-do-users-read/",
        "category": "reading_pattern",
        "title": "How Little Do Users Read?",
    },
    {
        "url": "https://www.nngroup.com/articles/scrolling-and-attention/",
        "category": "attention",
        "title": "Scrolling and Attention",
    },
    {
        "url": "https://www.nngroup.com/articles/bounce-rate-defined/",
        "category": "bounce_rate",
        "title": "Bounce Rate Defined",
    },
    {
        "url": "https://www.nngroup.com/articles/top-10-mistakes-web-design/",
        "category": "usability_heuristic",
        "title": "Top 10 Mistakes in Web Design",
    },
    {
        "url": "https://www.nngroup.com/articles/task-success-rate/",
        "category": "task_success",
        "title": "Task Success Rate",
    },
    {
        "url": "https://www.nngroup.com/articles/error-rate/",
        "category": "error_rate",
        "title": "Error Rate",
    },
    {
        "url": "https://www.nngroup.com/articles/time-on-task/",
        "category": "task_time",
        "title": "Time on Task",
    },
]

# 숫자 + 단위 패턴 추출용 정규식
_STAT_PATTERNS = [
    # "43% slower", "20% of the text", "80% of their time"
    re.compile(r"(\d+\.?\d*)\s*%\s+(slower|faster|more|less|of (?:the |their )?[\w\s]+)", re.IGNORECASE),
    # "average of 5.59 seconds", "median of 10 seconds"
    re.compile(r"(?:average|median|mean)\s+(?:of\s+)?(\d+\.?\d*)\s*(seconds?|minutes?|%)", re.IGNORECASE),
    # "N out of N users", "N of N participants"
    re.compile(r"(\d+)\s+(?:out of|of)\s+(\d+)\s+(users?|participants?|people)", re.IGNORECASE),
    # "between 10 and 20 seconds"
    re.compile(r"between\s+(\d+\.?\d*)\s+and\s+(\d+\.?\d*)\s*(seconds?|minutes?|%)", re.IGNORECASE),
    # "44-45%", "10-20 seconds"
    re.compile(r"(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)\s*(seconds?|minutes?|%)", re.IGNORECASE),
    # "users read only 20%" 같은 핵심 통계
    re.compile(r"(?:users?|people|visitors?)\s+(?:read|scan|spend|view|click)\s+(?:only\s+)?(\d+\.?\d*)\s*%", re.IGNORECASE),
]

# 특정 키워드가 포함된 문장에서 벤치마크 추출
_BENCHMARK_KEYWORDS = [
    "success rate", "completion rate", "error rate", "bounce rate",
    "time on task", "task time", "average time", "median time",
    "slower", "faster", "abandon", "leave", "exit",
    "read", "scan", "scroll", "attention",
    "senior", "older", "elderly", "65",
    "age group", "age range",
]


def _extract_benchmarks_from_text(
    text: str,
    category: str,
    source_url: str,
    source_title: str,
) -> list[NNGroupBenchmark]:
    """기사 본문 텍스트에서 벤치마크 수치를 추출."""
    benchmarks: list[NNGroupBenchmark] = []
    sentences = re.split(r"[.!?]\s+", text)

    for sentence in sentences:
        # 벤치마크 키워드가 포함된 문장만 처리
        has_keyword = any(kw in sentence.lower() for kw in _BENCHMARK_KEYWORDS)
        if not has_keyword:
            continue

        for pattern in _STAT_PATTERNS:
            for match in pattern.finditer(sentence):
                groups = match.groups()

                # 값 파싱
                value = groups[0]
                try:
                    value = float(value)
                except ValueError:
                    pass

                # 단위 추정
                unit = ""
                full_match = match.group(0)
                if "%" in full_match:
                    unit = "%"
                elif "second" in full_match.lower():
                    unit = "seconds"
                elif "minute" in full_match.lower():
                    unit = "minutes"

                # 대상 집단 추정
                population = "all users"
                if any(w in sentence.lower() for w in ["senior", "older", "elderly", "65"]):
                    population = "65+ users"
                elif "young" in sentence.lower():
                    population = "young users"

                # 메트릭 이름 생성
                metric_name = re.sub(r"\s+", "_", sentence[:60].strip().lower())
                metric_name = re.sub(r"[^a-z0-9_]", "", metric_name)

                benchmarks.append(NNGroupBenchmark(
                    category=category,
                    metric_name=metric_name,
                    value=value,
                    unit=unit,
                    context=sentence.strip()[:500],
                    population=population,
                    source_url=source_url,
                    source_title=source_title,
                ))

    return benchmarks


async def _crawl_article(
    page: Page,
    article: dict[str, str],
) -> list[NNGroupBenchmark]:
    """단일 NNGroup 기사에서 벤치마크 추출."""
    url = article["url"]
    category = article["category"]
    title = article["title"]

    logger.info(f"[NNGroup] 크롤링: {title}")

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(random.uniform(2.0, 4.0))

        # 기사 본문 추출 — NNGroup은 article 태그 또는 main content 영역
        body_selectors = [
            "article",
            '[class*="article-body"]',
            '[class*="article-content"]',
            "main",
            '[role="main"]',
        ]

        body_text = ""
        for sel in body_selectors:
            el = page.locator(sel).first
            if await el.count() > 0:
                body_text = await el.inner_text()
                break

        if not body_text:
            body_text = await page.locator("body").inner_text()

        # 연구 연도 추출
        study_year = None
        year_match = re.search(r"(19|20)\d{2}", await page.locator("time, [class*='date']").first.inner_text()
                               if await page.locator("time, [class*='date']").first.count() > 0 else "")
        if year_match:
            study_year = year_match.group(0)

        benchmarks = _extract_benchmarks_from_text(body_text, category, url, title)

        # 연도 추가
        for b in benchmarks:
            b.study_year = study_year

        logger.info(f"  → {len(benchmarks)}개 벤치마크 추출")
        return benchmarks

    except Exception as e:
        logger.error(f"  기사 크롤링 실패 ({url}): {e}")
        return []


async def crawl_nngroup_benchmarks(
    headless: bool = True,
    output_dir: Path | None = None,
    articles: list[dict[str, str]] | None = None,
) -> list[NNGroupBenchmark]:
    """NNGroup 기사들에서 벤치마크 수치를 크롤링한다.

    Args:
        headless: 헤드리스 모드 여부
        output_dir: JSONL 저장 디렉토리
        articles: 크롤링할 기사 목록 (None이면 기본 목록 사용)

    Returns:
        NNGroupBenchmark 리스트
    """
    target_articles = articles or TARGET_ARTICLES
    all_benchmarks: list[NNGroupBenchmark] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
        )
        page = await context.new_page()

        for article in target_articles:
            benchmarks = await _crawl_article(page, article)
            all_benchmarks.extend(benchmarks)
            await asyncio.sleep(random.uniform(1.5, 3.5))

        await browser.close()

    # 저장
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[3] / "data" / "benchmarks"
    output_path = output_dir / "nngroup_benchmarks.jsonl"
    saved = save_jsonl(all_benchmarks, output_path)
    logger.info(f"[NNGroup] {saved}개 벤치마크 저장 → {output_path}")

    return all_benchmarks
