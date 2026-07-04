import pandas as pd

from src.performance import backtest_stats, trades_per_year, exit_reason_breakdown


def test_backtest_stats_empty_trades():
    trades = pd.DataFrame(columns=["R Result"])
    stats = backtest_stats(trades)

    assert stats["Trades"] == 0
    assert stats["Total R"] == 0


def test_backtest_stats_calculates_results():
    trades = pd.DataFrame({"R Result": [1, -1, 0, 2]})
    stats = backtest_stats(trades)

    assert stats["Trades"] == 4
    assert stats["Wins"] == 2
    assert stats["Losses"] == 1
    assert stats["Breakevens"] == 1
    assert stats["Total R"] == 2


def test_trades_per_year():
    trades = pd.DataFrame({
        "Entry Time": ["2024-01-01", "2024-06-01", "2025-01-01"]
    })

    result = trades_per_year(trades)

    assert len(result) == 2
    assert result.loc[result["Year"] == 2024, "Trades"].iloc[0] == 2


def test_exit_reason_breakdown():
    trades = pd.DataFrame({
        "Exit Reason": ["Stop", "Stop", "Trail"]
    })

    result = exit_reason_breakdown(trades)

    assert result.loc[result["Exit Reason"] == "Stop", "Count"].iloc[0] == 2