# modules/model_trainer.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib
import config
from modules.utils import load_from_csv
import os

def get_data_for_model(stock_code):
    """Loads processed data and prepares it for model training."""
    df = load_from_csv(config.PROCESSED_DATA_DIR, f"{stock_code}_processed_data.csv")
    df['target'] = df['close'].shift(-config.MONTHLY_RETURN_DAYS) # Predicting 30 days ahead
    df.dropna(inplace=True)
    X = df.drop(columns=['target', 'date', 'stock_code'])
    y = df['target']
    return X, y

def train_random_forest(X_train, y_train):
    """Trains a Random Forest model."""
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    return model

def train_xgboost(X_train, y_train):
    """Trains an XGBoost model."""
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_lstm(X_train, y_train):
    """Trains an LSTM model."""
    X_train_reshaped = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train_reshaped, y_train, epochs=50, batch_size=32, verbose=0)
    return model

def train_and_save_models_for_stock(stock_code):
    """Trains all models for a given stock and saves them."""
    X, y = get_data_for_model(stock_code)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 - config.TRAIN_TEST_SPLIT_RATIO, shuffle=False)

    print(f"Training models for {stock_code}...")
    rf_model = train_random_forest(X_train, y_train)
    xgb_model = train_xgboost(X_train, y_train)
    lstm_model = train_lstm(X_train, y_train)

    if not os.path.exists(config.MODEL_DIR):
        os.makedirs(config.MODEL_DIR)

    joblib.dump(rf_model, os.path.join(config.MODEL_DIR, f"{stock_code}_rf_model.pkl"))
    joblib.dump(xgb_model, os.path.join(config.MODEL_DIR, f"{stock_code}_xgb_model.pkl"))
    lstm_model.save(os.path.join(config.MODEL_DIR, f"{stock_code}_lstm_model.h5"))

    print(f"Models for {stock_code} saved.")

def train_models_for_all_stocks():
    """Trains models for all stocks."""
    stocks = [f.split('_')[0] for f in os.listdir(config.PROCESSED_DATA_DIR)]
    for stock in stocks:
        train_and_save_models_for_stock(stock)
