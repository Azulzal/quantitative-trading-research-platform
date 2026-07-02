import pandas as pd

from src.indicators import add_emas


def build_weekly_data(daily):
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


def build_monthly_data(daily):
    monthly = daily.resample("ME").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }).dropna()

    monthly = add_emas(monthly)

    return monthly


def get_last_completed_week(weekly, current_time):
    current_date = pd.Timestamp(current_time).tz_localize(None).normalize()
    past = weekly.loc[:current_date].iloc[:-1]

    if len(past) == 0:
        return None

    return past.iloc[-1]