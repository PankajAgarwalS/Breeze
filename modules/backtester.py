# modules/backtester.py

import pandas as pd
import numpy as np
import app_config

def run_simple_backtest(stock_code):
    """Runs a simple backtest on historical predictions."""
    # This is a simplified example. A full backtester would be more complex.
    # It would involve generating predictions for each point in the test set
    # and simulating trades.

    processed_data = pd.read_csv(f"{app_config.PROCESSED_DATA_DIR}{stock_code}_processed_data.csv")
    returns = processed_data['close'].pct_change().dropna()

    # Assuming a simple long-only strategy
    sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) # Annualized

    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns/peak) - 1
    max_drawdown = drawdown.min()

    return {
        'stock_code': stock_code,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown
    }

def perform_full_backtesting():
    """Performs backtesting for all stocks."""
    results = []
    stocks = [f.split('_')[0] for f in os.listdir(app_config.PROCESSED_DATA_DIR)]
    for stock in stocks:
        results.append(run_simple_backtest(stock))
    return pd.DataFrame(results)
