"""Gerenciador de versão

Esse módulo gerencia a versão do God

"""

import os
import os.path

# Informação da versão atual
if os.path.isfile(".version"):
    with open(".version", "r") as version_file:
        _VERSION = {"tag": version_file.readline().strip()}
else:
    _VERSION = {"tag": "v2.1.0-beta"}


def current():
    """Obtém a versão atual do God"""

    return _VERSION["tag"]


def set_tag(version):
    """Atualiza a versão atual do god"""

    _VERSION["tag"] = version
