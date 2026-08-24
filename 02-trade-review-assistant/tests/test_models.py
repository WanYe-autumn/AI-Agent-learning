import pytest

from  models import Trade,prase_trade_input
from dataclasses import asdict

@pytest.mark.parametrize(
    "raw_input,expected",
    [
        (
            "beone,250,256,100",
            {
                "stock": "beone",
                "buy_price": 250.0,
                "sell_price": 256.0,
                "quantity": 100,
                "profit": 600.0
            }

        ),
        (
            "beone，250，256，100",
            {
                "stock": "beone",
                "buy_price": 250.0,
                "sell_price": 256.0,
                "quantity": 100,
                "profit": 600.0
            }
        ),
         (
            "  beone  , 250 , 256 , 100 ",
            {
                "stock": "beone",
                "buy_price": 250.0,
                "sell_price": 256.0,
                "quantity": 100,
                "profit": 600.0
            }
        )
    ]
)
def test_parse_trade_input_with_valid_input(
    raw_input:str,
    expected:dict
)   -> None:
    result = prase_trade_input(raw_input)
    assert isinstance(result, Trade)
    assert asdict(result) == expected

@pytest.mark.parametrize(
    "raw_input, expected_message",
    [
      (
            "beone,abc,256,100",
            "买入价和卖出价必须是数字"
        ),
        (
            "beone,250,256,100.5",
            "数量必须是整数"
        ),
        (
            "beone,0,256,100",
            "买入价和卖出价必须大于零"
        ),
        (
            "beone,250,256,0",
            "数量必须大于零"
        ),
        (
            " ,250,256,100",
            "股票名不能为空"
        ),
        (
            "beone,250,256",
            "请输入：股票名,买入价,卖出价,数量"
        )  
    ]
)
def test_parse_trade_input_with_invalid_input(
    raw_input: str,
    expected_message: str
) -> None:
    with pytest.raises(ValueError) as error:
        prase_trade_input(raw_input)

    assert str(error.value) == expected_message