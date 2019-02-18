import threading
import pythoncom
import time
import yaml

import god.cli as cli
import god.log as log
import god.config as config
import god.handler as handler

from wmi import WMI
from enum import Enum, auto


class GodState(Enum):
    IDLE = 'idle'
    SAFE = 'safe'
    ALERT = 'alert'


class Thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.die = False
        self.state = GodState.IDLE

    def check_memory(self):
        processes = self.wmi.Win32_Process(Name=config.get("psname"))
        for process in processes:
            working_set = int(process.WorkingSetSize)
            if working_set / 1024 >= config.get("threshold"):
                self.danger()
                break
        else:
            self.safe()

    def danger(self):
        if self.state != GodState.ALERT:
            self.state = GodState.ALERT
            handler.danger()
            cli.clear()
            cli.interactive_header()
            cli.prompt()

    def safe(self):
        if self.state == GodState.ALERT:
            self.state = GodState.SAFE
            handler.safe()
            cli.clear()
            cli.interactive_header()
            cli.prompt()

    def kill(self):
        self.die = True

    def run(self):
        try:
            pythoncom.CoInitialize()
            self.wmi = WMI()

            while not self.die:
                self.check_memory()
                time.sleep(1.0 / config.get("frequency"))

            pythoncom.CoUninitialize()

        except Exception as e:
            log.error('memory_checker_thread', e)
