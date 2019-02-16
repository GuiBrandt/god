import yaml
import random

_nice_phrases = []
_incredible_authors = []


def load_inet():
    print("Frases da internet ainda não estão disponíveis.", end=' ')
    return load_local()


def load_local():
    global _nice_phrases, _incredible_authors

    with open('phrases.yml', 'r', encoding='utf-8') as phrases_file:
        phrases_yml = yaml.load(phrases_file)
        _nice_phrases = phrases_yml['phrases']
        _incredible_authors = phrases_yml['authors']

    return len(_nice_phrases) * len(_incredible_authors)


def get_random():
    phrase = random.choice(_nice_phrases)
    author = random.choice(_incredible_authors)

    return phrase, author
