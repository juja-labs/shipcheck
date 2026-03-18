"""크롤링 데이터 모델 및 저장 유틸리티.

G2 리뷰, NNGroup 벤치마크 데이터의 구조 정의 및 JSONL 저장.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# G2 리뷰 데이터 모델
# ---------------------------------------------------------------------------

@dataclass
class G2ReviewerProfile:
    """리뷰어 프로필 — 페르소나 매칭의 핵심 메타데이터."""
    name: str | None = None
    role: str | None = None              # "Product Manager", "Teacher" 등
    company_size: str | None = None      # "Small-Business(50 or fewer emp.)" 등
    industry: str | None = None          # "Education", "Information Technology" 등
    region: str | None = None            # 국가/지역
    use_case: str | None = None          # 사용 목적
    time_used: str | None = None         # "Less than 12 months" 등
    frequency: str | None = None         # "Weekly", "Daily" 등


@dataclass
class G2Ratings:
    """G2 세부 평점."""
    overall: float | None = None         # 0-5 (반올림 0.5 단위)
    ease_of_use: float | None = None
    quality_of_support: float | None = None
    ease_of_setup: float | None = None
    meets_requirements: float | None = None


@dataclass
class G2Review:
    """G2 리뷰 한 건."""
    product_name: str = ""
    review_id: str = ""
    title: str = ""
    date: str = ""                       # ISO 날짜
    verified: bool = False
    incentivized: bool = False

    # 리뷰 본문
    likes: str = ""                      # "What do you like best?"
    dislikes: str = ""                   # "What do you dislike?"
    recommendations: str = ""            # "Recommendations to others"
    problems_solved: str = ""            # "What problems is ... solving?"
    switch_from: str = ""                # 이전에 쓰던 도구

    # 메타데이터
    ratings: G2Ratings = field(default_factory=G2Ratings)
    reviewer: G2ReviewerProfile = field(default_factory=G2ReviewerProfile)

    # 크롤링 메타
    crawled_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    source_url: str = ""


# ---------------------------------------------------------------------------
# NNGroup 벤치마크 데이터 모델
# ---------------------------------------------------------------------------

@dataclass
class NNGroupBenchmark:
    """NNGroup 연구에서 추출한 벤치마크 수치."""
    category: str = ""                   # "age_usability", "bounce_rate", "reading_pattern" 등
    metric_name: str = ""                # "task_completion_rate_65plus" 등
    value: float | str = ""              # 수치 또는 텍스트
    unit: str = ""                       # "%", "seconds", "ratio" 등
    context: str = ""                    # 벤치마크 맥락 설명
    population: str = ""                 # 대상 집단 ("65+ users", "all users" 등)
    source_url: str = ""
    source_title: str = ""
    study_year: str | None = None
    crawled_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ---------------------------------------------------------------------------
# JSONL 저장 유틸리티
# ---------------------------------------------------------------------------

def save_jsonl(data: list[Any], path: Path) -> int:
    """dataclass 리스트를 JSONL로 저장. 반환: 저장된 레코드 수."""
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            d = asdict(item) if hasattr(item, "__dataclass_fields__") else item
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
            count += 1
    return count


def load_jsonl(path: Path) -> list[dict]:
    """JSONL 파일 로드."""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
