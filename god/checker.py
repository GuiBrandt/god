"""Gerenciador de uso de memória

Esse módulo traz a implementação da thread que monitora o uso de
memória do processo configurado

"""

import threading
import time

import pythoncom
from wmi import WMI

import god.cli as cli
import god.config as config
import god.handler as handler
import god.log as log


class Thread(threading.Thread):
    """Thread de monitoramento de uso de memória"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.wmi = None
        self.die = False
        self.state = 'idle'

    def check_memory(self):
        """Verifica a quantidade de memória usada e executa ações

        Testa os valores do conjunto de trabalho público dos processos
        com nome igual ao configurado e executa as ações necessárias de
        acordo com o resultado

        """

        processes = self.wmi.Win32_Process(Name=config.get("psname"))
        for process in processes:
            working_set = int(process.WorkingSetSize)
            if working_set / 1024 >= config.get("threshold"):
                self.danger()
                break
        else:
            self.safe()

    def danger(self):
        """Ativador do estado de alerta"""

        if self.state != 'alert':
            self.state = 'alert'
            handler.danger()
            cli.clear()
            cli.interactive_header()
            cli.prompt()

    def safe(self):
        """Ativador do estado de segurança"""

        if self.state == 'alert':
            self.state = 'safe'
            handler.safe()
            cli.clear()
            cli.interactive_header()
            cli.prompt()

    def kill(self):
        """Termina a thread"""

        self.die = True

    def run(self):
        try:
            pythoncom.CoInitialize()
            self.wmi = WMI()

            while not self.die:
                self.check_memory()
                time.sleep(1.0 / config.get("frequency"))

            pythoncom.CoUninitialize()

        except RuntimeError as ex:
            log.error('memory_checker_thread', ex)
