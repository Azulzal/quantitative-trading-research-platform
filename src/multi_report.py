from pathlib import Path

import pandas as pd


def generate_multi_stock_report(results_dir: str = "results") -> None:
    """
    Generate an HTML report for the multi-stock backtest.
    """
    output_dir = Path(results_dir)

    summary = pd.read_csv(output_dir / "multi_stock_summary.csv")

    equity_curve = "multi_stock_equity_curve.png"
    drawdown = "multi_stock_drawdown.png"

    html = f"""
<html>
<head>
<title>Multi-Stock Backtest Report</title>

<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 40px;
        color: #222;
        background-color: #f8f9fb;
    }}

    h1 {{
        color: #111827;
    }}

    h2 {{
        margin-top: 35px;
        color: #1f2937;
        border-bottom: 2px solid #ddd;
        padding-bottom: 6px;
    }}

    table {{
        border-collapse: collapse;
        width: 100%;
        background-color: white;
    }}

    th, td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }}

    th {{
        background-color: #111827;
        color: white;
    }}

    img {{
        background-color: white;
        padding: 10px;
        border: 1px solid #ddd;
        margin-top: 10px;
    }}
</style>
</head>

<body>

<h1>Multi-Stock Strategy Report</h1>

<h2>Performance Summary</h2>

{summary.to_html(index=False)}

<h2>Combined Equity Curve</h2>

<img src="{equity_curve}" width="900">

<h2>Combined Drawdown</h2>

<img src="{drawdown}" width="900">

</body>
</html>
"""

    (output_dir / "multi_stock_report.html").write_text(html)