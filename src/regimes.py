import pandas as pd

from src.structure import add_confirmed_structure, classify_structure_regime
from src.timeframes import build_weekly_data, build_monthly_data

BULLISH_REGIMES = ["Accumulation", "Reaccumulation"]


def build_structure_timeframes(daily: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Build daily, weekly and monthly structure dataframes.
    """
    weekly = build_weekly_data(daily)
    monthly = build_monthly_data(daily)

    daily_structure = add_confirmed_structure(daily)
    weekly_structure = add_confirmed_structure(weekly)
    monthly_structure = add_confirmed_structure(monthly)

    return daily_structure, weekly_structure, monthly_structure


def get_latest_regime(structure_df: pd.DataFrame) -> str:
    """
    Return the latest non-empty structure regime.
    """
    latest = structure_df["Structure Regime"].dropna()

    if len(latest) == 0:
        return "Neutral"

    return latest.iloc[-1]


def prepare_regime_data(daily: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Build and classify daily, weekly and monthly market regimes.
    """
    daily_s, weekly_s, monthly_s = build_structure_timeframes(daily)

    daily_s = classify_structure_regime(daily_s)
    weekly_s = classify_structure_regime(weekly_s)
    monthly_s = classify_structure_regime(monthly_s)

    return daily_s, weekly_s, monthly_s


def get_regime_at_time(structure_df: pd.DataFrame, current_time: pd.Timestamp) -> str:
    """
    Return the latest completed regime available before the current timestamp.
    """
    current_date = pd.Timestamp(current_time).tz_localize(None).normalize()
    past = structure_df.loc[:current_date].iloc[:-1]

    if len(past) == 0:
        return "Neutral"

    regimes = past["Structure Regime"].dropna()

    if len(regimes) == 0:
        return "Neutral"

    return regimes.iloc[-1]


def check_precomputed_regimes(
    daily_s: pd.DataFrame,
    weekly_s: pd.DataFrame,
    monthly_s: pd.DataFrame,
    current_time: pd.Timestamp,
) -> dict:
    """
    Check whether daily, weekly and monthly regimes are bullish at a historical time.
    """
    daily_regime = get_regime_at_time(daily_s, current_time)
    weekly_regime = get_regime_at_time(weekly_s, current_time)
    monthly_regime = get_regime_at_time(monthly_s, current_time)

    overall = (
        daily_regime in BULLISH_REGIMES
        and weekly_regime in BULLISH_REGIMES
        and monthly_regime in BULLISH_REGIMES
    )

    return {
        "daily": daily_regime,
        "weekly": weekly_regime,
        "monthly": monthly_regime,
        "overall": overall,
    }