@echo off

echo Resolvendo dependências...
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

echo Compilando... 
pyinstaller --onefile -n god -i god.ico --upx-dir %LocalAppData%/upx-3.95-win64 --add-data ./fonts;./pyfiglet/fonts god\__main__.py
if ERRORLEVEL 1 goto failed_build
echo OK.

goto end

:failed_deps
    echo.
    echo Falha ao obter dependências. Abortando...
    goto end

:failed_pyinstaller
    echo.
    echo Não foi possível localizar o pyinstaller, tem certeza que você tem Python instalado?
    goto end

:failed_build
    echo.
    echo Não foi possível compilar o God, tenha certeza de que configurou o ambiente corretamente, caso o problema persista, abra uma Issue no github (https://github.com/GuiBrandt/god)
    goto end

:end
