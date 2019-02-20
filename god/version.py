"""Gerenciador de versão

Esse módulo gerencia a versão do God

"""

import os
import os.path

# Informação da versão atual
if os.path.isfile(".version"):
    with open(".version", "r") as version:
        _VERSION = {"tag": version.readline().strip()}
else:
    _VERSION = None


def current():
    """Obtém a versão atual do God"""

    return _VERSION["tag"] if _VERSION else "2.0.0"


def set_tag(version):
    """Atualiza a versão atual do god"""

    _VERSION["tag"] = version
