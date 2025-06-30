# src/config.py

# Data Extraction
FROM_DATE = (datetime.datetime.today() - datetime.timedelta(days=365*3)).strftime('%Y-%m-%d') + 'T05:30:00.000Z'
TO_DATE = datetime.datetime.today().strftime('%Y-%m-%d') + 'T05:30:00.000Z'
INTERVAL = "1day"
EXCHANGE_CODE = "NSE"
PRODUCT_TYPE = "cash"
NIFTY_CODE = "NIFTY" # Adjust if your API uses a different code for the Nifty 50 index

# File Paths
STOCK_LIST_FILE = "stocknames.txt"
RAW_DATA_DIR = "data/raw/"
PROCESSED_DATA_DIR = "data/processed/"
MODELS_DIR = "models/"
REPORTS_DIR = "reports/"
