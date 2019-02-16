import os.path
import yaml

DEFAULTS = {
    "psname": "notepad.exe",
    "threshold": 1,
    "frequency": 30
}

_config = {}


def load(cfg_file="config.yml"):
    if not os.path.isfile(cfg_file):
        return

    global _config
    with open(cfg_file, "r") as file:
        _config = yaml.load(file) or _config


def save(cfg_file="config.yml"):
    with open(cfg_file, 'w') as file:
        yaml.dump(_config, file, default_flow_style=False)


def get(key):
    return _config[key] if key in _config else DEFAULTS[key]


def set(key, value):
    _config[key] = value
