"""Gerenciador de configurações

Esse módulo tem funções para carregar, manipular e salvar configurações

"""

import os.path
import yaml

_DEFAULTS = {
    "psname": "notepad.exe",
    "threshold": 1,
    "frequency": 30
}

_config = {}


def load(cfg_file="config.yml"):
    """Carrega as configurações de um arquivo"""

    if not os.path.isfile(cfg_file):
        return

    global _config
    with open(cfg_file, "r") as file:
        _config = yaml.load(file) or _config


def save(cfg_file="config.yml"):
    """Salva as configurações para um arquivo"""

    with open(cfg_file, 'w') as file:
        yaml.dump(_config, file, default_flow_style=False)


def get(key):
    """Obtém o valor de uma chave de configuração"""

    return _config[key] if key in _config else _DEFAULTS[key]


def set(key, value):
    """Define o valor de uma chave de configuração"""

    _config[key] = value


def keys():
    """Obtém todas as chaves de configuração disponíveis"""

    return _DEFAULTS.keys() | _config.keys()
