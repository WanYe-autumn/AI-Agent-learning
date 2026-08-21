import pytest
from services import (calculate_total_profit, calculate_win_rate, find_highest_profit_trade)

def test_calculate_total_profit_with_mixed_results() -> None:
    trades = [
        {"profit": 600.0},
        {"profit": -300.0},
        {"profit": 0.0}
    ]

    result = calculate_total_profit(trades)

    assert result == 300.0

def test_calculate_total_profit_with_empty_list() -> None:
    result = calculate_total_profit([])

    assert result == 0

def test_calculate_win_rate_with_mixed_results() -> None:
    trades = [
            {"profit": 600.0},
            {"profit": -300.0},
            {"profit": 0.0}
        ]

    result = calculate_win_rate(trades)

    assert result == pytest.approx(1 / 3)

def test_calculate_win_rate_with_empty_list() -> None:
    result = calculate_win_rate([])

    assert result == 0

def test_find_highest_profit_trade_with_mixed_results() -> None:
    trades = [
        {"stock":"beone","profit":600.0},
        {"stock":"alibaba","profit":-300.0},
        {"stock":"skhy","profit":0.0}
    ]

    result = find_highest_profit_trade(trades)

    assert result == {"stock":"beone","profit":600.0}

def test_find_highest_profit_trade_with_all_losses() -> None:
    trades = [
        {"stock": "alibaba", "profit": -300.0},
        {"stock": "skhy", "profit": -100.0}
    ]

    result = find_highest_profit_trade(trades)

    assert result == {"stock": "skhy", "profit": -100.0}


def test_find_highest_profit_trade_with_empty_list() -> None:
    result = find_highest_profit_trade([])

    assert result is None