from src.structure import add_confirmed_structure, classify_structure_regime
from src.timeframes import build_weekly_data, build_monthly_data

BULLISH_REGIMES = ["Accumulation", "Reaccumulation"]


def build_structure_timeframes(daily):
    weekly = build_weekly_data(daily)
    monthly = build_monthly_data(daily)

    daily_structure = add_confirmed_structure(daily)
    weekly_structure = add_confirmed_structure(weekly)
    monthly_structure = add_confirmed_structure(monthly)

    return daily_structure, weekly_structure, monthly_structure


def get_latest_regime(structure_df):
    latest = structure_df["Structure Regime"].dropna()

    if len(latest) == 0:
        return "Neutral"

    return latest.iloc[-1]


def prepare_regime_data(daily):
    daily_s, weekly_s, monthly_s = build_structure_timeframes(daily)

    daily_s = classify_structure_regime(daily_s)
    weekly_s = classify_structure_regime(weekly_s)
    monthly_s = classify_structure_regime(monthly_s)

    return daily_s, weekly_s, monthly_s


def regime_screener(symbol, download_daily_data):
    daily = download_daily_data(symbol)

    daily_s, weekly_s, monthly_s = prepare_regime_data(daily)

    daily_regime = get_latest_regime(daily_s)
    weekly_regime = get_latest_regime(weekly_s)
    monthly_regime = get_latest_regime(monthly_s)

    allowed = (
        daily_regime in BULLISH_REGIMES
        and weekly_regime in BULLISH_REGIMES
        and monthly_regime in BULLISH_REGIMES
    )

    return {
        "Ticker": symbol,
        "Daily Regime": daily_regime,
        "Weekly Regime": weekly_regime,
        "Monthly Regime": monthly_regime,
        "Trade Allowed": allowed,
    }