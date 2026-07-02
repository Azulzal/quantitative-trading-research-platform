import ta


def add_emas(df):
    df = df.copy()
    df["EMA9"] = df["Close"].ewm(span=9).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["EMA50"] = df["Close"].ewm(span=50).mean()
    return df


def add_atr(df, window=14):
    df = df.copy()
    df["ATR"] = ta.volatility.average_true_range(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=window,
    )
    return df