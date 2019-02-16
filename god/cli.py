import os

import god
import god.config as config
import god.quotes as quotes

from termcolor import colored, cprint
from pyfiglet import Figlet

_LIST_ITEM_MARKER = "~>"
_in_list = False


def width():
    return os.get_terminal_size().columns


def header(color='blue'):
    f = Figlet(font='alligator2', justify='center', width=width())
    print()
    print(colored(f.renderText('G o d'), color))
    print()
    print(colored("v2.0.0".center(width()), color))
    print(flush=True)


def print_random_phrase():
    phrase, author = quotes.get_random()
    text = ('"{}" ~ {}').format(phrase, author)
    cprint(text.center(width()), 'yellow')
    print(flush=True)


def print_settings():
    for key in config.DEFAULTS.keys():
        value = config.get(key)
        print("\t", key, colored(':', 'cyan'), " \t", value, sep='')
    print(flush=True)


def log():
    pass


def i_am(doing):
    if _in_list:
        print("\t", colored(_LIST_ITEM_MARKER, 'cyan'), end=' ')
    print(colored(doing, 'yellow'), end=' ', flush=True)


def success(text):
    print(colored(text, 'green'), flush=True)


def error(text):
    print(colored(text, 'red'), flush=True)


def warning(text):
    print(colored(text, 'yellow'), flush=True)


def info(text):
    print(colored(text, 'blue'), flush=True)


def list_begin():
    global _in_list
    _in_list = True


def list_end():
    global _in_list
    _in_list = False
    print()


def clear():
    os.system("cls || clear")


def interactive_header():
    header()
    print_random_phrase()
    print_settings()
