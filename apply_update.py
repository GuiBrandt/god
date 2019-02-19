"""Aplica a última atualização baixada

Esse arquivo é basicamente um `.cmd` glorificado
"""

import os
import os.path

if os.path.isdir(".update"):
    # Atualiza tudo da pasta raíz
    os.system("move /Y .update\\*.* .\\ >nul 2>nul")

    # Cria e atualiza cada uma das subpastas necessárias
    for subdir in os.walk(".update"):
        dirname = subdir[0].replace(".update\\", '')

        os.system(
            f"if not exist .\\{dirname}" +
            f" mkdir .\\{dirname} >nul 2>nul")

        os.system(
            f"move /Y .update\\{dirname}\\*.* .\\{dirname}\\ " +
            ">nul 2>nul")

# Apaga a .update (agora vazia)
os.system("rmdir .update /s /q >nul 2>nul")

# Roda o god
os.system("start python .")
