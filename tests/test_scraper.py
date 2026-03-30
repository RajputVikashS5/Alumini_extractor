"""Tests for Phase 3 scraper utility helpers."""

import hashlib
import json
from pathlib import Path

from src.scraper.scraper_utils import (
    get_profile_id_from_url,
    hash_profile_url,
    is_linkedin_url_accessible,
    load_discovered_urls,
    normalize_linkedin_url,
)


def test_normalize_linkedin_url_removes_query_and_trailing_slash():
    url = "http://www.linkedin.com/in/jane-doe-123/?trk=public_profile"
    assert normalize_linkedin_url(url) == "https://www.linkedin.com/in/jane-doe-123"


def test_get_profile_id_from_url():
    url = "https://www.linkedin.com/in/john-doe-456/"
    assert get_profile_id_from_url(url) == "john-doe-456"


def test_is_linkedin_url_accessible_filters_non_profile_urls():
    assert is_linkedin_url_accessible("https://www.linkedin.com/in/alex-789/") is True
    assert is_linkedin_url_accessible("https://www.linkedin.com/company/openai/") is False
    assert is_linkedin_url_accessible("https://example.com/in/not-linkedin/") is False


def test_hash_profile_url_uses_normalized_value():
    raw = "http://www.linkedin.com/in/alex-123/?trk=foo"
    normalized = "https://www.linkedin.com/in/alex-123"
    assert hash_profile_url(raw) == hashlib.md5(normalized.encode("utf-8")).hexdigest()


def test_load_discovered_urls_reads_and_deduplicates(tmp_path: Path):
    output_file = tmp_path / "discovered_urls.json"
    payload = {
        "urls": [
            "https://www.linkedin.com/in/one/",
            "https://www.linkedin.com/in/one/?trk=foo",
            "https://www.linkedin.com/in/two/",
        ]
    }
    output_file.write_text(json.dumps(payload), encoding="utf-8")

    urls = load_discovered_urls(str(output_file))

    assert urls == [
        "https://www.linkedin.com/in/one",
        "https://www.linkedin.com/in/two",
    ]
