import pandas as pd
import yfinance as yf

from src.indicators import add_atr, add_emas


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten yfinance multi-index columns into standard OHLCV columns.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe returned by yfinance.

    Returns
    -------
    pd.DataFrame
        Dataframe with simplified column names.
    """
    df = df.copy()

    if hasattr(df.columns, "levels") and len(df.columns.levels) > 1:
        df.columns = df.columns.get_level_values(0)

    return df


def download_daily_data(symbol: str, period: str = "10y") -> pd.DataFrame:
    """
    Download daily OHLCV market data and add technical indicators.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol.
    period : str
        Historical data period to download.

    Returns
    -------
    pd.DataFrame
        Daily market data with EMA and ATR columns.
    """
    daily = yf.download(
        symbol,
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if daily.empty:
        raise ValueError(f"No data found for {symbol}")

    daily = clean_columns(daily)
    daily = add_emas(daily)
    daily = add_atr(daily)

    return daily