"""ANOVAExporter — sessions.jsonl → ANOVA 분석용 CSV."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class ANOVAExporter:
    """sessions.jsonl을 ANOVA 분석에 적합한 CSV로 변환."""

    # ANOVA 독립변수 (Big Five + segment)
    INDEPENDENT = [
        "openness", "conscientiousness", "extraversion",
        "agreeableness", "neuroticism", "digital_literacy", "segment",
    ]

    # ANOVA 종속변수
    DEPENDENT = [
        # 행동 메트릭
        "total_steps",
        "unique_pages",
        "total_back_navigations",
        "total_hesitations",
        # 감정 메트릭
        "final_pad_pleasure",
        "final_pad_arousal",
        "final_pad_dominance",
        # TAM 메트릭
        "final_perceived_usefulness",
        "final_perceived_ease_of_use",
        # 이탈 메트릭
        "abandoned",  # 0/1
        "abandonment_step",
    ]

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.sessions_path = output_dir / "sessions.jsonl"

    def export(self) -> Path:
        """sessions.jsonl → anova_data.csv 변환."""
        rows = []
        with open(self.sessions_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                row = {}

                # 식별자
                row["session_id"] = data.get("session_id", "")
                row["persona_id"] = data.get("persona_id", "")
                row["product_name"] = data.get("product_name", "")

                # 독립변수
                for col in self.INDEPENDENT:
                    row[col] = data.get(col, None)

                # 종속변수
                for col in self.DEPENDENT:
                    if col == "abandoned":
                        row[col] = 1 if data.get("terminated_by") == "abandoned" else 0
                    else:
                        row[col] = data.get(col, None)

                rows.append(row)

        df = pd.DataFrame(rows)
        csv_path = self.output_dir / "anova_data.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logger.info("ANOVA CSV 내보내기 완료: %d rows → %s", len(df), csv_path)
        return csv_path
