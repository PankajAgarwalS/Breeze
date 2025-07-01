import datetime
import time
import pandas as pd
from breezesdk.breeze import BreezeApi
from tqdm import tqdm

def initialize_api(api_key, secret_key, session_token):
    """
    Initializes and connects to the Breeze API.

    Args:
        api_key (str): Your ICICI Direct API key.
        secret_key (str): Your ICICI Direct secret key.
        session_token (str): The session token obtained after login.

    Returns:
        BreezeApi: An initialized and connected BreezeApi object, or None on failure.
    """
    try:
        breeze = BreezeApi(api_key=api_key)
        breeze.get_session(api_secret=secret_key, session_token=session_token)
        print("✅ Successfully connected to Breeze API.")
        return breeze
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return None

def fetch_historical_data(breeze, stock_list, years=3, interval="1day", exchange_code="NSE"):
    """
    Fetches historical data for a list of stocks and saves it to a CSV file.

    Args:
        breeze (BreezeApi): The initialized Breeze API object.
        stock_list (list): A list of stock codes to fetch data for.
        years (int): The number of years of historical data to fetch.
        interval (str): The data interval (e.g., "1day", "1hour").
        exchange_code (str): The exchange code (e.g., "NSE").

    Returns:
        pd.DataFrame: A DataFrame containing the combined historical data for all stocks.
    """
    if not breeze:
        print("API not initialized. Cannot fetch data.")
        return None

    all_stock_data = []
    from_date = (datetime.datetime.now() - datetime.timedelta(days=365 * years)).strftime('%Y-%m-%dT07:00:00.000Z')
    to_date = datetime.datetime.now().strftime('%Y-%m-%dT07:00:00.000Z')

    print(f"Fetching {years} years of historical data for {len(stock_list)} stocks...")

    for stock_code in tqdm(stock_list, desc="Fetching Data"):
        try:
            response = breeze.get_historical_data_v2(
                interval=interval,
                from_date=from_date,
                to_date=to_date,
                stock_code=stock_code,
                exchange_code=exchange_code,
                product_type="cash"
            )

            if response['Status'] == 200 and 'Success' in response and response['Success']:
                data = response['Success']
                df = pd.DataFrame(data)
                df['stock_code'] = stock_code  # Add stock code column for identification
                all_stock_data.append(df)
            else:
                print(f"⚠️ Warning: Could not fetch data for {stock_code}. Response: {response.get('Message', 'No message')}")
            
            # Add a small delay to avoid hitting API rate limits
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ An error occurred while fetching data for {stock_code}: {e}")
            continue
            
    if not all_stock_data:
        print("No data was fetched. Returning empty DataFrame.")
        return pd.DataFrame()

    # Combine all dataframes into a single one
    combined_df = pd.concat(all_stock_data, ignore_index=True)
    
    # Basic data cleaning
    combined_df['datetime'] = pd.to_datetime(combined_df['datetime'])
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
    
    print(f"\n✅ Successfully fetched data for {len(combined_df['stock_code'].unique())} stocks.")
    return combined_df
