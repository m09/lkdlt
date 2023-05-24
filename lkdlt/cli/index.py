from ..loading import load_kanji_infos
from . import app


@app.command()
def index() -> None:
    kanji_infos = load_kanji_infos(do_replacements=True, do_stories=False)
    for kanji_info in kanji_infos:
        print(f"{kanji_info.kanji}\t{kanji_info.keyword}")
