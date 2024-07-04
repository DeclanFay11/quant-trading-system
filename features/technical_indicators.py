import pandas as pd

def calculate_sma(data: pd.DataFrame, window: int) -> pd.Series:
    """Calculate Simple Moving Average."""
    return data['Close'].rolling(window=window).mean()

def calculate_rsi(data: pd.DataFrame, window: int) -> pd.Series:
    """Calculate Relative Strength Index."""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))