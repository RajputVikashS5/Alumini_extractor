"""Phase 4 profile extraction from raw LinkedIn HTML payloads."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from bs4 import BeautifulSoup  # type: ignore[import-untyped]

from src.utils.logger import app_logger


class ProfileExtractor:
    """Extract structured profile fields from LinkedIn HTML pages."""

    def __init__(self) -> None:
        self.extracted_fields = [
            "name",
            "headline",
            "current_company",
            "current_position",
            "education",
        ]

    def extract(self, html_content: str, profile_url: str) -> dict[str, Any]:
        """Extract structured data from one HTML document."""
        try:
            soup = BeautifulSoup(html_content or "", "lxml")

            data: dict[str, Any] = {
                "url": profile_url,
                "name": self._extract_name(soup),
                "headline": self._extract_headline(soup),
                "current_company": self._extract_current_company(soup),
                "current_position": self._extract_current_position(soup),
                "education": self._extract_education(soup),
                "extraction_timestamp": datetime.now().isoformat(),
                "extraction_success": True,
            }

            app_logger.info(f"Phase 4 extracted structured profile data for {profile_url}")
            return data
        except Exception as exc:
            app_logger.error(f"Phase 4 extraction error for {profile_url}: {exc}")
            return {
                "url": profile_url,
                "error": str(exc),
                "extraction_success": False,
            }

    def _extract_name(self, soup: Any) -> str | None:
        selectors = [
            "h1.text-heading-xlarge",
            "h1 span[aria-hidden='true']",
            "h1",
        ]
        return self._find_first_non_empty_text(soup, selectors)

    def _extract_headline(self, soup: Any) -> str | None:
        selectors = [
            "div.text-body-medium.break-words",
            "div.text-body-medium",
            "div.top-card-layout__headline",
        ]
        text = self._find_first_non_empty_text(soup, selectors)
        if text and len(text) >= 8:
            return text
        return None

    def _extract_current_company(self, soup: Any) -> str | None:
        selectors = [
            "section#experience h3 span[aria-hidden='true']",
            "section#experience h3",
            "div[data-section='experience'] h3",
        ]
        return self._find_first_non_empty_text(soup, selectors)

    def _extract_current_position(self, soup: Any) -> str | None:
        selectors = [
            "section#experience .t-bold span[aria-hidden='true']",
            "section#experience .t-bold",
            "section#experience h2 span[aria-hidden='true']",
        ]
        return self._find_first_non_empty_text(soup, selectors)

    def _extract_education(self, soup: Any) -> dict[str, Any] | None:
        section = soup.select_one("section#education")
        if not section:
            return None

        education_list: list[dict[str, str | None]] = []

        schools = section.select("li")
        for school_item in schools:
            school = self._safe_text(
                school_item.select_one("h3 span[aria-hidden='true']")
                or school_item.select_one("h3")
            )
            degree = self._safe_text(
                school_item.select_one(".t-14.t-normal span[aria-hidden='true']")
                or school_item.select_one(".t-14.t-normal")
            )

            if school or degree:
                education_list.append({"school": school, "degree": degree})

        if not education_list:
            school = self._safe_text(section.select_one("h3"))
            degree = self._safe_text(section.select_one(".t-14.t-normal"))
            if school or degree:
                education_list.append({"school": school, "degree": degree})

        if not education_list:
            return None

        return {
            "primary_school": education_list[0].get("school"),
            "primary_degree": education_list[0].get("degree"),
            "all_education": education_list,
        }

    def _find_first_non_empty_text(self, soup: Any, selectors: list[str]) -> str | None:
        for selector in selectors:
            node = soup.select_one(selector)
            text = self._safe_text(node)
            if text:
                return text
        return None

    @staticmethod
    def _safe_text(node: Any) -> str | None:
        if node is None:
            return None
        text = node.get_text(strip=True)
        return text if text else None


def process_raw_profiles(raw_profiles_file: str = "output/raw_profiles.json") -> list[dict[str, Any]]:
    """Process Phase 3 raw output and extract structured profiles."""
    source = Path(raw_profiles_file)
    if not source.exists():
        app_logger.warning(f"Phase 4 skipped: raw profile file not found at {raw_profiles_file}")
        return []

    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        app_logger.error(f"Phase 4 failed to read raw profile JSON: {exc}")
        return []

    profiles_raw = payload.get("profiles", [])
    if not isinstance(profiles_raw, list):
        app_logger.error("Phase 4 failed: raw profile payload has invalid 'profiles' format")
        return []

    profiles = cast(list[object], profiles_raw)

    extractor = ProfileExtractor()
    extracted_profiles: list[dict[str, Any]] = []

    for profile_item in profiles:
        if not isinstance(profile_item, dict):
            continue
        profile = cast(dict[str, Any], profile_item)

        if profile.get("scraped_successfully") is not True:
            continue

        html_content = profile.get("html_content", "")
        profile_url = profile.get("url", "")

        if not isinstance(html_content, str) or not isinstance(profile_url, str):
            continue

        extracted_profiles.append(extractor.extract(html_content, profile_url))

    app_logger.info(f"Phase 4 extracted {len(extracted_profiles)} profiles")
    return extracted_profiles


def save_extracted_data(data: list[dict[str, Any]], filename: str = "output/extracted_data.json") -> None:
    """Save Phase 4 structured extraction output to JSON."""
    output: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "total_profiles": len(data),
        "profiles": data,
    }

    destination = Path(filename)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2), encoding="utf-8")

    app_logger.info(f"Phase 4 extracted data saved to {filename}")
