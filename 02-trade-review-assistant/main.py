from models import prase_trade_input,Trade
from services import calculate_total_profit
from services import calculate_win_rate
from services import find_highest_profit_trade
from io_utils import save_report_to_json,load_trades_from_json

from dataclasses import asdict

def build_report(trades: list[Trade]) -> dict:
    total_profit = calculate_total_profit(trades)
    win_rate = calculate_win_rate(trades)
    highest_profit = find_highest_profit_trade(trades)

    return {
        "trades": [asdict(trade) for trade in trades],
        "total_profit": total_profit,
        "win_rate": win_rate,
        "highest_profit_trade": (
            asdict(highest_profit)
            if highest_profit
            else None
        )
    }

def main() -> None:
    print("交易记录分析器 V0.1")
    trades = load_trades_from_json()
    print(f"已加载{len(trades)}条历史记录")

    while True:
        raw_input = input("请输入交易记录（格式：股票名,买入价,卖出价,数量）：").strip()

        if raw_input == "":
            break

        try:
            trade = prase_trade_input(raw_input)
            trades.append(trade)

            report = build_report(trades)
            save_report_to_json(report)
            print(f"添加成功并已保存：{trade}")

        except ValueError as e:
            print(f"输入错误：{e}")

    if not trades:
        print("没有有效的交易记录")
        return

    total_profit = calculate_total_profit(trades)
    print(f"总盈亏: {total_profit}")

    win_rate = calculate_win_rate(trades)
    print(f"胜率: {win_rate:.2%}")

    highest_profit = find_highest_profit_trade(trades)
    print(f"最高盈利{highest_profit}")

    report = build_report(trades)

    save_report_to_json(report)
    print("报告已保存至 trade_report.json")

if __name__ == "__main__":
    main()