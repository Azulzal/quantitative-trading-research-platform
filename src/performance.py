def backtest_stats(trades):
    if len(trades) == 0:
        return {
            "Trades": 0,
            "Wins": 0,
            "Losses": 0,
            "Breakevens": 0,
            "Win Rate": None,
            "Average R": None,
            "Total R": 0,
            "Best R": None,
            "Worst R": None,
        }

    wins = trades[trades["R Result"] > 0]
    losses = trades[trades["R Result"] < 0]
    breakevens = trades[trades["R Result"] == 0]

    return {
        "Trades": len(trades),
        "Wins": len(wins),
        "Losses": len(losses),
        "Breakevens": len(breakevens),
        "Win Rate": len(wins) / len(trades),
        "Average R": trades["R Result"].mean(),
        "Total R": trades["R Result"].sum(),
        "Best R": trades["R Result"].max(),
        "Worst R": trades["R Result"].min(),
    }