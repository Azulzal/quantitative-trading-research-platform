from pathlib import Path
import pandas as pd

from src.performance import backtest_stats


def save_backtest_results(trades: pd.DataFrame, symbol: str, results_dir: str = "results") -> None:
    """
    Save trade log and performance summary for a backtest.
    """
    output_dir = Path(results_dir)
    output_dir.mkdir(exist_ok=True)

    trades.to_csv(output_dir / f"{symbol}_trade_log.csv", index=False)

    stats = backtest_stats(trades)
    stats_df = pd.DataFrame([stats])
    stats_df.to_csv(output_dir / f"{symbol}_performance_summary.csv", index=False)