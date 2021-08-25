#!"C:\Winpython\python-3.8.5.amd64\python.exe"

# importation du module necessaires
import sqlite3
import mariadb

class database:
    # https://docs.python.org/3/library/sqlite3.html
    def __init__(self, base, module = "sqlite3"):
        """
        méthode constructrice de la classe
        parametres:
                   base, une chaine de caracteres avec le chemin d'accès à la base de données
                   module, optionnel, chaine de caracteres indiquant le module à utiliser, soit 'sqlite3', soit 'mariadb'
        """
        self.base = base

        if module == "sqlite3":
            self.module = module
        else:
            self.module = "mariadb"

    def test_connexion(self):
        """
        méthode permettant de savoir si la base de données peut-être connectées
        renvoie un booléen
        """
        try:
            if self.module == "sqlite3":
                conn = sqlite3.connect(self.base)
            else:
                conn = mariadb.connect(
                user = "root",
                database=self.base)
        except:
            return False

        conn.close()
        return True

    def connexion(self):
        """
        méthode permettant de se connecter à la base de donnée
        """
        if self.module == "sqlite3":
            self.conn = sqlite3.connect(self.base)
        else:
            self.conn = mariadb.connect(
                user="root",
                database=self.base)

        self.cur = self.conn.cursor()

    def deconnexion(self):
        """
        méthode permettant de se deconnecter à la base de donnée
        """
        self.conn.close()

    def execute(self,sql):
        """
        méthode permettant d'executer une requete de modification dans la base
        parametres:
            sql, une chaine de caracteres correspondant à une requete SQL
        """
        self.connexion()

        try:
            result = self.cur.execute(sql).fetchall()
        except:
            result = None

        self.conn.commit()
        self.deconnexion()
        return result


    def contenue_table(self, table):
        return self.execute("SELECT * FROM " + table)

    def infotable(self, table):
        """
        méthode permettant de connaitre les informations d'une table
        parametres:
                   table, une chaine de caracteres contenant le nom de la table
        renvoie les informations de la table
        """
        return self.execute("DESCRIBE " + table)