from src.backtester import backtest_daily_strategy
from src.performance import backtest_stats
from src.reporting import save_backtest_results
from src.html_report import generate_html_report
from src.plotting import plot_equity_curve, plot_drawdown, plot_exit_reasons


SYMBOL = "AAPL"


def main():
    trades = backtest_daily_strategy(SYMBOL)

    save_backtest_results(trades, SYMBOL)

    plot_equity_curve(trades, f"results/{SYMBOL}_equity_curve.png")
    plot_drawdown(trades, f"results/{SYMBOL}_drawdown.png")
    plot_exit_reasons(trades, f"results/{SYMBOL}_exit_reasons.png")

    stats = backtest_stats(trades)
    generate_html_report(SYMBOL, stats)

    print(f"Backtest complete for {SYMBOL}. Results saved to results/")


if __name__ == "__main__":
    main()