import time

import god
import god.interactive
import god.cli as cli
import god.log as log
import god.quotes as quotes
import god.config as config
import god.version as version


def load_settings():
    cli.i_am("Carregando configurações...")
    config.load()
    cli.success("OK")
    cli.print_settings()


def use_inet_phrases():
    cli.i_am("Pegando umas frases aleatórias...")
    try:
        n = quotes.load_inet()
        cli.success("{} frases".format(n))
    except:
        cli.error("Falhou :(")
        use_stored_phrases()


def use_stored_phrases():
    cli.i_am("Usando frases aleatórias locais...")
    n = quotes.load_local()
    cli.success("Got {} phrases".format(n))


def load_phrases():
    cli.i_am("Checando conexão com a internet...")

    if god.check_internet():
        cli.success("OK")
        cli.list_begin()
        use_inet_phrases()
        cli.list_end()
    else:
        cli.error("Internet indisponível")
        cli.list_begin()
        use_stored_phrases()
        cli.list_end()


def main():
    cli.clear()
    cli.header()

    version.check_updates()
    load_settings()
    load_phrases()

    cli.success("Pronto.")
    print()
    cli.i_am("Iniciando ambiente interativo. Se divirta!")
    time.sleep(2)

    cli.clear()
    cli.interactive_header()

    god.start()
    god.interactive.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error("main", e)
