from re import VERBOSE, Match
from re import compile as re_compile

from jcconv3 import kata2hira


class Furigana:
    def __init__(self, furigana: str) -> None:
        self.original = furigana
        self.nonempty = clean_empty_furigana(furigana)
        self.normalized = normalize_furigana(self.nonempty)
        self.kanji = furigana_to_kanji(self.normalized)
        self.kana = furigana_to_kana(self.normalized)
        self.ruby = furigana_to_ruby(self.normalized)
        self.sgml = furigana_to_sgml(self.normalized)


_pattern = re_compile(r"(?P<space>	| )?(?P<kanji>[^ 	\[\]]+)\[(?P<kana>.*?)\]")
_pattern_double = re_compile(
    r"""
     (?P<space>[ ]?)
     (?P<kanji1>[^ \[\]]+)
     \[(?P<kana1>.*?)\]
     (?P<kanji2>[^ \[\]]+)
     \[(?P<kana2>.*?)\]
     """,
    flags=VERBOSE,
)


def _repl_clean_empty(match: Match) -> str:
    return match.group().replace("\t", " ")


def _repl_double(match: Match) -> str:
    space, kanji1, kana1, kanji2, kana2 = match.groups()
    return f"{space}{kanji1}{kanji2}[{kana1}{kana2}]"


def _repl_convert(match: Match) -> str:
    space, kanji, kana = match.groups()
    return f"{space or ''}{kanji}[{kata2hira(kana)}]"


def furigana_to_kanji(furigana: str) -> str:
    return _pattern.sub(r"\g<kanji>", furigana)


def furigana_to_kana(furigana: str) -> str:
    return _pattern.sub(r"\g<kana>", furigana)


def furigana_to_ruby(furigana: str) -> str:
    return _pattern.sub(r"<ruby><rb>\g<kanji></rb><rt>\g<kana></rt></ruby>", furigana)


def furigana_to_sgml(furigana: str) -> str:
    return _pattern.sub(r'<sub alias="\g<kana>">\g<kanji></sub>', furigana)


def clean_empty_furigana(furigana: str) -> str:
    furigana = furigana.replace("[ ]", "\t")
    furigana = _pattern.sub(_repl_clean_empty, furigana)
    return furigana.replace("\t", "")


def normalize_furigana(furigana: str) -> str:
    while (new_furigana := _pattern_double.sub(_repl_double, furigana)) != furigana:
        furigana = new_furigana
    return _pattern.sub(_repl_convert, furigana)
