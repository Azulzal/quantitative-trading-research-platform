import pandas as pd

from src.data import download_daily_data
from src.regimes import prepare_regime_data, check_precomputed_regimes
from src.timeframes import build_weekly_data, get_last_completed_week

MIN_HISTORY_DAYS = 300
FORWARD_BUFFER_DAYS = 10
RISK_ATR_MULTIPLIER = 1.5
CANCEL_ATR_MULTIPLIER = 2
ORDER_EXPIRY_DAYS = 8

def backtest_daily_strategy(symbol: str) -> pd.DataFrame:
    """
    Backtest the daily quantitative trading strategy for a single ticker.

    The strategy uses market structure regimes, EMA pullback/reclaim logic,
    ATR-based risk management and weekly trailing exits.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol.

    Returns
    -------
    pd.DataFrame
        Trade log containing entries, exits, R results and exit reasons.
    """
    daily = download_daily_data(symbol)

    daily_s, weekly_s, monthly_s = prepare_regime_data(daily)

    weekly_data = build_weekly_data(daily)

    trades = []

    locked = False
    lock_high = None

    order_active = False
    in_trade = False

    signal_high = None
    signal_time = None
    signal_atr = None
    order_created_index = None

    pullback_seen = False
    reclaim_seen = False

    entry_price = None
    stop_loss = None
    initial_risk = None
    entry_time = None
    moved_to_breakeven = False
    weekly_trail_active = False

    signal_daily_regime = None
    signal_weekly_regime = None
    signal_monthly_regime = None
 
    trade_taken_dates = set()

    for i in range(MIN_HISTORY_DAYS, len(daily) - FORWARD_BUFFER_DAYS):
        current_time = daily.index[i]
        candle = daily.iloc[i]

        current_date = pd.Timestamp(current_time).tz_localize(None).normalize()
        trade_date = current_date.date()

        daily_past = daily.loc[:current_date].iloc[:-1]

        if len(daily_past) < MIN_HISTORY_DAYS:
            continue

        last_week = get_last_completed_week(weekly_data, current_time)

        if last_week is None:
            continue

        recent_10w_high = last_week["Recent 10W High"]

        # =========================
        # MANAGE OPEN TRADE
        # =========================
        if in_trade:
            

            # Move to breakeven after +1R
            if not moved_to_breakeven and candle["High"] >= entry_price + initial_risk:
                stop_loss = entry_price
                moved_to_breakeven = True

            # Weekly EMA9 trail only starts once weekly EMA9 is above breakeven/entry
            if moved_to_breakeven and last_week["EMA9"] > entry_price:
                weekly_trail_active = True

            # Exit when completed weekly candle closes below weekly EMA9
            if weekly_trail_active and last_week["Close"] < last_week["EMA9"]:
                exit_price = last_week["Close"]
                r_result = (exit_price - entry_price) / initial_risk

                trades.append({
                    "Ticker": symbol,
                    "Signal Time": signal_time,
                    "Entry Time": entry_time,
                    "Exit Time": last_week.name,
                    "Entry Price": entry_price,
                    "Exit Price": exit_price,
                    "Initial Stop": entry_price - initial_risk,
                    "Final Stop": last_week["EMA9"],
                    "R Result": r_result,
                    "Moved BE": moved_to_breakeven,
                    "Trail Active": weekly_trail_active,
                    "Exit Reason": "Weekly close below EMA9"
                })

                in_trade = False
                locked = True
                lock_high = recent_10w_high

                pullback_seen = False
                reclaim_seen = False
                weekly_trail_active = False
                continue

            # Normal stop loss before weekly trail exits
            if candle["Low"] <= stop_loss:
                exit_price = stop_loss
                r_result = (exit_price - entry_price) / initial_risk

                trades.append({
                    "Ticker": symbol,
                    "Signal Time": signal_time,
                    "Entry Time": entry_time,
                    "Exit Time": current_time,
                    "Entry Price": entry_price,
                    "Exit Price": exit_price,
                    "Initial Stop": entry_price - initial_risk,
                    "Final Stop": stop_loss,
                    "R Result": r_result,
                    "Moved BE": moved_to_breakeven,
                    "Trail Active": weekly_trail_active,
                    "Exit Reason": "Stop loss hit",
                    "Daily Regime": signal_daily_regime,
                    "Weekly Regime": signal_weekly_regime,
                    "Monthly Regime": signal_monthly_regime,
                })

                in_trade = False
                locked = True
                lock_high = recent_10w_high

                pullback_seen = False
                reclaim_seen = False
                weekly_trail_active = False
                continue

            continue

        # =========================
        # RESET LOCK
        # =========================
        if locked:
            if candle["High"] > lock_high:
                locked = False
                lock_high = None
                pullback_seen = False
                reclaim_seen = False
                order_active = False
            else:
                continue

        # =========================
        # MANAGE ACTIVE DAILY BUY STOP
        # =========================
        if order_active:
            candles_waited = i - order_created_index

            # Entry check first
            if candle["High"] > signal_high:
                entry_price = signal_high
                entry_time = current_time
                initial_risk = RISK_ATR_MULTIPLIER * signal_atr
                stop_loss = entry_price - initial_risk
                moved_to_breakeven = False
                weekly_trail_active = False

                in_trade = True
                order_active = False
                trade_taken_dates.add(trade_date)
                continue

            # Cancel if drops 2 ATR below setup high
            if candle["Low"] <= signal_high - (CANCEL_ATR_MULTIPLIER * signal_atr):
                order_active = False
                signal_high = None
                signal_time = None
                signal_atr = None
                order_created_index = None
                pullback_seen = False
                reclaim_seen = False
                continue

            # Expires after 8 daily candles
            if candles_waited > ORDER_EXPIRY_DAYS:
                order_active = False
                signal_high = None
                signal_time = None
                signal_atr = None
                order_created_index = None
                pullback_seen = False
                reclaim_seen = False
                continue

            continue


        # =========================
        # DAILY SETUP
        # old hourly logic now on daily candles
        # =========================

        if not pullback_seen:
            if candle["Close"] < candle["EMA50"]:
                pullback_seen = True
            continue

        if pullback_seen and not reclaim_seen:
            if candle["Close"] > candle["EMA20"]:
                reclaim_seen = True
            continue

        if reclaim_seen:
            next_candle = daily.iloc[i + 1]

            # Max 1 trade per day
            if trade_date in trade_taken_dates:
                continue

            # Signal candle must close above EMA20
            if candle["Close"] <= candle["EMA20"]:
                continue

            # Signal candle must be bullish
            if candle["Close"] <= candle["Open"]:
                continue

            # Next candle must not break this candle's high
            if next_candle["High"] >= candle["High"]:
                continue

            # Do not create setup above/breaking recent 10-week high
            if candle["High"] >= recent_10w_high or candle["Open"] >= recent_10w_high:
                locked = True
                lock_high = recent_10w_high
                pullback_seen = False
                reclaim_seen = False
                continue

            filters = check_precomputed_regimes(
                daily_s,
                weekly_s,
                monthly_s,
                current_time
            )

            if not filters["overall"]:
                pullback_seen = False
                reclaim_seen = False
                continue

            signal_high = candle["High"]
            signal_time = current_time
            signal_atr = candle["ATR"]
            order_created_index = i
            order_active = True

            signal_daily_regime = filters["daily"]
            signal_weekly_regime = filters["weekly"]
            signal_monthly_regime = filters["monthly"]

            continue

    return pd.DataFrame(trades)