@echo off
pyinstaller --onefile -n god -i god.ico --add-data %PY_HOME%/Lib/site-packages/pyfiglet;./pyfiglet __main__.py god\__init__.py god\cli.py
pause