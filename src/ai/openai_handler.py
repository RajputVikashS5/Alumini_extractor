"""OpenAI provider for Phase 5 profile validation."""

from __future__ import annotations

import json
from typing import Any

from openai import OpenAI  # type: ignore[import-untyped]

from config.settings import config
from src.ai.prompts import ENRICHMENT_PROMPT, VALIDATION_PROMPT, VALIDATION_SYSTEM_PROMPT
from src.utils.logger import app_logger


class OpenAIHandler:
    """Validate and enrich extracted profile data using OpenAI or OpenRouter."""

    def __init__(self) -> None:
        # Get API key (prefer OpenRouter if available, else use OpenAI)
        api_key = config.OPENROUTER_API_KEY or config.OPENAI_API_KEY
        
        if not api_key:
            raise ValueError(
                "OpenAI/OpenRouter API key is required but not configured. "
                "Set OPENAI_API_KEY or OPENROUTER_API_KEY in .env file."
            )
        
        # Use OpenRouter base URL if OpenRouter key is detected
        if config.OPENROUTER_API_KEY:
            self.client = OpenAI(
                api_key=config.OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1"
            )
            app_logger.info("Using OpenRouter API for AI validation")
        else:
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)
            app_logger.info("Using OpenAI API for AI validation")
        
        self.model = config.OPENAI_MODEL  # Now configurable via settings

    def validate_profile(self, profile_data: dict[str, Any]) -> dict[str, Any]:
        """Validate a single profile with OpenAI/OpenRouter JSON output."""
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=700,
            )
            
            # Safe list indexing
            if not response.choices or len(response.choices) == 0:
                app_logger.warning("Empty response choices from API")
                return {}
            
            text = response.choices[0].message.content or "{}"
            return self._extract_json_payload(text)
        except ValueError as exc:
            app_logger.error(f"Validation error (likely invalid API key): {exc}")
            return {}
        except Exception as exc:
            app_logger.error(f"OpenAI/OpenRouter validation failed: {exc}")
            return {}

    def enrich_profile(self, profile_data: dict[str, Any]) -> dict[str, Any]:
        """Optional enrichment call for future phases."""
        university, _ = self._get_education_fields(profile_data)
        prompt = ENRICHMENT_PROMPT.format(
            name=profile_data.get("name", ""),
            current_company=profile_data.get("current_company", ""),
            current_position=profile_data.get("current_position", ""),
            university=university,
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=500,
            )
            
            # Safe list indexing
            if not response.choices or len(response.choices) == 0:
                app_logger.warning("Empty response choices from enrichment API")
                return {}
            
            text = response.choices[0].message.content or "{}"
            return self._extract_json_payload(text)
        except Exception as exc:
            app_logger.error(f"OpenAI/OpenRouter enrichment failed: {exc}")
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
                app_logger.info(f"OpenAI/OpenRouter validating profile {index}/{len(profiles)}")
                validated.append(self.validate_profile(profile))
        
        return validated

    @staticmethod
    def _extract_json_payload(text: str) -> dict[str, Any]:
        """Extract JSON object from a text response."""
        stripped = text.strip()
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            start = stripped.find("{")
            end = stripped.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return {}
            candidate = stripped[start : end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                return {}

    @staticmethod
    def _get_education_fields(profile_data: dict[str, Any]) -> tuple[str, str]:
        education_raw = profile_data.get("education")
        if not isinstance(education_raw, dict):
            return "", ""

        education = cast(dict[str, Any], education_raw)
        university = education.get("primary_school")
        degree = education.get("primary_degree")
        return (
            university if isinstance(university, str) else "",
            degree if isinstance(degree, str) else "",
        )
