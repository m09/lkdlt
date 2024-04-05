from pathlib import Path

from appdirs import user_config_dir, user_data_dir

from . import app_name

config_dir = Path(user_config_dir(app_name))
data_dir = Path(user_data_dir(app_name))
config_path = config_dir / "config.yml"
jmdict_pickle_path = data_dir / "jmdict.pkl"
