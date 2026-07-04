import pandas as pd

from src.indicators import add_emas, add_atr


def sample_ohlcv():
    return pd.DataFrame({
        "Open": range(1, 31),
        "High": range(2, 32),
        "Low": range(0, 30),
        "Close": range(1, 31),
        "Volume": range(100, 130),
    })


def test_add_emas_creates_columns():
    df = add_emas(sample_ohlcv())

    assert "EMA9" in df.columns
    assert "EMA20" in df.columns
    assert "EMA50" in df.columns


def test_add_atr_creates_column():
    df = add_atr(sample_ohlcv())

    assert "ATR" in df.columns
    assert len(df) == 30