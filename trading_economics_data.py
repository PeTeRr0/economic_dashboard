# trading_economics_data.py

import requests
import pandas as pd
from config import TRADING_ECONOMICS_API_KEY
from datetime import datetime, timedelta


def fetch_trading_economics_data(endpoint):
    """Fetches data from Trading Economics API."""
    url = f"https://api.tradingeconomics.com/{endpoint}"
    params = {
        "c": TRADING_ECONOMICS_API_KEY,
        "f": "json",
    }
    response = requests.get(url, params=params)
    try:
        data = response.json()
    except ValueError:
        return pd.DataFrame()  # Return empty DataFrame on error
    return pd.DataFrame(data)


def get_global_stock_indices():
    """Fetches global stock market indices."""
    df = fetch_trading_economics_data("markets/indices")
    if df.empty:
        return pd.DataFrame(columns=["Symbol", "Name", "Close", "Change", "Percentage"])
    return df[["symbol", "name", "close", "daily_change", "daily_percentual_change"]]


def get_index_historical_data(symbol):
    """Fetches historical data for a given stock index over the last 100 days."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=100)
    endpoint = f"historical/markets/index/{symbol}?d1={start_date.strftime('%Y-%m-%d')}&d2={end_date.strftime('%Y-%m-%d')}"
    df = fetch_trading_economics_data(endpoint)
    return df
