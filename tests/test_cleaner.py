"""Tests for Phase 6 data cleaning module."""

import json
from pathlib import Path
from typing import Any

from src.data.cleaner import DataCleaner, process_validated_profiles, save_cleaned_data
from src.data.validator import DataValidator


def test_data_validator_rules():
    assert DataValidator.validate_email("john@example.com") is True
    assert DataValidator.validate_email("not-an-email") is False
    assert DataValidator.validate_linkedin_url("https://www.linkedin.com/in/jane-doe") is True
    assert DataValidator.validate_linkedin_url("https://example.com/u/jane") is False
    assert DataValidator.validate_batch_year(2020) is True
    assert DataValidator.validate_batch_year(1900) is False


def test_cleaner_deduplicate_normalize_score():
    cleaner = DataCleaner()
    profiles: list[dict[str, Any]] = [
        {
            "url": "https://www.linkedin.com/in/jane-doe",
            "name": "jane doe",
            "current_company": "google",
            "current_position": "software engineer",
            "university": "mit",
            "degree": "bs",
            "graduation_year": 2020,
            "headline": "Engineer",
            "confidence": {"name": 95, "current_company": 90},
            "validation_model": "fallback",
        },
        {
            "url": "https://www.linkedin.com/in/jane-doe-dup",
            "name": "Jane Doe",
            "current_company": "Google",
            "current_position": "Software Engineer",
            "university": "MIT",
            "degree": "BS",
            "graduation_year": 2020,
            "headline": "Engineer",
            "confidence": {"name": 95, "current_company": 90},
            "validation_model": "fallback",
        },
    ]

    cleaned = cleaner.clean_profiles(profiles)

    assert len(cleaned) == 1
    row = cleaned[0]
    assert row["name"] == "Jane Doe"
    assert row["current_company"] == "Google"
    assert row["university"] == "Massachusetts Institute of Technology"
    assert row["degree"] == "Bachelor of Science"
    assert isinstance(row["quality_score"], int)
    assert row["quality_score"] > 0


def test_process_and_save_cleaned_profiles(tmp_path: Path):
    input_file = tmp_path / "ai_validated_data.json"
    output_file = tmp_path / "cleaned_data.json"

    payload: dict[str, Any] = {
        "profiles": [
            {
                "url": "https://www.linkedin.com/in/jane-doe",
                "name": "Jane Doe",
                "current_company": "google",
                "current_position": "software engineer",
                "university": "mit",
                "degree": "bs",
                "graduation_year": 2020,
                "headline": "Engineer",
                "confidence": {"name": 90},
                "validation_model": "fallback",
            }
        ]
    }
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    cleaned = process_validated_profiles(str(input_file))
    save_cleaned_data(cleaned, str(output_file))

    assert len(cleaned) == 1
    saved = json.loads(output_file.read_text(encoding="utf-8"))
    assert saved["total_profiles"] == 1
    assert saved["profiles"][0]["current_company"] == "Google"
