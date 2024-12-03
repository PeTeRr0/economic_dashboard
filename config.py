# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables or Streamlit secrets
FRED_API_KEY = os.getenv('FRED_API_KEY')
TRADING_ECONOMICS_API_KEY = os.getenv('TRADING_ECONOMICS_API_KEY')
