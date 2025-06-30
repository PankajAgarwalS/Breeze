# modules/feature_engineer.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import config
from modules.utils import load_from_csv, save_to_csv

def calculate_ema(data, window):
    """Calculates the Exponential Moving Average (EMA)."""
    return data['close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window):
    """Calculates the Relative Strength Index (RSI)."""
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, fast_window, slow_window, signal_window):
    """Calculates the Moving Average Convergence Divergence (MACD)."""
    ema_fast = data['close'].ewm(span=fast_window, adjust=False).mean()
    ema_slow = data['close'].ewm(span=slow_window, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def calculate_bollinger_bands(data, window):
    """Calculates Bollinger Bands."""
    sma = data['close'].rolling(window=window).mean()
    std = data['close'].rolling(window=window).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return upper_band, lower_band

def create_lagged_features(data, n_lags):
    """Creates lagged features for time series data."""
    for i in range(1, n_lags + 1):
        data[f'lag_{i}'] = data['close'].shift(i)
    return data

def engineer_features_for_stock(stock_code):
    """
    Loads raw data for a stock, engineers features, and saves the processed data.
    """
    df = load_from_csv(config.HISTORICAL_DATA_DIR, f"{stock_code}_historical_data.csv")

    for window in config.EMA_WINDOWS:
        df[f'ema_{window}'] = calculate_ema(df, window)

    df['rsi'] = calculate_rsi(df, config.RSI_WINDOW)

    df['macd'], df['macd_signal'] = calculate_macd(df, config.MACD_FAST, config.MACD_SLOW, config.MACD_SIGNAL)

    df['bb_upper'], df['bb_lower'] = calculate_bollinger_bands(df, config.BB_WINDOW)

    df = create_lagged_features(df, config.LAG_FEATURES)

    df.dropna(inplace=True)

    # Normalize features
    scaler = StandardScaler()
    feature_cols = [col for col in df.columns if col not in ['date', 'stock_code']]
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    save_to_csv(df, config.PROCESSED_DATA_DIR, f"{stock_code}_processed_data.csv")
    print(f"Feature engineering complete for {stock_code}")

def engineer_features_for_all_stocks():
    """Runs the feature engineering process for all stocks."""
    stocks = [f.split('_')[0] for f in os.listdir(config.HISTORICAL_DATA_DIR)]
    for stock in stocks:
        engineer_features_for_stock(stock)
