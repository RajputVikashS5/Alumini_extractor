"""Phase 7 CSV export and summary reporting utilities."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import pandas as pd

from src.utils.logger import app_logger


class CSVExporter:
    """Export cleaned profile data to CSV and generate text summaries."""

    DEFAULT_COLUMNS = [
        "name",
        "url",
        "current_company",
        "current_position",
        "university",
        "degree",
        "graduation_year",
        "headline",
        "quality_score",
    ]

    def __init__(self, columns: list[str] | None = None) -> None:
        self.columns = columns or self.DEFAULT_COLUMNS

    def export_to_csv(
        self,
        profiles: list[dict[str, Any]],
        output_file: str = "output/alumni_data.csv",
    ) -> str:
        """Export profiles to CSV and return output file path."""
        app_logger.info(f"Phase 7 exporting {len(profiles)} profiles to CSV")

        destination = Path(output_file)
        destination.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(profiles)
        if df.empty:
            df = pd.DataFrame(columns=self.columns)

        available_columns = [col for col in self.columns if col in df.columns]
        if available_columns:
            df = df[available_columns]

        if "quality_score" in df.columns:
            df = df.sort_values("quality_score", ascending=False)

        if "name" in df.columns:
            df = df[df["name"].notna() & (df["name"] != "")]

        df.to_csv(destination, index=False, encoding="utf-8")
        app_logger.info(f"Phase 7 CSV exported successfully to {destination}")
        return str(destination)

    def generate_summary_report(
        self,
        profiles: list[dict[str, Any]],
        output_file: str = "output/summary_report.txt",
    ) -> str:
        """Generate a text summary report and return output file path."""
        destination = Path(output_file)
        destination.parent.mkdir(parents=True, exist_ok=True)

        total_profiles = len(profiles)
        companies = [str(p.get("current_company", "Unknown")) for p in profiles]
        universities = [str(p.get("university", "Unknown")) for p in profiles]
        quality_scores: list[float] = []
        for profile in profiles:
            score = profile.get("quality_score")
            if isinstance(score, (int, float)):
                quality_scores.append(float(score))

        avg_quality = (sum(quality_scores) / len(quality_scores)) if quality_scores else 0.0

        company_freq: dict[str, int] = {}
        for company in companies:
            company_freq[company] = company_freq.get(company, 0) + 1

        year_freq: dict[int, int] = {}
        for profile in profiles:
            year = profile.get("graduation_year")
            if isinstance(year, int):
                year_freq[year] = year_freq.get(year, 0) + 1

        lines = [
            "ALUMNI DATA EXTRACTION REPORT",
            "=" * 50,
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "SUMMARY STATISTICS",
            "-----------------",
            f"Total Profiles: {total_profiles}",
            f"Average Quality Score: {avg_quality:.2f}/100",
            f"Unique Companies: {len(set(companies))}",
            f"Unique Universities: {len(set(universities))}",
            "",
            "TOP COMPANIES",
            "-----------",
        ]

        for company, count in sorted(company_freq.items(), key=lambda item: item[1], reverse=True)[:10]:
            lines.append(f"{company}: {count} profiles")

        lines.extend(["", "GRADUATION YEAR DISTRIBUTION", "----------------------------"])
        if year_freq:
            for year in sorted(year_freq):
                lines.append(f"{year}: {year_freq[year]} graduates")
        else:
            lines.append("No graduation years available")

        lines.extend(["", "UNIVERSITIES REPRESENTED", "-----------------------"])
        unique_universities = sorted({u for u in universities if u and u != "Unknown"})
        if unique_universities:
            for university in unique_universities:
                lines.append(f"- {university}")
        else:
            lines.append("No university values available")

        destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
        app_logger.info(f"Phase 7 summary report generated at {destination}")
        return str(destination)


def load_and_export(
    json_file: str = "output/cleaned_data.json",
    csv_output: str = "output/alumni_data.csv",
) -> str | None:
    """Load cleaned JSON data and export CSV + summary report."""
    source = Path(json_file)
    if not source.exists():
        app_logger.warning(f"Phase 7 skipped: cleaned data file not found at {json_file}")
        return None

    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        app_logger.error(f"Phase 7 failed to parse cleaned data JSON: {exc}")
        return None

    profiles_raw = payload.get("profiles", [])
    if not isinstance(profiles_raw, list):
        app_logger.error("Phase 7 failed: cleaned payload has invalid 'profiles' format")
        return None

    profiles_list = cast(list[object], profiles_raw)
    profiles: list[dict[str, Any]] = [
        cast(dict[str, Any], item) for item in profiles_list if isinstance(item, dict)
    ]
    exporter = CSVExporter()

    csv_file = exporter.export_to_csv(profiles, csv_output)
    report_file = str(Path(csv_output).with_name(Path(csv_output).stem + "_report.txt"))
    exporter.generate_summary_report(profiles, report_file)

    return csv_file
