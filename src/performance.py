import pandas as pd


def calculate_win_rate(trades):
    if len(trades) == 0:
        return 0

    wins = sum(t["Profit"] > 0 for t in trades)
    return wins / len(trades)