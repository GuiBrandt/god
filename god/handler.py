"""Gerenciador de estado e ações do God

Esse módulo tem funções para executar as instruções de alerta e
segurança do God e atualizar o estado do programa

"""

import os

import yaml
import win32con
from wmi import WMI

import win32process

import god
import god.cli as cli
import god.log as log


def flashbang_notepad():
    """Joga um bloco de notas maximizado na tela

    TODO: Opção de abrir um arquivo nesse bloco de notas

    """

    start_info = win32process.STARTUPINFO()
    start_info.dwFlags = win32con.STARTF_USESHOWWINDOW
    start_info.wShowWindow = win32con.SW_MAXIMIZE
    win32process.CreateProcess(
        None,
        "notepad",
        None,
        None,
        False,
        0,
        None,
        None,
        start_info
    )


def kill_processes(process_list):
    """Mata todos os processos listados por nome

    Parâmetros
    ----------
    process_list : list
        Lista de nomes de processos a serem terminados

    """

    wmi = WMI()
    for process_name in process_list:
        if not process_name.endswith(".exe"):
            process_name += ".exe"

        for process in wmi.Win32_Process(Name=process_name):
            os.kill(process.ProcessId, 9)


def danger():
    """Sinaliza uso de memória elevado e toma as ações necessárias

    Nota
    ----
    Esse método altera o estado do programa para `alert`

    Em caso de falha ao executar as instruções de alerta, usa-se um
    bloco de notas "flashbang" como medida provisória.

    """

    god.state = 'alert'

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

    except RuntimeError as ex:
        log.error("on_danger", ex)
        cli.error("OH GOD OH FUCK, I CAN'T RUN THE INSTRUCTIONS!!!!1!!1!!!")
        cli.error("Flashbang it is, then.")
        flashbang_notepad()


def safe():
    """Sinaliza uso de memória regular e executa as ações estipuladas

    TODO: Mensagem de aviso (de preferência opcional)

    Nota
    ----
    Esse método altera o estado do programa para `safe`

    """

    god.state = 'safe'

    try:
        with open('safe.yml', 'r') as safe_file:
            safe_yml = yaml.load(safe_file)

            if 'cmd' in safe_yml and safe_yml['cmd']:
                for pname in safe_yml['cmd']:
                    os.system(pname)

    except RuntimeError as ex:
        log.error("on_safe", ex)
        cli.info("Hmmmmm, não consigo rodar essas instruções aqui...")
