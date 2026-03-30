"""Validation helpers for cleaned alumni profile data."""

from __future__ import annotations

import re
from typing import Any


class DataValidator:
    """Validation rules for profile fields."""

    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(DataValidator.EMAIL_PATTERN.match(email or ""))

    @staticmethod
    def validate_linkedin_url(url: str) -> bool:
        lowered = (url or "").lower()
        return lowered.startswith("https://www.linkedin.com/in/") or lowered.startswith(
            "https://linkedin.com/in/"
        )

    @staticmethod
    def validate_batch_year(year: Any) -> bool:
        try:
            value = int(year)
        except (TypeError, ValueError):
            return False
        return 1950 <= value <= 2035

    @staticmethod
    def validate_profile(profile: dict[str, Any]) -> tuple[bool, list[str]]:
        errors: list[str] = []

        if not DataValidator.validate_linkedin_url(str(profile.get("url", ""))):
            errors.append("Invalid LinkedIn URL")

        if not profile.get("name"):
            errors.append("Name is required")

        graduation_year = profile.get("graduation_year")
        if graduation_year is not None and graduation_year != "":
            if not DataValidator.validate_batch_year(graduation_year):
                errors.append("Invalid graduation year")

        return (len(errors) == 0, errors)
