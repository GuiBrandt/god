import os

if os.path.isdir(".update"):
    os.system("move .update\\*.* .\\ >nul 2>nul")

    for subdir in os.walk(".update"):
        dirname = subdir[0].replace(".update\\", '')
        os.system(
            f"if not exist .\\{dirname}" +
            f" mkdir .\\{dirname} >nul 2>nul")
        os.system(
            f"move .update\\{dirname}\\*.* .\\{dirname}\\ " +
            ">nul 2>nul")

os.system("rmdir .update /s /q >nul 2>nul")
os.system("start python .")
