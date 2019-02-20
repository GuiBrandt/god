"""Módulo central do god"""

import god.checker as checker

from urllib.request import urlopen, URLError

thread = None
"""god.checker.Thread: Thread de verificação de memória"""

state = 'idle'
"""str: Estado do sistema (idle/alert/safe)"""


def check_internet():
    """Testa a conexão com a internet"""

    try:
        urlopen('http://google.com', timeout=5)
        return True
    except URLError:
        return False


def start():
    """Inicia o monitoramento"""

    global thread
    thread = checker.Thread()
    thread.start()


def stop():
    """Termina o monitoramento"""

    thread.kill()
