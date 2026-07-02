import numpy as np


def add_confirmed_structure(df):
    df = df.copy()

    df["Bull Break"] = False
    df["Bear Break"] = False
    df["Bull Count"] = 0
    df["Bear Count"] = 0

    df["Candidate High"] = np.nan
    df["Candidate Low"] = np.nan
    df["Confirmed High"] = np.nan
    df["Confirmed Low"] = np.nan

    candidate_high = df["High"].iloc[0]
    candidate_low = df["Low"].iloc[0]

    confirmed_high = None
    confirmed_low = None
    bull_count = 0
    bear_count = 0

    for i in range(1, len(df)):
        candle = df.iloc[i]
        prev = df.iloc[i - 1]

        bearish_confirm = candle["Close"] < prev["Low"]
        bullish_confirm = candle["Close"] > prev["High"]

        candidate_high = max(candidate_high, candle["High"])
        candidate_low = min(candidate_low, candle["Low"])

        if bearish_confirm:
            confirmed_high = candidate_high
            candidate_low = candle["Low"]

        if bullish_confirm:
            confirmed_low = candidate_low
            candidate_high = candle["High"]

        if confirmed_high is not None and candle["Close"] > confirmed_high:
            bull_count += 1
            bear_count = 0

            df.loc[df.index[i], "Bull Break"] = True
            df.loc[df.index[i], "Bull Count"] = bull_count

            confirmed_low = candidate_low
            candidate_high = candle["High"]
            candidate_low = candle["Low"]
            confirmed_high = None

        if confirmed_low is not None and candle["Close"] < confirmed_low:
            bear_count += 1
            bull_count = 0

            df.loc[df.index[i], "Bear Break"] = True
            df.loc[df.index[i], "Bear Count"] = bear_count

            confirmed_high = candidate_high
            candidate_high = candle["High"]
            candidate_low = candle["Low"]
            confirmed_low = None

        df.loc[df.index[i], "Candidate High"] = candidate_high
        df.loc[df.index[i], "Candidate Low"] = candidate_low
        df.loc[df.index[i], "Confirmed High"] = confirmed_high
        df.loc[df.index[i], "Confirmed Low"] = confirmed_low

    return df


def classify_structure_regime(df, lookback_breaks=10):
    df = df.copy()
    df["Structure Regime"] = None

    break_history = []
    last_major_side = None

    for i in range(len(df)):
        row = df.iloc[i]

        if row["Bull Break"]:
            break_history.append(("bull", row["Bull Count"]))

        if row["Bear Break"]:
            break_history.append(("bear", row["Bear Count"]))

        recent = break_history[-lookback_breaks:]

        if len(recent) == 0:
            df.loc[df.index[i], "Structure Regime"] = "Neutral"
            continue

        current_side, current_count = recent[-1]

        if current_side == "bull" and current_count >= 3:
            last_major_side = "bull"

        if current_side == "bear" and current_count >= 3:
            last_major_side = "bear"

        if current_side == "bull":
            if last_major_side == "bear" and current_count < 3:
                regime = "Redistribution"
            else:
                regime = "Accumulation"
        else:
            if last_major_side == "bull" and current_count <= 2:
                regime = "Reaccumulation"
            else:
                regime = "Distribution"

        df.loc[df.index[i], "Structure Regime"] = regime

    return df