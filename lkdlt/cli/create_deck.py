import importlib.resources as importlib_resources
from pathlib import Path

from genanki import Deck, Model, Note, Package, guid_for

from .. import card
from ..animcjk import get_svg
from . import app


class MyNote(Note):
    @property
    def guid(self) -> int:
        return guid_for(self.fields[-1])


css = importlib_resources.read_text(card, "style.css")
front = importlib_resources.read_text(card, "front.html")
back = importlib_resources.read_text(card, "back.html")


model = Model(
    1294535707,
    "Kanji",
    fields=[
        {"name": "Mot"},
        {"name": "Kanji"},
        {"name": "SVG-Présent"},
        {"name": "SVG"},
        {"name": "Histoire"},
        {"name": "Identifiant"},
    ],
    templates=[{"name": "Card 1", "qfmt": front, "afmt": back}],
    css=css,
)


@app.command()
def create_deck() -> None:
    deck = Deck(1253852384, "Japonais::Les Kanjis dans la tête")

    lkdlt_path = Path.home() / "work" / "m09" / "nihongo" / "kanjis"

    replacements = {}

    with (lkdlt_path / "edits.txt").open(encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                _, kanji, replacement = line.split(" ", maxsplit=2)
                replacements[kanji] = replacement

    with (lkdlt_path / "main-list.txt").open(encoding="utf8") as fh:
        unknown = []
        for i, line in enumerate(fh, start=1):
            if line.strip():
                kanji, rest = line.split(maxsplit=1)
                word = replacements.get(kanji, rest.strip())
                svg = get_svg(kanji)
                if svg is None:
                    unknown.append(kanji)
                    svg = ""
                    svg_found = ""
                else:
                    svg_found = "Oui"
                deck.add_note(
                    MyNote(
                        model=model,
                        fields=[word, kanji, svg_found, svg, "", str(i)],
                    )
                )

    Package(deck).write_to_file(str(Path.home() / "output.apkg"))
    print(unknown)
