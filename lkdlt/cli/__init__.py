from importlib import import_module
from importlib import invalidate_caches as importlib_invalidate_caches
from importlib import reload
from logging import INFO, basicConfig
from pkgutil import walk_packages
from sys import modules

from rich.logging import RichHandler
from typer import Typer

app = Typer(
    help="Tool to handle a large number of beamer decks, "
    "used by several persons, with shared slides amongst the decks.",
    chain=True,
)


def import_module_and_submodules(package_name: str) -> None:
    """
    From https://github.com/allenai/allennlp/blob/master/allennlp/common/util.py
    """
    importlib_invalidate_caches()

    if package_name in modules:
        module = modules[package_name]
        reload(module)
    else:
        module = import_module(package_name)
    path = getattr(module, "__path__", [])
    path_string = "" if not path else path[0]

    for module_finder, name, _ in walk_packages(path):
        if (
            path_string
            and hasattr(module_finder, "path")
            and module_finder.path != path_string  # type: ignore
        ):
            continue
        subpackage = f"{package_name}.{name}"
        import_module_and_submodules(subpackage)


def main() -> None:
    basicConfig(
        level=INFO,
        format="%(message)s",
        datefmt="%H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    import_module_and_submodules(__name__)
    app()
