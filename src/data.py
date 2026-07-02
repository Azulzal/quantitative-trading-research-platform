import yfinance as yf


def download_daily_data(symbol, period="2y"):
    return yf.download(symbol, period=period, interval="1d", auto_adjust=True)


def download_hourly_data(symbol, period="730d"):
    return yf.download(symbol, period=period, interval="1h", auto_adjust=True)