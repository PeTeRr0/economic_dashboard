import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables or Streamlit secrets
FRED_API_KEY = os.getenv('FRED_API_KEY')
TRADING_ECONOMICS_API_KEY = os.getenv('TRADING_ECONOMICS_API_KEY')


def fetch_fred_data(series_id, start_date, end_date):
    """Fetch data from FRED API with additional logging."""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        # Print the response to the console so you can see it in Streamlit logs
        print(f"API Response Text: {response.text}")

        if response.status_code == 200 and response.text:
            data = response.json().get("observations", [])
        else:
            print("No valid data found in the response.")
            return pd.DataFrame(columns=["Date", "Value"])

    except requests.exceptions.RequestException as e:
        # Print the error if something goes wrong
        print(f"HTTP Request failed: {e}")
        return pd.DataFrame()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON response")
        return pd.DataFrame()

    # Create DataFrame from response data
    df = pd.DataFrame(data)
    if df.empty:
        print("Received empty data frame.")
        return pd.DataFrame(columns=["Date", "Value"])

    # Convert columns to appropriate types
    df["Value"] = pd.to_numeric(df["value"], errors="coerce")
    df["Date"] = pd.to_datetime(df["date"])
    df = df[["Date", "Value"]]
    return df

def fetch_trading_economics_data(category):
    """Fetch data from Trading Economics API."""
    url = f"https://api.tradingeconomics.com/{category}"
    params = {
        "c": TRADING_ECONOMICS_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(f"Trading Economics API Response: {response.text}")  # Debugging line

        if response.status_code == 200 and response.text:
            data = response.json()
            return data
        else:
            print("No valid data found in the Trading Economics response.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return []
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON response from Trading Economics API")
        return []

def get_us_gdp():
    """Get US GDP data from FRED API."""
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    return fetch_fred_data("GDP", start_date, end_date)

def get_unemployment_rate():
    """Get US Unemployment Rate data from FRED API."""
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    return fetch_fred_data("UNRATE", start_date, end_date)

def get_financial_stress_index():
    """Get Financial Stress Index data from FRED API."""
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    return fetch_fred_data("STLFSI2", start_date, end_date)

def get_global_stock_indices():
    """Get Global Stock Indices data from Trading Economics API."""
    return fetch_trading_economics_data("markets/indices")
