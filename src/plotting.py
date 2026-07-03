import matplotlib.pyplot as plt
import pandas as pd


def plot_equity_curve(trades: pd.DataFrame, save_path: str):
    """
    Plot cumulative R multiple over time.
    """

    equity = trades["R Result"].cumsum()

    plt.figure(figsize=(10, 5))
    plt.plot(equity)

    plt.title("Equity Curve")
    plt.xlabel("Trade Number")
    plt.ylabel("Cumulative R")

    plt.grid(True)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_drawdown(trades: pd.DataFrame, save_path: str):
    """
    Plot drawdown based on cumulative R.
    """

    equity = trades["R Result"].cumsum()

    running_max = equity.cummax()
    drawdown = equity - running_max

    plt.figure(figsize=(10, 5))
    plt.plot(drawdown)

    plt.title("Drawdown")
    plt.xlabel("Trade Number")
    plt.ylabel("Drawdown (R)")

    plt.grid(True)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_exit_reasons(trades: pd.DataFrame, save_path: str):
    """
    Plot exit reason breakdown as a pie chart.
    """
    counts = trades["Exit Reason"].value_counts()

    plt.figure(figsize=(7, 7))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
    plt.title("Exit Reason Breakdown")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()