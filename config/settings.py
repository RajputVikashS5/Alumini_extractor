"""
Configuration management for Alumni Data Extractor
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class"""
    
    # API Keys
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Alternative to OPENAI_API_KEY
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # LinkedIn Credentials
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
    
    # Search Configuration
    COLLEGE_NAME = os.getenv('COLLEGE_NAME', 'Default University')
    BATCH_YEAR: int = 2020
    SEARCH_PAGES: int = 5
    SCRAPE_LIMIT: int = 10
    
    # Rate Limiting
    REQUEST_DELAY: float = 2.0
    MAX_RETRIES: int = 3
    
    # AI Model
    AI_MODEL = os.getenv('AI_MODEL', 'openai')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # Paths
    OUTPUT_DIR = 'output'
    LOGS_DIR = 'logs'
    
    # Initialize numeric values safely
    def __init__(self):
        try:
            self.BATCH_YEAR = int(os.getenv('BATCH_YEAR', 2020))
        except ValueError:
            print("Warning: BATCH_YEAR is not a valid integer, using default 2020")
            self.BATCH_YEAR = 2020
            
        try:
            self.SEARCH_PAGES = int(os.getenv('SEARCH_PAGES', 5))
        except ValueError:
            print("Warning: SEARCH_PAGES is not a valid integer, using default 5")
            self.SEARCH_PAGES = 5
            
        try:
            self.SCRAPE_LIMIT = int(os.getenv('SCRAPE_LIMIT', 10))
        except ValueError:
            print("Warning: SCRAPE_LIMIT is not a valid integer, using default 10")
            self.SCRAPE_LIMIT = 10
            
        try:
            self.REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', 2.0))
        except ValueError:
            print("Warning: REQUEST_DELAY is not a valid float, using default 2.0")
            self.REQUEST_DELAY = 2.0
            
        try:
            self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
        except ValueError:
            print("Warning: MAX_RETRIES is not a valid integer, using default 3")
            self.MAX_RETRIES = 3
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        # Check core required keys
        required_keys = ['SERPAPI_API_KEY']
        missing_keys = []
        
        for key in required_keys:
            value = getattr(cls, key, None)
            if not value or value.startswith("your_"):
                missing_keys.append(key)
        
        # Check AI keys based on selected model
        ai_model = os.getenv('AI_MODEL', 'openai').lower()
        if ai_model == 'openai':
            ai_key = getattr(cls, 'OPENAI_API_KEY', None) or getattr(cls, 'OPENROUTER_API_KEY', None)
            if not ai_key or (isinstance(ai_key, str) and ai_key.startswith("your_")):
                missing_keys.append("OPENAI_API_KEY or OPENROUTER_API_KEY")
        elif ai_model == 'gemini':
            gemini_key = getattr(cls, 'GEMINI_API_KEY', None)
            if not gemini_key or (isinstance(gemini_key, str) and gemini_key.startswith("your_")):
                missing_keys.append("GEMINI_API_KEY")
        
        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}. "
                f"Please configure them in .env file."
            )
    
    @classmethod
    def get_ai_api_key(cls) -> str | None:
        """Get the appropriate AI API key (OpenRouter or OpenAI)"""
        # Prefer OPENROUTER_API_KEY if set
        if cls.OPENROUTER_API_KEY:
            return cls.OPENROUTER_API_KEY
        return cls.OPENAI_API_KEY
            raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")
        
        return True


# Create singleton instance
config = Config()
