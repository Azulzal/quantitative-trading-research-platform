from pathlib import Path

import pandas as pd

from src.performance import backtest_stats, trades_per_year, exit_reason_breakdown


def save_backtest_results(
    trades: pd.DataFrame,
    symbol: str,
    results_dir: str = "results",
) -> None:
    """
    Save trade log, performance summary and yearly trade counts.
    """
    output_dir = Path(results_dir)
    output_dir.mkdir(exist_ok=True)

    trades.to_csv(output_dir / f"{symbol}_trade_log.csv", index=False)

    stats_df = pd.DataFrame([backtest_stats(trades)])
    stats_df.to_csv(output_dir / f"{symbol}_performance_summary.csv", index=False)

    yearly_trades = trades_per_year(trades)
    yearly_trades.to_csv(output_dir / f"{symbol}_trades_per_year.csv", index=False)

    exit_reasons = exit_reason_breakdown(trades)
    exit_reasons.to_csv(output_dir / f"{symbol}_exit_reasons.csv", index=False)