"""Phase 6 data cleaning and deduplication module."""

from __future__ import annotations

import difflib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from src.data.validator import DataValidator
from src.utils.logger import app_logger


class DataCleaner:
    """Clean, normalize, deduplicate, and score profile records."""

    def __init__(self) -> None:
        self.similarity_threshold = 0.85

    def clean_profiles(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Clean and validate profile list with comprehensive error handling."""
        if not profiles:
            app_logger.warning("No profiles provided for cleaning")
            return []
        
        if not isinstance(profiles, list):
            app_logger.error(f"Expected list of profiles, got {type(profiles)}")
            return []

        app_logger.info(f"Phase 6 cleaning started for {len(profiles)} profiles")

        valid_profiles = self._filter_valid_profiles(profiles)
        deduplicated = self._deduplicate(valid_profiles)
        normalized = self._normalize_data(deduplicated)
        filled = self._fill_missing_values(normalized)
        scored = self._add_quality_score(filled)

        app_logger.info(
            "Phase 6 cleaning complete: "
            f"input={len(profiles)} valid={len(valid_profiles)} deduplicated={len(scored)}"
        )
        return scored

    def _filter_valid_profiles(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        valid: list[dict[str, Any]] = []
        for profile in profiles:
            if not isinstance(profile, dict):
                app_logger.debug(f"Skipping invalid profile type: {type(profile)}")
                continue
            
            is_valid, _errors = DataValidator.validate_profile(profile)
            if is_valid:
                valid.append(profile)
        
        if len(valid) < len(profiles):
            app_logger.info(f"Filtered out {len(profiles) - len(valid)} invalid profiles")
        
        return valid

    def _deduplicate(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        deduplicated: list[dict[str, Any]] = []
        seen_keys: list[str] = []

        for profile in profiles:
            name = str(profile.get("name", "")).strip().lower()
            company = str(profile.get("current_company", "")).strip().lower()
            composite_key = f"{name}|{company}"

            if not composite_key.strip("|"):
                deduplicated.append(profile)
                continue

            is_duplicate = any(self._is_duplicate(composite_key, existing) for existing in seen_keys)
            if is_duplicate:
                continue

            seen_keys.append(composite_key)
            deduplicated.append(profile)

        return deduplicated

    def _is_duplicate(self, key1: str, key2: str) -> bool:
        similarity = difflib.SequenceMatcher(None, key1, key2).ratio()
        return similarity >= self.similarity_threshold

    def _normalize_data(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        for profile in profiles:
            normalized.append(
                {
                    "name": self._normalize_name(profile.get("name")),
                    "url": profile.get("url"),
                    "current_company": self._normalize_company(profile.get("current_company")),
                    "current_position": self._normalize_position(profile.get("current_position")),
                    "university": self._normalize_university(profile.get("university")),
                    "degree": self._normalize_degree(profile.get("degree")),
                    "graduation_year": profile.get("graduation_year"),
                    "headline": profile.get("headline"),
                    "confidence": profile.get("confidence", {}),
                    "validation_model": profile.get("validation_model"),
                }
            )
        return normalized

    def _normalize_name(self, name: Any) -> str | None:
        if not isinstance(name, str) or not name.strip():
            return None
        cleaned = " ".join(name.split())
        return " ".join(word.capitalize() for word in cleaned.split(" "))

    def _normalize_company(self, company: Any) -> str | None:
        if not isinstance(company, str) or not company.strip():
            return None

        company_mapping = {
            "google": "Google",
            "microsoft": "Microsoft",
            "apple": "Apple",
            "amazon": "Amazon",
            "meta": "Meta",
            "facebook": "Meta",
            "tesla": "Tesla",
        }

        cleaned = " ".join(company.split()).strip()
        return company_mapping.get(cleaned.lower(), cleaned)

    def _normalize_position(self, position: Any) -> str | None:
        if not isinstance(position, str) or not position.strip():
            return None
        cleaned = " ".join(position.split())
        return " ".join(word.capitalize() for word in cleaned.split(" "))

    def _normalize_university(self, university: Any) -> str | None:
        if not isinstance(university, str) or not university.strip():
            return None

        university_mapping = {
            "mit": "Massachusetts Institute of Technology",
            "stanford": "Stanford University",
            "berkeley": "University of California, Berkeley",
            "uc berkeley": "University of California, Berkeley",
            "harvard": "Harvard University",
        }

        cleaned = " ".join(university.split()).strip()
        return university_mapping.get(cleaned.lower(), cleaned)

    def _normalize_degree(self, degree: Any) -> str | None:
        if not isinstance(degree, str) or not degree.strip():
            return None

        degree_mapping = {
            "bs": "Bachelor of Science",
            "ba": "Bachelor of Arts",
            "ms": "Master of Science",
            "ma": "Master of Arts",
            "phd": "Doctor of Philosophy",
            "mba": "Master of Business Administration",
        }

        cleaned = " ".join(degree.split()).strip()
        return degree_mapping.get(cleaned.lower(), cleaned)

    def _fill_missing_values(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for profile in profiles:
            for key in ["current_company", "current_position", "university", "degree"]:
                if profile.get(key) in (None, ""):
                    profile[key] = "Unknown"
        return profiles

    def _add_quality_score(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for profile in profiles:
            score = 0

            if profile.get("name") and profile.get("name") != "Unknown":
                score += 20
            if profile.get("current_company") and profile.get("current_company") != "Unknown":
                score += 20
            if profile.get("current_position") and profile.get("current_position") != "Unknown":
                score += 15
            if profile.get("university") and profile.get("university") != "Unknown":
                score += 20
            if profile.get("degree") and profile.get("degree") != "Unknown":
                score += 10
            if profile.get("graduation_year"):
                score += 10

            confidence = profile.get("confidence")
            if isinstance(confidence, dict) and confidence:
                confidence_dict = cast(dict[str, Any], confidence)
                values: list[float] = [
                    float(v) for v in confidence_dict.values() if isinstance(v, (int, float))
                ]
                if values:
                    if (sum(values) / len(values)) >= 80:
                        score += 5

            profile["quality_score"] = min(score, 100)

        return profiles


def process_validated_profiles(file_path: str = "output/ai_validated_data.json") -> list[dict[str, Any]]:
    """Load Phase 5 output and return cleaned records."""
    source = Path(file_path)
    if not source.exists():
        app_logger.warning(f"Phase 6 skipped: validated data file not found at {file_path}")
        return []

    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        app_logger.error(f"Phase 6 failed to parse validated data JSON: {exc}")
        return []

    profiles_raw = payload.get("profiles", [])
    if not isinstance(profiles_raw, list):
        app_logger.error("Phase 6 failed: validated payload has invalid 'profiles' format")
        return []

    profiles_list = cast(list[object], profiles_raw)
    profiles: list[dict[str, Any]] = [
        cast(dict[str, Any], item) for item in profiles_list if isinstance(item, dict)
    ]
    cleaner = DataCleaner()
    return cleaner.clean_profiles(profiles)


def save_cleaned_data(data: list[dict[str, Any]], filename: str = "output/cleaned_data.json") -> None:
    """Persist Phase 6 cleaned output."""
    payload: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "total_profiles": len(data),
        "profiles": data,
    }

    destination = Path(filename)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    app_logger.info(f"Phase 6 cleaned data saved to {filename}")
