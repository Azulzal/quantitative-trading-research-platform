import pandas as pd


def portfolio_summary(summary: pd.DataFrame) -> dict:
    """
    Calculate portfolio-level statistics from a multi-stock backtest summary.
    """

    traded = summary[summary["Trades"] > 0]

    return {
        "Universe Size": len(summary),
        "Stocks With Trades": len(traded),
        "Total Trades": summary["Trades"].sum(),
        "Average Trades / Stock": traded["Trades"].mean(),
        "Average Win Rate": traded["Win Rate"].mean(),
        "Average Total R": traded["Total R"].mean(),
        "Median Total R": traded["Total R"].median(),
        "Best Stock": traded.loc[traded["Total R"].idxmax(), "Ticker"],
        "Worst Stock": traded.loc[traded["Total R"].idxmin(), "Ticker"],
        "Best Total R": traded["Total R"].max(),
        "Worst Total R": traded["Total R"].min(),
    }


def top_performers(summary: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Return the top-performing stocks ranked by Total R.
    """
    return summary.sort_values("Total R", ascending=False).head(n)


def bottom_performers(summary: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Return the worst-performing stocks ranked by Total R.
    """
    return summary.sort_values("Total R").head(n)