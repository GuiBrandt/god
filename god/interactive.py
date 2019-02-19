import re
import sys

import god
import god.version as version
import god.cli as cli
import god.log as log
import god.config as config

from colorama import Fore, Style


def no_arg(cmd_func):
    def func_wrapper(*args):
        if len(args) > 1:
            cli.error("\tNão esperava parâmetros, mas OK.")
        return cmd_func(*args)
    return func_wrapper


def require_arg(cmd_func):
    def func_wrapper(*args):
        if len(args) != 1:
            cli.error("\tSintaxe incorreta. Veja `help`.")
            return None
        else:
            return cmd_func(*args)
    return func_wrapper


def numeric(cmd_func):
    def func_wrapper(*args):
        if not args[0].isnumeric():
            cli.error("\tEsperava um número. Veja `help`.")
            return None
        else:
            return cmd_func(int(args[0]))
    return func_wrapper


@no_arg
def cmd_quit():
    god.stop()
    sys.exit(0)


@no_arg
def cmd_help():
    print(Fore.YELLOW + f"""
    GOD {version.current()}, by PD16

    sm|threshold X      : Define o limite de memória para X Kb
    sp|process X        : Define o processo monitorado para X
    sf|frequency X      : Define a frequência de atualização para X Hz
    ss|save             : Salva as configurações
    cc|clear            : Limpa a tela
    h|help              : Mostra a ajuda
    q|quit|exit         : Sai do programa
    """)


@no_arg
def cmd_save():
    config.save()


@no_arg
def cmd_clear():
    cli.clear()
    cli.interactive_header()


@require_arg
@numeric
def cmd_threshold(value):
    config.set('threshold', value)
    cli.print_settings()


@require_arg
@numeric
def cmd_frequency(value):
    config.set('frequency', value)
    cli.print_settings()


@require_arg
def cmd_process(*parts):
    psname = ' '.join(parts)
    if not psname.endswith(".exe"):
        psname += ".exe"
    config.set('psname', psname)
    cli.print_settings()


_COMMAND_MAP = {
    ('q', 'quit', 'exit'): cmd_quit,
    ('h', 'help'): cmd_help,
    ('ss', 'save'): cmd_save,
    ('cc', 'clear'): cmd_clear,
    ('sm', 'threshold'): cmd_threshold,
    ('sf', 'frequency'): cmd_frequency,
    ('sp', 'process'): cmd_process
}


def run():
    try:
        while True:
            line = cli.read_command()
            parts = re.split(r"\s+", line)
            command = parts[0].lower()

            for alternatives in _COMMAND_MAP.keys():
                if command in alternatives:
                    _COMMAND_MAP[alternatives](*parts[1:])
                    break
            else:
                cli.error(
                    f"\tComando não reconhecido `{command}`. Veja `help`.")
    except Exception as e:
        log.error("interactive", e)
