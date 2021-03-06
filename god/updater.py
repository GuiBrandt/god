"""Gerenciador de atualização

Esse módulo faz o pareamento com a última versão disponível no GitHub,
e faz a atualização de forma automática.

"""

import io
import os
import sys
import zipfile
import tempfile
import glob
from shutil import copyfile

import requests

import god.cli as cli
import god.gui as gui
import god.log as log
import god.version as version

# Informações do GitHub
_GITHUB_API_URL = "https://api.github.com"
_REPO = "GuiBrandt/god"


def check_updates():
    """Executa o procedimento de busca e instalação de atualizações"""

    cli.i_am("Procurando atualizações...")

    try:
        latest_release = _fetch_latest_release()
    except RuntimeError as ex:
        gui.error("Falha na atualização." +
                  "Verifique sua conexão com a internet.")
        log.error("fetch-releases", ex)
        return

    cli.info("Encontrado: " + latest_release['tag_name'])

    if latest_release['tag_name'] == version.current():
        cli.success("O god está atualizado.")
        return

    cli.error("O god está desatualizado!")

    if _confirm(latest_release):
        update_dir = _download_update(latest_release)
        _install_update(update_dir)

        version.set_tag(latest_release['tag_name'])

        with open(".version", "w") as version_file:
            version_file.write(version.current())

        os.system("start python apply_update.py")
        sys.exit(0)
    else:
        cli.warning("Ignorando atualização. " +
                    "Cuidado, isso geralmente dá ruim.")


def _fetch_latest_release():
    """Obtém informações da última release no GitHub em JSON"""

    res = requests.get(f"{_GITHUB_API_URL}/repos/{_REPO}/releases/latest")
    return res.json()


def _download_update(release):
    """Faz download e extrai o zip de uma release

    Parâmetros
    ----------
    release : json
        JSON da release, retornado pelo `_fetch_latest_release`

    Retorno
    -------
    O caminho da pasta com os arquivos do `.zip` extraídos

    """

    cli.i_am("Obtendo arquivo zip...")
    zip_url = release['zipball_url']
    res = requests.get(zip_url, stream=True)
    release_zip_file = zipfile.ZipFile(io.BytesIO(res.content))
    cli.success("OK")

    cli.i_am("Extraindo...")
    tmp_dir = tempfile.mkdtemp()
    root_dir = release_zip_file.namelist()[0]
    release_zip_file.extractall(path=tmp_dir)
    cli.success("OK")

    tmp_dir = f"{tmp_dir}/{root_dir}".replace("\\", "/")

    return tmp_dir


def _confirm(latest_release):
    """Faz a confirmação de atualização via janela de mensagem"""

    return gui.confirm(
        f"Versão atual: {version.current()}\r\n" +
        f"Versão encontrada: {latest_release['tag_name']}\r\n" +
        "\r\n" +
        "Changelog\r\n" +
        "--------------\r\n" +
        latest_release['body'] + "\r\n" +
        "\r\n" +
        "Atualizar?",
        title="Atualização disponível")


def _install_update(update_dir):
    """Faz a instalação de uma atualização

    Isso envolve resolver dependências com pip e mover os arquivos
    baixados para suas respectivas pastas.

    """

    cli.i_am("Instalando dependências...")
    requirements_file = f"{update_dir}/requirements.txt"
    result = os.system(
        f"pip install --upgrade -r \"{requirements_file}\" >nul 2>nul")

    if result == 0:
        cli.success("OK")
    else:
        gui.error("Falha na instalação. Abortando atualização...\r\n" +
                  "\r\n" +
                  "Veja o arquivo `error.log' para mais informações.")
        log.error("update", "Falha na instação das dependências")
        return

    cli.i_am("Atualizando código fonte...")
    sources = _map_update_sources(update_dir)
    _touch_directories(sources)

    for fname, dirname in sources:
        path = fname if dirname == '.' else f"{dirname}/{fname}"
        copyfile(f"{update_dir}/{path}", f".update/{path}")

    # O arquivo apply_update.py é especial: ele não pode atualizar ele
    # mesmo
    os.system("move /Y .update\\apply_update.py .")

    cli.success("OK")


def _map_update_sources(update_dir):
    """Mapeia o índice de uma atualização em um formato mais usável

    Parâmetros
    ----------
    update_dir : str
        Caminho da pasta onde os arquivos da atualização estão

    Retorno
    -------
    Lista de tuplas com o nome dos arquivos (sem pasta) e o nome da
    pasta onde devem ser colocados (relativo à pasta raíz do god)

    """

    files = glob.glob(f"{update_dir}/**/*.py", recursive=True)
    directories = map(os.path.dirname, files)

    def strip_update_dir(dirname):
        if dirname in update_dir:  # Na prática, se é o diretório raíz
            return '.'
        return dirname.replace("\\", "/").replace(update_dir, '')

    directories = map(strip_update_dir, directories)

    return list(zip(map(os.path.basename, files), directories))


def _touch_directories(sources):
    """Cria os diretórios para salvar os arquivos da atualização"""

    for _, dirname in sources:
        path = f".update/{dirname}"
        if not os.path.isdir(path):
            os.makedirs(path)
