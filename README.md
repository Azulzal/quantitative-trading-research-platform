# Quantitative Trading Research Platform

A modular quantitative research framework for developing, testing and evaluating systematic equity trading strategies using Python.

The platform automates the complete research workflow—from downloading historical market data through to strategy evaluation, performance analysis and HTML report generation.

---

## Features

- Historical market data collection using Yahoo Finance
- Technical indicators (EMA, ATR)
- Multi-timeframe analysis
- Market structure detection
- Market regime classification
- Rule-based backtesting engine
- ATR-based risk management
- Single-stock and multi-stock backtesting
- Automated performance reporting
- Equity curve and drawdown visualisation
- HTML report generation
- Configurable stock universes

---

## Repository Structure

```text
quantitative-trading-research-platform/

├── docs/
├── notebooks/
├── results/
├── src/
│   ├── backtester.py
│   ├── data.py
│   ├── html_report.py
│   ├── indicators.py
│   ├── multi_report.py
│   ├── performance.py
│   ├── plotting.py
│   ├── regimes.py
│   ├── reporting.py
│   ├── structure.py
│   ├── timeframes.py
│   └── universe.py
│
├── run_backtest.py
├── run_multi_backtest.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## Quick Start

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/quantitative-trading-research-platform.git
cd quantitative-trading-research-platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run a single-stock backtest

```bash
python run_backtest.py
```

Run a multi-stock backtest

```bash
python run_multi_backtest.py
```

---

## Example Outputs

The framework automatically generates:

- Trade logs
- Performance summaries
- Equity curve charts
- Drawdown charts
- Exit reason summaries
- HTML reports

Outputs are saved to the `results/` directory.

---

## Current Research Pipeline

1. Download historical market data
2. Calculate technical indicators
3. Build weekly and monthly timeframes
4. Detect market structure
5. Classify market regimes
6. Execute trading strategy
7. Evaluate performance
8. Generate charts and HTML reports

---

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- yfinance
- TA-Lib / ta
- Git
- GitHub

---

## Future Work

- Full S&P 100 and S&P 500 universe support
- Parameter optimisation
- Walk-forward analysis
- Monte Carlo robustness testing
- Portfolio optimisation
- Parallel backtesting
- Unit testing
- Interactive dashboard