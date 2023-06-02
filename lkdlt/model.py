from dataclasses import dataclass
from typing import Iterable, Mapping, Optional

from .animcjk import get_svg


@dataclass
class Kanji:
    kanji: str
    glosses: dict[str, tuple[str, ...]]
    on: tuple[str, ...]
    kun: tuple[str, ...]


@dataclass
class KanjiInfo:
    keyword: str
    kanji: str
    svg: Optional[str]
    story: str
    identifier: int

    @classmethod
    def from_data(
        cls,
        kanjis_and_keywords: Iterable[tuple[str, str]],
        replacements: Mapping[str, str],
        stories: Mapping[str, str],
    ) -> list["KanjiInfo"]:
        kanji_infos = []
        for i, (kanji, keyword) in enumerate(kanjis_and_keywords, start=1):
            kanji_infos.append(
                KanjiInfo(
                    keyword=replacements.get(kanji, keyword),
                    kanji=kanji,
                    svg=get_svg(kanji),
                    story=stories.get(kanji, ""),
                    identifier=i,
                )
            )

        return kanji_infos
