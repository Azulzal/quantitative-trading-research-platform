import pandas as pd

from src.indicators import add_emas


def build_weekly_data(daily: pd.DataFrame) -> pd.DataFrame:
    """
    Convert daily OHLCV data into weekly candles.

    Parameters
    ----------
    daily : pd.DataFrame
        Daily OHLCV market data.

    Returns
    -------
    pd.DataFrame
        Weekly OHLCV data with EMA columns and recent 10-week high.
    """
    weekly = daily.resample("W").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }).dropna()

    weekly = add_emas(weekly)
    weekly["Recent 10W High"] = weekly["High"].rolling(10).max()

    return weekly


def build_monthly_data(daily: pd.DataFrame) -> pd.DataFrame:
    """
    Convert daily OHLCV data into monthly candles.

    Parameters
    ----------
    daily : pd.DataFrame
        Daily OHLCV market data.

    Returns
    -------
    pd.DataFrame
        Monthly OHLCV data with EMA columns.
    """
    monthly = daily.resample("ME").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }).dropna()

    monthly = add_emas(monthly)

    return monthly


def get_last_completed_week(
    weekly: pd.DataFrame,
    current_time: pd.Timestamp,
) -> pd.Series | None:
    """
    Return the most recent completed weekly candle before the current date.

    Parameters
    ----------
    weekly : pd.DataFrame
        Weekly OHLCV market data.
    current_time : pd.Timestamp
        Current backtest timestamp.

    Returns
    -------
    pd.Series | None
        Most recent completed weekly candle, or None if unavailable.
    """
    current_date = pd.Timestamp(current_time).tz_localize(None).normalize()
    past = weekly.loc[:current_date].iloc[:-1]

    if len(past) == 0:
        return None

    return past.iloc[-1]