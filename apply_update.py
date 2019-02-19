"""Aplica a última atualização baixada

TODO: Implementar remoção de arquivos não utilizados"""

import os
import os.path

if os.path.isdir(".update"):

    # Atualiza a pasta raíz
    os.system("move /Y .update\\*.* .\\ >nul 2>nul")

    # Cria e atualiza os subdiretórios
    for subdir in os.walk(".update"):
        dirname = subdir[0].replace(".update\\", '')

        os.system(
            f"if not exist .\\{dirname}" +
            f" mkdir .\\{dirname} >nul 2>nul")

        os.system(
            f"move /Y .update\\{dirname}\\*.* .\\{dirname}\\ " +
            ">nul 2>nul")

# Some com a .update
os.system("rmdir .update /s /q >nul 2>nul")

# Roda o god de novo
os.system("start python .")
