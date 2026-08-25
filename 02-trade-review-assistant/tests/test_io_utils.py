from dataclasses import asdict

from io_utils import load_trades_from_json, save_report_to_json
from models import Trade

def test_save_and_load_trades(tmp_path) -> None:                                       #测试正常读取和保存
    file_path = tmp_path / "report.json"
    trade = Trade(
        stock="beone",
        buy_price=250.0,
        sell_price=256.0,
        quantity=100,
        profit=600.0
    )
    report = {
        "trades": [asdict(trade)]
    }

    save_report_to_json(report, file_path)
    result = load_trades_from_json(file_path)

    assert result == [trade]

def test_load_missing_file(tmp_path) -> None:                                          #文件不存在
    file_path = tmp_path / "missing.json"

    result = load_trades_from_json(file_path)

    assert result == []

def test_load_empty_file(tmp_path) -> None:                                            #文件为空
    file_path = tmp_path / "empty.json"
    file_path.write_text("",encoding="utf-8")

    result = load_trades_from_json(file_path)

    assert result == []

def test_load_corrupt_json(tmp_path) -> None:                                          #json文件损坏
    file_path = tmp_path / "corrupt.json"
    file_path.write_text("这不是正确的 JSON", encoding="utf-8")

    result = load_trades_from_json(file_path)

    assert result == []