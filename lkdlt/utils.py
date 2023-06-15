from itertools import takewhile
from re import compile as re_compile
from sys import exit, stderr

from rich import print


def error(message: str, quit: bool = True) -> None:
    print(f"[red bold]{message}[/]", file=stderr)
    if quit:
        exit(1)


_pattern = re_compile(r"[㐀-䶵一-鿋豈-頻々]")


def is_kanji(character: str) -> bool:
    assert len(character) == 1
    return bool(_pattern.match(character))


def common_prefix(a: str, b: str) -> str:
    return "".join(c for c, _ in takewhile(lambda t: t[0] == t[1], zip(a, b)))


def common_suffix(a: str, b: str) -> str:
    return "".join(
        c for c, _ in takewhile(lambda t: t[0] == t[1], zip(a[::-1], b[::-1]))
    )[::-1]
