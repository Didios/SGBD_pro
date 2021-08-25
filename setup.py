from cx_Freeze import setup, Executable

executables = [
        Executable(script = "main.py", icon = "images/icone.ico", base = "Win32GUI")
]

buildOptions = dict(
        includes = ["tkinter","tkinter.messagebox","datetime","module_lecture_fichier.py","module_database.py","sqlite3","mariadb","os"],
        include_files = ["images", "base_de_donnees","preferences.txt"]
)

setup(
    name = "SGBD DGourmandises",
    version = "1.5",
    description = "Systeme de Gestion de Base de Données conçu pour la société DGourmandises",
    author = "Didier Mathias",
    options = dict(build_exe = buildOptions),
    executables = executables
)