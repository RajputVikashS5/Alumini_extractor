"""LinkedIn scraper using Playwright browser automation."""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from playwright.async_api import Browser, BrowserContext, Error, Page, TimeoutError, async_playwright

from config.settings import config
from src.scraper.scraper_utils import is_linkedin_url_accessible
from src.utils.logger import app_logger


class LinkedInScraper:
    """Automate LinkedIn profile scraping with authentication."""

    def __init__(self) -> None:
        self.email = config.LINKEDIN_EMAIL or ""
        self.password = config.LINKEDIN_PASSWORD or ""
        self.request_delay = config.REQUEST_DELAY

        self._playwright = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    async def initialize(self) -> None:
        """Initialize Playwright browser session."""
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        self.page = await self.context.new_page()
        app_logger.info("Phase 3 browser initialized")

    async def authenticate(self) -> bool:
        """Authenticate to LinkedIn using configured credentials."""
        if not self.page:
            app_logger.error("Scraper page is not initialized")
            return False

        if self._has_placeholder_credentials():
            app_logger.warning("LinkedIn credentials look like placeholders. Skipping authentication.")
            return False

        try:
            app_logger.info("Phase 3 authenticating to LinkedIn")
            await self.page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
            await self.page.fill('input[name="session_key"]', self.email)
            await self.page.fill('input[name="session_password"]', self.password)
            await self.page.click('button[type="submit"]')

            await self.page.wait_for_url("https://www.linkedin.com/**", timeout=20000)
            app_logger.info("LinkedIn authentication successful")
            return True
        except (TimeoutError, Error) as exc:
            app_logger.error(f"LinkedIn authentication failed: {exc}")
            return False

    async def scrape_profile(self, profile_url: str) -> dict[str, str | bool]:
        """Scrape one LinkedIn profile and return raw HTML payload."""
        if not self.page:
            return {
                "url": profile_url,
                "error": "Browser page not initialized",
                "scraped_successfully": False,
            }

        if not is_linkedin_url_accessible(profile_url):
            return {
                "url": profile_url,
                "error": "Invalid LinkedIn profile URL",
                "scraped_successfully": False,
            }

        try:
            await self.page.goto(profile_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(self.request_delay)
            await self._scroll_page()

            html_content = await self.page.content()
            return {
                "url": profile_url,
                "html_content": html_content,
                "timestamp": datetime.now().isoformat(),
                "scraped_successfully": True,
            }
        except (TimeoutError, Error) as exc:
            app_logger.error(f"Failed to scrape {profile_url}: {exc}")
            return {
                "url": profile_url,
                "error": str(exc),
                "scraped_successfully": False,
            }

    async def scrape_multiple_profiles(self, urls: list[str], limit: int | None = None) -> list[dict[str, str | bool]]:
        """Scrape multiple profiles sequentially with delay control."""
        targets = urls if limit is None else urls[:limit]
        results: list[dict[str, str | bool]] = []

        for idx, url in enumerate(targets, start=1):
            app_logger.info(f"Phase 3 scraping profile {idx}/{len(targets)}")
            result = await self.scrape_profile(url)
            results.append(result)
            await asyncio.sleep(self.request_delay)

        return results

    async def save_results(self, results: list[dict[str, str | bool]], filename: str = "output/raw_profiles.json") -> None:
        """Save Phase 3 raw scraping output as JSON."""
        payload: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "total_profiles": len(results),
            "successful": sum(1 for item in results if item.get("scraped_successfully") is True),
            "profiles": results,
        }

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        app_logger.info(f"Saved Phase 3 results to {filename}")

    async def close(self) -> None:
        """Close browser resources safely."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        app_logger.info("Phase 3 browser closed")

    def _has_placeholder_credentials(self) -> bool:
        email_placeholder = self.email.lower().startswith("your_linkedin")
        password_placeholder = self.password.lower().startswith("your_linkedin")
        return (not self.email or not self.password or email_placeholder or password_placeholder)

    async def _scroll_page(self) -> None:
        """Scroll profile to trigger lazy-loaded sections."""
        if not self.page:
            return

        for _ in range(3):
            await self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            await asyncio.sleep(0.8)

        await self.page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.5)


async def main_scraper(urls: list[str], scrape_limit: int = 10) -> list[dict[str, str | bool]]:
    """Run end-to-end Phase 3 workflow for a URL list."""
    scraper = LinkedInScraper()

    try:
        await scraper.initialize()
        is_authenticated = await scraper.authenticate()

        if not is_authenticated:
            app_logger.warning("Phase 3 skipped: LinkedIn authentication unavailable")
            return []

        results = await scraper.scrape_multiple_profiles(urls=urls, limit=scrape_limit)
        await scraper.save_results(results)
        return results
    finally:
        await scraper.close()
