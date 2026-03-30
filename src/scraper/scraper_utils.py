"""Utility helpers for LinkedIn scraping workflows."""

import hashlib
import json
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse


def normalize_linkedin_url(url: str) -> str:
    """Normalize LinkedIn URLs for consistency and deduplication."""
    if not url or not url.strip():
        return ""

    normalized = url.strip().split("?")[0].split("#")[0].rstrip("/")

    if normalized.startswith("http://"):
        normalized = normalized.replace("http://", "https://", 1)
    elif normalized.startswith("www."):
        normalized = f"https://{normalized}"
    elif normalized.startswith("linkedin.com"):
        normalized = f"https://www.{normalized}"

    return normalized


def get_profile_id_from_url(url: str) -> str | None:
    """Extract the LinkedIn profile handle from a profile URL."""
    normalized = normalize_linkedin_url(url)
    if not normalized:
        return None

    parts = normalized.rstrip("/").split("/")
    return parts[-1] if parts else None


def is_linkedin_url_accessible(url: str) -> bool:
    """Validate URL format for a LinkedIn person profile."""
    normalized = normalize_linkedin_url(url)
    if not normalized:
        return False

    try:
        parsed = urlparse(normalized)
        return (
            parsed.scheme in {"http", "https"}
            and "linkedin.com" in parsed.netloc.lower()
            and "/in/" in parsed.path.lower()
        )
    except Exception:
        return False


def hash_profile_url(url: str) -> str:
    """Generate deterministic hash for normalized profile URL."""
    normalized = normalize_linkedin_url(url)
    return hashlib.md5(normalized.encode("utf-8")).hexdigest()


def load_discovered_urls(file_path: str = "output/discovered_urls.json") -> list[str]:
    """Load discovered profile URLs produced by Phase 2."""
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    raw_urls: Any = payload.get("urls", [])
    if not isinstance(raw_urls, list):
        return []

    cleaned: list[str] = []
    seen: set[str] = set()

    raw_urls_list = cast(list[object], raw_urls)
    for raw_url in raw_urls_list:
        if not isinstance(raw_url, str):
            continue
        normalized = normalize_linkedin_url(raw_url)
        if normalized and normalized not in seen:
            seen.add(normalized)
            cleaned.append(normalized)

    return cleaned
