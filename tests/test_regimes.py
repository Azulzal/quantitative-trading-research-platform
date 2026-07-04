import pandas as pd

from src.regimes import (
    BULLISH_REGIMES,
    check_precomputed_regimes,
    get_latest_regime,
)


def test_get_latest_regime_returns_latest_value():
    df = pd.DataFrame({
        "Structure Regime": ["Neutral", "Accumulation", "Reaccumulation"]
    })

    assert get_latest_regime(df) == "Reaccumulation"


def test_bullish_regimes_contains_expected_values():
    assert "Accumulation" in BULLISH_REGIMES
    assert "Reaccumulation" in BULLISH_REGIMES


def test_check_precomputed_regimes_returns_overall_true():
    dates = pd.date_range("2024-01-01", periods=5, freq="D")

    daily = pd.DataFrame({"Structure Regime": ["Accumulation"] * 5}, index=dates)
    weekly = pd.DataFrame({"Structure Regime": ["Accumulation"] * 5}, index=dates)
    monthly = pd.DataFrame({"Structure Regime": ["Reaccumulation"] * 5}, index=dates)

    result = check_precomputed_regimes(daily, weekly, monthly, dates[-1])

    assert result["overall"] is True