"""Gemini provider for Phase 5 profile validation."""

from __future__ import annotations

import json
from typing import Any

import google.generativeai as genai  # type: ignore[import-untyped]

from config.settings import config
from src.ai.prompts import VALIDATION_PROMPT
from src.utils.logger import app_logger


class GeminiHandler:
    """Validate extracted profile data using Gemini."""

    def __init__(self) -> None:
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "Gemini API key is required but not configured. "
                "Set GEMINI_API_KEY in .env file."
            )
        
        genai.configure(api_key=config.GEMINI_API_KEY)  # type: ignore[reportUnknownMemberType]
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)  # Now configurable via settings
        app_logger.info(f"Initialized Gemini handler with model: {config.GEMINI_MODEL}")

    def validate_profile(self, profile_data: dict[str, Any]) -> dict[str, Any]:
        """Validate one profile and return JSON result."""
        university, degree = self._get_education_fields(profile_data)
        prompt = VALIDATION_PROMPT.format(
            name=profile_data.get("name", ""),
            headline=profile_data.get("headline", ""),
            current_company=profile_data.get("current_company", ""),
            current_position=profile_data.get("current_position", ""),
            university=university,
            degree=degree,
        )

        try:
            response = self.model.generate_content(prompt)  # type: ignore[reportUnknownMemberType]
            
            # Validate response has text attribute
            if not hasattr(response, 'text'):
                app_logger.warning("Gemini response missing 'text' attribute")
                return {}
            
            text = (response.text or "").strip()
            if not text:
                app_logger.warning("Empty response from Gemini")
                return {}
            
            return self._extract_json_payload(text)
        except ValueError as exc:
            app_logger.error(f"Gemini validation error (likely invalid API key): {exc}")
            return {}
        except Exception as exc:
            app_logger.error(f"Gemini validation failed: {exc}")
            return {}

    def batch_validate(self, profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Validate all profiles sequentially with batch size limits."""
        if not profiles:
            app_logger.warning("No profiles provided for validation")
            return []
        
        validated: list[dict[str, Any]] = []
        batch_size = 10  # Process 10 at a time to avoid rate limits
        
        for batch_idx in range(0, len(profiles), batch_size):
            batch = profiles[batch_idx : batch_idx + batch_size]
            for index, profile in enumerate(batch, start=batch_idx + 1):
                app_logger.info(f"Gemini validating profile {index}/{len(profiles)}")
                validated.append(self.validate_profile(profile))
        
        return validated

    @staticmethod
    def _extract_json_payload(text: str) -> dict[str, Any]:
        """Extract JSON object from model text output."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return {}
            candidate = text[start : end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                return {}

    @staticmethod
    def _get_education_fields(profile_data: dict[str, Any]) -> tuple[str, str]:
        education_raw = profile_data.get("education")
        if not isinstance(education_raw, dict):
            return "", ""

        education: dict[str, Any] = education_raw
        university = education.get("primary_school")
        degree = education.get("primary_degree")
        return (
            university if isinstance(university, str) else "",
            degree if isinstance(degree, str) else "",
        )
