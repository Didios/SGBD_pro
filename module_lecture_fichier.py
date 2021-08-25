#!"C:\Winpython\python-3.8.5.amd64\python.exe"

# module permettant la lecture, la modification et l'analyse de fichier/répertoire
# fait par Didier Mathias

# importation des modules necessaires
import os
import os.path


def devine_numero(texte):
        """
        sous-fonction permettant d'isoler les nombre présent dans une chaine de caracteres, les nombres décimaux ne sont pas compter
        parametres:
            texte, une chaine de caracteres
        renvoi une liste avec tout les nombres trouver dans texte
        """
        liste_numero = []

        i = 0
        while i < len(texte): # tant que toute la chaîne n'as pas été parcouru

            nbr = ""
            while i < len(texte): # tant que le caractere observer est un chiffre
                if texte[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    nbr += texte[i] # on ajoute le caractere au nombre
                    i += 1
                else:
                    break

            if nbr != "": # Si on a trouvé un nombre
                nbr = int(nbr) # on le transforme en entier
                liste_numero += [nbr] # on ajoute le nombre entier final à la liste des nombres trouvés

            i += 1
        return liste_numero

################################################################################

def fichier_existe(path):
    """
    fonction permettant de connaitre l'existence d'un répertoire ou d'un fichier
    parametres:
        path, le chemin vers le répertoire souhaité sous forme de chaine de caracteres
    renvoie un booléen, True si le répertoire/fichier existe et False sinon
    """
    if "." in path and os.path.isfile(path): # On dit que s'il y a un point dans le chemin, alors c'est un fichier que l'on recherche
        return True
    elif os.path.isdir(path): # sinon c'est un repertoire
        return True
    else:
        return False

############################## obtenir contenu #################################

def lire_fichier(file, ligne_vide = False):
    """
    fonction qui lit un fichier choisit
    parametres:
        file, une chaine de caracteres contenant le chemin vers le fichier à lire
        ligne_vide, optionnel, un booléen indiquant si les lignes vides représenté par "" doivent être garder, par défaut False
    renvoie une liste de chaine de caracteres, chaque élément est une ligne du fichier
    """
    if fichier_existe(file): # on vérifie que le fichier existe
        import codecs # ce module permet la retranscription des caractères spéciaux au format utf-8
        with codecs.open(file, "r", "utf-8") as f: # with permet de gerer l'ouverture et la fermeture automatique du fichier
            f = [x.rstrip("\n") for x in f.readlines()] # On enlève les sauts de ligne et les retours à la ligne, inutile puisque chaque ligne est un éléments du tableau

        if not ligne_vide:
            l = 0
            while l < len(f):

                if f[l] == "": # On enlève les lignes vides
                    f = f[:l] + f[l+1:]
                else:
                    l += 1

        return f

def lister_fichier(path):
    """
    fonction permettant de lister tous les éléments d'un répertoire donnée
    parametres:
        path, une chaine de caracteres indiquant le chemin vers le repertoire à lister
    renvoie une liste avec le nom de tous les éléments présent
    """
    return os.listdir(path)

############################ ajout/suppression #################################

def add_ligne(path, file, contenu):
    """
    fonction permettant d'ajouter des lignes à un fichier, si celui-ci n'existe pas, il est crée
    parametres:
        path, une chaine de caracteres avec le chemin d'accès au répertoire qui contiendrat le fichier
        file, une chaine de caracteres avec le nom du fichier
        contenu, une chaine de caracteres à mettre dans le fichier crée
    """
    if not fichier_existe(path + "/" + file):
        add_fichier(path, file)

    with open(path + "/" + file, "a") as fichier:
        fichier.write("\n" + contenu)

def remplacer_ligne(path, file, numero, texte):
    """
    fonction permettant de remplacer des lignes d'un fichier par un autre texte, si la ligne n'existe pas, le texte est placé en dernière ligne
    parametres:
        path, une chaine de caracteres avec le chemin d'accès au répertoire qui contiendrat le fichier
        file, une chaine de caracteres avec le nom du fichier
        numero, un nombre entier étant l'indice de la ligne à remplacer (la première ligne à pour indice 1)
        texte, une chaine de caractères à mettre à la place de la ligne
    """
    contenu = lire_fichier(path + "/" + file, True)
    taille = len(contenu)

    if numero > taille:
        contenu += [texte]
    else:
        contenu[numero -1] = texte

    suppr_lignes(path + "/" + file, *[i for i in range(1, taille +1)])

    nouveau = ""
    for i in contenu:
        nouveau += i + "\n"

    add_ligne(path, file, nouveau)

def suppr_lignes(file, *i_lines):
    """
    fonction permettant de supprimer les lignes d'un document grâce à leurs indices
    parametres:
        file, une chaine de caracteres indiquant le chemin vers le fichier
        i_lines, des nombres entier étant les indices des lignes à supprimer (la première ligne à pour indice 1)
    """
    if fichier_existe(file):
        save = []

        with open(file) as f:

            # on enregistre que les lignes que l'ont souhaite gardé
            i = 1
            for line in f.readlines():
                if i not in i_lines:
                    save.append(line)
                i += 1

        # on réecrit le fichier avec seulement les lignes enregistrées
        with open(file, "w") as f:
            f.writelines(save)

def add_fichier(path, file, contenu = ""):
    """
    fonction permettant de créer un fichier
    parametres:
        path, une chaine de caracteres avec le chemin d'accès au répertoire qui contiendrat le fichier
        file, une chaine de caracteres avec le nom du fichier
        contenu, une chaine de caracteres à mettre dans le fichier crée
    """
    with open(path + "/" + file, "x") as fichier:
        fichier.write(contenu)

def suppr_fichier(file, verif = True):
    """
    fonction permettant de supprimer un fichier
    parametres:
        file, une chaine de caracteres avec le chemin d'accès au fichier ou au répertoire
        verif, optionnel, un booléen indiquant si le programme doit demander la confirmation de l'utilisateur ou non, par défaut sur True
    """
    if fichier_existe(file) and "." in file: # on vérifie que le fichier existe
        kill = True
        if verif:
            from tkinter import messagebox
            if not messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer le fichier " + file +  " ?"):
                kill = False

        if kill:
            os.remove(file)

def add_repertoire(path, name):
    """
    fonction permettant de supprimer un répertoire
    parametres:
        path, une chaine de caracteres indiquant le chemin vers le repertoire parent
        name, une chaine de caracteres avec le nom du nouveau repertoire
    """
    os.mkdir(path + "/" + name)

def suppr_repertoire(path):
    """
    fonction permettant de supprimer un répertoire
    parametres:
        path, une chaine de caracteres indiquant le chemin vers le repertoire à supprimer
    """
    import shutil as sh # ce module sert à supprimer tous le contenu du répertoire avant de la supprimer
    sh.rmtree(path)
    os.rmdir(path)

################################################################################

def execute_sql_file(path, file, db):
    """
    fonction permettant d'exécuter une requete sql dans une base de données, ici, on lit le fichier puis on l'éxécute
    parametres:
        path, une chaine de caracteres contenant le chemin d'accès au fichier avec le fichier sql
        file, une chaine de caracteres contenant le nom du fichier à exécuter
        db, une chaine de caracteres avec le chemin entier vers la base de données dans laquelle exécuter la requete
    renvoie les résultats de la requetes sous forme de liste
    """
    # l'importation de ce module change selon l'utilisation du fichier (directe ou non)
    try:
        import module_database as Database
    except:
        from modules import module_database as Database

    sql_liste = lire_fichier(path + "/" + file) # on lit le fichier contenant le code SQL

    # On établit la requête sql dans une seule ligne/chaine de caractères
    sql = ""
    for i in range(len(sql_liste)):
        sql += sql_liste[i] + " "

    try: # Résolution du probleme "sqlite3.OperationalError: no such table:", si on y arrive pas avec le module dédié
        base = Database.database(db)
        result = base.execute(sql)
    except: # On l'effectue de manière directe
        import sqlite3
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        result = cur.execute(sql).fetchall()
        conn.close()

    return result

def derniere_modif(path):
    """
    fonction permettant de connaitre la date de la derniere modification d'un fichier
    parametres:
        path, le chemin complet vers le fichier a éxaminé
    renvoie une chaine de caracteres contenant une date, si le fichier n'existe pas, renvoie None
    """
    if fichier_existe(path):
        return os.path.getmtime(path)
    return None