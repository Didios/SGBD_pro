from cx_Freeze import setup, Executable

executables = [
        Executable(script = "SGBD_DGourmandises.py", icon = "images/icone.ico", base = "Win32GUI")
]

buildOptions = dict(
        includes = ["tkinter","tkinter.messagebox","datetime","module_lecture_fichier.py","module_database.py","sqlite3","os"],
        include_files = ["images", "base_de_donnees","data","__pycache__"]
)

setup(
    name = "SGBD DGourmandises",
    version = "1.6",
    description = "Systeme de Gestion de Base de Données conçu pour la société DGourmandises",
    author = "Didier Mathias",
    options = dict(build_exe = buildOptions),
    executables = executables
)