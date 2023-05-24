from typing import Optional

from .config import config


def get_svg(kanji: str) -> Optional[str]:
    dirnames = ("svgsJa",)
    for dirname in dirnames:
        svg_path = config.animcjk_dir / dirname / f"{ord(kanji)}.svg"
        if svg_path.exists():
            return svg_path.read_text(encoding="utf8")
    return None
