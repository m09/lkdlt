from dataclasses import dataclass
from typing import Optional


@dataclass
class KanjiInfo:
    keyword: str
    kanji: str
    svg: Optional[str]
    story: str
    identifier: int
