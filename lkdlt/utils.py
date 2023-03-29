from sys import exit, stderr

from rich import print


def error(message: str, quit: bool = True) -> None:
    print(f"[red bold]{message}[/]", file=stderr)
    if quit:
        exit(1)
