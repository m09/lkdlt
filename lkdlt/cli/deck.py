from importlib.resources import read_text
from itertools import islice
from pathlib import Path
from typing import Optional

from genanki import Deck, Model, Note, Package, guid_for
from typer import Argument

from .. import card
from ..kanji_infos import KanjiInfos
from ..loading import load_kanjis_and_keywords, load_replacements
from . import app


class MyNote(Note):
    @property
    def guid(self) -> int:
        return guid_for(self.fields[-1])


model = Model(
    1294535707,
    "Kanji",
    fields=[
        {"name": "Mot-clef"},
        {"name": "Kanji"},
        {"name": "SVG-Présent"},
        {"name": "SVG"},
        {"name": "Histoire"},
        {"name": "Identifiant"},
    ],
    templates=[
        dict(
            name="Génération",
            qfmt=read_text(card, "generation-front.html"),
            afmt=read_text(card, "generation-back.html"),
        ),
    ],
    css=read_text(card, "style.css"),
)


@app.command()
def deck(limit: Optional[int] = Argument(None)) -> None:  # noqa: B008
    deck = Deck(1253852384, "Japonais::Les Kanjis dans la tête")

    lkdlt_path = Path.home() / "work" / "m09" / "nihongo" / "kanjis"

    replacements = load_replacements(lkdlt_path / "edits.txt")
    kanjis_and_keywords = load_kanjis_and_keywords(lkdlt_path / "main-list.txt")

    kanji_infos = KanjiInfos.from_data(kanjis_and_keywords, replacements)

    unknown = []
    for kanji_info in islice(kanji_infos, limit):
        if kanji_info.svg is None:
            unknown.append(kanji_info.kanji)
            svg = ""
            svg_found = ""
        else:
            svg = kanji_info.svg
            svg_found = "Oui"
        deck.add_note(
            MyNote(
                model=model,
                fields=[
                    kanji_info.keyword,
                    kanji_info.kanji,
                    svg_found,
                    svg,
                    kanji_info.story,
                    str(kanji_info.identifier),
                ],
            )
        )

    Package(deck).write_to_file(str(Path.home() / "output.apkg"))
    print(unknown)
