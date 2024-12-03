# data.py

import requests
import pandas as pd
from config import FRED_API_KEY
from datetime import datetime, timedelta

def get_us_gdp():
    """Fetches U.S. GDP data for the last 100 days."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=100)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'GDP',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date.strftime('%Y-%m-%d'),
        'observation_end': end_date.strftime('%Y-%m-%d'),
    }
    response = requests.get(url, params=params)
    data = response.json().get('observations', [])
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=['Date', 'Value'])
    df['Value'] = pd.to_numeric(df['value'], errors='coerce')
    df['Date'] = pd.to_datetime(df['date'])
    df = df[['Date', 'Value']]
    return df

def get_unemployment_rate():
    """Fetches U.S. Unemployment Rate data for the last 100 days."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=100)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'UNRATE',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date.strftime('%Y-%m-%d'),
        'observation_end': end_date.strftime('%Y-%m-%d'),
    }
    response = requests.get(url, params=params)
    data = response.json().get('observations', [])
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=['Date', 'Value'])
    df['Value'] = pd.to_numeric(df['value'], errors='coerce')
    df['Date'] = pd.to_datetime(df['date'])
    df = df[['Date', 'Value']]
    return df

def get_financial_stress_index():
    """Fetches the Financial Stress Index data for the last 100 days and normalizes it to percentage."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=100)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'STLFSI2',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date.strftime('%Y-%m-%d'),
        'observation_end': end_date.strftime('%Y-%m-%d'),
    }
    response = requests.get(url, params=params)
    data = response.json().get('observations', [])
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=['Date', 'Value', 'Value_Percent'])
    df['Value'] = pd.to_numeric(df['value'], errors='coerce')
    df['Date'] = pd.to_datetime(df['date'])
    df = df[['Date', 'Value']]
    # Normalize to 0-100% scale
    min_value = df['Value'].min()
    max_value = df['Value'].max()
    if max_value - min_value == 0:
        df['Value_Percent'] = 0
    else:
        df['Value_Percent'] = 100 * (df['Value'] - min_value) / (max_value - min_value)
    return df
