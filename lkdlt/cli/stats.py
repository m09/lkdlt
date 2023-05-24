from . import app


@app.command()
def stats() -> None:
    from collections import defaultdict

    from ..loading import load_kanji_infos

    kanji_infos = load_kanji_infos(do_replacements=False, do_stories=False)
    keywords = defaultdict(set)

    for kanji_info in kanji_infos:
        keywords[kanji_info.keyword].add(kanji_info.kanji)

    for keyword, kanjis in keywords.items():
        if len(kanjis) > 1:
            print(keyword, " ⋅ ".join(kanjis))
