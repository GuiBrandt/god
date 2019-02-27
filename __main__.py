"""GOD - Monitorador de uso de memória e tudo mais"""

import time

import god
import god.interactive
import god.cli as cli
import god.log as log
import god.version as version
import god.quotes as quotes
import god.config as config
import god.updater as updater


def load_settings():
    """Carrega as configurações do programa"""

    cli.i_am("Carregando configurações...")
    config.load()
    cli.success("OK")
    cli.print_settings()


def use_inet_phrases():
    """Tenta usar frases e autores da internet, se falha usa os locais"""

    cli.i_am("Pegando umas frases aleatórias...")
    try:
        amount = quotes.load_inet()
        cli.success("{} frases".format(amount))
    except RuntimeError:
        cli.error("Falhou :(")
        use_stored_phrases()


def use_stored_phrases():
    """Carrega frases e autores locais para citações"""

    cli.i_am("Usando frases aleatórias locais...")
    amount = quotes.load_local()
    cli.success("Got {} phrases".format(amount))


def load_phrases():
    """Carrega informações para citações da fonte mais adequada"""

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
    """Procedimento principal"""

    cli.title(f"God {version.current()}")
    cli.clear()
    cli.header()

    updater.check_updates()
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
    except RuntimeError as ex:
        log.error("main", ex)
