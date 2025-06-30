# src/data_extraction.py
import os
import time
import pandas as pd
import datetime
from src.config import *

# This is a placeholder for your actual breeze object
# from your_api_connection_file import breeze

def fetch_historical_data(breeze, stock_code):
    """Fetches 3 years of historical data for a given stock code."""
    try:
        print(f"Fetching data for {stock_code}...")
        response = breeze.get_historical_data_v2(
            interval=INTERVAL,
            from_date=FROM_DATE,
            to_date=TO_DATE,
            stock_code=stock_code,
            exchange_code=EXCHANGE_CODE,
            product_type=PRODUCT_TYPE
        )
        if response['Status'] == 200 and response['Success']:
            df = pd.DataFrame(response['Success'])
            # Basic preprocessing
            df['date'] = pd.to_datetime(df['datetime']).dt.date
            df = df.rename(columns={'close': 'Close', 'open': 'Open', 'high': 'High', 'low': 'Low', 'volume': 'Volume'})
            df[['Close', 'Open', 'High', 'Low', 'Volume']] = df[['Close', 'Open', 'High', 'Low', 'Volume']].apply(pd.to_numeric)
            df.to_csv(os.path.join(RAW_DATA_DIR, f"{stock_code}.csv"), index=False)
            print(f"Successfully fetched and saved data for {stock_code}.")
            time.sleep(0.5) # To avoid hitting API rate limits
            return True
        else:
            print(f"Could not fetch data for {stock_code}: {response.get('Message', 'Unknown Error')}")
            return False
    except Exception as e:
        print(f"An error occurred while fetching data for {stock_code}: {e}")
        return False

def run_data_extraction(breeze):
    """Main function to extract data for all stocks in the list."""
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)

    with open(STOCK_LIST_FILE, 'r') as f:
        stock_codes = [line.strip() for line in f.readlines()]

    for code in stock_codes:
        fetch_historical_data(breeze, code)

    # Also fetch Nifty 50 data for market correlation
    print("\nFetching Nifty 50 Index data...")
    fetch_historical_data(breeze, NIFTY_CODE)

# To run this module:
# from your_api_connection_file import breeze_object
# run_data_extraction(breeze_object)
