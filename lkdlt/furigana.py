from re import Match
from re import compile as re_compile

_pattern = re_compile(r" ?([^ \[\]]+)\[(.*?)\]")


def _repl_kana(match: Match) -> str:
    return match.group(2) if match.group(2) else match.group(1)


def _repl_sgml(match: Match) -> str:
    return (
        f'<sub alias="{match.group(2)}">match.group(1)</sub>'
        if match.group(2)
        else match.group(1)
    )


def furigana_to_kanji(furigana: str) -> str:
    return _pattern.sub(r"\1", furigana)


def furigana_to_kana(furigana: str) -> str:
    return _pattern.sub(_repl_kana, furigana)


def furigana_to_sgml(furigana: str) -> str:
    return _pattern.sub(_repl_sgml, furigana)
