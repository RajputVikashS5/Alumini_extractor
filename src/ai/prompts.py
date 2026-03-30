"""Prompt templates for AI validation and enrichment."""

VALIDATION_SYSTEM_PROMPT = (
    "You are a data validation assistant. "
    "Return valid JSON only, with no markdown code fences."
)

VALIDATION_PROMPT = """
Analyze and validate the following LinkedIn profile data.

Profile Data:
- Name: {name}
- Headline: {headline}
- Current Company: {current_company}
- Current Position: {current_position}
- University: {university}
- Degree: {degree}

Tasks:
1. Correct obvious formatting/typos.
2. Standardize company and degree names when possible.
3. Infer graduation_year if present in context, otherwise null.
4. Add confidence scores (0-100) per key field.

Return JSON with exactly this shape:
{{
  "name": "...",
  "headline": "...",
  "current_company": "...",
  "current_position": "...",
  "university": "...",
  "degree": "...",
  "graduation_year": null,
  "confidence": {{
    "name": 0,
    "headline": 0,
    "current_company": 0,
    "current_position": 0,
    "university": 0,
    "degree": 0
  }}
}}
"""

ENRICHMENT_PROMPT = """
Provide optional enrichment for this profile:

- Name: {name}
- Company: {current_company}
- Position: {current_position}
- University: {university}

Return JSON with:
{{
  "industry": "...",
  "likely_batch_year": null,
  "career_path_summary": "...",
  "inferred_skills": ["...", "..."]
}}
"""
