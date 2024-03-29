from csv import DictReader
from pathlib import Path
from typing import Dict, Iterator, Tuple, cast

from .config import config
from .model import KanjiInfo
from .stories import process_story_to_html


def load_kanji_infos(do_replacements: bool, do_stories: bool) -> list[KanjiInfo]:
    return KanjiInfo.from_data(
        _load_kanjis_and_keywords(config.paths.kanji),
        _load_replacements(config.paths.edits) if do_replacements else {},
        _load_stories(config.paths.stories) if do_stories else {},
    )


def _load_replacements(path: Path) -> Dict[str, str]:
    replacements = {}
    with path.open(encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                _, kanji, replacement = line.split("\t", maxsplit=2)
                replacements[kanji] = replacement
    return replacements


def _load_stories(path: Path) -> Dict[str, str]:
    result = {}
    with path.open(encoding="utf8") as fh:
        reader = DictReader(fh)
        for row in reader:
            result[row["kanji"]] = process_story_to_html(row["keyword"], row["story"])
    return result


def _load_kanjis_and_keywords(path: Path) -> Iterator[Tuple[str, str]]:
    with path.open(encoding="utf8") as fh:
        for line in fh:
            yield cast(Tuple[str, str], tuple(x.strip() for x in line.split("\t")))
