from collections import defaultdict
from typing import Any, TypeVar

from xmltodict import parse as xmltodict_parse

from .config import config
from .model import Kanji

_T = TypeVar("_T")


def _wrap(item: _T | list[_T]) -> list[_T]:
    return item if isinstance(item, list) else [item]


def _parse_rmgroup(
    data: dict[str, Any]
) -> tuple[dict[str, tuple[str, ...]], tuple[str, ...], tuple[str, ...]]:
    meanings = _wrap(data["meaning"])
    readings = _wrap(data["reading"])
    glosses = defaultdict(list)
    for meaning in meanings:
        if isinstance(meaning, str):
            glosses["en"].append(meaning)
        else:
            glosses[meaning["@m_lang"]].append(meaning["#text"])

    on = tuple(i["#text"] for i in readings if i["@r_type"] == "ja_on")
    kun = tuple(i["#text"] for i in readings if i["@r_type"] == "ja_kun")
    return {k: tuple(v) for k, v in glosses.items()}, on, kun


def parse() -> dict[str, Kanji]:
    with config.paths.kanjidic.open(mode="rb") as fh:
        data = xmltodict_parse(fh)

    result = {}
    for item in data["kanjidic2"]["character"]:
        if (
            "reading_meaning" not in item
            or "reading" not in item["reading_meaning"]["rmgroup"]
            or "meaning" not in item["reading_meaning"]["rmgroup"]
        ):
            continue
        glosses, on, kun = _parse_rmgroup(item["reading_meaning"]["rmgroup"])
        if on or kun:
            result[item["literal"]] = Kanji(item["literal"], glosses, on, kun)

    return result
