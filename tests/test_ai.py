"""Tests for Phase 5 AI validation workflows."""

import json
from pathlib import Path
from typing import Any

from src.ai.ai_validator import AIValidator


def test_fallback_profile_mapping_from_extracted_shape():
    validator = AIValidator()

    profile: dict[str, Any] = {
        "url": "https://www.linkedin.com/in/jane-doe",
        "name": "jane doe",
        "headline": "engineer",
        "current_company": "google",
        "current_position": "software engineer",
        "education": {
            "primary_school": "MIT",
            "primary_degree": "BS",
        },
    }

    validated = validator.validate_profile(profile)

    assert validated["name"] == "jane doe"
    assert validated["university"] == "MIT"
    assert validated["degree"] == "BS"
    assert "confidence" in validated


def test_process_extracted_profiles_and_save(tmp_path: Path):
    extracted_file = tmp_path / "extracted_data.json"
    output_file = tmp_path / "ai_validated_data.json"

    payload: dict[str, Any] = {
        "profiles": [
            {
                "url": "https://www.linkedin.com/in/jane-doe",
                "name": "Jane Doe",
                "headline": "Engineer",
                "current_company": "Acme",
                "current_position": "Software Engineer",
                "education": {
                    "primary_school": "MIT",
                    "primary_degree": "BS",
                },
            }
        ]
    }
    extracted_file.write_text(json.dumps(payload), encoding="utf-8")

    validator = AIValidator()
    validated = validator.process_extracted_profiles(str(extracted_file))
    validator.save_validated_data(validated, str(output_file))

    assert len(validated) == 1
    assert output_file.exists()

    saved = json.loads(output_file.read_text(encoding="utf-8"))
    assert saved["total_profiles"] == 1
    assert saved["profiles"][0]["name"] == "Jane Doe"
