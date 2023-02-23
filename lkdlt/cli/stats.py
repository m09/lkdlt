from collections import defaultdict
from pathlib import Path

from ..kanji_infos import KanjiInfos
from ..loading import load_kanjis_and_keywords, load_replacements
from . import app


@app.command()
def stats() -> None:
    lkdlt_path = Path.home() / "work" / "m09" / "nihongo" / "kanjis"

    replacements = load_replacements(lkdlt_path / "edits.txt")
    replacements = {}
    kanjis_and_keywords = load_kanjis_and_keywords(lkdlt_path / "main-list.txt")

    kanji_infos = KanjiInfos.from_data(kanjis_and_keywords, replacements)

    keywords = defaultdict(set)

    for kanji_info in kanji_infos:
        keywords[kanji_info.keyword].add(kanji_info.kanji)

    for keyword, kanjis in keywords.items():
        if len(kanjis) > 1:
            print(keyword, " ⋅ ".join(kanjis))
