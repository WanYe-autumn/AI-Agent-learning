import json
from json import JSONDecodeError
from pathlib import Path

from models import Trade

DEFAULT_REPORT_PATH = (
    Path(__file__).resolve().parent / "trade_report.json"
)

def save_report_to_json(
        report:dict,
        file_path:str = "trade_report.json"
) -> None:

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=4
        )

def load_trades_from_json(
        file_path: Path = DEFAULT_REPORT_PATH
) -> list[Trade]:
    if not file_path.exists():
        return[]

    try:
        content = file_path.read_text(encoding="utf-8")

        if content.strip() == "":
            return []

        report = json.loads(content)
        trade_dicts = report.get("trades", [])

        return [
            Trade(**trade_dict)
            for trade_dict in trade_dicts
        ]

    except (OSError, JSONDecodeError, TypeError, AttributeError):
        return []