from models import prase_trade_input,Trade
from services import calculate_total_profit,calculate_win_rate,find_highest_profit_trade,find_trade_by_number,delete_trade_by_number
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

def display_trades(trades: list[Trade]) -> None:
    if not trades:
        print("暂无交易记录")
        return

    print("\n全部交易:")

    for number, trade in enumerate(trades, start=1):
        print(
            f"{number}. "
            f"股票：{trade.stock}，"
            f"买入价：{trade.buy_price}，"
            f"卖出价：{trade.sell_price}，"
            f"数量：{trade.quantity}，"
            f"盈亏：{trade.profit}"
        )

def main() -> None:
    print("交易记录分析器 V0.1")

    trades = load_trades_from_json()
    print(f"已加载{len(trades)}条历史记录")
    

    while True:
        print("\n请选择操作：")
        print("1. 新增交易")
        print("2. 查看全部交易")
        print("3. 删除交易")
        print("0. 退出")

        choice = input("请输入编号：").strip()

        if choice == "1":
            raw_input = input(
                "请输入交易记录（格式：股票名,买入价,卖出价,数量）："
            ).strip()

            try:
                trade = prase_trade_input(raw_input)
                trades.append(trade)

                report = build_report(trades)
                save_report_to_json(report)

                print(f"添加成功并已保存：{trade}")

            except ValueError as e:
                print(f"输入错误：{e}")

            continue

        if choice == "2":
            display_trades(trades)

            continue

        if choice == "3":
            display_trades(trades)

            if not trades:
                continue

            try:
                number = int(input("请输入要删除的交易编号："))
            except ValueError:
                print("编号必须是整数")
                continue

            trade = find_trade_by_number(trades, number)

            if trade is None:
                print("交易编号不存在")
                continue

            confirm = input(
                f"确认删除 {trade.stock} 吗？输入 y 确认："
            ).strip().lower()

            if confirm != "y":
                print("已取消删除")
                continue

            deleted_trade = delete_trade_by_number(trades, number)

            report = build_report(trades)
            save_report_to_json(report)

            print(f"已删除并保存：{deleted_trade}")
            continue

        if choice == "0":
            break

        print("无效操作，请输入 0、1、2 或 3") 
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