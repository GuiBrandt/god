"""Gerenciador do modo interativo do God

Esse módulo é responsável pelo loop de comandos que fica disponível
enquanto o God monitora a memória em segundo plano

"""

import re
import sys
from functools import wraps

from colorama import Fore

import god
import god.version as version
import god.cli as cli
import god.log as log
import god.config as config


def run():
    """Executa o loop de comandos interativos

    Nota
    ----
    Esse método trava a execução até o usuário lançar um comando `quit`

    """

    try:
        while True:
            line = cli.read_command()
            parts = re.split(r"\s+", line)
            command = parts[0].lower()

            for alternatives in _COMMAND_MAP:
                if command in alternatives:
                    _COMMAND_MAP[alternatives](*parts[1:])
                    break
            else:
                cli.error(
                    f"\tComando não reconhecido: `{command}`. Veja `help`.")
    except RuntimeError as ex:
        log.error("interactive", ex)


def no_arg(cmd_func):
    """Wrapper para comandos sem parâmetro"""

    @wraps(cmd_func)
    def func_wrapper(*args):
        if len(args) > 1:
            cli.error("\tNão esperava parâmetros, mas OK.")
        return cmd_func(*args)
    return func_wrapper


def require_arg(cmd_func):
    """Wrapper para comandos com parâmetro"""

    @wraps(cmd_func)
    def func_wrapper(*args):
        if len(args) != 1:
            cli.error("\tSintaxe incorreta. Veja `help`.")
            return None
        return cmd_func(*args)
    return func_wrapper


def numeric(cmd_func):
    """Wrapper para comandos com parâmetro numérico"""

    @wraps(cmd_func)
    def func_wrapper(*args):
        if not args[0].isnumeric():
            cli.error("\tEsperava um número. Veja `help`.")
            return None
        return cmd_func(int(args[0]))
    return func_wrapper


@no_arg
def cmd_quit():
    """Fecha o God"""

    god.stop()
    sys.exit(0)


@no_arg
def cmd_help():
    """Mostra ajuda para os comandos do God"""

    def _syntax(command):
        options, method = command
        return ("|".join(options)).ljust(30) + " : " + method.__doc__

    commands_help = "\r\n\t".join(map(_syntax, _COMMAND_MAP.items()))

    print(Fore.YELLOW + f"""
    GOD {version.current()}

        {commands_help}
    """)


@no_arg
def cmd_save():
    """Salva as configurações"""

    config.save()


@no_arg
def cmd_load():
    """Carrega as configurações"""
    config.load()


@no_arg
def cmd_clear():
    """Limpa a tela"""

    cli.clear()
    cli.interactive_header()


@require_arg
@numeric
def cmd_threshold(value):
    """Define o limite de memória para X Kb"""

    config.set('threshold', value)
    cli.print_settings()


@require_arg
@numeric
def cmd_frequency(value):
    """Define a frequência de atualização para X Hz"""
    config.set('frequency', value)
    cli.print_settings()


@require_arg
def cmd_process(*parts):
    """Define o processo monitorado para X"""

    psname = ' '.join(parts)
    if not psname.endswith(".exe"):
        psname += ".exe"
    config.set('psname', psname)
    cli.print_settings()


@require_arg
def cmd_flashbang(*parts):
    """Define o arquivo de flashbang"""

    fname = ' '.join(parts)
    config.set('flashbang_file', fname)
    cli.print_settings()


_COMMAND_MAP = {
    ('h', 'help'): cmd_help,
    ('cc', 'cls', 'clear'): cmd_clear,
    ('sm', 'threshold'): cmd_threshold,
    ('sf', 'frequency'): cmd_frequency,
    ('sp', 'process'): cmd_process,
    ('fb', 'flashbang'): cmd_flashbang,
    ('ss', 'save'): cmd_save,
    ('ls', 'load'): cmd_load,
    ('q', 'quit', 'exit'): cmd_quit,
}
