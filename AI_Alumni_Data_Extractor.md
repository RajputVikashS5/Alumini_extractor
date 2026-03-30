# AI Alumni Data Extractor - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [System Architecture](#system-architecture)
6. [Folder Structure](#folder-structure)
7. [Phase-wise Implementation Plan](#phase-wise-implementation-plan)
8. [Developer Setup Guide](#developer-setup-guide)

---

## Project Overview

**AI Alumni Data Extractor** is an intelligent automation system designed to collect, validate, and structure alumni data from LinkedIn profiles. The system searches for LinkedIn profiles of students from a specific college and batch year, extracts relevant professional information, and uses AI to validate and structure the collected data into a clean, exportable dataset.

### Key Use Cases
- Build alumni networks for colleges and educational institutions
- Create databases of alumni for networking and career opportunities
- Research educational outcomes and alumni professional trajectories
- Generate insights about alumni employment patterns and company distributions

### Problem Statement
Manual collection of alumni data is time-consuming and error-prone. This system automates the entire process:
- Discovers LinkedIn profiles via smart searching
- Extracts structured data using web scraping
- Validates extracted information using AI
- Exports clean, deduplicated datasets

---

## Objectives

1. **Automated Discovery**: Find LinkedIn profiles of alumni from specific colleges and batch years
2. **Data Extraction**: Extract structured professional information (name, company, position, education)
3. **Data Validation**: Use AI/LLM to validate and correct extracted data
4. **Data Cleaning**: Remove duplicates, standardize formats, handle missing values
5. **Export**: Generate clean CSV files suitable for analysis and import into business systems
6. **Scalability**: Design the system to handle thousands of profiles efficiently
7. **Error Handling**: Implement robust error handling and logging for production reliability

---

## Key Features

### Core Features
- ✅ Google Search integration for discovering LinkedIn profiles
- ✅ Playwright-based LinkedIn scraping with browser automation
- ✅ Intelligent data extraction using AI models (OpenAI GPT / Google Gemini)
- ✅ Automatic data validation and correction
- ✅ Duplicate detection and removal
- ✅ CSV export with user-friendly formatting
- ✅ Comprehensive logging and error tracking
- ✅ Rate limiting and blocking avoidance mechanisms

### Advanced Features
- ✅ Data normalization (company names, education formats)
- ✅ Missing data handling and imputation
- ✅ Progress tracking and resumable scraping
- ✅ Batch processing for multiple search queries
- ✅ Email extraction and verification (optional)
- ✅ Web UI for input and result visualization (Phase 8)
- ✅ Scheduled automation and periodic updates (Phase 8)

---

## Technology Stack

### Core Technologies
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.9+ | Primary development language |
| Web Scraping | Playwright | LinkedIn automation & scraping |
| Search Integration | SerpAPI / Google Custom Search | Google search queries |
| AI/LLM | OpenAI API / Google Gemini API | Data extraction & validation |
| Data Processing | Pandas | Data manipulation & CSV export |
| HTTP Requests | Requests, HTTPX | API calls and web requests |
| Logging | Python logging | Event tracking and debugging |
| Database (Optional) | SQLite / PostgreSQL | Store intermediate results |
| Testing | Pytest | Unit and integration testing |

### Required Python Libraries
```
playwright==1.40.0
requests==2.31.0
pandas==2.1.3
python-dotenv==1.0.0
openai==1.3.0
google-generativeai==0.3.0
serpapi==0.3.1
beautifulsoup4==4.12.2
sqlalchemy==2.0.23
pytest==7.4.3
```

---

## System Architecture

### Architecture Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT                                    │
│            (College Name, Batch Year, Query)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 2: GOOGLE SEARCH SCRAPER                      │
│        (SerpAPI → Search Results → LinkedIn URLs)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            PHASE 3: LINKEDIN SCRAPER (Playwright)                │
│    (Open LinkedIn → Extract Profile Data → Raw Data Storage)     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│          PHASE 4: PROFILE DATA EXTRACTION                        │
│    (Parse HTML → Extract Names, Companies, Schools)             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│        PHASE 5: AI DATA STRUCTURING (OpenAI/Gemini)             │
│    (Validate Data → Correct Errors → Standardize Format)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│       PHASE 6: DATA CLEANING & DEDUPLICATION                     │
│    (Remove Duplicates → Fill Missing → Normalize Fields)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            PHASE 7: CSV EXPORT                                   │
│        (Format → Save → Generate Report)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  OUTPUT CSV FILE│
                    │  CLEAN DATASET  │
                    └─────────────────┘
```

### Component Interaction
1. **Search Module** → Discovers LinkedIn profile URLs using Google Search
2. **Scraper Module** → Automates LinkedIn page crawling and data extraction
3. **Parser Module** → Extracts structured information from HTML content
4. **AI Module** → Validates and enriches data using LLM capabilities
5. **Cleaner Module** → Removes duplicates and standardizes formats
6. **Exporter Module** → Formats and exports data to CSV

---

## Folder Structure

```
alumni-extractor/
│
├── README.md                          # Project overview
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore file
│
├── config/
│   ├── __init__.py
│   ├── settings.py                    # Configuration management
│   └── api_keys.py                    # API key handling
│
├── src/
│   ├── __init__.py
│   │
│   ├── search/
│   │   ├── __init__.py
│   │   ├── google_search.py           # Google search integration
│   │   └── search_utils.py            # Helper functions for searching
│   │
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── linkedin_scraper.py        # Playwright-based LinkedIn scraper
│   │   ├── profile_extractor.py       # HTML parsing and data extraction
│   │   └── scraper_utils.py           # Scraper helper functions
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── openai_handler.py          # OpenAI API integration
│   │   ├── gemini_handler.py          # Google Gemini API integration
│   │   ├── ai_validator.py            # Data validation logic
│   │   └── prompts.py                 # AI prompts for validation
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── cleaner.py                 # Data cleaning & deduplication
│   │   ├── validator.py               # Data validation rules
│   │   └── normalizer.py              # Data normalization
│   │
│   ├── export/
│   │   ├── __init__.py
│   │   └── csv_exporter.py            # CSV export functionality
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py                  # Logging configuration
│   │   ├── helpers.py                 # General utility functions
│   │   └── cache.py                   # Caching mechanisms
│   │
│   └── main.py                        # Main orchestration script
│
├── tests/
│   ├── __init__.py
│   ├── test_search.py                 # Search module tests
│   ├── test_scraper.py                # Scraper module tests
│   ├── test_ai.py                     # AI module tests
│   ├── test_cleaner.py                # Data cleaning tests
│   └── test_exporter.py               # Export module tests
│
├── output/
│   ├── raw_data.json                  # Raw extracted data
│   ├── processed_data.json            # AI-processed data
│   └── alumni_data.csv                # Final CSV export
│
├── logs/
│   └── app.log                        # Application logs
│
└── ui/ (Phase 8)
    ├── __init__.py
    ├── app.py                         # Flask/Streamlit web app
    └── templates/                     # HTML templates
```

---

# Phase-wise Implementation Plan

---

## PHASE 1: Environment Setup & Project Initialization

### Goal
Set up development environment, install dependencies, configure API keys, and establish project structure.

### What We'll Build
- Python virtual environment
- Dependency installation
- Environment configuration system
- Logging setup
- API key management

### Required Tools & Libraries

```bash
# Core dependencies
Python 3.9+
pip (Python package manager)
Git
```

### Step-by-Step Implementation

#### Step 1.1: Create Project Directory and Virtual Environment

```bash
# Create project directory
mkdir alumni-extractor
cd alumni-extractor

# Create virtual environment (Windows)
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Step 1.2: Create Requirements File

Create `requirements.txt`:
```text
playwright==1.40.0
requests==2.31.0
pandas==2.1.3
python-dotenv==1.0.0
openai==1.3.0
google-generativeai==0.3.0
beautifulsoup4==4.12.2
sqlalchemy==2.0.23
pytest==7.4.3
flask==3.0.0
streamlit==1.28.0
```

#### Step 1.3: Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for automation)
playwright install chromium

# Verify installation
python -c "import playwright; print('Playwright installed successfully')"
```

#### Step 1.4: Create Environment Configuration

Create `.env.example`:
```env
# API Keys
SERPAPI_API_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# LinkedIn Settings
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password

# Search Settings
COLLEGE_NAME=Your College Name
BATCH_YEAR=2020
SEARCH_PAGES=5

# Rate Limiting
REQUEST_DELAY=2
MAX_RETRIES=3

# AI Model Settings
AI_MODEL=openai  # or 'gemini'
```

Create `.env` (copy from `.env.example` and fill in values):
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

#### Step 1.5: Create Configuration Management

Create `config/settings.py`:
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # LinkedIn Credentials
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
    
    # Search Configuration
    COLLEGE_NAME = os.getenv('COLLEGE_NAME', 'Default University')
    BATCH_YEAR = int(os.getenv('BATCH_YEAR', 2020))
    SEARCH_PAGES = int(os.getenv('SEARCH_PAGES', 5))
    
    # Rate Limiting
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', 2))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # AI Model
    AI_MODEL = os.getenv('AI_MODEL', 'openai')
    
    # Paths
    OUTPUT_DIR = 'output'
    LOGS_DIR = 'logs'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_keys = ['SERPAPI_API_KEY', 'OPENAI_API_KEY', 'LINKEDIN_EMAIL']
        for key in required_keys:
            if not getattr(cls, key):
                raise ValueError(f"Missing required configuration: {key}")

config = Config()
```

#### Step 1.6: Create Logging System

Create `src/utils/logger.py`:
```python
import logging
import os
from datetime import datetime

def setup_logger(name, log_level=logging.INFO):
    """Setup logger configuration"""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    
    # Create file handler
    log_file = f"logs/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to handlers
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger

# Create application logger
app_logger = setup_logger('alumni_extractor')
```

#### Step 1.7: Create Folder Structure

```bash
# Create directory structure
mkdir -p config src/{search,scraper,ai,data,export,utils} tests output logs

# Create __init__.py files
touch config/__init__.py
touch src/__init__.py
touch src/search/__init__.py
touch src/scraper/__init__.py
touch src/ai/__init__.py
touch src/data/__init__.py
touch src/export/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

#### Step 1.8: Create Project Entry Point

Create `src/main.py`:
```python
"""
Main entry point for Alumni Data Extractor
"""
import sys
import os
from config.settings import config
from src.utils.logger import app_logger

def main():
    """Main execution function"""
    try:
        app_logger.info("Starting Alumni Data Extractor")
        
        # Validate configuration
        config.validate()
        app_logger.info("Configuration validated successfully")
        
        # TODO: Implement main workflow
        app_logger.info("Setup completed successfully")
        
    except Exception as e:
        app_logger.error(f"Error in main execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Expected Output
- ✅ Virtual environment created and activated
- ✅ All dependencies installed
- ✅ Environment variables configured
- ✅ Logging system ready
- ✅ Project folder structure organized
- ✅ Configuration management system in place

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'playwright'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `playwright: command not found` | Playwright browsers not installed | Run `playwright install chromium` |
| `python: command not found` (macOS/Linux) | Python not in PATH | Install Python or add to PATH |
| `Permission denied` (macOS/Linux) | Missing execute permissions | Run `chmod +x venv/bin/activate` |
| `KeyError: 'SERPAPI_API_KEY'` | Missing .env file | Copy .env.example to .env and fill in values |

---

## PHASE 2: Google Search Integration

### Goal
Implement smart Google search to discover LinkedIn profile URLs of target alumni.

### What We'll Build
- SerpAPI integration for Google searches
- LinkedIn URL filtering and validation
- Search query builder for targeted searches
- Result storage and deduplication

### Required Tools & Libraries
```python
requests==2.31.0
serpapi==0.3.1  # Official SerpAPI Python SDK
urllib3  # URL parsing and validation
```

### Step-by-Step Implementation

#### Step 2.1: Create Search Query Builder

Create `src/search/search_utils.py`:
```python
"""
Utility functions for search query building
"""

def build_linkedin_search_query(college_name, batch_year, profile_name=None):
    """
    Build optimized Google search query for LinkedIn profiles
    
    Args:
        college_name (str): Name of the college
        batch_year (int): Graduation year
        profile_name (str, optional): Specific person name
    
    Returns:
        str: Formatted search query
    """
    if profile_name:
        query = f'site:linkedin.com/in/ "{profile_name}" "{college_name}" {batch_year}'
    else:
        query = f'site:linkedin.com/in/ "{college_name}" {batch_year}'
    
    return query


def extract_linkedin_urls(search_results):
    """
    Extract LinkedIn URLs from search results
    
    Args:
        search_results (list): List of search result dictionaries
    
    Returns:
        list: Extracted LinkedIn profile URLs
    """
    linkedin_urls = []
    
    for result in search_results:
        url = result.get('link', '')
        if 'linkedin.com/in' in url:
            linkedin_urls.append(url)
    
    return linkedin_urls


def is_valid_linkedin_profile_url(url):
    """
    Validate if URL is a valid LinkedIn profile URL
    
    Args:
        url (str): URL to validate
    
    Returns:
        bool: True if valid LinkedIn profile URL
    """
    return (
        'linkedin.com/in/' in url and
        not '/company/' in url and
        not '/school/' in url
    )
```

#### Step 2.2: Create SerpAPI Integration

Create `src/search/google_search.py`:
```python
"""
Google Search integration using SerpAPI
"""
import requests
import json
import time
from datetime import datetime
from config.settings import config
from src.utils.logger import app_logger
from src.search.search_utils import (
    build_linkedin_search_query,
    extract_linkedin_urls,
    is_valid_linkedin_profile_url
)

class GoogleSearcher:
    """Handle Google search queries via SerpAPI"""
    
    def __init__(self):
        self.api_key = config.SERPAPI_API_KEY
        self.base_url = "https://serpapi.com/search"
        self.request_delay = config.REQUEST_DELAY
        self.max_retries = config.MAX_RETRIES
        
    def search(self, college_name, batch_year, num_pages=5):
        """
        Search for LinkedIn profiles
        
        Args:
            college_name (str): Name of the college
            batch_year (int): Graduation year
            num_pages (int): Number of search pages to retrieve
        
        Returns:
            list: Discovered LinkedIn URLs
        """
        all_urls = []
        
        try:
            for page in range(num_pages):
                app_logger.info(f"Searching page {page + 1}/{num_pages}")
                
                # Build search query
                query = build_linkedin_search_query(college_name, batch_year)
                
                # Make API request
                results = self._make_request(
                    query,
                    start=page * 10
                )
                
                if not results:
                    app_logger.warning(f"No results on page {page + 1}")
                    break
                
                # Extract LinkedIn URLs
                urls = extract_linkedin_urls(results)
                all_urls.extend(urls)
                
                app_logger.info(f"Found {len(urls)} profiles on page {page + 1}")
                
                # Rate limiting
                time.sleep(self.request_delay)
            
            # Remove duplicates
            all_urls = list(set(all_urls))
            
            app_logger.info(f"Total unique profiles discovered: {len(all_urls)}")
            return all_urls
            
        except Exception as e:
            app_logger.error(f"Search error: {str(e)}")
            return []
    
    def _make_request(self, query, start=0, retries=0):
        """
        Make API request to SerpAPI
        
        Args:
            query (str): Search query
            start (int): Result offset
            retries (int): Retry count
        
        Returns:
            list: Search results
        """
        try:
            params = {
                'api_key': self.api_key,
                'q': query,
                'engine': 'google',
                'start': start,
                'num': 10,
                'hl': 'en'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('organic_results', [])
            
        except requests.RequestException as e:
            if retries < self.max_retries:
                app_logger.warning(f"Request failed, retrying... ({retries + 1}/{self.max_retries})")
                time.sleep(2 ** retries)  # Exponential backoff
                return self._make_request(query, start, retries + 1)
            else:
                app_logger.error(f"Request failed after {self.max_retries} retries: {str(e)}")
                return []
    
    def search_specific_person(self, name, college_name, batch_year):
        """
        Search for a specific person's LinkedIn profile
        
        Args:
            name (str): Person's name
            college_name (str): College name
            batch_year (int): Graduation year
        
        Returns:
            str: LinkedIn profile URL or None
        """
        query = build_linkedin_search_query(college_name, batch_year, name)
        results = self._make_request(query)
        
        if results:
            urls = extract_linkedin_urls(results)
            return urls[0] if urls else None
        
        return None
    
    def save_results(self, urls, filename='output/discovered_urls.json'):
        """
        Save discovered URLs to file
        
        Args:
            urls (list): URLs to save
            filename (str): Output filename
        """
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'total_urls': len(urls),
                'urls': urls
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            app_logger.info(f"Results saved to {filename}")
            
        except Exception as e:
            app_logger.error(f"Error saving results: {str(e)}")
```

#### Step 2.3: Test Google Search Module

Create `tests/test_search.py`:
```python
"""
Tests for Google Search module
"""
import pytest
from src.search.google_search import GoogleSearcher
from src.search.search_utils import (
    build_linkedin_search_query,
    is_valid_linkedin_profile_url
)

def test_build_search_query():
    """Test search query building"""
    query = build_linkedin_search_query("MIT", 2020)
    assert "linkedin.com" in query
    assert "2020" in query
    assert "MIT" in query

def test_invalid_linkedin_urls():
    """Test LinkedIn URL validation"""
    valid_urls = [
        "https://www.linkedin.com/in/john-doe-123456/",
        "https://linkedin.com/in/jane-smith/"
    ]
    
    invalid_urls = [
        "https://www.linkedin.com/company/google/",
        "https://www.linkedin.com/school/mit/"
    ]
    
    for url in valid_urls:
        assert is_valid_linkedin_profile_url(url) == True
    
    for url in invalid_urls:
        assert is_valid_linkedin_profile_url(url) == False
```

### Expected Output
- ✅ SerpAPI integrated for Google searches
- ✅ Search query builder for targeted searches
- ✅ LinkedIn URL extraction and validation
- ✅ Result storage in JSON format
- ✅ Error handling with retries
- ✅ Logging of all search activities

### Sample Output (JSON)
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "total_urls": 145,
  "urls": [
    "https://www.linkedin.com/in/john-doe-123456/",
    "https://www.linkedin.com/in/jane-smith-789012/",
    "https://www.linkedin.com/in/robert-johnson-345678/"
  ]
}
```

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid API key | Check SERPAPI_API_KEY in .env |
| `429 Too Many Requests` | Rate limit exceeded | Increase REQUEST_DELAY in .env |
| `No results found` | College name not found | Try different college name format |
| `Connection timeout` | Network issue or SerpAPI down | Wait and retry, check internet connection |
| `Empty URL list` | Wrong search query format | Verify college name and batch year format |

---

## PHASE 3: LinkedIn Alumni Scraper (Playwright)

### Goal
Automate LinkedIn profile data collection using Playwright browser automation.

### What We'll Build
- Playwright-based LinkedIn scraper
- Authentication handling
- Profile page navigation
- HTML content extraction
- Error handling and retry logic

### Required Tools & Libraries
```python
playwright==1.40.0
beautifulsoup4==4.12.2
lxml==4.9.3
```

### Step-by-Step Implementation

#### Step 3.1: Create Playwright Scraper Base

Create `src/scraper/linkedin_scraper.py`:
```python
"""
LinkedIn scraper using Playwright for browser automation
"""
import asyncio
import json
import time
from datetime import datetime
from config.settings import config
from src.utils.logger import app_logger
from playwright.async_api import async_playwright, Page

class LinkedInScraper:
    """Automate LinkedIn profile scraping"""
    
    def __init__(self):
        self.email = config.LINKEDIN_EMAIL
        self.password = config.LINKEDIN_PASSWORD
        self.request_delay = config.REQUEST_DELAY
        self.browser = None
        self.context = None
        self.page = None
        
    async def initialize(self):
        """Initialize browser and context"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
            
            # Create context with user agent
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            )
            
            self.page = await self.context.new_page()
            app_logger.info("Browser initialized successfully")
            
        except Exception as e:
            app_logger.error(f"Failed to initialize browser: {str(e)}")
            raise
    
    async def authenticate(self):
        """Authenticate to LinkedIn"""
        try:
            app_logger.info("Attempting LinkedIn authentication")
            
            # Navigate to login page
            await self.page.goto('https://www.linkedin.com/login')
            await asyncio.sleep(2)
            
            # Fill in email
            await self.page.fill('input[name="session_key"]', self.email)
            await asyncio.sleep(1)
            
            # Fill in password
            await self.page.fill('input[name="session_password"]', self.password)
            await asyncio.sleep(1)
            
            # Click login button
            await self.page.click('button[type="submit"]')
            
            # Wait for navigation
            await self.page.wait_for_url('https://www.linkedin.com/feed/**', timeout=15000)
            
            app_logger.info("Authentication successful")
            return True
            
        except Exception as e:
            app_logger.error(f"Authentication failed: {str(e)}")
            return False
    
    async def scrape_profile(self, profile_url):
        """
        Scrape individual LinkedIn profile
        
        Args:
            profile_url (str): LinkedIn profile URL
        
        Returns:
            dict: Extracted profile data
        """
        try:
            app_logger.info(f"Scraping profile: {profile_url}")
            
            # Navigate to profile
            await self.page.goto(profile_url, wait_until='networkidle')
            await asyncio.sleep(self.request_delay)
            
            # Scroll to load all content
            await self._scroll_page()
            
            # Get page content
            content = await self.page.content()
            
            # Extract data
            profile_data = {
                'url': profile_url,
                'html_content': content,
                'timestamp': datetime.now().isoformat(),
                'scraped_successfully': True
            }
            
            app_logger.info(f"Profile scraped successfully: {profile_url}")
            return profile_data
            
        except Exception as e:
            app_logger.error(f"Error scraping profile {profile_url}: {str(e)}")
            return {
                'url': profile_url,
                'error': str(e),
                'scraped_successfully': False
            }
    
    async def _scroll_page(self):
        """Scroll page to load all content"""
        try:
            # Scroll to bottom multiple times
            for _ in range(3):
                await self.page.evaluate('window.scrollBy(0, window.innerHeight)')
                await asyncio.sleep(1)
            
            # Scroll back to top
            await self.page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(1)
            
        except Exception as e:
            app_logger.warning(f"Scroll error: {str(e)}")
    
    async def scrape_multiple_profiles(self, urls):
        """
        Scrape multiple LinkedIn profiles
        
        Args:
            urls (list): List of LinkedIn URLs
        
        Returns:
            list: Scraped data for all profiles
        """
        results = []
        
        for i, url in enumerate(urls):
            app_logger.info(f"Scraping {i+1}/{len(urls)} profiles")
            
            try:
                profile_data = await self.scrape_profile(url)
                results.append(profile_data)
                
                # Random delay to avoid blocking
                time.sleep(self.request_delay)
                
            except Exception as e:
                app_logger.error(f"Error processing {url}: {str(e)}")
                results.append({
                    'url': url,
                    'error': str(e),
                    'scraped_successfully': False
                })
        
        return results
    
    async def close(self):
        """Close browser and context"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            app_logger.info("Browser closed successfully")
        except Exception as e:
            app_logger.error(f"Error closing browser: {str(e)}")
    
    async def save_results(self, results, filename='output/raw_profiles.json'):
        """Save scraped data to file"""
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'total_profiles': len(results),
                'successful': len([r for r in results if r.get('scraped_successfully', False)]),
                'profiles': results
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            app_logger.info(f"Results saved to {filename}")
            
        except Exception as e:
            app_logger.error(f"Error saving results: {str(e)}")


async def main_scraper(urls):
    """Main scraper function"""
    scraper = LinkedInScraper()
    
    try:
        await scraper.initialize()
        
        # Authenticate
        if not await scraper.authenticate():
            app_logger.error("Authentication failed, exiting")
            return
        
        # Scrape profiles
        results = await scraper.scrape_multiple_profiles(urls)
        
        # Save results
        await scraper.save_results(results)
        
    finally:
        await scraper.close()

# Usage
if __name__ == "__main__":
    urls = [
        "https://www.linkedin.com/in/john-doe-123456/",
        "https://www.linkedin.com/in/jane-smith-789012/"
    ]
    asyncio.run(main_scraper(urls))
```

#### Step 3.2: Create Helper Functions

Create `src/scraper/scraper_utils.py`:
```python
"""
Utility functions for LinkedIn scraper
"""
import hashlib
from urllib.parse import urlparse

def normalize_linkedin_url(url):
    """
    Normalize LinkedIn URL to standard format
    
    Args:
        url (str): Raw LinkedIn URL
    
    Returns:
        str: Normalized URL
    """
    # Remove trailing slash and query parameters
    url = url.split('?')[0].rstrip('/')
    
    # Ensure HTTPS
    if url.startswith('http://'):
        url = url.replace('http://', 'https://', 1)
    
    return url


def get_profile_id_from_url(url):
    """
    Extract profile ID from LinkedIn URL
    
    Args:
        url (str): LinkedIn profile URL
    
    Returns:
        str: Profile identifier
    """
    parts = url.rstrip('/').split('/')
    if parts:
        return parts[-1]
    return None


def is_linkedin_url_accessible(url):
    """
    Check if LinkedIn URL is valid and accessible
    
    Args:
        url (str): URL to check
    
    Returns:
        bool: True if URL is valid
    """
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ['http', 'https'] and
            'linkedin.com' in parsed.netloc and
            '/in/' in parsed.path
        )
    except:
        return False


def hash_profile_url(url):
    """Generate hash for profile URL (for deduplication)"""
    normalized_url = normalize_linkedin_url(url)
    return hashlib.md5(normalized_url.encode()).hexdigest()
```

### Expected Output
- ✅ Browser automation with Playwright
- ✅ LinkedIn authentication
- ✅ HTML content extraction
- ✅ Error handling and retries
- ✅ Raw profile data saved in JSON

### Sample Output (JSON structure)
```json
{
  "timestamp": "2024-01-15T10:35:22.456789",
  "total_profiles": 145,
  "successful": 142,
  "profiles": [
    {
      "url": "https://www.linkedin.com/in/john-doe-123456/",
      "html_content": "<html>...</html>",
      "timestamp": "2024-01-15T10:35:22.456789",
      "scraped_successfully": true
    }
  ]
}
```

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `Timeout waiting for login` | LinkedIn blocked automated login | Use browser automation detection evasion or manual cookies |
| `403 Forbidden` | LinkedIn detected bot activity | Increase delays, use proxy, or rotate IP |
| `Page not found` | Profile URL invalid/deleted | Skip and continue with next profile |
| `Connection refused` | Network issue | Check internet connection, retry with longer timeout |
| `Browser not available` | Playwright browsers not installed | Run `playwright install chromium` |

---

## PHASE 4: Profile Data Extraction

### Goal
Parse HTML content and extract structured data from LinkedIn profiles.

### What We'll Build
- HTML parser for profile data
- Data extraction functions
- Field validation
- Error handling for malformed data

### Required Tools & Libraries
```python
beautifulsoup4==4.12.2
lxml==4.9.3
re (Python standard library - regex)
```

### Step-by-Step Implementation

#### Step 4.1: Create Profile Parser

Create `src/scraper/profile_extractor.py`:
```python
"""
Extract structured data from LinkedIn profile HTML
"""
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime
from src.utils.logger import app_logger

class ProfileExtractor:
    """Extract profile information from LinkedIn HTML"""
    
    def __init__(self):
        self.extracted_fields = [
            'name',
            'headline',
            'current_company',
            'current_position',
            'education',
            'education_list'
        ]
    
    def extract(self, html_content, profile_url):
        """
        Extract all available data from HTML
        
        Args:
            html_content (str): HTML content of profile
            profile_url (str): LinkedIn profile URL
        
        Returns:
            dict: Extracted profile data
        """
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            
            data = {
                'url': profile_url,
                'name': self._extract_name(soup),
                'headline': self._extract_headline(soup),
                'current_company': self._extract_current_company(soup),
                'current_position': self._extract_current_position(soup),
                'education': self._extract_education(soup),
                'extraction_timestamp': datetime.now().isoformat(),
                'extraction_success': True
            }
            
            app_logger.info(f"Data extracted from {profile_url}")
            return data
            
        except Exception as e:
            app_logger.error(f"Extraction error for {profile_url}: {str(e)}")
            return {
                'url': profile_url,
                'error': str(e),
                'extraction_success': False
            }
    
    def _extract_name(self, soup):
        """Extract person's name"""
        try:
            # Try multiple selectors
            selectors = [
                'h1 span',
                'h1.text-heading-xlarge',
                'div[aria-label*="name"]'
            ]
            
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    return element.get_text(strip=True)
            
            # Fallback: look for text in h1
            h1 = soup.find('h1')
            if h1:
                return h1.get_text(strip=True)
            
            return None
            
        except Exception as e:
            app_logger.warning(f"Error extracting name: {str(e)}")
            return None
    
    def _extract_headline(self, soup):
        """Extract profile headline/summary"""
        try:
            # Headlines are usually in div with specific classes
            selectors = [
                'div.text-body-medium',
                'div[aria-label*="Headline"]',
                'div.reader-main-headline'
            ]
            
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(strip=True)
                    if text and len(text) > 10:  # Filter out noise
                        return text
            
            return None
            
        except Exception as e:
            app_logger.warning(f"Error extracting headline: {str(e)}")
            return None
    
    def _extract_current_company(self, soup):
        """Extract current company"""
        try:
            # Look for current position section
            experience_section = soup.find('section', {'id': 'experience'})
            
            if experience_section:
                # Get first company (current company)
                company_element = experience_section.find(
                    'div',
                    class_='base-card'
                )
                
                if company_element:
                    # Try to find company name
                    company_name = company_element.find('h3')
                    if company_name:
                        return company_name.get_text(strip=True)
            
            return None
            
        except Exception as e:
            app_logger.warning(f"Error extracting company: {str(e)}")
            return None
    
    def _extract_current_position(self, soup):
        """Extract current position/title"""
        try:
            experience_section = soup.find('section', {'id': 'experience'})
            
            if experience_section:
                # Get first position
                position_element = experience_section.find('h4')
                if position_element:
                    return position_element.get_text(strip=True)
            
            return None
            
        except Exception as e:
            app_logger.warning(f"Error extracting position: {str(e)}")
            return None
    
    def _extract_education(self, soup):
        """Extract education information"""
        try:
            education_list = []
            education_section = soup.find('section', {'id': 'education'})
            
            if education_section:
                # Get all education entries
                entries = education_section.find_all('div', class_='base-card')
                
                for entry in entries:
                    school_name = entry.find('h3')
                    degree_info = entry.find('div', class_='base-card__subtitle')
                    
                    education_list.append({
                        'school': school_name.get_text(strip=True) if school_name else None,
                        'degree': degree_info.get_text(strip=True) if degree_info else None
                    })
            
            # Return as dict with primary education
            if education_list:
                return {
                    'primary_school': education_list[0].get('school'),
                    'primary_degree': education_list[0].get('degree'),
                    'all_education': education_list
                }
            
            return None
            
        except Exception as e:
            app_logger.warning(f"Error extracting education: {str(e)}")
            return None


def process_raw_profiles(raw_profiles_file):
    """
    Process raw profiles and extract structured data
    
    Args:
        raw_profiles_file (str): Path to raw profiles JSON
    
    Returns:
        list: Extracted profile data
    """
    try:
        # Load raw data
        with open(raw_profiles_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        extractor = ProfileExtractor()
        extracted_profiles = []
        
        for profile in raw_data.get('profiles', []):
            if profile.get('scraped_successfully'):
                extracted_data = extractor.extract(
                    profile.get('html_content'),
                    profile.get('url')
                )
                extracted_profiles.append(extracted_data)
        
        app_logger.info(f"Extracted data from {len(extracted_profiles)} profiles")
        return extracted_profiles
        
    except Exception as e:
        app_logger.error(f"Error processing raw profiles: {str(e)}")
        return []


def save_extracted_data(data, filename='output/extracted_data.json'):
    """Save extracted profile data"""
    try:
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_profiles': len(data),
            'profiles': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        app_logger.info(f"Extracted data saved to {filename}")
        
    except Exception as e:
        app_logger.error(f"Error saving extracted data: {str(e)}")
```

### Expected Output
- ✅ Name extraction
- ✅ Headline extraction
- ✅ Company extraction
- ✅ Position extraction
- ✅ Education extraction
- ✅ Structured JSON output

### Sample Output
```json
{
  "url": "https://www.linkedin.com/in/john-doe-123456/",
  "name": "John Doe",
  "headline": "Software Engineer at Google | MIT Graduate",
  "current_company": "Google",
  "current_position": "Senior Software Engineer",
  "education": {
    "primary_school": "Massachusetts Institute of Technology (MIT)",
    "primary_degree": "Bachelor of Science in Computer Science",
    "all_education": [
      {
        "school": "MIT",
        "degree": "BS Computer Science"
      }
    ]
  },
  "extraction_timestamp": "2024-01-15T10:40:15.123456",
  "extraction_success": true
}
```

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `KeyError: 'profiles'` | Raw data format incorrect | Verify raw profiles JSON structure |
| `AttributeError: 'NoneType'` | HTML selector returned None | Update selectors for LinkedIn changes |
| `UnicodeDecodeError` | Encoding issue | Ensure UTF-8 encoding when saving |
| `Empty extracted data` | Selectors don't match HTML structure | Inspect LinkedIn HTML and update selectors |

---

## PHASE 5: AI Data Structuring & Validation

### Goal
Use AI/LLM to validate extracted data, correct errors, and ensure consistent formatting.

### What We'll Build
- OpenAI API integration
- Google Gemini API integration
- Data validation prompts
- Error correction logic
- Confidence scoring

### Required Tools & Libraries
```python
openai==1.3.0
google-generativeai==0.3.0
```

### Step-by-Step Implementation

#### Step 5.1: Create AI Handler Base

Create `src/ai/prompts.py`:
```python
"""
AI prompts for data validation and enrichment
"""

VALIDATION_PROMPT = """
Analyze the following extracted LinkedIn profile data and validate/correct it:

Profile Data:
- Name: {name}
- Headline: {headline}
- Current Company: {current_company}
- Current Position: {current_position}
- University: {university}
- Degree: {degree}

Please:
1. Verify the data is accurate and complete
2. Correct any obvious errors (typos, formatting)
3. Standardize company names (e.g., "google" -> "Google")
4. Standardize degree names (e.g., "BS" -> "Bachelor of Science")
5. Extract batch/graduation year if available in headline
6. Provide confidence score (0-100) for each field

Return as JSON with this structure:
{{
    "name": "corrected name",
    "headline": "corrected headline",
    "current_company": "standardized company",
    "current_position": "corrected position",
    "university": "standardized university",
    "degree": "standardized degree",
    "graduation_year": 2020 or null,
    "confidence": {{"name": 95, "company": 90, ...}}
}}
"""

ENRICHMENT_PROMPT = """
Based on the following LinkedIn profile data, provide additional context:

Profile:
- Name: {name}
- Company: {current_company}
- Position: {current_position}
- University: {university}

Please provide:
1. Industry of the current company
2. Likely college batch year (if not provided)
3. Career path analysis (brief)
4. Skills that can be inferred from position

Return as JSON.
"""
```

#### Step 5.2: Create OpenAI Handler

Create `src/ai/openai_handler.py`:
```python
"""
OpenAI API integration for data validation
"""
import json
import re
from config.settings import config
from src.utils.logger import app_logger
from src.ai.prompts import VALIDATION_PROMPT, ENRICHMENT_PROMPT
from openai import OpenAI

class OpenAIHandler:
    """Handle data validation using OpenAI GPT"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
    
    def validate_profile(self, profile_data):
        """
        Validate and correct profile data using OpenAI
        
        Args:
            profile_data (dict): Extracted profile data
        
        Returns:
            dict: Validated profile data
        """
        try:
            # Prepare prompt
            prompt = VALIDATION_PROMPT.format(
                name=profile_data.get('name', ''),
                headline=profile_data.get('headline', ''),
                current_company=profile_data.get('current_company', ''),
                current_position=profile_data.get('current_position', ''),
                university=profile_data.get('education', {}).get('primary_school', ''),
                degree=profile_data.get('education', {}).get('primary_degree', '')
            )
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data validation expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            validated_data = json.loads(response_text)
            
            app_logger.info(f"Profile validated: {validated_data.get('name')}")
            return validated_data
            
        except json.JSONDecodeError as e:
            app_logger.error(f"JSON parsing error: {str(e)}")
            return profile_data
        except Exception as e:
            app_logger.error(f"Validation error: {str(e)}")
            return profile_data
    
    def enrich_profile(self, profile_data):
        """
        Enrich profile with additional AI-generated insights
        
        Args:
            profile_data (dict): Profile data to enrich
        
        Returns:
            dict: Enriched profile data
        """
        try:
            prompt = ENRICHMENT_PROMPT.format(
                name=profile_data.get('name', ''),
                current_company=profile_data.get('current_company', ''),
                current_position=profile_data.get('current_position', ''),
                university=profile_data.get('education', {}).get('primary_school', '')
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a career insights expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400
            )
            
            enrichment = json.loads(response.choices[0].message.content)
            
            # Merge enrichment data
            profile_data['enrichment'] = enrichment
            
            app_logger.info(f"Profile enriched: {profile_data.get('name')}")
            return profile_data
            
        except Exception as e:
            app_logger.error(f"Enrichment error: {str(e)}")
            return profile_data
    
    def batch_validate(self, profiles):
        """
        Validate multiple profiles
        
        Args:
            profiles (list): List of profile data
        
        Returns:
            list: Validated profiles
        """
        validated = []
        
        for i, profile in enumerate(profiles):
            app_logger.info(f"Validating profile {i+1}/{len(profiles)}")
            validated_profile = self.validate_profile(profile)
            validated.append(validated_profile)
        
        return validated
```

#### Step 5.3: Create Gemini Handler

Create `src/ai/gemini_handler.py`:
```python
"""
Google Gemini API integration for data validation
"""
import json
import google.generativeai as genai
from config.settings import config
from src.utils.logger import app_logger
from src.ai.prompts import VALIDATION_PROMPT, ENRICHMENT_PROMPT

class GeminiHandler:
    """Handle data validation using Google Gemini"""
    
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def validate_profile(self, profile_data):
        """
        Validate and correct profile data using Gemini
        
        Args:
            profile_data (dict): Extracted profile data
        
        Returns:
            dict: Validated profile data
        """
        try:
            prompt = VALIDATION_PROMPT.format(
                name=profile_data.get('name', ''),
                headline=profile_data.get('headline', ''),
                current_company=profile_data.get('current_company', ''),
                current_position=profile_data.get('current_position', ''),
                university=profile_data.get('education', {}).get('primary_school', ''),
                degree=profile_data.get('education', {}).get('primary_degree', '')
            )
            
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to find JSON in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                validated_data = json.loads(json_str)
                
                app_logger.info(f"Profile validated: {validated_data.get('name')}")
                return validated_data
            else:
                app_logger.warning("Could not extract JSON from response")
                return profile_data
                
        except Exception as e:
            app_logger.error(f"Validation error: {str(e)}")
            return profile_data
    
    def batch_validate(self, profiles):
        """Validate multiple profiles"""
        validated = []
        
        for i, profile in enumerate(profiles):
            app_logger.info(f"Validating profile {i+1}/{len(profiles)}")
            validated_profile = self.validate_profile(profile)
            validated.append(validated_profile)
        
        return validated
```

#### Step 5.4: Create AI Validator Wrapper

Create `src/ai/ai_validator.py`:
```python
"""
Unified AI validation interface
"""
import json
from config.settings import config
from src.utils.logger import app_logger
from src.ai.openai_handler import OpenAIHandler
from src.ai.gemini_handler import GeminiHandler

class AIValidator:
    """Unified interface for AI-based data validation"""
    
    def __init__(self):
        if config.AI_MODEL.lower() == 'openai':
            self.handler = OpenAIHandler()
            app_logger.info("Using OpenAI for validation")
        elif config.AI_MODEL.lower() == 'gemini':
            self.handler = GeminiHandler()
            app_logger.info("Using Gemini for validation")
        else:
            raise ValueError(f"Unknown AI model: {config.AI_MODEL}")
    
    def validate_profile(self, profile_data):
        """Validate profile using configured AI model"""
        return self.handler.validate_profile(profile_data)
    
    def validate_batch(self, profiles):
        """Validate multiple profiles"""
        return self.handler.batch_validate(profiles)
    
    def save_validated_data(self, profiles, filename='output/ai_validated_data.json'):
        """Save AI-validated data"""
        try:
            data = {
                'timestamp': json.dumps(datetime.now(), default=str),
                'ai_model': config.AI_MODEL,
                'total_profiles': len(profiles),
                'profiles': profiles
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            app_logger.info(f"Validated data saved to {filename}")
            
        except Exception as e:
            app_logger.error(f"Error saving validated data: {str(e)}")
```

### Expected Output
- ✅ Data validation using AI
- ✅ Error correction
- ✅ Format standardization
- ✅ Confidence scoring
- ✅ Data enrichment

### Sample Output
```json
{
  "name": "John Doe",
  "headline": "Software Engineer at Google | MIT Graduate",
  "current_company": "Google",
  "current_position": "Senior Software Engineer",
  "university": "Massachusetts Institute of Technology",
  "degree": "Bachelor of Science in Computer Science",
  "graduation_year": 2018,
  "confidence": {
    "name": 98,
    "company": 95,
    "position": 90,
    "university": 100,
    "degree": 95
  }
}
```

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `RateLimitError` | API rate limit exceeded | Implement backoff and queue requests |
| `InvalidAPIKey` | Wrong API key | Verify API key in .env |
| `JSON parse error` | Invalid JSON from API | Add JSON extraction fallback |
| `Timeout` | API request taking too long | Increase timeout or chunk data |

---

## PHASE 6: Data Cleaning & Deduplication

### Goal
Remove duplicates, standardize formats, and handle missing data.

### What We'll Build
- Deduplication logic
- Data normalization functions
- Missing value handling
- Quality scoring

### Required Tools & Libraries
```python
pandas==2.1.3
difflib (Python standard library)
```

### Step-by-Step Implementation

#### Step 6.1: Create Data Cleaner

Create `src/data/cleaner.py`:
```python
"""
Data cleaning and deduplication module
"""
import pandas as pd
import difflib
import json
from datetime import datetime
from src.utils.logger import app_logger

class DataCleaner:
    """Clean and deduplicate profile data"""
    
    def __init__(self):
        self.similarity_threshold = 0.85
    
    def clean_profiles(self, profiles):
        """
        Clean and deduplicate profiles
        
        Args:
            profiles (list): List of profile dictionaries
        
        Returns:
            list: Cleaned profiles
        """
        app_logger.info(f"Starting cleaning of {len(profiles)} profiles")
        
        try:
            # Remove invalid profiles
            valid_profiles = self._filter_valid_profiles(profiles)
            app_logger.info(f"Valid profiles: {len(valid_profiles)}")
            
            # Deduplicate
            deduplicated = self._deduplicate(valid_profiles)
            app_logger.info(f"After deduplication: {len(deduplicated)} profiles")
            
            # Normalize data
            normalized = self._normalize_data(deduplicated)
            
            # Handle missing values
            filled = self._fill_missing_values(normalized)
            
            # Add quality score
            scored = self._add_quality_score(filled)
            
            app_logger.info(f"Cleaning completed. Final count: {len(scored)}")
            return scored
            
        except Exception as e:
            app_logger.error(f"Cleaning error: {str(e)}")
            return profiles
    
    def _filter_valid_profiles(self, profiles):
        """Remove invalid profiles"""
        valid = []
        
        for profile in profiles:
            # Check if profile has required fields
            if profile.get('name') and profile.get('url'):
                valid.append(profile)
            else:
                app_logger.warning(f"Invalid profile: {profile}")
        
        return valid
    
    def _deduplicate(self, profiles):
        """Remove duplicate profiles"""
        deduplicated = []
        seen_names = {}
        
        for profile in profiles:
            name = profile.get('name', '').lower().strip()
            company = profile.get('current_company', '').lower().strip()
            
            # Create composite key
            composite_key = f"{name}|{company}"
            
            if composite_key not in seen_names:
                # Check for similar names (fuzzy matching)
                is_duplicate = False
                for seen_key in seen_names:
                    if self._is_duplicate(composite_key, seen_key):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    deduplicated.append(profile)
                    seen_names[composite_key] = True
                else:
                    app_logger.info(f"Duplicate removed: {name}")
            else:
                app_logger.info(f"Exact duplicate removed: {name}")
        
        return deduplicated
    
    def _is_duplicate(self, key1, key2):
        """Check if two keys represent duplicates"""
        similarity = difflib.SequenceMatcher(None, key1, key2).ratio()
        return similarity > self.similarity_threshold
    
    def _normalize_data(self, profiles):
        """Standardize data formats"""
        normalized = []
        
        for profile in profiles:
            normalized_profile = {
                'name': self._normalize_name(profile.get('name')),
                'url': profile.get('url'),
                'current_company': self._normalize_company(profile.get('current_company')),
                'current_position': self._normalize_position(profile.get('current_position')),
                'university': self._normalize_university(profile.get('university')),
                'degree': self._normalize_degree(profile.get('degree')),
                'graduation_year': profile.get('graduation_year'),
                'headline': profile.get('headline'),
                'confidence': profile.get('confidence', {})
            }
            
            normalized.append(normalized_profile)
        
        return normalized
    
    def _normalize_name(self, name):
        """Normalize person's name"""
        if not name:
            return None
        
        # Title case
        name = ' '.join(word.capitalize() for word in name.split())
        
        # Remove extra spaces
        name = ' '.join(name.split())
        
        return name
    
    def _normalize_company(self, company):
        """Normalize company name"""
        if not company:
            return None
        
        # Company name mapping
        company_mapping = {
            'google': 'Google',
            'microsoft': 'Microsoft',
            'apple': 'Apple',
            'amazon': 'Amazon',
            'meta': 'Meta',
            'facebook': 'Meta',
            'tesla': 'Tesla'
        }
        
        normalized = company.strip()
        lower_company = normalized.lower()
        
        if lower_company in company_mapping:
            return company_mapping[lower_company]
        
        return normalized
    
    def _normalize_position(self, position):
        """Normalize job title"""
        if not position:
            return None
        
        # Remove extra spaces and title case
        return ' '.join(word.capitalize() for word in position.split())
    
    def _normalize_university(self, university):
        """Normalize university name"""
        if not university:
            return None
        
        # Common university mappings
        university_mapping = {
            'mit': 'Massachusetts Institute of Technology',
            'stanford': 'Stanford University',
            'berkeley': 'University of California, Berkeley',
            'harvard': 'Harvard University',
            'uc berkeley': 'University of California, Berkeley'
        }
        
        lower_uni = university.lower().strip()
        
        if lower_uni in university_mapping:
            return university_mapping[lower_uni]
        
        return university.strip()
    
    def _normalize_degree(self, degree):
        """Normalize degree name"""
        if not degree:
            return None
        
        degree_mapping = {
            'bs': 'Bachelor of Science',
            'ba': 'Bachelor of Arts',
            'ms': 'Master of Science',
            'ma': 'Master of Arts',
            'phd': 'Doctor of Philosophy',
            'mba': 'Master of Business Administration'
        }
        
        lower_degree = degree.lower().strip()
        
        if lower_degree in degree_mapping:
            return degree_mapping[lower_degree]
        
        return degree.strip()
    
    def _fill_missing_values(self, profiles):
        """Handle missing values"""
        filled = []
        
        for profile in profiles:
            # Set defaults for None values
            if profile['current_company'] is None:
                profile['current_company'] = 'Unknown'
            
            if profile['current_position'] is None:
                profile['current_position'] = 'Unknown'
            
            if profile['university'] is None:
                profile['university'] = 'Unknown'
            
            if profile['degree'] is None:
                profile['degree'] = 'Unknown'
            
            filled.append(profile)
        
        return filled
    
    def _add_quality_score(self, profiles):
        """Add data quality score to each profile"""
        scored = []
        
        for profile in profiles:
            score = 0
            max_score = 100
            
            # Score each field
            if profile['name'] and profile['name'] != 'Unknown':
                score += 20
            
            if profile['current_company'] and profile['current_company'] != 'Unknown':
                score += 20
            
            if profile['university'] and profile['university'] != 'Unknown':
                score += 25
            
            if profile['graduation_year']:
                score += 20
            
            if profile['confidence']:
                avg_confidence = sum(profile['confidence'].values()) / len(profile['confidence'])
                if avg_confidence > 80:
                    score += 15
            
            profile['quality_score'] = min(score, max_score)
            scored.append(profile)
        
        return scored
```

#### Step 6.2: Create Data Validator

Create `src/data/validator.py`:
```python
"""
Data validation rules and quality checks
"""
import re
from src.utils.logger import app_logger

class DataValidator:
    """Validate profile data quality"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_linkedin_url(url):
        """Validate LinkedIn URL format"""
        return url.startswith('https://www.linkedin.com/in/') or url.startswith('https://linkedin.com/in/')
    
    @staticmethod
    def validate_batch_year(year):
        """Validate batch/graduation year"""
        try:
            year = int(year)
            return 1950 <= year <= 2030
        except:
            return False
    
    @staticmethod
    def validate_profile(profile):
        """
        Comprehensive profile validation
        
        Args:
            profile (dict): Profile data
        
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        # Validate URL
        if not DataValidator.validate_linkedin_url(profile.get('url', '')):
            errors.append("Invalid LinkedIn URL")
        
        # Validate name
        if not profile.get('name'):
            errors.append("Name is required")
        
        # Validate graduation year if present
        if profile.get('graduation_year'):
            if not DataValidator.validate_batch_year(profile['graduation_year']):
                errors.append("Invalid graduation year")
        
        is_valid = len(errors) == 0
        return is_valid, errors
```

### Expected Output
- ✅ Deduplicated profiles
- ✅ Standardized company names
- ✅ Standardized education data
- ✅ Quality scores for each profile
- ✅ Consistent data formats

### Sample Output
```json
{
  "name": "John Doe",
  "url": "https://www.linkedin.com/in/john-doe-123456/",
  "current_company": "Google",
  "current_position": "Senior Software Engineer",
  "university": "Massachusetts Institute of Technology",
  "degree": "Bachelor of Science",
  "graduation_year": 2018,
  "quality_score": 95
}
```

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `Duplicate removal too aggressive` | Threshold too low | Increase similarity_threshold |
| `Missing values not handled` | Exception in fill function | Check field names match |
| `Quality score calculation fails` | Empty confidence dict | Add default confidence values |

---

## PHASE 7: CSV Export

### Goal
Export cleaned and validated data to CSV format for easy consumption.

### What We'll Build
- CSV exporter with configurable columns
- Data formatting
- File generation
- Summary reports

### Required Tools & Libraries
```python
pandas==2.1.3
csv (Python standard library)
```

### Step-by-Step Implementation

#### Step 7.1: Create CSV Exporter

Create `src/export/csv_exporter.py`:
```python
"""
Export cleaned profile data to CSV
"""
import pandas as pd
import json
from datetime import datetime
from src.utils.logger import app_logger

class CSVExporter:
    """Export profile data to CSV format"""
    
    # Default columns for CSV export
    DEFAULT_COLUMNS = [
        'name',
        'url',
        'current_company',
        'current_position',
        'university',
        'degree',
        'graduation_year',
        'headline',
        'quality_score'
    ]
    
    def __init__(self, columns=None):
        self.columns = columns or self.DEFAULT_COLUMNS
    
    def export_to_csv(self, profiles, output_file='output/alumni_data.csv'):
        """
        Export profiles to CSV
        
        Args:
            profiles (list): List of cleaned profile dictionaries
            output_file (str): Path to output CSV file
        
        Returns:
            str: Path to exported file
        """
        try:
            app_logger.info(f"Exporting {len(profiles)} profiles to CSV")
            
            # Create DataFrame
            df = pd.DataFrame(profiles)
            
            # Select only specified columns (if they exist)
            available_columns = [col for col in self.columns if col in df.columns]
            df = df[available_columns]
            
            # Sort by quality score (descending)
            if 'quality_score' in df.columns:
                df = df.sort_values('quality_score', ascending=False)
            
            # Remove rows with empty names
            df = df[df['name'].notna() & (df['name'] != '')]
            
            # Export to CSV
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            app_logger.info(f"CSV exported successfully: {output_file}")
            app_logger.info(f"Total rows: {len(df)}")
            
            return output_file
            
        except Exception as e:
            app_logger.error(f"CSV export error: {str(e)}")
            raise
    
    def generate_summary_report(self, profiles, output_file='output/summary_report.txt'):
        """
        Generate summary report of exported data
        
        Args:
            profiles (list): List of profiles
            output_file (str): Path to output file
        """
        try:
            # Calculate statistics
            total_profiles = len(profiles)
            
            # Get unique companies
            companies = set(p.get('current_company', 'Unknown') for p in profiles)
            
            # Get unique universities
            universities = set(p.get('university', 'Unknown') for p in profiles)
            
            # Average quality score
            quality_scores = [p.get('quality_score', 0) for p in profiles if p.get('quality_score')]
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            # Generate graduation year distribution
            years = {}
            for profile in profiles:
                year = profile.get('graduation_year')
                if year:
                    years[year] = years.get(year, 0) + 1
            
            # Generate report
            report = f"""
ALUMNI DATA EXTRACTION REPORT
{'='*50}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS
-----------------
Total Profiles: {total_profiles}
Average Quality Score: {avg_quality:.2f}/100
Unique Companies: {len(companies)}
Unique Universities: {len(universities)}

TOP COMPANIES
-----------
"""
            
            # Sort companies by frequency
            company_freq = {}
            for p in profiles:
                company = p.get('current_company', 'Unknown')
                company_freq[company] = company_freq.get(company, 0) + 1
            
            for company, count in sorted(company_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
                report += f"\n{company}: {count} profiles"
            
            report += f"""

GRADUATION YEAR DISTRIBUTION
-----------------------------
"""
            for year in sorted(years.keys()):
                report += f"\n{year}: {years[year]} graduates"
            
            report += f"""

UNIVERSITIES REPRESENTED
------------------------
"""
            for university in sorted(universities):
                if university != 'Unknown':
                    report += f"\n- {university}"
            
            # Save report
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            app_logger.info(f"Summary report generated: {output_file}")
            print(report)
            
        except Exception as e:
            app_logger.error(f"Report generation error: {str(e)}")


def load_and_export(json_file, csv_output='output/alumni_data.csv'):
    """
    Load profiles from JSON and export to CSV
    
    Args:
        json_file (str): Path to JSON file with cleaned profiles
        csv_output (str): Path to output CSV file
    
    Returns:
        str: Path to exported CSV
    """
    try:
        # Load JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        profiles = data.get('profiles', [])
        
        # Export to CSV
        exporter = CSVExporter()
        csv_file = exporter.export_to_csv(profiles, csv_output)
        
        # Generate summary report
        report_file = csv_output.replace('.csv', '_report.txt')
        exporter.generate_summary_report(profiles, report_file)
        
        return csv_file
        
    except Exception as e:
        app_logger.error(f"Load and export error: {str(e)}")
        return None
```

#### Step 7.2: Create Export Utilities

Create utility functions for export validation:

```python
def validate_csv(csv_file):
    """Validate exported CSV file"""
    try:
        df = pd.read_csv(csv_file)
        
        # Check minimum columns
        required_cols = ['name', 'url']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Check for empty rows
        empty_rows = df[df['name'].isna() | (df['name'] == '')].shape[0]
        
        app_logger.info(f"CSV validation: {len(df)} rows, {empty_rows} empty")
        return True
        
    except Exception as e:
        app_logger.error(f"CSV validation error: {str(e)}")
        return False
```

### Expected Output
- ✅ Clean CSV file with proper headers
- ✅ All required columns populated
- ✅ UTF-8 encoding
- ✅ Summary report with statistics
- ✅ Company and university distribution

### Sample CSV Output
```csv
name,url,current_company,current_position,university,degree,graduation_year,quality_score
John Doe,https://www.linkedin.com/in/john-doe-123456/,Google,Senior Software Engineer,Massachusetts Institute of Technology,Bachelor of Science,2018,95
Jane Smith,https://www.linkedin.com/in/jane-smith-789012/,Microsoft,Principal Engineer,Stanford University,Bachelor of Science,2016,92
Robert Johnson,https://www.linkedin.com/in/robert-johnson-345678/,Amazon,Engineering Manager,Harvard University,Master of Business Administration,2020,88
```

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `UnicodeEncodeError` | Special characters in data | Ensure UTF-8 encoding |
| `FileNotFoundError` | Output directory doesn't exist | Create output directory first |
| `Missing columns` | Profile data structure changed | Update column mapping |

---

## PHASE 8: Optional Enhancements

### Goal
Add advanced features for production deployment.

### 8.1: Web UI (Flask/Streamlit)

Create `ui/app.py` (Streamlit version):
```python
"""
Web UI for Alumni Data Extractor
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from config.settings import config
from src.utils.logger import app_logger

st.set_page_config(page_title="Alumni Data Extractor", layout="wide")

st.title("🎓 Alumni Data Extractor")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    college = st.text_input("College Name", value=config.COLLEGE_NAME)
    batch = st.number_input("Batch Year", min_value=1950, max_value=2030, value=config.BATCH_YEAR)
    num_pages = st.slider("Search Pages", 1, 10, value=5)
    
    if st.button("▶️ Start Extraction"):
        st.success("Extraction started!")

# Main content
tab1, tab2, tab3 = st.tabs(["Overview", "Results", "Analytics"])

with tab1:
    st.header("Project Overview")
    st.markdown("""
    This tool automatically:
    1. Searches for LinkedIn profiles of alumni
    2. Scrapes profile information
    3. Validates data using AI
    4. Exports to CSV
    """)

with tab2:
    st.header("Extraction Results")
    
    # Display sample results
    if st.button("Load Results"):
        try:
            with open('output/alumni_data.csv', 'r') as f:
                df = pd.read_csv(f)
            st.dataframe(df, use_container_width=True)
            
            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False),
                file_name=f"alumni_data_{datetime.now().strftime('%Y%m%d')}.csv"
            )
        except FileNotFoundError:
            st.error("No results found")

with tab3:
    st.header("Analytics")
    
    try:
        with open('output/alumni_data.csv', 'r') as f:
            df = pd.read_csv(f)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Profiles", len(df))
        
        with col2:
            st.metric("Unique Companies", df['current_company'].nunique())
        
        with col3:
            st.metric("Avg Quality Score", f"{df['quality_score'].mean():.1f}/100")
        
        # Top companies chart
        st.subheader("Top Companies")
        company_counts = df['current_company'].value_counts().head(10)
        st.bar_chart(company_counts)
        
        # Graduation year distribution
        st.subheader("Graduation Year Distribution")
        year_counts = df['graduation_year'].value_counts().sort_index()
        st.line_chart(year_counts)
        
    except:
        st.info("Run extraction first to see analytics")
```

Runcommand:
```bash
streamlit run ui/app.py
```

### 8.2: Scheduling & Automation

Create `src/scheduler.py`:
```python
"""
Schedule periodic extraction runs
"""
import schedule
import time
from src.main import run_extraction
from src.utils.logger import app_logger

def schedule_daily_extraction():
    """Schedule daily extraction at specific time"""
    
    def job():
        app_logger.info("Running scheduled extraction")
        try:
            run_extraction(
                college_name="Your College",
                batch_year=2020
            )
        except Exception as e:
            app_logger.error(f"Scheduled extraction failed: {str(e)}")
    
    # Schedule job at 2 AM daily
    schedule.every().day.at("02:00").do(job)
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_daily_extraction()
```

### 8.3: Database Storage

Create `src/database.py` (SQLAlchemy setup):
```python
"""
Database storage for profiles
"""
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class AlumniProfile(Base):
    """Profile table schema"""
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    current_company = Column(String)
    current_position = Column(String)
    university = Column(String)
    degree = Column(String)
    graduation_year = Column(Integer)
    quality_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database initialization
engine = create_engine('sqlite:///alumni_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
```

### Expected Outputs
- ✅ Web interface for easy access
- ✅ Real-time progress tracking
- ✅ Automated scheduling
- ✅ Database persistence
- ✅ Export analytics dashboard

---

## Developer Setup Guide

### Quick Start

```bash
# 1. Clone repository
git clone <repository-url>
cd alumni-extractor

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run the application
python src/main.py
```

### API Setup Instructions

#### SerpAPI Setup
1. Visit https://serpapi.com
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env`: `SERPAPI_API_KEY=your_key`

#### OpenAI Setup
1. Visit https://platform.openai.com
2. Create account and go to API keys
3. Generate new secret key
4. Add to `.env`: `OPENAI_API_KEY=your_key`

#### Google Gemini Setup
1. Visit https://makersuite.google.com/app/apikey
2. Create new API key
3. Add to `.env`: `GEMINI_API_KEY=your_key`

#### LinkedIn Credentials
1. Use your LinkedIn email and password
2. Add to `.env`: `LINKEDIN_EMAIL=your_email` and `LINKEDIN_PASSWORD=your_password`

### Best Practices for Scraping

1. **Rate Limiting**
   - Always maintain delays between requests (2-5 seconds)
   - Use exponential backoff on errors
   - Respect LinkedIn's robots.txt

2. **Avoiding Blocking**
   - Rotate user agents
   - Use proxies if doing large-scale scraping
   - Monitor for CAPTCHA challenges
   - Keep sessions alive with periodic activity

3. **Data Quality**
   - Always validate extracted data
   - Use AI to correct errors
   - Remove duplicates before exporting
   - Track data quality scores

4. **Error Handling**
   - Implement comprehensive logging
   - Use retry mechanisms
   - Handle timeouts gracefully
   - Save intermediate results

### Production Deployment

1. **Environment Configuration**
   - Use production-grade secrets management
   - Enable SSL/TLS for sensitive data
   - Use environment-specific configuration

2. **Monitoring**
   - Set up application logging
   - Monitor API quota usage
   - Track extraction success rates

3. **Scheduling**
   - Use cron jobs or task schedulers
   - Implement job monitoring
   - Set up alerts for failures

4. **Scaling**
   - Use database for persistence
   - Implement caching mechanisms
   - Load balance API requests

### Testing

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_search.py -v

# Run with coverage
pytest --cov=src tests/
```

### Troubleshooting Guide

**Issue: LinkedIn login fails**
- Solution: Check email/password, enable 2FA bypass mode, use cookies instead

**Issue: SerpAPI quota exceeded**
- Solution: Upgrade plan, reduce pages, implement caching

**Issue: AI validation timeouts**
- Solution: Use batching, increase timeout, switch to faster model

**Issue: High duplicate rate**
- Solution: Adjust similarity threshold, improve normalization

---

## Project Checklist

- [ ] Phase 1: Environment setup completed
- [ ] Phase 2: Google search integration working
- [ ] Phase 3: LinkedIn scraper functional
- [ ] Phase 4: Data extraction operational
- [ ] Phase 5: AI validation implemented
- [ ] Phase 6: Data cleaning working
- [ ] Phase 7: CSV export operational
- [ ] Phase 8 (Optional): Web UI deployed
- [ ] Documentation complete
- [ ] Comprehensive testing done
- [ ] Production deployment completed

---

## Support & Resources

- **GitHub**: Link to project repository
- **Documentation**: See README.md
- **Issues**: Report bugs on GitHub issues
- **Contributing**: See CONTRIBUTING.md

---

**Last Updated**: January 2024
**Version**: 1.0.0
**Maintainer**: [Your Name/Team]

