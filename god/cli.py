import os

import god
import god.config as config
import god.quotes as quotes

from colorama import init as color_init, Fore
from pyfiglet import Figlet

_LIST_ITEM_MARKER = "~>"
_in_list = False


color_init(autoreset=True)


def width():
    return os.get_terminal_size().columns


def newline():
    print()


def header(color=Fore.BLUE):
    f = Figlet(font='alligator2', justify='center', width=width())
    newline()
    print(color + f.renderText('G o d'))
    newline()
    print(color + "v2.0.0".center(width()))
    print(flush=True)


def print_random_phrase():
    phrase, author = quotes.get_random()
    text = ('"{}" ~ {}').format(phrase, author)
    print(Fore.YELLOW + text.center(width()))
    print(flush=True)


def print_settings():
    for key in config.DEFAULTS.keys():
        value = config.get(key)
        print("\t", key, Fore.CYAN + ':' + Fore.RESET, " \t", value, sep='')
    print(flush=True)


def log():
    pass


def i_am(doing):
    if _in_list:
        print("\t", Fore.CYAN + _LIST_ITEM_MARKER + Fore.RESET, end=' ')
    print(Fore.YELLOW + doing, end=' ', flush=True)


def success(text):
    print(Fore.GREEN + text, flush=True)


def error(text):
    print(Fore.RED + text, flush=True)


def warning(text):
    print(Fore.YELLOW + text, flush=True)


def info(text):
    print(Fore.BLUE + text, flush=True)


def list_begin():
    global _in_list
    _in_list = True


def list_end():
    global _in_list
    _in_list = False
    newline()


def clear():
    os.system("cls || clear")


def prompt():
    print(Fore.CYAN + ">", end=' ')


def read_command():
    prompt()
    return input().strip()


def interactive_header():
    header(Fore.RED if god.state == 'alert' else Fore.BLUE)
    print_random_phrase()

    if god.state == 'alert':
        warning("Run, berg! Run!".center(width()))
        newline()
    elif god.state == 'safe':
        success("Back to business...".center(width()))
        newline()

    print_settings()
