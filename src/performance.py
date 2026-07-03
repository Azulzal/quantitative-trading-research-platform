import pandas as pd


def backtest_stats(trades: pd.DataFrame) -> dict:
    """
    Calculate summary statistics from a backtest trade log.
    """
    if len(trades) == 0:
        return {
            "Trades": 0,
            "Wins": 0,
            "Losses": 0,
            "Breakevens": 0,
            "Win Rate": None,
            "Average R": None,
            "Total R": 0,
            "Best R": None,
            "Worst R": None,
            "Max Drawdown": None,
            "Profit Factor": None,
        }

    r = trades["R Result"]

    wins = trades[r > 0]
    losses = trades[r < 0]
    breakevens = trades[r == 0]

    equity = r.cumsum()
    drawdown = equity - equity.cummax()

    gross_profit = wins["R Result"].sum()
    gross_loss = abs(losses["R Result"].sum())

    profit_factor = None if gross_loss == 0 else gross_profit / gross_loss

    return {
        "Trades": len(trades),
        "Wins": len(wins),
        "Losses": len(losses),
        "Breakevens": len(breakevens),
        "Win Rate": len(wins) / len(trades),
        "Average R": r.mean(),
        "Total R": r.sum(),
        "Best R": r.max(),
        "Worst R": r.min(),
        "Max Drawdown": drawdown.min(),
        "Profit Factor": profit_factor,
    }


def trades_per_year(trades: pd.DataFrame) -> pd.DataFrame:
    """
    Count number of trades taken per year.
    """
    trades = trades.copy()
    trades["Entry Time"] = pd.to_datetime(trades["Entry Time"])
    trades["Year"] = trades["Entry Time"].dt.year

    return trades.groupby("Year").size().reset_index(name="Trades")


def exit_reason_breakdown(trades: pd.DataFrame) -> pd.DataFrame:
    if len(trades) == 0 or "Exit Reason" not in trades.columns:
        return pd.DataFrame(columns=["Exit Reason", "Count"])

    return (
        trades["Exit Reason"]
        .value_counts()
        .rename_axis("Exit Reason")
        .reset_index(name="Count")
    )