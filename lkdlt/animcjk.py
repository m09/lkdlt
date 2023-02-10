from pathlib import Path
from typing import Optional


def get_svg(kanji: str) -> Optional[str]:
    dirnames = ("svgsJa",)
    for dirname in dirnames:
        svg_path = Path.home() / "opt" / "animcjk" / dirname / f"{ord(kanji)}.svg"
        if svg_path.exists():
            return svg_path.read_text(encoding="utf8")
    return None
