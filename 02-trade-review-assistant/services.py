def calculate_total_profit(trades:list) -> float:
    total_profit = 0
    for trade in trades:
        total_profit += trade["profit"]
    return total_profit

def calculate_win_rate(trades:list) -> float:
    win_count = 0
    for trade in trades:
        if trade["profit"] > 0:
            win_count += 1

    win_rate = win_count / len(trades) if trades else 0
    return win_rate

def find_highest_profit_trade(trades:list) -> dict | None:
    if not trades:
        return None
    highest_profit_trade = sorted(trades, key=lambda x: x["profit"], reverse=True)[0]
    return highest_profit_trade