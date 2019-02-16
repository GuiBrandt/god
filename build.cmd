@echo off

echo Resolvendo dependˆncias...
pip install --upgrade -r requirements.txt 2>nul
if ERRORLEVEL 1 goto failed_deps
echo.
echo OK.
echo.

echo Procurando pyinstaller...
pip install --upgrade pyinstaller 2>nul
if ERRORLEVEL 1 goto failed_pyinstaller
echo.
echo OK.
echo.

<NUL set /p=Compilando... 
pyinstaller --onefile -n god -i god.ico --add-data %PY_HOME%/Lib/site-packages/pyfiglet;./pyfiglet __main__.py god\__init__.py god\cli.py 2>nul
if ERRORLEVEL 1 goto failed_build
echo OK.

goto end

:failed_deps
    echo.
    echo Falha ao obter dependˆncias. Abortando...
    goto end

:failed_pyinstaller
    echo.
    echo NÆo foi poss¡vel localizar o pyinstaller, tem certeza que vocˆ tem Python instalado?
    goto end

:failed_build
    echo.
    echo NÆo foi poss¡vel compilar o God, tenha certeza de que configurou o ambiente corretamente, caso o problema persista, abra uma Issue no github! (https://github.com/GuiBrandt/god)
    goto end

:end
