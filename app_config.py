# config.py

# ICICI Direct Breeze API Configuration
API_KEY = "627A38310@5+509v591p67950M9559X4"
API_SECRET = "n4x21572_6183l2)107I7k914d97571Z"
SESSION_TOKEN = "52043012"

# File Paths
STOCK_LIST_FILE = "stocknames.txt"
HISTORICAL_DATA_DIR = "data/historical_data/"
PROCESSED_DATA_DIR = "data/processed_data/"
REPORTS_DIR = "reports/"
MODEL_DIR = "models/"

# Data Collection Parameters
FROM_DATE_YEARS = 3
INTERVAL = "1day"

# Feature Engineering Parameters
EMA_WINDOWS = [20, 50, 100]
RSI_WINDOW = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_WINDOW = 20
LAG_FEATURES = 5

# Model Training Parameters
TRAIN_TEST_SPLIT_RATIO = 0.7
VALIDATION_SPLIT_RATIO = 0.15

# Prediction Parameters
MONTHLY_RETURN_DAYS = 30
CONFIDENCE_THRESHOLD = 0.65
