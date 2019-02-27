"""Gerenciador de interface do usuário

Esse módulo tem funções para gerenciar a interface com o usuário, incluindo CLI
e GUI.

"""

import win32con
import win32console
from win32gui import MessageBox


def confirm(text, title="God"):
    """Pede confirmação para o usuário na forma de popup

    Parâmetros
    ----------
    text : str
        Texto da caixa de mensagem

    title : str
        Título da caixa de mensagem (Padrão: God)


    Retorno
    -------
    True caso o usuário confirme, False se não

    """

    res = MessageBox(win32console.GetConsoleWindow(),
                     text, title,
                     win32con.MB_YESNO | win32con.MB_ICONINFORMATION)
    return res == win32con.IDYES


def info(text, title="God"):
    """Mostra uma caixa de mensagem de informação

    Parâmetros
    ----------
    text : str
        Texto da caixa de mensagem

    title : str
        Título da caixa de mensagem (Padrão: God)

    """

    MessageBox(win32console.GetConsoleWindow(),
               text, title,
               win32con.MB_OK | win32con.MB_ICONINFORMATION)


def error(text, title="God"):
    """Mostra uma caixa de mensagem de erro

    Parâmetros
    ----------
    text : str
        Texto da caixa de mensagem

    title : str
        Título da caixa de mensagem (Padrão: God)

    """

    MessageBox(win32console.GetConsoleWindow(),
               text, title,
               win32con.MB_OK | win32con.MB_ICONERROR)


def warning(text, title="God"):
    """Mostra uma caixa de mensagem de aviso

    Parâmetros
    ----------
    text : str
        Texto da caixa de mensagem

    title : str
        Título da caixa de mensagem (Padrão: God)

    """

    MessageBox(win32console.GetConsoleWindow(),
               text, title,
               win32con.MB_OK | win32con.MB_ICONWARNING)
