# importation du module necessaires
import sqlite3

class database:
    # https://docs.python.org/3/library/sqlite3.html
    def __init__(self, base):
        """
        méthode constructrice de la classe
        parametres:
                   base, une chaine de caracteres avec le chemin d'accès à la base de données
                   module, optionnel, chaine de caracteres indiquant le module à utiliser, soit 'sqlite3', soit 'mariadb'
        """
        self.base = base

    def test_connexion(self):
        """
        méthode permettant de savoir si la base de données peut-être connectées
        renvoie un booléen
        """
        try:
            conn = sqlite3.connect(self.base)
        except:
            return False

        conn.close()
        return True

    def connexion(self):
        """
        méthode permettant de se connecter à la base de donnée
        """
        self.conn = sqlite3.connect(self.base)
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
        result = self.cur.execute(sql).fetchall()

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