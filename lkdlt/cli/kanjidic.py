# from typing import Any

# from xmltodict import parse

# from ..config import Config
# from . import app

# def parse_rmgroup(data):
#     if not isinstance(data, list):
#         data = [data]


# def parse_reading_meaning(data: list[dict[str, Any]] | dict[str, Any]) -> list[Any]:
#     if not isinstance(data, list):
#         data = [data]
#     return [parse_rmgroup(item) for item in data]


# @app.command()
# def kanji_dic() -> None:
#     config = Config.load()

#     with open(config.kanji_dic_path, mode="rb") as fh:
#         data = parse(fh)

#     filtered = {item["literal"]: item for item in data}
