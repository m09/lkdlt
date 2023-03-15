from csv import DictReader
from pathlib import Path
from typing import Dict, Iterator, Tuple, cast

from .stories import process_story_to_html


def load_replacements(path: Path) -> Dict[str, str]:
    replacements = {}
    with path.open(encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                _, kanji, replacement = line.split(" ", maxsplit=2)
                replacements[kanji] = replacement
    return replacements


def load_stories(path: Path) -> Dict[str, str]:
    result = {}
    with path.open(encoding="utf8") as fh:
        reader = DictReader(fh)
        for row in reader:
            result[row["kanji"]] = process_story_to_html(row["keyword"], row["story"])
    return result


def load_kanjis_and_keywords(path: Path) -> Iterator[Tuple[str, str]]:
    with path.open(encoding="utf8") as fh:
        for line in fh:
            yield cast(
                Tuple[str, str], tuple(x.strip() for x in line.split(maxsplit=1))
            )
