"""Tests for Phase 2 search utilities."""

from src.search.search_utils import (
    build_linkedin_search_query,
    extract_linkedin_urls,
    is_valid_linkedin_profile_url,
)


def test_build_search_query_with_college_and_year():
    query = build_linkedin_search_query("MIT", 2020)
    assert "site:linkedin.com/in/" in query
    assert "MIT" in query
    assert "2020" in query


def test_build_search_query_with_profile_name():
    query = build_linkedin_search_query("Stanford", 2019, profile_name="Jane Doe")
    assert "Jane Doe" in query
    assert "Stanford" in query
    assert "2019" in query


def test_linkedin_profile_url_validation():
    valid_urls = [
        "https://www.linkedin.com/in/john-doe-123456/",
        "https://linkedin.com/in/jane-smith/",
    ]

    invalid_urls = [
        "https://www.linkedin.com/company/google/",
        "https://www.linkedin.com/school/mit/",
        "https://example.com/in/not-linkedin/",
    ]

    for url in valid_urls:
        assert is_valid_linkedin_profile_url(url) is True

    for url in invalid_urls:
        assert is_valid_linkedin_profile_url(url) is False


def test_extract_linkedin_urls_filters_and_deduplicates():
    search_results = [
        {"link": "https://www.linkedin.com/in/john-doe-123/"},
        {"link": "https://www.linkedin.com/company/acme/"},
        {"link": "https://linkedin.com/in/jane-smith/"},
        {"link": "https://www.linkedin.com/in/john-doe-123/?trk=test"},
    ]

    urls = extract_linkedin_urls(search_results)
    assert len(urls) == 2
    assert "https://www.linkedin.com/in/john-doe-123" in urls
    assert "https://linkedin.com/in/jane-smith" in urls or "https://www.linkedin.com/in/jane-smith" in urls
