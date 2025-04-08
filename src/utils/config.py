import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

# Scraping Configuration
SCRAPING_DELAY = int(os.getenv("SCRAPING_DELAY", "3"))
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")