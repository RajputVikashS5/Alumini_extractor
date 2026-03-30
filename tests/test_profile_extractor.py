"""Tests for Phase 4 profile extraction."""

import json
from pathlib import Path
from typing import Any

from src.scraper.profile_extractor import (
    ProfileExtractor,
    process_raw_profiles,
    save_extracted_data,
)


def _sample_profile_html() -> str:
    return """
    <html>
      <body>
        <h1 class="text-heading-xlarge">Jane Doe</h1>
        <div class="text-body-medium break-words">Software Engineer at Acme Corp</div>

        <section id="experience">
          <h3>Acme Corp</h3>
          <div class="t-bold">Senior Software Engineer</div>
        </section>

        <section id="education">
          <li>
            <h3>Massachusetts Institute of Technology</h3>
            <div class="t-14 t-normal">Bachelor of Science in Computer Science</div>
          </li>
        </section>
      </body>
    </html>
    """


def test_extract_profile_fields():
    extractor = ProfileExtractor()
    result = extractor.extract(_sample_profile_html(), "https://www.linkedin.com/in/jane-doe")

    assert result["extraction_success"] is True
    assert result["name"] == "Jane Doe"
    assert result["headline"] == "Software Engineer at Acme Corp"
    assert result["current_company"] == "Acme Corp"
    assert result["current_position"] == "Senior Software Engineer"

    education = result["education"]
    assert isinstance(education, dict)
    assert education["primary_school"] == "Massachusetts Institute of Technology"


def test_process_raw_profiles_filters_unsuccessful(tmp_path: Path):
    raw_file = tmp_path / "raw_profiles.json"
    payload: dict[str, Any] = {
        "profiles": [
            {
                "url": "https://www.linkedin.com/in/jane-doe",
                "html_content": _sample_profile_html(),
                "scraped_successfully": True,
            },
            {
                "url": "https://www.linkedin.com/in/failure",
                "html_content": "",
                "scraped_successfully": False,
            },
        ]
    }
    raw_file.write_text(json.dumps(payload), encoding="utf-8")

    data = process_raw_profiles(str(raw_file))

    assert len(data) == 1
    assert data[0]["name"] == "Jane Doe"


def test_save_extracted_data_writes_json(tmp_path: Path):
    output_file = tmp_path / "extracted_data.json"
    data: list[dict[str, Any]] = [
        {
            "url": "https://www.linkedin.com/in/jane-doe",
            "name": "Jane Doe",
            "extraction_success": True,
        }
    ]

    save_extracted_data(data, str(output_file))

    assert output_file.exists()
    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["total_profiles"] == 1
    assert payload["profiles"][0]["name"] == "Jane Doe"
