import pytest
from models import Trade
from services import (calculate_total_profit, calculate_win_rate, find_highest_profit_trade)

def make_trade(profit: float, stock: str = "test") -> Trade:
    return Trade(
        stock=stock,
        buy_price=1.0,
        sell_price=1.0,
        quantity=1,
        profit=profit
    )

def test_calculate_total_profit_with_mixed_results() -> None:
    trades = [
        make_trade(600.0),
            make_trade(-300.0),
            make_trade(0.0)
    ]

    result = calculate_total_profit(trades)

    assert result == 300.0

def test_calculate_total_profit_with_empty_list() -> None:
    result = calculate_total_profit([])

    assert result == 0

def test_calculate_win_rate_with_mixed_results() -> None:
    trades = [
    make_trade(600.0),
    make_trade(-300.0),
    make_trade(0.0)
]

    result = calculate_win_rate(trades)

    assert result == pytest.approx(1 / 3)

def test_calculate_win_rate_with_empty_list() -> None:
    result = calculate_win_rate([])

    assert result == 0

def test_find_highest_profit_trade_with_mixed_results() -> None:
    trades = [
        make_trade(600.0, stock="beone"),
        make_trade(-300.0, stock="alibaba"),
        make_trade(0.0, stock="skhy")
    ]

    result = find_highest_profit_trade(trades)

    assert result == make_trade(600.0, stock="beone")

def test_find_highest_profit_trade_with_all_losses() -> None:
    trades = [
        make_trade(-300.0, stock="alibaba"),
                make_trade(0.0, stock="skhy")
    ]

    result = find_highest_profit_trade(trades)

    assert result == make_trade(0.0, stock="skhy")


def test_find_highest_profit_trade_with_empty_list() -> None:
    result = find_highest_profit_trade([])

    assert result is None