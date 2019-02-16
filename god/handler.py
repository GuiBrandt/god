import os
import yaml
import win32process
import win32con

import god.cli as cli
import god.log as log

from wmi import WMI


def flashbang_notepad():
    si = win32process.STARTUPINFO()
    si.dwFlags = win32con.STARTF_USESHOWWINDOW
    si.wShowWindow = win32con.SW_MAXIMIZE
    win32process.CreateProcess(
        None,
        "notepad",
        None,
        None,
        False,
        0,
        None,
        None,
        si
    )


def kill_processes(list):
    wmi = WMI()
    for process_name in list:
        if not process_name.endswith(".exe"):
            process_name += ".exe"

        for process in wmi.Win32_Process(Name=process_name):
            process.Terminate(1)


def danger():
    try:
        with open('danger.yml', 'r') as danger_file:
            danger_yml = yaml.load(danger_file)

            if 'flashbang' in danger_yml and danger_yml['flashbang']:
                flashbang_notepad()

            if 'kill' in danger_yml and danger_yml['kill']:
                kill_processes(danger_yml['kill'])

            if 'cmd' in danger_yml and danger_yml['cmd']:
                for pname in danger_yml['cmd']:
                    os.system(pname)

    except Exception as e:
        log.error("on_danger", e)
        cli.error("OH GOD OH FUCK, I CAN'T RUN THE INSTRUCTIONS!!!!1!!1!!!")
        cli.error("Flashbang it is, then.")
        flashbang_notepad()


def safe():
    try:
        with open('safe.yml', 'r') as safe_file:
            safe_yml = yaml.load(safe_file)

            if 'cmd' in safe_yml and safe_yml['cmd']:
                for pname in safe_yml['cmd']:
                    os.system(pname)

    except Exception as e:
        log.error("on_safe", e)
        cli.info("Hmmmmm, não tem instruções aqui...")
