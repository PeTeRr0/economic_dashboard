import requests
import pandas as pd

# Replace 'YOUR_FRED_API_KEY' with your actual FRED API key
FRED_API_KEY = "YOUR_FRED_API_KEY"

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
