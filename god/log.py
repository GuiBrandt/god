"""Gerenciador de log

Esse módulo cria e alimenta arquivos de log
"""

import time


def error(location, exception):
    """Cria um log de erro no arquivo `error.log`

    Parâmetros
    ----------
    location : str
        Localização do erro no código. Deve ser uma tag que facilite
        procurar o local do erro

    exception : Exception
        Exceção lançada no código

    Exemplo
    -------

        ```
            try:
                # Código explosivo
            except Exception as e:
                god.log.error("example", e)
        ```

    """

    with open("error.log", "a") as log_file:
        timestamp = time.ctime(time.time())
        log_file.write(f"<{timestamp} at `{location}`> {exception}\n")
