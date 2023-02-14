from typing import Iterable, Iterator, Mapping, Tuple

from .animcjk import get_svg
from .model import KanjiInfo


class KanjiInfos:
    def __init__(self, kanji_infos: Iterable[KanjiInfo]):
        self._kanji_infos = tuple(kanji_infos)

    def __iter__(self) -> Iterator[KanjiInfo]:
        return iter(self._kanji_infos)

    @classmethod
    def from_data(
        cls,
        kanjis_and_keywords: Iterable[Tuple[str, str]],
        replacements: Mapping[str, str],
    ) -> "KanjiInfos":
        kanji_infos = []
        for i, (kanji, keyword) in enumerate(kanjis_and_keywords, start=1):
            keyword = replacements.get(kanji, keyword)
            svg = get_svg(kanji)
            kanji_infos.append(
                KanjiInfo(keyword=keyword, kanji=kanji, svg=svg, story="", identifier=i)
            )

        return KanjiInfos(kanji_infos)
