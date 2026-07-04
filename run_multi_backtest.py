import pandas as pd

from src.backtester import backtest_daily_strategy
from src.performance import backtest_stats
from src.plotting import plot_equity_curve, plot_drawdown
from src.multi_report import generate_multi_stock_report


from src.universe import SP100_TICKERS 

TICKERS = SP100_TICKERS


def main():
    all_trades = []
    summary_rows = []

    for ticker in TICKERS:
        try:
            print(f"Running {ticker}...")

            trades = backtest_daily_strategy(ticker)

            if len(trades) > 0:
                all_trades.append(trades)

            stats = backtest_stats(trades)
            stats["Ticker"] = ticker
            summary_rows.append(stats)

            print(f"✓ {ticker}: {len(trades)} trades")

        except Exception as error:
            print(f"✗ {ticker} skipped: {error}")

    summary = pd.DataFrame(summary_rows)
    summary.to_csv("results/multi_stock_summary.csv", index=False)

    if all_trades:
        combined_trades = pd.concat(all_trades, ignore_index=True)
        combined_trades.to_csv("results/multi_stock_trade_log.csv", index=False)

        plot_equity_curve(combined_trades, "results/multi_stock_equity_curve.png")
        plot_drawdown(combined_trades, "results/multi_stock_drawdown.png")

    generate_multi_stock_report()
    print("Multi-stock backtest complete. Results saved to results/")


if __name__ == "__main__":
    main()