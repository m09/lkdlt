from csv import DictReader
from pathlib import Path
from sys import stderr
from typing import Dict, Iterator, Tuple, cast

from .model import KanjiInfo
from .stories import process_story_to_html


def load_kanji_infos(
    should_replace: bool = True, stories_required: bool = False
) -> list[KanjiInfo]:
    lkdlt_path = Path.home() / "gh" / "m09" / "nihongo" / "kanjis"

    return KanjiInfo.from_data(
        _load_kanjis_and_keywords(lkdlt_path / "main-list.txt"),
        _load_replacements(lkdlt_path / "edits.txt") if should_replace else {},
        _load_stories(Path.home() / "downloads" / "my_stories.csv", stories_required),
    )


def _load_replacements(path: Path) -> Dict[str, str]:
    replacements = {}
    with path.open(encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                _, kanji, replacement = line.split(" ", maxsplit=2)
                replacements[kanji] = replacement
    return replacements


def _load_stories(path: Path, required: bool) -> Dict[str, str]:
    result = {}
    try:
        with path.open(encoding="utf8") as fh:
            reader = DictReader(fh)
            for row in reader:
                result[row["kanji"]] = process_story_to_html(
                    row["keyword"], row["story"]
                )
    except IOError as e:
        if required:
            raise e
        else:
            print(
                f"The following error occurred while loading stories: {e}", file=stderr
            )
    return result


def _load_kanjis_and_keywords(path: Path) -> Iterator[Tuple[str, str]]:
    with path.open(encoding="utf8") as fh:
        for line in fh:
            yield cast(
                Tuple[str, str], tuple(x.strip() for x in line.split(maxsplit=1))
            )
