from re import Match
from re import compile as re_compile

_pattern = re_compile(r"(?:	| )?(?P<kanji>[^ 	\[\]]+)\[(?P<kana>.*?)\]")


def _repl_kanji(match: Match) -> str:
    return match.group("kanji")


def _repl_kana(match: Match) -> str:
    return match.group("kana") if match.group("kana") else match.group("kanji")


def _repl_sgml(match: Match) -> str:
    return (
        f'<sub alias="{match.group("kana")}">match.group(1)</sub>'
        if match.group("kana")
        else match.group("kanji")
    )


def _repl_ruby(match: Match) -> str:
    return (
        f"<ruby><rb>{match.group('kanji')}</rb><rt>{match.group('kana')}</rt></ruby>"
        if match.group("kana")
        else match.group("kanji")
    )


def _repl_clean_empty(match: Match) -> str:
    return match.group().replace("\t", " ")


def furigana_to_kanji(furigana: str) -> str:
    return _pattern.sub(_repl_kanji, furigana)


def furigana_to_kana(furigana: str) -> str:
    return _pattern.sub(_repl_kana, furigana)


def furigana_to_ruby(furigana: str) -> str:
    return _pattern.sub(_repl_ruby, furigana)


def furigana_to_sgml(furigana: str) -> str:
    return _pattern.sub(_repl_sgml, furigana)


def clean_empty_furigana(furigana: str) -> str:
    furigana = furigana.replace("[ ]", "\t")
    furigana = _pattern.sub(_repl_clean_empty, furigana)
    return furigana.replace("\t", "")
