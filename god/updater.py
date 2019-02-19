import requests
import zipfile
import tempfile
import urllib.request
import io
import os
import sys
import os.path
import glob

from shutil import copyfile

import god.cli as cli
import god.log as log

_GITHUB_API_URL = "https://api.github.com"
_REPO = "/repos/GuiBrandt/god"


def fetch_latest_release():
    r = requests.get(_GITHUB_API_URL + _REPO + "/releases/latest")
    print(r.headers["X-RateLimit-Remaining"])
    return r.json()


def fetch_zip(release):
    zip_url = release['zipball_url']
    r = requests.get(zip_url, stream=True)
    zip_file = zipfile.ZipFile(io.BytesIO(r.content))
    return zip_file


def check_updates():
    cli.i_am("Procurando atualizações...")
    latest_release = fetch_latest_release()

    cli.info("Encontrado: " + latest_release['tag_name'])

    while True:
        answer = input("\tAtualizar? [Y/n] ").lower().strip()
        if answer in ['y', '', 'n']:
            break

    cli.newline()

    if not answer.lower().strip() in ['y', '']:
        return

    cli.i_am("Obtendo arquivo zip...")
    release_zip_file = fetch_zip(latest_release)
    cli.success("OK")

    tmp_dir = tempfile.mkdtemp()

    cli.i_am("Extraindo...")
    root_dir = release_zip_file.namelist()[0]
    release_zip_file.extractall(path=tmp_dir)
    cli.success("OK")

    tmp_dir = f"{tmp_dir}/{root_dir}".replace("\\", "/")

    cli.i_am("Instalando dependências...")
    requirements_file = f"{tmp_dir}/requirements.txt"
    result = os.system(
        f"pip install --upgrade -r \"{requirements_file}\" >nul 2>nul")

    if result == 0:
        cli.success("OK")
    else:
        cli.error("Falha na instalação. Abortando atualização...")
        log.error("update", "Falha na instação das dependências")
        return

    cli.i_am("Updating source files...")
    main_file = f"{tmp_dir}/__main__.py"
    source_files = glob.glob(f"{tmp_dir}/**/*.py")

    for f in source_files:
        path = ".update/" + \
            os.path.dirname(f).replace("\\", "/").replace(tmp_dir, '')
        if not os.path.isdir(path):
            os.makedirs(path)

    copyfile(main_file, f".update/__main__.py")

    for f in source_files:
        path = os.path.dirname(f).replace("\\", "/").replace(tmp_dir, '')
        copyfile(f, f".update/{path}/{os.path.basename(f)}")
    cli.success("OK")

    os.system("start python apply_update.py")
    sys.exit(0)
