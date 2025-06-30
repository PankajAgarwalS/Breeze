# modules/predictor.py

import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import config
import os

def make_predictions_for_stock(stock_code):
    """Makes future predictions for a given stock."""
    processed_data = pd.read_csv(os.path.join(config.PROCESSED_DATA_DIR, f"{stock_code}_processed_data.csv"))
    latest_data = processed_data.drop(columns=['date', 'stock_code']).iloc[-1]

    rf_model = joblib.load(os.path.join(config.MODEL_DIR, f"{stock_code}_rf_model.pkl"))
    xgb_model = joblib.load(os.path.join(config.MODEL_DIR, f"{stock_code}_xgb_model.pkl"))
    lstm_model = load_model(os.path.join(config.MODEL_DIR, f"{stock_code}_lstm_model.h5"))

    latest_data_reshaped = latest_data.values.reshape(1, -1)
    latest_data_lstm = latest_data.values.reshape(1, 1, -1)

    rf_pred = rf_model.predict(latest_data_reshaped)[0]
    xgb_pred = xgb_model.predict(latest_data_reshaped)[0]
    lstm_pred = lstm_model.predict(latest_data_lstm)[0][0]

    # Simple averaging ensemble
    final_prediction = (rf_pred + xgb_pred + lstm_pred) / 3

    current_price = processed_data['close'].iloc[-1]
    predicted_return = ((final_prediction - current_price) / current_price) * 100

    return {
        'stock_code': stock_code,
        'current_price': current_price,
        'predicted_price': final_prediction,
        'predicted_return_percent': predicted_return,
        'confidence': np.std([rf_pred, xgb_pred, lstm_pred]) # Lower std dev means higher confidence
    }

def generate_all_predictions():
    """Generates predictions for all stocks."""
    predictions = []
    stocks = [f.split('_')[0] for f in os.listdir(config.MODEL_DIR) if f.endswith('.pkl')]
    for stock in stocks:
        predictions.append(make_predictions_for_stock(stock))
    return pd.DataFrame(predictions)
