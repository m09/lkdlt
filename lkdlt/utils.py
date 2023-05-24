from dataclasses import dataclass, field
from io import StringIO
from re import compile as re_compile
from sys import exit, stderr

from rich import print


def error(message: str, quit: bool = True) -> None:
    print(f"[red bold]{message}[/]", file=stderr)
    if quit:
        exit(1)


_pattern = re_compile(r"[㐀-䶵一-鿋豈-頻]")


def is_kanji(character: str) -> bool:
    assert len(character) == 1
    return bool(_pattern.match(character))


@dataclass
class Stats:
    plural_name: str
    added: int = 0
    modified: int = 0
    unknown: set[str] = field(default_factory=set)

    def __str__(self) -> str:
        with StringIO() as string_io:
            if self.unknown:
                string_io.write(
                    f"{len(self.unknown)} {self.plural_name} were not found: "
                    f"{', '.join(self.unknown)}.\n"
                )

            string_io.write(
                f"Added {self.added} {self.plural_name}, "
                f"modified {self.modified} {self.plural_name}."
            )
            return string_io.getvalue()
