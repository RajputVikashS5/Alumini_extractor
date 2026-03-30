"""Google Search integration using SerpAPI for LinkedIn profile discovery."""

import json
import os
import time
from datetime import datetime
from typing import Any

import requests

from config.settings import config
from src.search.search_utils import (
    build_linkedin_search_query,
    extract_linkedin_urls,
    normalize_linkedin_profile_url,
)
from src.utils.logger import app_logger


class GoogleSearcher:
    """Handle Google search queries via SerpAPI."""

    def __init__(self):
        self.api_key = config.SERPAPI_API_KEY
        self.base_url = "https://serpapi.com/search"
        self.request_delay = config.REQUEST_DELAY
        self.max_retries = config.MAX_RETRIES

    def search(self, college_name: str, batch_year: int, num_pages: int = 5) -> list[str]:
        """Search for LinkedIn profile URLs across multiple result pages."""
        all_urls: list[str] = []

        if not self.api_key:
            app_logger.warning("SERPAPI_API_KEY is missing. Skipping Phase 2 search.")
            return []
        
        # Input validation
        if not college_name or not isinstance(college_name, str):
            app_logger.error("Invalid college_name: must be non-empty string")
            return []
        
        if not isinstance(batch_year, int) or batch_year < 1950 or batch_year > 2035:
            app_logger.error(f"Invalid batch_year: {batch_year} (must be 1950-2035)")
            return []
        
        if not isinstance(num_pages, int) or num_pages < 1 or num_pages > 100:
            app_logger.error(f"Invalid num_pages: {num_pages} (must be 1-100)")
            return []

        for page in range(num_pages):
            app_logger.info(f"Phase 2 search page {page + 1}/{num_pages}")
            query = build_linkedin_search_query(college_name, batch_year)

            results = self._make_request(query=query, start=page * 10)
            if not results:
                app_logger.warning(f"No organic results returned on page {page + 1}")
                break

            page_urls = extract_linkedin_urls(results)
            all_urls.extend(page_urls)
            app_logger.info(f"Discovered {len(page_urls)} profile URLs on page {page + 1}")

            if page < num_pages - 1:
                time.sleep(self.request_delay)

        unique_urls = sorted(set(all_urls))
        app_logger.info(f"Phase 2 complete. Total unique profile URLs discovered: {len(unique_urls)}")
        return unique_urls

    def search_specific_person(self, name: str, college_name: str, batch_year: int) -> str | None:
        """Search LinkedIn URL for a specific person in a target college and batch."""
        if not self.api_key:
            app_logger.warning("SERPAPI_API_KEY is missing. Cannot run specific person search.")
            return None
        
        # Input validation
        if not name or not isinstance(name, str):
            app_logger.error("Invalid name: must be non-empty string")
            return None

        query = build_linkedin_search_query(college_name, batch_year, profile_name=name)
        results = self._make_request(query=query, start=0)
        if not results:
            return None

        urls = extract_linkedin_urls(results)
        return urls[0] if urls else None

    def search_by_keywords(self, keywords: str, num_pages: int = 3) -> list[dict[str, str]]:
        """Search LinkedIn profiles directly via advanced Google query and return result cards.

        This flow only requires SerpAPI and does not require LinkedIn credentials.
        """
        if not self.api_key:
            app_logger.warning("SERPAPI_API_KEY is missing. Cannot run keyword search.")
            return []
        
        # Input validation
        if not keywords or not isinstance(keywords, str):
            app_logger.error("Invalid keywords: must be non-empty string")
            return []
        
        if not isinstance(num_pages, int) or num_pages < 1 or num_pages > 100:
            app_logger.error(f"Invalid num_pages: {num_pages} (must be 1-100)")
            return []

        cleaned_keywords = " ".join((keywords or "").split())
        if not cleaned_keywords:
            return []

        query = f"site:linkedin.com/in/ {cleaned_keywords}"
        cards: list[dict[str, str]] = []
        seen_urls: set[str] = set()

        for page in range(num_pages):
            app_logger.info(f"Keyword search page {page + 1}/{num_pages} for query: {query}")
            results = self._make_request(query=query, start=page * 10)
            if not results:
                break

            for item in results:
                raw_url = str(item.get("link", ""))
                url = normalize_linkedin_profile_url(raw_url)
                if not url or url in seen_urls or "/in/" not in url:
                    continue

                seen_urls.add(url)
                cards.append(
                    {
                        "title": str(item.get("title", "")).strip(),
                        "url": url,
                        "snippet": str(item.get("snippet", "")).strip(),
                    }
                )

            if page < num_pages - 1:
                time.sleep(self.request_delay)

        app_logger.info(f"Keyword search complete. Found {len(cards)} LinkedIn profile results")
        return cards

    def save_results(self, urls: list[str], filename: str = "output/discovered_urls.json") -> None:
        """Persist discovered URLs to JSON for downstream phases."""
        payload: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "total_urls": len(urls),
            "urls": urls,
        }

        try:
            output_dir = os.path.dirname(filename)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(payload, file, indent=2)

            app_logger.info(f"Saved discovered URLs to {filename}")
        except Exception as exc:
            app_logger.error(f"Failed to save discovered URLs: {exc}")

    def _make_request(self, query: str, start: int = 0, retry_count: int = 0) -> list[dict[str, Any]]:
        """Execute a SerpAPI request with bounded retries and backoff."""
        params: dict[str, str | int] = {
            "api_key": self.api_key or "",
            "q": query,
            "engine": "google",
            "start": start,
            "num": 10,
            "hl": "en",
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=20)
            response.raise_for_status()
            
            # Safe JSON parsing with error handling
            try:
                data = response.json()
            except json.JSONDecodeError as json_err:
                app_logger.error(f"Failed to parse JSON response from SerpAPI: {json_err}")
                app_logger.debug(f"Response content: {response.text[:500]}")
                return []
            
            return data.get("organic_results", [])
        except requests.RequestException as exc:
            if retry_count < self.max_retries:
                next_retry = retry_count + 1
                wait_seconds = 2 ** retry_count
                app_logger.warning(
                    f"SerpAPI request failed ({exc}). Retrying {next_retry}/{self.max_retries} in {wait_seconds}s"
                )
                time.sleep(wait_seconds)
                return self._make_request(query=query, start=start, retry_count=next_retry)

            app_logger.error(f"SerpAPI request failed after {self.max_retries} retries: {exc}")
            return []
