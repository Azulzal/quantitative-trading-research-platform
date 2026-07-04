import pandas as pd

from src.timeframes import build_weekly_data, build_monthly_data


def sample_daily_data():
    dates = pd.date_range("2024-01-01", periods=40, freq="D")

    return pd.DataFrame({
        "Open": range(40),
        "High": range(1, 41),
        "Low": range(40),
        "Close": range(1, 41),
        "Volume": [100] * 40,
    }, index=dates)


def test_build_weekly_data_creates_weekly_dataframe():
    daily = sample_daily_data()
    weekly = build_weekly_data(daily)

    assert len(weekly) > 0
    assert "EMA9" in weekly.columns
    assert "Recent 10W High" in weekly.columns


def test_build_monthly_data_creates_monthly_dataframe():
    daily = sample_daily_data()
    monthly = build_monthly_data(daily)

    assert len(monthly) > 0
    assert "EMA9" in monthly.columns