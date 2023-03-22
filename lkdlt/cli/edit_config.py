from typer import launch

from ..paths import config_path
from . import app


@app.command()
def edit_config() -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.touch(0o644)
    launch(str(config_path))
