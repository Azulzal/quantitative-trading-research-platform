from pathlib import Path
import pandas as pd



def generate_html_report(symbol: str, stats: dict, results_dir: str = "results"):
    output_dir = Path(results_dir)
    equity_curve = f"{symbol}_equity_curve.png"
    drawdown = f"{symbol}_drawdown.png"
    exit_reasons = f"{symbol}_exit_reasons.png"

    html = f"""
    <html>

    <head>
    <title>{symbol} Backtest Report</title>
    </head>

    <body>

    <h1>{symbol} Strategy Report</h1>

    <h2>Performance Summary</h2>

    {pd.DataFrame([stats]).to_html(index=False)}

    <h2>Equity Curve</h2>

    <img src="{equity_curve}" width="900">

    <h2>Drawdown</h2>

    <img src="{drawdown}" width="900">

    <h2>Exit Reason Breakdown</h2>

    <img src="{exit_reasons}" width="600">

    </body>

    </html>
    """

    (output_dir / f"{symbol}_report.html").write_text(html)