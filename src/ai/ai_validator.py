"""Unified Phase 5 AI validator with model fallback support."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config.settings import config
from src.ai.gemini_handler import GeminiHandler
from src.ai.openai_handler import OpenAIHandler
from src.utils.logger import app_logger


class AIValidator:
    """Unified interface for AI-based validation and normalization."""

    def __init__(self) -> None:
        self.model_name = (config.AI_MODEL or "openai").lower()
        self.handler: Any | None = None

        if self.model_name == "openai" and self._has_real_key(config.OPENAI_API_KEY):
            self.handler = OpenAIHandler()
            app_logger.info("Phase 5 using OpenAI handler")
        elif self.model_name == "gemini" and self._has_real_key(config.GEMINI_API_KEY):
            self.handler = GeminiHandler()
            app_logger.info("Phase 5 using Gemini handler")
        else:
            app_logger.warning("Phase 5 AI key unavailable or placeholder, using deterministic fallback")

    def validate_profile(self, profile_data: dict[str, Any]) -> dict[str, Any]:
        """Validate a single profile using selected provider or fallback."""
        base = self._fallback_profile(profile_data)

        if not self.handler:
            return base

        ai_output = self.handler.validate_profile(profile_data)
        if not ai_output:
            return base

        # Validate type instead of unsafe cast
        if isinstance(ai_output, dict):
            ai_output_typed: dict[str, Any] = ai_output
        else:
            app_logger.warning(f"AI output is not a dict, got {type(ai_output).__name__}")
            return base
        
        merged: dict[str, Any] = {**base, **ai_output_typed}
        merged["validation_model"] = self.model_name
        return merged

    def validate_batch(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Validate multiple profiles."""
        if not profiles:
            app_logger.warning("No profiles provided for batch validation")
            return []
        
        return [self.validate_profile(profile) for profile in profiles]

    def process_extracted_profiles(self, file_path: str = "output/extracted_data.json") -> list[dict[str, Any]]:
        """Load Phase 4 output and validate all extracted profiles."""
        source = Path(file_path)
        if not source.exists():
            app_logger.warning(f"Phase 5 skipped: extracted data file not found at {file_path}")
            return []

        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            app_logger.error(f"Phase 5 failed to parse extracted data: {exc}")
            return []

        profiles_raw = payload.get("profiles", [])
        if not isinstance(profiles_raw, list):
            app_logger.error("Phase 5 failed: extracted payload has invalid 'profiles' format")
            return []

        profiles_list = cast(list[object], profiles_raw)
        clean_profiles: list[dict[str, Any]] = [
            cast(dict[str, Any], item) for item in profiles_list if isinstance(item, dict)
        ]
        validated = self.validate_batch(clean_profiles)
        app_logger.info(f"Phase 5 validated {len(validated)} profiles")
        return validated

    def save_validated_data(self, profiles: list[dict[str, Any]], filename: str = "output/ai_validated_data.json") -> None:
        """Save Phase 5 output to JSON."""
        payload: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "ai_model": self.model_name,
            "total_profiles": len(profiles),
            "profiles": profiles,
        }

        destination = Path(filename)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        app_logger.info(f"Phase 5 data saved to {filename}")

    @staticmethod
    def _has_real_key(value: str | None) -> bool:
        if not value:
            return False
        lowered = value.lower().strip()
        return not lowered.startswith("your_")

    @staticmethod
    def _fallback_profile(profile_data: dict[str, Any]) -> dict[str, Any]:
        education_raw = profile_data.get("education")
        education = cast(dict[str, Any], education_raw) if isinstance(education_raw, dict) else {}
        university_raw = education.get("primary_school")
        degree_raw = education.get("primary_degree")
        university = university_raw if isinstance(university_raw, str) else None
        degree = degree_raw if isinstance(degree_raw, str) else None

        return {
            "url": profile_data.get("url"),
            "name": profile_data.get("name"),
            "headline": profile_data.get("headline"),
            "current_company": profile_data.get("current_company"),
            "current_position": profile_data.get("current_position"),
            "university": university,
            "degree": degree,
            "graduation_year": None,
            "confidence": {
                "name": 70,
                "headline": 65,
                "current_company": 65,
                "current_position": 65,
                "university": 70,
                "degree": 70,
            },
            "validation_model": "fallback",
        }
