"""Gerenciador de citações

Esse módulo carrega frases e autores aleatórios da internet ou do
arquivo local e permite sortear uma combinação frase-autor

"""

import random
import yaml

_NICE_PHRASES = []
_INCREDIBLE_AUTHORS = []


def load_inet():
    """Carrega frases e autores aleatórios da internet

    TODO: Implementar!!!

    Retorno
    -------
    Número de combinações possíveis obtidas

    """

    print("Frases da internet ainda não estão disponíveis.", end=' ')
    return load_local()


def load_local():
    """Carrega frases e autores aleatórios do arquivo local

    Retorno
    -------
    Número de combinações possíveis obtidas

    """

    with open('phrases.yml', 'r', encoding='utf-8') as phrases_file:
        phrases_yml = yaml.load(phrases_file)
        _NICE_PHRASES.extend(phrases_yml['phrases'])
        _INCREDIBLE_AUTHORS.extend(phrases_yml['authors'])

    return len(_NICE_PHRASES) * len(_INCREDIBLE_AUTHORS)


def get_random():
    """Sorteia uma frase e um autor

    Retorno
    -------
    Uma tupla (frase, autor)

    """

    phrase = random.choice(_NICE_PHRASES)
    author = random.choice(_INCREDIBLE_AUTHORS)

    return phrase, author
