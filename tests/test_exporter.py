"""Tests for Phase 7 CSV export and summary reporting."""

import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.export.csv_exporter import CSVExporter, load_and_export


def _sample_profiles() -> list[dict[str, Any]]:
    return [
        {
            "name": "Jane Doe",
            "url": "https://www.linkedin.com/in/jane-doe",
            "current_company": "Google",
            "current_position": "Software Engineer",
            "university": "Massachusetts Institute of Technology",
            "degree": "Bachelor of Science",
            "graduation_year": 2020,
            "headline": "Engineer",
            "quality_score": 95,
        },
        {
            "name": "John Smith",
            "url": "https://www.linkedin.com/in/john-smith",
            "current_company": "Microsoft",
            "current_position": "Product Manager",
            "university": "Stanford University",
            "degree": "Master of Science",
            "graduation_year": 2019,
            "headline": "PM",
            "quality_score": 88,
        },
    ]


def test_export_to_csv(tmp_path: Path):
    exporter = CSVExporter()
    csv_path = tmp_path / "alumni_data.csv"

    output = exporter.export_to_csv(_sample_profiles(), str(csv_path))

    assert Path(output).exists()
    df = pd.read_csv(output)
    assert len(df) == 2
    assert "name" in df.columns
    assert "quality_score" in df.columns


def test_generate_summary_report(tmp_path: Path):
    exporter = CSVExporter()
    report_path = tmp_path / "summary_report.txt"

    output = exporter.generate_summary_report(_sample_profiles(), str(report_path))

    text = Path(output).read_text(encoding="utf-8")
    assert "ALUMNI DATA EXTRACTION REPORT" in text
    assert "Total Profiles: 2" in text
    assert "TOP COMPANIES" in text


def test_load_and_export(tmp_path: Path):
    cleaned_json = tmp_path / "cleaned_data.json"
    csv_output = tmp_path / "alumni_data.csv"

    payload = {"profiles": _sample_profiles()}
    cleaned_json.write_text(json.dumps(payload), encoding="utf-8")

    output = load_and_export(str(cleaned_json), str(csv_output))

    assert output is not None
    assert csv_output.exists()
    report = tmp_path / "alumni_data_report.txt"
    assert report.exists()
