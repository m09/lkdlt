from pathlib import Path

from ..kanji_infos import KanjiInfos
from ..loading import load_kanjis_and_keywords, load_replacements
from . import app


@app.command()
def index() -> None:
    lkdlt_path = Path.home() / "work" / "m09" / "nihongo" / "kanjis"

    replacements = load_replacements(lkdlt_path / "edits.txt")
    kanjis_and_keywords = load_kanjis_and_keywords(lkdlt_path / "main-list.txt")

    kanji_infos = KanjiInfos.from_data(kanjis_and_keywords, replacements)

    for kanji_info in kanji_infos:
        print(f"{kanji_info.kanji}\t{kanji_info.keyword}")
