"""Utility functions for search query construction and URL validation."""

from typing import Any
from urllib.parse import urlparse


def build_linkedin_search_query(
    college_name: str,
    batch_year: int,
    profile_name: str | None = None,
) -> str:
    """Build optimized Google query targeting public LinkedIn profile pages."""
    if profile_name:
        return f'site:linkedin.com/in/ "{profile_name}" "{college_name}" {batch_year}'

    return f'site:linkedin.com/in/ "{college_name}" {batch_year}'


def normalize_linkedin_profile_url(url: str) -> str:
    """Normalize LinkedIn profile URLs for reliable deduplication."""
    if not url.strip():
        return ""

    cleaned = url.strip().split("?")[0].split("#")[0].rstrip("/")

    if cleaned.startswith("www."):
        cleaned = f"https://{cleaned}"
    elif cleaned.startswith("linkedin.com"):
        cleaned = f"https://www.{cleaned}"

    return cleaned


def is_valid_linkedin_profile_url(url: str) -> bool:
    """Validate whether URL points to an individual LinkedIn profile."""
    normalized = normalize_linkedin_profile_url(url)
    if not normalized:
        return False

    try:
        parsed = urlparse(normalized)
        host = parsed.netloc.lower()
        path = parsed.path.lower()

        is_linkedin_host = host == "linkedin.com" or host.endswith(".linkedin.com")
        is_profile_path = "/in/" in path
        blocked_paths = ["/company/", "/school/", "/jobs/", "/posts/"]
        not_blocked = all(part not in path for part in blocked_paths)

        return is_linkedin_host and is_profile_path and not_blocked
    except Exception:
        return False


def extract_linkedin_urls(search_results: list[dict[str, Any]]) -> list[str]:
    """Extract and deduplicate valid LinkedIn profile URLs from search results."""
    urls: list[str] = []
    seen: set[str] = set()

    for result in search_results or []:
        link = result.get("link", "")
        normalized = normalize_linkedin_profile_url(link)

        if is_valid_linkedin_profile_url(normalized) and normalized not in seen:
            seen.add(normalized)
            urls.append(normalized)

    return urls
