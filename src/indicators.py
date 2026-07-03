import pandas as pd
import ta


def add_emas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add exponential moving averages to price data.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV market data with a Close column.

    Returns
    -------
    pd.DataFrame
        Market data with EMA9, EMA20 and EMA50 columns.
    """
    df = df.copy()
    df["EMA9"] = df["Close"].ewm(span=9).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["EMA50"] = df["Close"].ewm(span=50).mean()
    return df


def add_atr(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add Average True Range to price data.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV market data with High, Low and Close columns.
    window : int
        ATR lookback period.

    Returns
    -------
    pd.DataFrame
        Market data with an ATR column.
    """
    df = df.copy()
    df["ATR"] = ta.volatility.average_true_range(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=window,
    )
    return df