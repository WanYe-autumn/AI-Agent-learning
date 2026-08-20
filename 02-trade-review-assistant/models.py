def prase_trade_input(raw_input: str) -> dict:
    raw_input = raw_input.replace("， ", ",").replace("；", ";")
    fields = raw_input.split(",")

    if len(fields) != 4:
        raise ValueError("请输入：股票名,买入价,卖出价,数量")

    stock = fields[0].strip()
    try:
        sell_price = float(fields[2])
        buy_price = float(fields[1])
        quantity = int(fields[3])
    except ValueError:
        raise ValueError("买入价和卖出价必须是数字，数量必须是整数")

    if stock == "":
        raise ValueError("股票名不能为空")

    if buy_price <= 0 or sell_price <= 0 :
        raise ValueError("买入价和卖出价必须大于零")

    if quantity <= 0 :
        raise ValueError("数量必须大于零")

    profit = (sell_price - buy_price) * quantity
    return {
        "stock": stock,
        "buy_price": buy_price,
        "sell_price": sell_price,
        "quantity": quantity,
        "profit": profit
    }