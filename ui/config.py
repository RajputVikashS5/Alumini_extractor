"""
Configuration for Streamlit UI
"""

# Streamlit configuration
STREAMLIT_CONFIG = {
    "theme": {
        "primaryColor": "#667eea",
        "backgroundColor": "#f0f2f6",
        "secondaryBackgroundColor": "#ffffff",
        "textColor": "#262730",
        "font": "sans serif"
    },
    "client": {
        "showErrorDetails": True
    },
    "logger": {
        "level": "info"
    }
}

# UI Constants
APP_TITLE = "Alumni Data Extractor"
APP_SUBTITLE = "Extract, validate, and structure LinkedIn alumni data automatically"
APP_ICON = "🎓"

# Data paths
CSV_OUTPUT_PATH = "output/alumni_data.csv"
JSON_OUTPUT_PATH = "output/extracted_data.json"
LOGS_DIR = "logs"

# Extraction defaults
DEFAULT_COLLEGE = "Your College Name"
DEFAULT_BATCH_YEAR = 2020
DEFAULT_SEARCH_PAGES = 5
DEFAULT_REQUEST_DELAY = 2
