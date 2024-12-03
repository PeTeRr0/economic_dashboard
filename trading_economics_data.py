# trading_economics_data.py

import requests
import pandas as pd
from config import TRADING_ECONOMICS_API_KEY
from datetime import datetime, timedelta

def fetch_trading_economics_data(endpoint):
    """
    Fetches data from the Trading Economics API.
    Parameters:
    - endpoint (str): The API endpoint to fetch data from.
    Returns:
    - pd.DataFrame: DataFrame containing the requested data.
    """
    url = f'https://api.tradingeconomics.com/{endpoint}'
    params = {
        'c': TRADING_ECONOMICS_API_KEY,
        'f': 'json',
    }
    response = requests.get(url, params=params)
    data = response.json()
    if isinstance(data, dict) and data.get('error'):
        return pd.DataFrame()
    df = pd.DataFrame(data)
    return df

def get_global_stock_indices():
    """Fetches global stock market indices."""
    df = fetch_trading_economics_data('markets/indices')
    return df

def get_index_historical_data(symbol):
    """Fetches historical data for a given stock index over the last 100 days."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=100)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    endpoint = f'historical/markets/index/{symbol}?d1={start_str}&d2={end_str}'
    df = fetch_trading_economics_data(endpoint)
    return df
