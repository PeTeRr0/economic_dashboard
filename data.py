# data.py

import requests
import pandas as pd
import json
import os
from config import FRED_API_KEY
from datetime import datetime, timedelta

DATA_STORE_FILE = "data_store.json"


def load_data():
    """Load stored data from JSON file with error handling."""
    if os.path.exists(DATA_STORE_FILE):
        with open(DATA_STORE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # If JSON is invalid or corrupted, reset to default structure
                return {"us_gdp": [], "unemployment_rate": [], "financial_stress": []}
    # If file doesn't exist, return default structure
    return {"us_gdp": [], "unemployment_rate": [], "financial_stress": []}


def save_data(data):
    """Save data to JSON file."""
    # Convert Timestamps to strings for serialization
    for key in data:
        for record in data[key]:
            if isinstance(record['Date'], pd.Timestamp):
                record['Date'] = record['Date'].strftime('%Y-%m-%d')
    with open(DATA_STORE_FILE, "w") as file:
        json.dump(data, file)


def fetch_fred_data(series_id, start_date, end_date):
    """Fetch data from FRED API."""
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
        response.raise_for_status()  # Raises an error if the response status code indicates failure
        data = response.json().get("observations", [])
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=["Date", "Value"])
    df["Value"] = pd.to_numeric(df["value"], errors="coerce")
    df["Date"] = pd.to_datetime(df["date"])
    df = df[["Date", "Value"]]
    return df


def get_updated_data(series_id, data_key):
    """Fetch updated data and accumulate it."""
    # Load existing data
    stored_data = load_data()
    current_data = pd.DataFrame(stored_data[data_key])

    # Determine start and end date for new data
    if current_data.empty:
        start_date = datetime.today() - timedelta(days=100)
    else:
        last_date = pd.to_datetime(current_data["Date"]).max()
        start_date = last_date + timedelta(days=1)

    end_date = datetime.today()

    # Fetch new data
    new_data = fetch_fred_data(series_id, start_date, end_date)

    # Concatenate with existing data and remove duplicates
    if not new_data.empty:
        updated_data = pd.concat([current_data, new_data]).drop_duplicates(subset=["Date"]).reset_index(drop=True)
    else:
        updated_data = current_data

    # Update the stored data
    stored_data[data_key] = updated_data.to_dict(orient="records")
    save_data(stored_data)

    return updated_data


def get_us_gdp():
    """Get accumulated U.S. GDP data."""
    return get_updated_data("GDP", "us_gdp")


def get_unemployment_rate():
    """Get accumulated Unemployment Rate data."""
    return get_updated_data("UNRATE", "unemployment_rate")


def get_financial_stress_index():
    """Get accumulated Financial Stress Index data."""
    return get_updated_data("STLFSI2", "financial_stress")
