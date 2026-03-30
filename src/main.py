"""
Main entry point for Alumni Data Extractor
"""
import asyncio
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config.settings import config
from src.ai.ai_validator import AIValidator
from src.data.cleaner import process_validated_profiles, save_cleaned_data
from src.export.csv_exporter import load_and_export
from src.scraper.linkedin_scraper import main_scraper
from src.scraper.profile_extractor import process_raw_profiles, save_extracted_data
from src.scraper.scraper_utils import load_discovered_urls
from src.search.google_search import GoogleSearcher
from src.utils.logger import app_logger


def main():
    """Main execution function"""
    try:
        app_logger.info("=" * 60)
        app_logger.info("Starting Alumni Data Extractor")
        app_logger.info("=" * 60)
        
        # Validate configuration
        try:
            config.validate()
            app_logger.info("[OK] Configuration validated successfully")
        except ValueError as e:
            app_logger.warning(f"Configuration warning: {str(e)}")
            app_logger.info("Some features may not work without proper API keys")
        
        # Display configuration
        app_logger.info(f"College: {config.COLLEGE_NAME}")
        app_logger.info(f"Batch Year: {config.BATCH_YEAR}")
        app_logger.info(f"Search Pages: {config.SEARCH_PAGES}")
        app_logger.info(f"AI Model: {config.AI_MODEL}")

        # Phase 2: Google Search Integration
        if config.SERPAPI_API_KEY:
            app_logger.info("Starting Phase 2: Google Search Integration")
            searcher = GoogleSearcher()
            discovered_urls = searcher.search(
                college_name=config.COLLEGE_NAME,
                batch_year=config.BATCH_YEAR,
                num_pages=config.SEARCH_PAGES,
            )
            searcher.save_results(discovered_urls)
            app_logger.info(f"Phase 2 output ready: {len(discovered_urls)} URLs")
        else:
            app_logger.warning("SERPAPI_API_KEY is not set. Skipping Phase 2 execution.")

        # Phase 3: LinkedIn Scraper
        discovered_urls = load_discovered_urls()
        has_linkedin_credentials = (
            bool(config.LINKEDIN_EMAIL)
            and bool(config.LINKEDIN_PASSWORD)
            and not config.LINKEDIN_EMAIL.lower().startswith("your_linkedin")
            and not config.LINKEDIN_PASSWORD.lower().startswith("your_linkedin")
        )

        if discovered_urls and has_linkedin_credentials:
            app_logger.info("Starting Phase 3: LinkedIn Alumni Scraper")
            phase3_results = asyncio.run(
                main_scraper(discovered_urls, scrape_limit=config.SCRAPE_LIMIT)
            )
            app_logger.info(f"Phase 3 output ready: {len(phase3_results)} raw profiles")
        elif not discovered_urls:
            app_logger.warning("No discovered URLs found. Run Phase 2 first before Phase 3.")
        else:
            app_logger.warning("LinkedIn credentials are missing/placeholder. Skipping Phase 3.")

        # Phase 4: Profile Data Extraction
        app_logger.info("Starting Phase 4: Profile Data Extraction")
        phase4_profiles = process_raw_profiles()
        if phase4_profiles:
            save_extracted_data(phase4_profiles)
            app_logger.info(f"Phase 4 output ready: {len(phase4_profiles)} structured profiles")
        else:
            app_logger.warning("Phase 4 produced no extracted profiles")

        # Phase 5: AI Data Structuring and Validation
        app_logger.info("Starting Phase 5: AI Data Structuring")
        validator = AIValidator()
        phase5_profiles = validator.process_extracted_profiles()
        if phase5_profiles:
            validator.save_validated_data(phase5_profiles)
            app_logger.info(f"Phase 5 output ready: {len(phase5_profiles)} validated profiles")
        else:
            app_logger.warning("Phase 5 produced no validated profiles")

        # Phase 6: Data Cleaning and Deduplication
        app_logger.info("Starting Phase 6: Data Cleaning")
        phase6_profiles = process_validated_profiles()
        if phase6_profiles:
            save_cleaned_data(phase6_profiles)
            app_logger.info(f"Phase 6 output ready: {len(phase6_profiles)} cleaned profiles")
        else:
            app_logger.warning("Phase 6 produced no cleaned profiles")

        # Phase 7: CSV Export
        app_logger.info("Starting Phase 7: CSV Export")
        csv_file = load_and_export()
        if csv_file:
            app_logger.info(f"Phase 7 output ready: {csv_file}")
        else:
            app_logger.warning("Phase 7 did not produce a CSV file")
        
        app_logger.info("=" * 60)
        app_logger.info("[OK] Setup completed successfully!")
        app_logger.info("Core pipeline complete through Phase 7")
        app_logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        app_logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    success = main()
    if success:
        app_logger.info("Application initialized successfully")
