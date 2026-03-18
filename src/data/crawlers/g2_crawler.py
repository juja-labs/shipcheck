"""G2 리뷰 크롤러.

browser-operator를 통해 로컬 Chrome으로 G2 리뷰를 수집한다.
봇 탐지 우회를 위해 실제 사용자 브라우저 + 검색 경유 네비게이션 사용.

리뷰어 프로필(role, company_size, industry 등)을 최대한 수집하여
합성 페르소나와의 비교 근거를 확보한다.

사전 조건:
    1. browser-operator 서버 실행 (cd browser-operator/server && npm run dev)
    2. Chrome에 browser-operator 확장 로드 + 연결
    3. G2에 로그인 상태 (Show More 접근 위해)

사용법:
    python -m shipcheck.data.crawlers g2 --product tally
    python -m shipcheck.data.crawlers g2 --product typeform --max-pages 20
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from .browser_client import BrowserClient, BrowserOperatorError
from .models import G2Ratings, G2Review, G2ReviewerProfile, save_jsonl

logger = logging.getLogger(__name__)

# G2 검색용 제품명 매핑
PRODUCT_NAMES: dict[str, str] = {
    "tally": "Tally",
    "typeform": "Typeform",
}

G2_BASE = "https://www.g2.com"


# JavaScript: Show More 버튼 모두 클릭
CLICK_SHOW_MORE_JS = r"""
(() => {
    const buttons = document.querySelectorAll('button');
    let count = 0;
    for (const b of buttons) {
        if (b.innerText.trim().toLowerCase().includes('show more')) {
            b.click();
            count++;
        }
    }
    return count;
})()
"""

# JavaScript: 페이지에서 리뷰 데이터를 한번에 추출
EXTRACT_REVIEWS_JS = r"""
(() => {
    try {
        const reviewEls = Array.from(document.querySelectorAll('[itemprop="review"]'));
        const reviews = reviewEls.map((el, idx) => {
            try {
                const fullText = el.innerText || "";
                const reviewId = el.id || "";

                // 평점
                let overall = null;
                const ratingEl = el.querySelector("[itemprop=ratingValue]");
                if (ratingEl) overall = parseFloat(ratingEl.getAttribute("content") || ratingEl.innerText) || null;
                if (!overall) {
                    const stars = el.querySelectorAll('svg[class*="star"], [class*="fill-yellow"]');
                    if (stars.length > 0) overall = stars.length;
                }

                // verified / incentivized
                const lowerText = fullText.toLowerCase();
                const verified = lowerText.includes('validated reviewer');
                const incentivized = lowerText.includes('incentivized');

                // 리뷰 본문
                const extractSection = (pattern) => {
                    const m = fullText.match(pattern);
                    if (!m) return "";
                    let val = m[1].trim();
                    val = val.split("Review collected by")[0].trim();
                    return val;
                };
                const likes = extractSection(
                    /What do you like best[^?]*\?([\s\S]+?)(?=What do you dislike|Recommendations|What problems|$)/i
                );
                const dislikes = extractSection(
                    /What do you dislike[^?]*\?([\s\S]+?)(?=What do you like|Recommendations|What problems|$)/i
                );
                const recommendations = extractSection(
                    /Recommendations to others[^:]*[:\n]([\s\S]+?)(?=What do you|What problems|$)/i
                );
                const problemsSolved = extractSection(
                    /What problems[\s\S]*?solving[^?]*\?([\s\S]+?)(?=What do you|Recommendations|$)/i
                );

                // 이전 도구
                const switchEl = el.querySelector('[class*="switch"], [class*="alternative"]');
                const switchFrom = switchEl ? switchEl.innerText.trim() : "";

                // ---- 리뷰어 프로필 ----
                let reviewerName = "", role = "", companySize = "", industry = "";
                const avatarEl = el.querySelector("[class*=avatar]");
                if (avatarEl) {
                    const container = avatarEl.closest("div[class*='elv-flex'][class*='elv-items-center']")
                        || avatarEl.parentElement?.parentElement;
                    if (container) {
                        const lines = container.innerText.trim().split("\n").map(l => l.trim()).filter(l => l);
                        const nonSize = [];
                        for (const line of lines) {
                            if (line.toLowerCase().includes("emp.") || line.toLowerCase().includes("employee")) {
                                companySize = line;
                            } else if (line.length <= 3 && /^[A-Z]+$/.test(line)) {
                                // avatar 모노그램 (이니셜) 건너뛰기
                            } else {
                                nonSize.push(line);
                            }
                        }
                        if (nonSize.length >= 1) reviewerName = nonSize[0];
                        if (nonSize.length >= 2) role = nonSize[1];
                        if (nonSize.length >= 3) industry = nonSize[2];
                    }
                }
                if (!reviewerName) {
                    const authorEl = el.querySelector("[itemprop=author]");
                    if (authorEl) reviewerName = authorEl.innerText.trim();
                }

                // 날짜
                let date = "";
                const labels = el.querySelectorAll("label");
                for (const l of labels) {
                    const t = l.innerText.trim();
                    if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(t)) { date = t; break; }
                }

                // 제목
                let title = "";
                const titleMatch = fullText.match(/\u201C([^\u201D]+)\u201D/);
                if (titleMatch) title = titleMatch[1];

                // 배지 메타데이터
                let timeUsed = "";
                for (const l of labels) {
                    if (l.innerText.trim().toLowerCase().includes('current user')) {
                        timeUsed = 'Current User'; break;
                    }
                }

                return {
                    review_id: reviewId, title, date, overall,
                    verified, incentivized,
                    likes, dislikes, recommendations,
                    problems_solved: problemsSolved,
                    switch_from: switchFrom,
                    reviewer: {
                        name: reviewerName, role, industry,
                        company_size: companySize, time_used: timeUsed,
                    },
                    sub_ratings: {},
                };
            } catch(e) { return { error: e.message, idx }; }
        });
        return { reviews, count: reviewEls.length };
    } catch(e) { return { topError: e.message }; }
})()
"""

# "Next ›" 링크 클릭으로 다음 페이지 이동
# href에 page= 포함된 링크 중 "next" 텍스트를 가진 것만 클릭
CLICK_NEXT_PAGE_JS = r"""
(() => {
    const links = document.querySelectorAll('a');
    // 1차: href에 page= 있고 텍스트에 next 포함
    for (const a of links) {
        const href = a.href || "";
        const text = a.innerText.trim().toLowerCase();
        if (href.includes('page=') && text.includes('next')) {
            a.scrollIntoView({behavior: 'instant', block: 'center'});
            a.click();
            return { clicked: true, href };
        }
    }
    // 2차: href에 page= 있고 SVG(화살표) 포함 + 현재 페이지 다음 번호
    const currentPage = new URLSearchParams(window.location.search).get('page') || '1';
    const nextPage = parseInt(currentPage) + 1;
    for (const a of links) {
        const href = a.href || "";
        if (href.includes('page=' + nextPage)) {
            a.scrollIntoView({behavior: 'instant', block: 'center'});
            a.click();
            return { clicked: true, href };
        }
    }
    return { clicked: false };
})()
"""

# 검색 결과에서 제품 리뷰 URL 찾기
FIND_PRODUCT_LINK_JS = r"""
((productName) => {
    const links = document.querySelectorAll('a');
    for (const a of links) {
        if (a.href.includes('/products/') && a.href.includes('/reviews') &&
            a.innerText.trim().toLowerCase() === productName.toLowerCase()) {
            return { found: true, href: a.href, text: a.innerText.trim() };
        }
    }
    return { found: false };
})
"""


def _parse_extracted_review(raw: dict, product_name: str, source_url: str) -> G2Review | None:
    """JavaScript에서 추출한 raw dict를 G2Review로 변환."""
    if "error" in raw:
        logger.warning(f"  리뷰 파싱 오류: {raw['error']}")
        return None

    r = raw.get("reviewer", {})
    reviewer = G2ReviewerProfile(
        name=r.get("name") or None,
        role=r.get("role") or None,
        company_size=r.get("company_size") or None,
        industry=r.get("industry") or None,
        time_used=r.get("time_used") or None,
    )

    ratings = G2Ratings(overall=raw.get("overall"))

    return G2Review(
        product_name=product_name,
        review_id=raw.get("review_id", ""),
        title=raw.get("title", ""),
        date=raw.get("date", ""),
        verified=raw.get("verified", False),
        incentivized=raw.get("incentivized", False),
        likes=raw.get("likes", ""),
        dislikes=raw.get("dislikes", ""),
        recommendations=raw.get("recommendations", ""),
        problems_solved=raw.get("problems_solved", ""),
        switch_from=raw.get("switch_from", ""),
        ratings=ratings,
        reviewer=reviewer,
        source_url=source_url,
    )


def _navigate_via_search(client: BrowserClient, tab_id: int, product: str) -> str | None:
    """G2 메인 → 검색 → 제품 리뷰 페이지로 자연스럽게 이동. 반환: 리뷰 페이지 URL."""
    product_name = PRODUCT_NAMES.get(product.lower(), product)

    # 1. G2 메인 (쿠키 세팅)
    logger.info(f"[G2] 메인 페이지로 이동...")
    client.navigate(f"{G2_BASE}", tabId=tab_id)
    client.wait(3.0, 5.0)

    # 2. 검색
    logger.info(f"[G2] '{product_name}' 검색...")
    client.navigate(f"{G2_BASE}/search?query={product_name}", tabId=tab_id)
    client.wait(3.0, 5.0)

    # 3. 쿠키 배너 닫기
    client.evaluate(r"""
        const btns = document.querySelectorAll('button');
        for (const b of btns) {
            const t = b.innerText.toLowerCase();
            if (t.includes('reject') || t.includes('거부') || t.includes('필수적이지')) {
                b.click(); break;
            }
        }
    """, tabId=tab_id)
    client.wait(1.0, 2.0)

    # 4. 제품 리뷰 링크 찾기 + 클릭
    result = client.evaluate(
        f'{FIND_PRODUCT_LINK_JS}("{product_name}")',
        tabId=tab_id,
    )

    if not result or not result.get("found"):
        logger.error(f"[G2] 검색 결과에서 '{product_name}' 제품을 찾지 못함")
        return None

    review_url = result["href"]
    logger.info(f"[G2] 제품 발견: {review_url}")

    # 링크 클릭으로 이동 (직접 URL 접근 대신)
    client.evaluate(f"""
        const links = document.querySelectorAll('a');
        for (const a of links) {{
            if (a.href === "{review_url}") {{ a.click(); break; }}
        }}
    """, tabId=tab_id)
    client.wait(4.0, 6.0)

    return review_url


def crawl_g2_reviews(
    product: str,
    max_pages: int = 10,
    output_dir: Path | None = None,
    server_url: str = "http://127.0.0.1:9002",
) -> list[G2Review]:
    """G2에서 제품 리뷰를 크롤링한다.

    검색 경유 네비게이션으로 봇 탐지 우회.
    Show More 버튼을 클릭하여 완전한 리뷰 텍스트 수집.

    Args:
        product: 제품명 (tally, typeform)
        max_pages: 최대 페이지 수
        output_dir: JSONL 저장 디렉토리
        server_url: browser-operator 서버 URL

    Returns:
        G2Review 리스트
    """
    if product.lower() not in PRODUCT_NAMES:
        raise ValueError(f"지원하지 않는 제품: {product}. 사용 가능: {list(PRODUCT_NAMES.keys())}")

    client = BrowserClient(server_url)

    if not client.is_ready():
        raise BrowserOperatorError(
            "browser-operator 서버가 준비되지 않았습니다.\n"
            "1) browser-operator/server 에서 npm run dev 실행\n"
            "2) Chrome에 확장 로드 + 연결 확인"
        )
    logger.info(f"[G2] browser-operator 연결됨 ({server_url})")

    # 새 탭에서 작업
    tab_id = client.new_tab()
    logger.info(f"[G2] 새 탭에서 작업 (tab_id={tab_id})")

    all_reviews: list[G2Review] = []

    try:
        # 검색 경유로 리뷰 페이지 도달
        review_url = _navigate_via_search(client, tab_id, product)
        if not review_url:
            logger.error("[G2] 리뷰 페이지 접근 실패")
            return all_reviews

        for page_num in range(1, max_pages + 1):
            logger.info(f"[G2] {product} 페이지 {page_num}/{max_pages}")

            try:
                # 스크롤해서 리뷰 로드
                for _ in range(3):
                    client.scroll_down(pixels=800, tabId=tab_id)
                    client.wait(1.0, 2.0)

                # Show More 버튼 클릭
                show_more_count = client.evaluate(CLICK_SHOW_MORE_JS, tabId=tab_id)
                if show_more_count:
                    logger.info(f"  Show More {show_more_count}개 클릭")
                    client.wait(2.0, 3.0)

                # 리뷰 추출
                result = client.evaluate(EXTRACT_REVIEWS_JS, tabId=tab_id)

                if not result or not isinstance(result, dict):
                    logger.warning(f"  페이지 {page_num}: 데이터 추출 실패")
                    break

                if "topError" in result:
                    logger.error(f"  JS 오류: {result['topError']}")
                    break

                raw_reviews = result.get("reviews", [])
                if not raw_reviews:
                    logger.info(f"  페이지 {page_num}에서 리뷰를 찾지 못함. 크롤링 종료.")
                    break

                page_count = 0
                for raw in raw_reviews:
                    review = _parse_extracted_review(raw, product, review_url)
                    if review:
                        all_reviews.append(review)
                        page_count += 1

                logger.info(f"  이 페이지: {page_count}개 / 누적: {len(all_reviews)}개")

                # 다음 페이지: 하단까지 확실히 스크롤 → "Next ›" 클릭
                for _ in range(3):
                    client.scroll_to_bottom(tabId=tab_id)
                    client.wait(0.5, 1.0)
                next_result = client.evaluate(CLICK_NEXT_PAGE_JS, tabId=tab_id)
                if not next_result or not next_result.get("clicked"):
                    logger.info("  마지막 페이지 도달.")
                    break
                client.wait(3.0, 6.0)

            except BrowserOperatorError as e:
                logger.error(f"  browser-operator 오류: {e}")
                raise
            except Exception as e:
                logger.error(f"  페이지 {page_num} 크롤링 실패: {e}")
                continue
    finally:
        try:
            client.close_tab(tab_id)
            logger.info(f"[G2] 작업 탭 닫음 (tab_id={tab_id})")
        except Exception:
            pass

    # 저장
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[3] / "data" / "benchmarks"
    output_path = output_dir / f"g2_{product}_reviews.jsonl"
    saved = save_jsonl(all_reviews, output_path)
    logger.info(f"[G2] {product}: {saved}개 리뷰 저장 → {output_path}")

    return all_reviews
