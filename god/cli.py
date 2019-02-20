"""Gerenciador da CLI

Esse módulo tem métodos usados para isolar a lógica de CLI do resto do
programa

"""

import os

from colorama import Fore
from colorama import init as color_init
from pyfiglet import Figlet

import god
import god.config as config
import god.quotes as quotes
from god.version import current as version

_LIST_ITEM_MARKER = "~>"
_INT_LIST = False


color_init(autoreset=True)


def width():
    """Obtém a largura da janela do terminal"""

    return os.get_terminal_size().columns


def newline():
    """Printa uma linha em branco"""

    print()


def header(color=Fore.BLUE):
    """Printa o cabeçalho do God"""

    f = Figlet(font='alligator2', justify='center', width=width())
    newline()
    print(color + f.renderText('G o d'))
    newline()
    print(color + version().center(width()))
    print(flush=True)


def print_random_phrase():
    """Printa uma citação sorteada"""

    phrase, author = quotes.get_random()
    text = ('"{}" ~ {}').format(phrase, author)
    print(Fore.YELLOW + text.center(width()))
    print(flush=True)


def print_settings():
    """Printa as configurações"""

    for key in config.keys():
        value = config.get(key)
        print("\t", key, Fore.CYAN + ':' + Fore.RESET, " \t", value, sep='')
    print(flush=True)


def i_am(doing):
    """Escreve uma mensagem  de indicador de ação"""

    if _INT_LIST:
        print("\t", Fore.CYAN + _LIST_ITEM_MARKER + Fore.RESET, end=' ')
    print(Fore.YELLOW + doing, end=' ', flush=True)


def success(text):
    """Escreve uma mensagem de sucesso"""

    print(Fore.GREEN + text, flush=True)


def error(text):
    """Escreve uma mensagem de erro"""

    print(Fore.RED + text, flush=True)


def warning(text):
    """Escreve uma mensagem de aviso"""

    print(Fore.YELLOW + text, flush=True)


def info(text):
    """Escreve uma mensagem de informação"""

    print(Fore.BLUE + text, flush=True)


def list_begin():
    """Entra no modo de listagem"""

    global _INT_LIST
    _INT_LIST = True


def list_end():
    """Termina o modo de listagem"""

    global _INT_LIST
    _INT_LIST = False
    newline()


def clear():
    """Limpa a tela do terminal"""

    os.system("cls || clear")


def prompt():
    """Escreve um prompt de entrada de comando para o usuário"""

    print(Fore.CYAN + ">", end=' ')


def read_command():
    """Lê um comando da entrada padrão"""

    prompt()
    return input().strip()


def yesno(prompt="Confirmar?"):
    """Faz uma confirmação de Sim/Não"""

    while True:
        answer = input(f"\t{prompt} [S/n] ").lower().strip()
        if answer in ['s', '', 'n']:
            break

    newline()
    return answer.lower().strip() in ['s', '']


def interactive_header():
    """Printa um cabeçalho para o modo interativo"""

    header(Fore.RED if god.state == 'alert' else Fore.BLUE)
    print_random_phrase()

    if god.state == 'alert':
        warning("Run, berg! Run!".center(width()))
        newline()
    elif god.state == 'safe':
        success("Back to business...".center(width()))
        newline()

    print_settings()
