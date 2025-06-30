# modules/data_collector.py

import datetime
from breeze_connect import BreezeConnect
import pandas as pd
import config
from modules.utils import save_to_csv

def get_stock_list():
    """Reads the list of stock codes from the stocknames.txt file."""
    with open(config.STOCK_LIST_FILE, 'r') as f:
        stocks = [line.strip() for line in f.readlines()]
    return stocks

def initialize_breeze():
    """Initializes the Breeze API connection."""
    return BreezeConnect(api_key=config.API_KEY)

def get_historical_data_for_stock(breeze, stock_code, from_date, to_date, interval):
    """Fetches historical data for a single stock."""
    try:
        data = breeze.get_historical_data_v2(
            interval=interval,
            from_date=from_date,
            to_date=to_date,
            stock_code=stock_code,
            exchange_code="NSE",
            product_type="cash"
        )
        if data['Status'] == 200 and data['Success']:
            return pd.DataFrame(data['Success'])
        else:
            print(f"Error fetching data for {stock_code}: {data.get('Message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"An exception occurred while fetching data for {stock_code}: {e}")
        return None

def collect_all_historical_data():
    """
    Fetches historical data for all stocks in the list and saves it to CSV files.
    """
    breeze = initialize_breeze()
    # You will need to handle the login flow here as per the Breeze API documentation
    # This might involve redirecting the user to a login URL to get a session token.
    # For this example, we assume the session token is already set in config.py
    # breeze.generate_session(api_secret=config.API_SECRET, session_token=config.SESSION_TOKEN)

    stocks = get_stock_list()
    from_date = (datetime.datetime.today() - datetime.timedelta(days=365 * config.FROM_DATE_YEARS)).strftime('%Y-%m-%d') + 'T05:30:00.000Z'
    to_date = datetime.datetime.today().strftime('%Y-%m-%d') + 'T05:30:00.000Z'

    for stock in stocks:
        print(f"Fetching data for {stock}...")
        df = get_historical_data_for_stock(breeze, stock, from_date, to_date, config.INTERVAL)
        if df is not None and not df.empty:
            save_to_csv(df, config.HISTORICAL_DATA_DIR, f"{stock}_historical_data.csv")
