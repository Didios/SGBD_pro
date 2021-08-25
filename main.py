# SGBD DGourmandises
# fait par Didier Mathias

from tkinter import Tk, Button, Scrollbar, Frame, Entry, Listbox, StringVar, Label, Checkbutton, BooleanVar, Text, Scale, ttk, Spinbox, Toplevel, PhotoImage
from tkinter.messagebox import showerror, showinfo, askyesno, showwarning
import module_lecture_fichier as read
import module_database as db
import datetime


"""
ajouter des scrollbar à toutes les zones de texte
faire en sorte que les zones de texte ne coupent pas les mots
faire en sorte que toutes les fenetres aient leurs éléments qui s'ajustent selon la taille de la fenêtre
faire en sorte que le bouton de fin de commande mette à jour les quantite des ingrdients, puis alerter si il reste 1kg ou moins des ingredients
"""
class SGBD:
    """
    Gestionnaire de Base de Données
    """
    def __init__(self, base, option):
        """
        constructeur de la classe
        parametres:
            base, une chaine de caracteres, indique le chemin vers la base de données
            option, une chaine de caracteres, indique le chemin vers le fichier des options de l'utilisateur
        """
        self.base = db.database(base)

        option = read.lire_fichier(option)
        dico = {}
        for ligne in option:
            ligne = ligne.split(":")
            dico[ligne[0]] = ligne[1].split("\r")[0]

        self.option = dico

    def lancement(self):
        def recherche(event):
            """
            méthode permettant de rendre active la barre de recherche
            ne laisse dans la listbox que les éléments qui contiennent la recherche
            """
            # on réinitialise la liste complète (au cas ou la recherche est totalement différente)
            if self.onglet.get() == "Client":
                self.client()
            elif self.onglet.get() == "Commande":
                self.commande()
            elif self.onglet.get() == "Ingredient":
                self.ingredient()
            elif self.onglet.get() == "Brique":
                self.brique()
            elif self.onglet.get() == "Gateau":
                self.gateau()

            # on enlève
            i_ligne = -1
            for ligne in self.list.get(0, "end"):
                i_ligne += 1
                if self.contenue_barre.get() not in ligne:
                    self.list.delete(i_ligne)
                    i_ligne -= 1

        # on initialise la fenêtre
        self.root = Tk()
        self.root.title("SGBD DGourmandises")
        self.root.iconbitmap("images/icone.ico")
        self.root.configure(bg = self.option["color_bg"])
        self.menu = Frame(self.root, bg = self.option["color_menu"])

        # on charge les image de la barre de menu
        photo = PhotoImage(file = "images/image_client.png")
        image_client = photo.subsample(2, 2)
        photo = PhotoImage(file = "images/image_commande.png")
        image_commande = photo.subsample(2, 2)
        photo = PhotoImage(file = "images/image_gateaux.png")
        image_gateau = photo.subsample(2, 2)
        photo = PhotoImage(file = "images/image_recette.png")
        image_recette = photo.subsample(2, 2)
        photo = PhotoImage(file = "images/image_ingredient.png")
        image_ingredient = photo.subsample(2, 2)

        # on affiche la barre de menu
        Button(self.menu, bg = self.option["color_button"], text = "Client"     , image = image_client, compound = "bottom", command = self.client).grid(row = 0, column = 0, sticky="NSEW")
        Button(self.menu, bg = self.option["color_button"], text = "Commandes"  , image = image_commande, compound = "bottom", command = self.commande).grid(row = 0, column = 1, sticky="NSEW")
        Button(self.menu, bg = self.option["color_button"], text = "Gateaux"    , image = image_gateau, compound = "bottom", command = self.gateau).grid(row = 0, column = 2, sticky="NSEW")
        Button(self.menu, bg = self.option["color_button"], text = "Recettes"   , image = image_recette, compound = "bottom", command = self.brique).grid(row = 0, column = 3, sticky="NSEW")
        Button(self.menu, bg = self.option["color_button"], text = "Ingrédients", image = image_ingredient, compound = "bottom", command = self.ingredient).grid(row = 0, column = 4, sticky="NSEW")

        self.menu.grid(row = 0, column = 0, columnspan = 3, sticky="NSEW")

        # on crée la barre de recherche
        self.contenue_barre = StringVar()

        barre = Entry(self.root, textvariable = self.contenue_barre)
        barre.bind("<Return>", recherche)
        barre.grid(row = 1, column = 0, columnspan = 2, sticky="EW")

        # on crée la liste des éléments avec la scrollbar
        scrollbar = Scrollbar(self.root, orient = "vertical", width = 20)
        scrollbar.grid_propagate(0)
        scrollbar.grid(row = 2, column = 0, sticky="NSW")

        self.list = Listbox(self.root, yscrollcommand = scrollbar.set)
        self.list.grid(row = 2, column = 1, sticky="NSEW")

        scrollbar.config(command = self.list.yview)

        # on crée la variable de sélection (savoir dans quoi on est)
        self.onglet = StringVar()
        self.onglet.set("None")

        # bouton d'ajout
        Button(self.root, text = "+", command = lambda x=self.onglet: self.ajout(x), bg = self.option["color_button"]).grid(row = 3, column = 0, columnspan = 2, sticky="NSEW")

        # frame des informations complémentaires
        self.information = Frame(self.root, bg = self.option["color_bg"])
        self.information.grid(row = 1, column = 2, rowspan = 3, sticky="NSEW")

        # on gère l'adaptabilité à la fenêtre
        grid(self.menu, 1, 4)
        grid(self.root, 4, 3)
        self.root.grid_columnconfigure(0, weight = 0)
        self.root.grid_rowconfigure(1, weight = 0)
        self.root.grid_columnconfigure(2, weight = 2)

        # on gère le double-clic sur un élément de la liste
        self.list.bind("<Double-1>", lambda x :  self.show_information(self.list.get(self.list.curselection()[0])))
        self.root.mainloop()


    def client(self):
        """
        méthode permettant d'afficher la liste des clients dans la listbox
        """
        self.onglet.set("Client")
        self.list.delete(0,'end')

        liste = self.base.execute("Select ID, nom, prenom From Client")
        if liste == []:
            self.list.insert(0, "Aucun client n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = str(liste[i][0]) + " | " + liste[i][1] + " " + liste[i][2]
                self.list.insert(i, texte)

    def commande(self):
        """
        méthode permettant d'afficher la liste des commandes dans la listbox
        """
        self.onglet.set("Commande")
        self.list.delete(0,'end')

        liste = self.base.execute("Select ID, date_dbt, date_limite, date_fn From Commandes")
        plus_proche = []
        if liste == []:
            self.list.insert(0, "Aucune commandes n'as été enregistré")
        else:
            demain = datetime.datetime.now() + datetime.timedelta(1)

            for i in range(len(liste)):
                self.list.insert(i, str(liste[i][0]) + " | " + liste[i][1])

                # transformation de la date limite
                date = liste[i][2].split("/")
                date = date[:2] + date[2].split("-")
                date = date[:3] + date[3].split(":")
                date = [date[2]] + [date[1]] + [date[0]] + date[3:]
                for j in range(len(date)):
                    date[j] = int(date[j])
                date_limite = datetime.datetime(*date)

                if demain > date_limite and liste[i][3] == None: # on récupére l'ID et la date de la commande la plus proche
                    plus_proche += ["%d | %s  ->  %s" %(liste[i][0], liste[i][1], liste[i][2])]

            if plus_proche != []:
                liste_rapide = ""
                for j in plus_proche:
                    liste_rapide += "- " + j + "\n"
                showwarning("Commandes rapides", "Les commandes suivantes sont à faire dans un délai de 24H : \n" + liste_rapide)


    def gateau(self):
        """
        méthode permettant d'afficher la liste des gâteaux dans la listbox
        """
        self.onglet.set("Gateau")
        self.list.delete(0,'end')

        liste = self.base.execute("Select nom From Gateaux")
        if liste == []:
            self.list.insert(0, "Aucun gateau n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = liste[i][0]
                self.list.insert(i, texte)

    def brique(self):
        """
        méthode permettant d'afficher la liste des 'briques' dans la listbox
        """
        self.onglet.set("Brique")
        self.list.delete(0,'end')

        liste = self.base.execute("Select nom From Briques")
        if liste == []:
            self.list.insert(0, "Aucune recette n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = liste[i][0]
                self.list.insert(i, texte)

    def ingredient(self):
        """
        méthode permettant d'afficher la liste des ingrédients dans la listbox
        """
        self.onglet.set("Ingredient")
        self.list.delete(0,'end')

        liste = self.base.execute("Select nom From Ingredients")
        if liste == []:
            self.list.insert(0, "Aucun ingredient n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = liste[i][0]
                self.list.insert(i, texte)

    def ajout(self, onglet):
        """
        méthode permettant d'ajouter un éléments quel qu'il soit
        """
        if self.onglet.get() != "None":
            plus = Toplevel(self.root, bg = self.option["color_bg"])
            plus.title("Ajout " + onglet.get())

            def validation():
                """
                validation : on vérifie les informations
                    si elles sont bonnes:
                        ont les ajoute à la base
                        ont ferme la fenetre
                        ont relance la méthode correspondante pour mettre à jour
                    sinon:
                        on affiche un message d'erreur qui indique ce qui ne va pas
                """
                if self.onglet.get() == "Client":###############################
                    if vide(nom.get()):
                        showerror("Pas de Nom", "Tout client doit posséder un nom de famille")
                    elif vide(prenom.get()):
                        showerror("Pas de prenom", "Tout client doit posséder un prénom")
                    elif (vide(telephone.get()) or len(telephone.get()) < 10) and vide(email.get()):
                        showerror("Information suplémentaires", "Les clients doivent posséder un numéro de téléphone ou un e-mail, ceci afin de les différencier en cas de patronymes identique")
                    else:
                        if vide(telephone.get()) or len(telephone.get()) < 10:
                            self.base.execute("INSERT INTO Client(nom, prenom, mail) VALUES('%s', '%s', '%s')" %(nom.get(), prenom.get(), email.get()))
                        elif vide(email.get()):
                            self.base.execute("INSERT INTO Client(nom, prenom, telephone) VALUES('%s', '%s', %s)" %(nom.get(), prenom.get(), telephone.get()))
                        else:
                            self.base.execute("INSERT INTO Client(nom, prenom, telephone, mail) VALUES('%s', '%s', %s , '%s')" %(nom.get(), prenom.get(), telephone.get(), email.get()))
                        plus.destroy()
                        self.client()

                elif self.onglet.get() == "Commande":###########################
                    if clients.get() == "":
                        showerror("Pas de client", "Un client doit être sélectionné")
                    elif prix_total.get() == "0.0":
                        showerror("Pas de prix", "Une commande doit avoir un certain prix")
                    else:
                        date = datetime.datetime.now()
                        date_dbt = "%d/%d/%d-%d:%d:%d" %(date.day, date.month, date.year, date.hour, date.minute, date.second) # on détermine la date exacte de commande
                        ID_client = clients.get().split("/ ")[0] # on détermine l'ID du client
                        date_limite = "%s/%s/%s-%s:%s" %(jour.get(), mois.get(), annee.get(), heure.get(), minute.get())

                        self.base.execute("INSERT INTO Commandes(prix, livraison, date_dbt, date_limite, soldes, ID_client) VALUES(%s, '%s', '%s', '%s', %s, %s)" %(prix_total.get(), livraison.get(), date_dbt, date_limite, soldes.get(), ID_client)) # On crée la commande

                        ID = self.base.execute("SELECT ID FROM Commandes WHERE date_dbt = '%s'" %(date_dbt))[0][0] # on détermine l'ID de commande grâce à l'heure qui est unique

                        # insertion de la liste de gateaux dans composition
                        nbr_gateau = note.grid_size()[1] -1
                        for ligne in range(1, nbr_gateau):
                            ID_gateau = self.base.execute("SELECT ID FROM Gateaux WHERE nom='%s'" %(note.grid_slaves(row = ligne, column = 0)[0].get()))[0][0]

                            personnalisation = "nbr_part=%s, prix=%s, supplement=%s|" %(note.grid_slaves(row = ligne, column = 1)[0].get(), note.grid_slaves(row = ligne, column = 3)[0].get(), note.grid_slaves(row = ligne, column = 4)[0].get())
                            personnalisation += note.grid_slaves(row = ligne, column = 2)[0].get("0.0", "end")

                            self.base.execute("INSERT INTO Composition VALUES(%d, %d, '%s')" %(ID, ID_gateau, personnalisation))

                        plus.destroy()
                        self.commande()

                elif self.onglet.get() == "Gateau":#############################
                    if vide(type_.get()):
                        showerror("Absence de type", "Le gateau doit posséder un type : dessert, entrée, crème, pâte, ...")
                    elif vide(nom.get()):
                        showerror("Absence de nom", "Le gateau doit posséder un nom")
                    elif nom.get() in [x[0] for x in self.base.execute("SELECT nom FROM Gateaux")]:
                        showerror("Nom existant", "Le nom du gateau doit être unique")
                    else:
                        liste_brique = []
                        for ligne in range(1, espace_brique.grid_size()[1]):
                            liste_brique += [espace_brique.grid_slaves(row = ligne, column = 0)[0].get()]

                        if liste_brique == []:
                            showerror("Absence Brique", "Le gateau doit posséder une brique minimum")
                        else:
                            self.base.execute("INSERT INTO Gateaux(type, nom, nb_parts, prix_part, prix_assemblage, marge) VALUES('%s', '%s', %s, %s, %s, %s)" %(type_.get(), nom.get(), nbr_part.get(), prix_part.get()[:-2], prix_assemblage.get(), marge.get()[:3]))
                            ID = self.base.execute("SELECT ID FROM Gateaux WHERE nom='%s'" %(nom.get()))[0][0]
                            nbr_brique = espace_brique.grid_size()[1]
                            for ligne in range(1, nbr_brique):
                                ID_brique = self.base.execute("SELECT ID FROM Briques WHERE nom='%s'" %(espace_brique.grid_slaves(row = ligne, column = 0)[0].get()))[0][0]

                                self.base.execute("INSERT INTO Construction VALUES(%d, %d, %s)" %(ID, ID_brique, espace_brique.grid_slaves(row = ligne, column = 1)[0].get()))

                            plus.destroy()
                            self.gateau()

                elif self.onglet.get() == "Brique":#############################
                    if vide(nom.get()):
                        showerror("Absence de nom", "La recette doit posséder un nom")
                    elif nom.get() in [x[0] for x in self.base.execute("SELECT nom FROM Briques")]:
                        showerror("Nom existant", "Le nom de la brique doit être unique")
                    elif vide(recette.get("0.0", "end")):
                        showerror("Absence d'instructions", "La recette doit posséder une suite d'instructions")
                    else:
                        liste_ingredient = []
                        for ligne in range(1, espace_ingredient.grid_size()[1] -1):
                            if espace_ingredient.grid_slaves(row = ligne, column = 0) != []:
                                liste_ingredient += [espace_ingredient.grid_slaves(row = ligne, column = 0)[0].get()]

                        if liste_ingredient == []:
                            showerror("Absence Ingrédient", "La recette doit posséder au moins un ingrédient")
                        else:
                            self.base.execute('INSERT INTO Briques(nom, prix, poid, recette) VALUES("%s", %s, %s, "%s")' %(nom.get(), prix.get(), poid.get(), recette.get("0.0", "end")))
                            ID = self.base.execute("SELECT ID FROM Briques WHERE nom='%s'" %(nom.get()))[0][0]
                            nbr_ingredient = espace_ingredient.grid_size()[1] -1
                            for ligne in range(1, nbr_ingredient):
                                if espace_ingredient.grid_slaves(row = ligne, column = 0) != []:
                                    ID_ingredient = self.base.execute("SELECT ID FROM Ingredients WHERE nom='%s'" %(espace_ingredient.grid_slaves(row = ligne, column = 0)[0].get()))[0][0]

                                    self.base.execute("INSERT INTO Recettes VALUES(%d, %d, %s)" %(ID, ID_ingredient, espace_ingredient.grid_slaves(row = ligne, column = 1)[0].get()))

                            plus.destroy()
                            self.brique()

                elif self.onglet.get() == "Ingredient":#########################
                    if vide(nom.get()):
                        showerror("Absence nom", "L'ingrédients doit posséder un nom")
                    elif nom.get() in [x[0] for x in self.base.execute("SELECT nom FROM Ingredients")]:
                        showerror("Nom existant", "Le nom de l'ingrédient doit être unique")
                    else:
                        self.base.execute("INSERT INTO Ingredients(nom, poid_base, prix_base, quantite) VALUES('%s', %s, %s, %s)" %(nom.get(), poid.get(), prix.get(), quantite.get()))

                        plus.destroy()
                        self.ingredient()


            if self.onglet.get() == "Client":                                   ############################################################################################
                plus.iconbitmap("images/icone_client.ico")
                # champ nom
                Label(plus, text = "Nom :", bg = self.option["color_bg"]).pack()

                nom = Entry(plus)
                nom.pack()

                # champ prenom
                Label(plus, text = "Prénom :", bg = self.option["color_bg"]).pack()
                prenom = Entry(plus)
                prenom.pack()

                # champ numero de telephone
                Label(plus, text = "Numéro de téléphone :", bg = self.option["color_bg"]).pack()

                telephone = Entry(plus)
                telephone.pack()

                # champ addresse e-mail
                Label(plus, text = "Addresse E-mail :", bg = self.option["color_bg"]).pack()

                email = Entry(plus)
                email.pack()

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"]).pack()
            elif self.onglet.get() == "Commande":                               ############################################################################################
                plus.iconbitmap("images/icone_commande.ico")
                # on choisit le client
                Label(plus, text = "Client commanditaire :", bg = self.option["color_bg"]).grid(row = 0, column = 0, columnspan = 5)

                liste_clients = []
                liste_compose = self.base.execute("SELECT ID, nom, prenom FROM Client")
                for elmt in liste_compose:
                    liste_clients += [str(elmt[0]) + "/ " + elmt[1] + " " + elmt[2]]

                clients = ttk.Combobox(plus, values = liste_clients, state = "readonly")
                clients.grid(row = 1, column = 0, columnspan = 5)

                # on met la possibilité d'une livraison
                Label(plus, text = "Addresse de Livraison :", bg = self.option["color_bg"]).grid(row = 2, column = 0, columnspan = 4, sticky = "W")
                livraison = Entry(plus)
                livraison.insert("0", "Boutique")
                livraison.grid(row = 3, column = 0, columnspan = 4, sticky = "W")

                # on demande une date de fin prévu
                Label(plus, text = "Date limite :", bg = self.option["color_bg"]).grid(row = 4, column = 0, columnspan = 5)
                Label(plus, text = "Heure", bg = self.option["color_bg"]).grid(row = 5, column = 0)
                Label(plus, text = "minute", bg = self.option["color_bg"]).grid(row = 5, column = 1)
                Label(plus, text = "Jour", bg = self.option["color_bg"]).grid(row = 5, column = 2)
                Label(plus, text = "Mois", bg = self.option["color_bg"]).grid(row = 5, column = 3)
                Label(plus, text = "Année", bg = self.option["color_bg"]).grid(row = 5, column = 4)
                date = datetime.datetime.now()
                jour = Spinbox(plus, from_ = 00, to = 31, increment = 1, width = 3)
                jour.delete("0", "end")
                jour.insert("0", date.day)
                mois = Spinbox(plus, from_ = 00, to = 12, increment = 1, width = 3)
                mois.delete("0", "end")
                mois.insert("0", date.month)
                annee = Spinbox(plus, from_ = date.year, to = date.year + 10, width = 4)
                heure = Spinbox(plus, from_ = 00, to = 23, width = 4)
                heure.delete("0", "end")
                heure.insert("0", date.hour)
                minute = Spinbox(plus, from_ = 00, to = 59, width = 5)
                minute.delete("0", "end")
                minute.insert("0", date.minute)

                heure.grid(row = 6, column = 0)
                minute.grid(row = 6, column = 1)
                jour.grid(row = 6, column = 2)
                mois.grid(row = 6, column = 3)
                annee.grid(row = 6, column = 4)

                # on affiche les gateaux
                scroll_gateau = Scrollbar(plus, orient = "vertical", width = 20)
                scroll_gateau.grid_propagate(0)
                scroll_gateau.grid(row = 7, column = 0, sticky = "NSEW")

                liste_gateau = Listbox(plus, yscrollcommand = scroll_gateau.set, height = 20)
                liste_gateau.grid(row = 7, column = 1, columnspan = 4, sticky = "NSEW")

                scroll_gateau.config(command = liste_gateau.yview)
                    # on insere les gateaux dans la liste
                liste = self.base.execute("Select nom From Gateaux")
                for i in range(len(liste)):
                    liste_gateau.insert(i, liste[i][0])

                # Frame de note de fin
                note = Frame(plus, width = 500)
                note.grid(row = 0, column = 5, rowspan = 8, sticky = "NSEW")

                # on met le prix total
                prix_total = StringVar()
                prix_total.set("0.0")
                Label(note, text = "Gateau", bg = self.option["color_bg"]).grid(row = 0, column = 0)
                Label(note, text = "Nbr de part", bg = self.option["color_bg"]).grid(row = 0, column = 1)
                Label(note, text = "personnalisation", bg = self.option["color_bg"]).grid(row = 0, column = 2)
                Label(note, text = "Prix €", bg = self.option["color_bg"]).grid(row = 0, column = 3)
                Label(note, text = "Supplément €", bg = self.option["color_bg"]).grid(row = 0, column = 4)

                Label(note, text = "Prix Total : " + prix_total.get() + " €", bg = self.option["color_bg"]).grid(row = 1, column = 3, columnspan = 2, sticky = "SE")

                def change_prix():
                    """
                    sous-fonction permettant de mettre à jour le prix global de la commande
                    """
                    nbr_ligne = note.grid_size()[1] -1
                    note.grid_slaves(row = nbr_ligne)[0].destroy()

                    prix = 0.0
                    prix_min = 0.0
                    for i_ligne in range(1, nbr_ligne):
                        try:
                            prix += float(note.grid_slaves(row = i_ligne, column = 3)[0].get())
                            info = self.base.execute("SELECT marge, prix_part, nb_parts, prix_assemblage FROM Gateaux WHERE nom = '%s'" %(note.grid_slaves(row = i_ligne, column = 0)[0].get()))[0]
                            prix_min += float(((info[1] * info[2]) + info[3]) / info[0])
                        except:
                            pass

                    # on effectue la réduction
                    prix = prix * (100 - int(soldes.get())) / 100
                    prix = round(prix, 2)

                    # on prévient si les réductions sont trop grandes
                    if prix < prix_min:
                        soldes.config(repeatinterval = 0)
                        showinfo("Soldes trop grandes", "Attention, les soldes sont trop grandes ! Marge négative ou nul.")
                    else:
                        soldes.config(repeatinterval = 100)

                    prix_total.set(str(prix))
                    Label(note, text = "Prix Total : " + prix_total.get() + " €", bg = self.option["color_bg"]).grid(row = nbr_ligne, column = 3, columnspan = 2, sticky = "SE")

                # on met la case de solde
                Label(plus, text = "Soldes (%):", bg = self.option["color_bg"]).grid(row = 2, column = 4, sticky = "E")
                soldes = Spinbox(plus, from_ = 0, to = 100, increment = 1, width = 5, command = lambda x=None : change_prix())
                soldes.grid(row = 3, column = 4, sticky = "E")

                # permet de gérer la note finale
                def ajout_gateau(gateau):
                    """
                    sous-fonction permettant de gérer les gâteaux présent dans la commande, de leur ajout jusqu'à leurs suppression
                    paramètres:
                        gateau, une chaine de caracteres indiquant le nom du gateau a ajouté à la commande
                    """
                    def change_prix_ligne(ligne):
                        """
                        sous-sous-fonction permettant de mettre à jour le prix d'un gateau en fonction de ses paramètres
                        paramètres:
                            ligne, un index indiquant le numero de ligne du gateau à mettre à jour
                        """
                        selection = note.grid_slaves(row = ligne, column = 0)[0].get()
                        prix_part = float(self.base.execute("SELECT prix_part FROM Gateaux WHERE nom = '%s'" %selection)[0][0])
                        prix_assemblage = float(self.base.execute("SELECT prix_assemblage FROM Gateaux WHERE nom = '%s'" %selection)[0][0])
                        nbr_part = int(note.grid_slaves(row = ligne, column = 1)[0].get())
                        prix_suppl = float(note.grid_slaves(row = ligne, column = 4)[0].get())

                        prix = (prix_part * nbr_part) + prix_suppl
                        prix = round(prix, 2)

                        spin = note.grid_slaves(row = ligne, column = 3)[0]
                        spin.configure(state = "normal")
                        spin.delete("0", "end")
                        spin.insert("0", str(prix))
                        spin.configure(state = "readonly")

                        change_prix()

                    def delete_ligne(ligne):
                        """
                        sous-sous-fonction permettant de supprimer une ligne de la commande
                        """
                        for elmt in note.grid_slaves(row = ligne):
                            elmt.destroy()

                        change_prix()

                    # regarder si le gateau n'est pas déjà dans note, si c'est le cas, on affiche une erreur = "gateau déjà présent"
                    liste_gateau = []
                    if note.grid_size()[1] > 2:
                        for i in range(1, note.grid_size()[1] -1):
                            if note.grid_slaves(row = i, column = 0) != []:
                                liste_gateau += [note.grid_slaves(row = i, column = 0)[0].get()]
                        if gateau in liste_gateau:
                            showerror("Présence", "Le gâteau que vous souhaitez ajoutez et déjà présent dans la commande")
                            return None

                    # on enlève la dernière ligne contenant le prix total
                    taille = note.grid_size()[1]
                    note.grid_slaves(row = taille -1)[0].destroy()

                    # on insère la ligne
                        # nom du gateau (pour être récupérer)
                    nouv_ligne = Entry(note)
                    nouv_ligne.insert("0", gateau)
                    nouv_ligne.configure(state = "readonly")
                    nouv_ligne.grid(row = taille -1, column = 0)
                        # nombre de parts
                    Spinbox(note, command = lambda x=int("%d" %(taille-1)) :change_prix_ligne(x), from_ = 1, to = 50, increment = 1, width = 5).grid(row = taille-1, column = 1)
                        # personnalisation
                    Text(note, height = 2, width = 20).grid(row = taille-1, column = 2)
                        # prix du gateau
                    nouv_prix = Entry(note)
                    nouv_prix.insert("0", "0.00")
                    nouv_prix.configure(state = "readonly")
                    nouv_prix.grid(row = taille -1, column  = 3)
                        # prix supplémentaires
                    Spinbox(note, command = lambda x=int("%d" %(taille-1)) :change_prix_ligne(x), from_ = 0.00, to = 100.00, increment = 0.01, width = 10).grid(row = taille-1, column = 4)
                        # bouton de suppression
                    Button(note, text = "X", command = lambda x=int("%d" %(taille-1)) : delete_ligne(x), bg = self.option["color_button"]).grid(row = taille-1, column = 5)

                    # on met la dernière ligne contenant le prix total
                    Label(note, text = "Prix Total : " + prix_total.get() + " €", bg = self.option["color_bg"]).grid(row = taille, column = 3, columnspan = 3, sticky = "SE")
                    change_prix_ligne(taille -1)

                liste_gateau.bind("<Double-1>", lambda x :  ajout_gateau(liste_gateau.get(liste_gateau.curselection()[0])))

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"]).grid(row = 8, column = 0, columnspan = 6)
            elif self.onglet.get() == "Gateau":                                 ############################################################################################
                plus.iconbitmap("images/icone_gateau.ico")
                espace_brique = Frame(plus, width = 200)
                Label(espace_brique, text = "Nom", bg = self.option["color_bg"]).grid(row = 0, column = 0)
                Label(espace_brique, text = "Poid", bg = self.option["color_bg"]).grid(row = 0, column = 1)

                def changer_prix():
                    """
                    le prix de la part est calculé ainsi :
                        nbr_part / [ (poid_brique1_choisi * prix_brique1_base / poid_brique1_base) + ... + assemblage ]
                    """
                    """
                    la marge est calculé ainsi :
                        si l'ensemble des ingredients coute 5 €
                        si le gateau coute au final 20 €
                        alors la marge est de 4
                        cout_total / cout_ingredients
                    """
                    taille = espace_brique.grid_size()[1]

                    prix = 0.0
                    for ligne in range(1, taille):
                        try:
                            prix_poid = self.base.execute("SELECT prix, poid FROM Briques WHERE nom = '%s'" %(espace_brique.grid_slaves(row = ligne, column = 0)[0].get()))[0]
                            poid_choisi = float(espace_brique.grid_slaves(row = ligne, column = 1)[0].get())
                            prix += (poid_choisi * prix_poid[0] / prix_poid[1])
                        except:
                            pass

                    cout_ingredient = prix
                    prix += float(prix_assemblage.get())
                    point_marge = prix / cout_ingredient
                    point_marge = round(point_marge, 1)

                    prix /= int(nbr_part.get())
                    prix = round(prix, 2)

                    prix_part.configure(state = "normal")
                    prix_part.delete("0", "end")
                    prix_part.insert("0", "%s €" %(str(prix)))
                    prix_part.configure(state = "readonly")

                    marge.configure(state = "normal")
                    marge.delete("0", "end")
                    marge.insert("0", "%s points" %(str(point_marge)))
                    marge.configure(state = "readonly")

                def ajout_brique(brique):
                    taille = espace_brique.grid_size()[1] # on détermine la taille de la grille

                    if espace_brique.grid_size()[1] > 1:
                        for i in range(1, taille):
                            if brique == espace_brique.grid_slaves(row = i, column = 0)[0].get():
                                showerror("Présence", "La recette que vous souhaitez ajoutez et déjà présente dans le gateau")
                                return None

                    # on ajoute le nom
                    name = Entry(espace_brique)
                    name.insert("0", brique)
                    name.configure(state = "readonly")
                    name.grid(row = taille, column = 0)

                    # on ajoute le poids
                    Spinbox(espace_brique, from_ = 0.001, to = 100.000, increment = 0.001, command = changer_prix).grid(row = taille, column = 1)

                    # on ajoute le bouton
                    Button(espace_brique, text = "X", command = lambda x=int("%d" %(taille), bg = self.option["color_button"]) : delete_ligne(x)).grid(row = taille, column = 2)

                    changer_prix()

                def delete_ligne(ligne):
                    for elmt in espace_brique.grid_slaves(row = ligne):
                        elmt.destroy()

                    changer_prix()

                # le type de gateau
                Label(plus, text = "Type de Gateau :", bg = self.option["color_bg"]).grid(row = 0, column = 0)
                type_ = Entry(plus)
                type_.grid(row = 1, column = 0)

                # le nom du gateau
                Label(plus, text = "Nom du Gateau (unique) :", bg = self.option["color_bg"]).grid(row = 2, column = 0)
                nom = Entry(plus)
                nom.grid(row = 3, column = 0)

                # le nombre de part
                Label(plus, text = "Nombre de part :", bg = self.option["color_bg"]).grid(row = 4, column = 0)
                nbr_part = Spinbox(plus, from_ = 1, to = 100, increment = 1, command = changer_prix)
                nbr_part.grid(row = 5, column = 0)

                # le prix de l'assemblage
                Label(plus, text = "prix de la main d'oeuvre :", bg = self.option["color_bg"]).grid(row = 6, column = 0)
                prix_assemblage = Spinbox(plus, from_ = 0.00, to = 100.00, increment = 0.01, command = changer_prix)
                prix_assemblage.grid(row = 7, column = 0)

                # Le prix de la part
                Label(plus, text = "Prix de la part :", bg = self.option["color_bg"]).grid(row = 8, column = 0, sticky = "W")
                prix_part = Entry(plus, width = 10)
                prix_part.insert("0", "0.0 €")
                prix_part.configure(state = "readonly")
                prix_part.grid(row = 9, column = 0, sticky = "W")

                # la marge
                Label(plus, text = "marge : ", bg = self.option["color_bg"]).grid(row = 8, column = 0, sticky = "E")
                marge = Entry(plus, width = 10)
                marge.insert("0", "0.0 points")
                marge.configure(state = "readonly")
                marge.grid(row = 9, column = 0, sticky = "E")

                # les briques
                    # l'espace necessaires
                espace_brique.grid(row = 0, column = 3, rowspan = 10, sticky = "NSEW")
                    # l'affichage des briques avec une scrollbar
                Label(plus, text = "Recettes disponibles :", bg = self.option["color_bg"]).grid(row = 0, column = 1, columnspan = 2)
                        # scrollbar
                scroll_brique = Scrollbar(plus, orient = "vertical", width = 20)
                scroll_brique.grid_propagate(0)
                scroll_brique.grid(row = 1, column = 1, rowspan = 9, sticky = "NSEW")
                        # listbox
                liste_brique = Listbox(plus, yscrollcommand = scroll_brique.set, height = 10)
                liste_brique.grid(row = 1, column = 2, rowspan = 9, sticky = "NSEW")
                        # configuration scrollbar
                scroll_brique.config(command = liste_brique.yview)
                    # on insere les briques dans la liste
                liste = self.base.execute("Select nom From Briques")
                for i in range(len(liste)):
                    liste_brique.insert(i, liste[i][0])

                liste_brique.bind("<Double-1>", lambda x : ajout_brique(liste_brique.get(liste_brique.curselection()[0])))

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"]).grid(row = 12, column = 0, columnspan = 4)
            elif self.onglet.get() == "Brique":                                 ############################################################################################
                plus.iconbitmap("images/icone_recette.ico")
                # le nom de la brique
                Label(plus, text = "Nom de la Recette :", bg = self.option["color_bg"]).grid(row = 0, column = 0)
                nom = Entry(plus)
                nom.grid(row = 1, column = 0)

                # le poid de la brique
                Label(plus, text = "Poids de la préparation :", bg = self.option["color_bg"]).grid(row = 2, column = 0)
                poid = Spinbox(plus, from_ = 0.001, to = 100.000, increment = 0.001)
                poid.grid(row = 3, column = 0)

                # espace ingrédients
                espace_ingredient = Frame(plus)
                espace_ingredient.grid(row = 0, column = 3, rowspan = 8, sticky = "NSEW")
                Label(espace_ingredient, text = "Nom", bg = self.option["color_bg"]).grid(row = 0, column = 0)
                Label(espace_ingredient, text = "Poids", bg = self.option["color_bg"]).grid(row = 0, column = 1)
                Label(espace_ingredient, text = "Prix", bg = self.option["color_bg"]).grid(row = 0, column = 2)

                # le prix
                prix = StringVar()
                prix.set("0.00")
                Label(espace_ingredient, text = "Prix total : %s €" %(prix.get()), bg = self.option["color_bg"]).grid(row = 1, column = 2, columnspan = 2)

                def changer_prix():
                    """
                    on prend chaque prix indique et on l'additione avec le prix_assemblage
                    """
                    prix_ = 0.00
                    taille = espace_ingredient.grid_size()[1]

                    for i in range(1, taille-1):
                        try:
                            prix_ += float(espace_ingredient.grid_slaves(row = i, column = 2)[0].get())
                        except:
                            pass

                    prix_ += float(prix_assemblage.get())
                    prix_ = round(prix_, 2)
                    prix.set(str(prix_))

                    espace_ingredient.grid_slaves(row = taille-1, column = 2)[0].destroy()
                    Label(espace_ingredient, text = "Prix total : %s €" %(prix.get()), bg = self.option["color_bg"]).grid(row = taille-1, column = 2, columnspan = 2)

                def changer_prix_ligne(ligne):
                    nom = espace_ingredient.grid_slaves(row = ligne, column = 0)[0].get()
                    prix_poid = self.base.execute("SELECT prix_base, poid_base FROM Ingredients WHERE nom='%s'" %(nom))[0]
                    poid = float(espace_ingredient.grid_slaves(row = ligne, column = 1)[0].get())
                    prix_ = poid * prix_poid[0] / prix_poid[1]
                    prix_ = round(prix_, 2)

                    emplacement = espace_ingredient.grid_slaves(row = ligne, column = 2)[0]
                    emplacement.configure(state = "normal")
                    emplacement.delete("0", "end")
                    emplacement.insert("0", prix_)
                    emplacement.configure(state = "readonly")

                    changer_prix()


                def ajout_ingredient(ingredient):
                    taille = espace_ingredient.grid_size()[1] # on détermine la taille de la grille

                    if espace_ingredient.grid_size()[0] > 2:
                        for i in range(1, taille -1):
                            try:
                                if ingredient == espace_ingredient.grid_slaves(row = i, column = 0)[0].get():
                                    showerror("Présence", "L'ingrédient que vous souhaitez ajoutez et déjà présente dans la brique")
                                    return None
                            except:
                                pass

                    espace_ingredient.grid_slaves(row = taille-1, column = 2)[0].destroy() # on enlève le précédent prix

                    # on ajoute le nom
                    name = Entry(espace_ingredient)
                    name.insert("0", ingredient)
                    name.configure(state = "readonly")
                    name.grid(row = taille -1, column = 0)

                    # on ajoute le poids
                    Spinbox(espace_ingredient, from_ = 0.001, to = 100.000, increment = 0.001, command = lambda x = int("%d" %(taille-1)): changer_prix_ligne(x)).grid(row = taille -1, column = 1)

                    # on affiche le prix
                    prix = Entry(espace_ingredient)
                    prix.insert("0", "0.00")
                    prix.configure(state = "readonly")
                    prix.grid(row = taille -1, column = 2)

                    # on ajoute le bouton
                    Button(espace_ingredient, text = "X", command = lambda x=int("%d" %(taille -1)) : delete_ligne(x), bg = self.option["color_button"]).grid(row = taille -1, column = 3)

                    # le prix
                    Label(espace_ingredient, text = "Prix total : %s €" %(prix.get()), bg = self.option["color_bg"]).grid(row = taille, column = 2, columnspan = 2)

                    changer_prix_ligne(taille-1)

                def delete_ligne(ligne):
                    for elmt in espace_ingredient.grid_slaves(row = ligne):
                        elmt.destroy()

                    changer_prix()

                # prix assemblage
                Label(plus, text = "Prix de la main d'oeuvre :", bg = self.option["color_bg"]).grid(row = 4, column = 0)
                prix_assemblage = Spinbox(plus, from_ = 0.00, to = 100.00, increment = 0.01, command = lambda x=None: changer_prix())
                prix_assemblage.grid(row = 5, column = 0)

                # recette
                Label(plus, text = "Recette :", bg = self.option["color_bg"]).grid(row = 6, column = 0)
                recette = Text(plus, width = 50, height = 20)
                recette.grid(row = 7, column = 0)

                # liste des ingrédients
                Label(plus, text = "Ingrédients disponibles :", bg = self.option["color_bg"]).grid(row = 0, column = 1, columnspan = 2)
                        # scrollbar
                scroll_ingredient = Scrollbar(plus, orient = "vertical", width = 20)
                scroll_ingredient.grid_propagate(0)
                scroll_ingredient.grid(row = 1, column = 1, rowspan = 7, sticky = "NSEW")
                        # listbox
                liste_ingredient = Listbox(plus, yscrollcommand = scroll_ingredient.set, height = 20)
                liste_ingredient.grid(row = 1, column = 2, rowspan = 7, sticky = "NSEW")
                        # configuration scrollbar
                scroll_ingredient.config(command = liste_ingredient.yview)
                    # on insere les briques dans la liste
                liste = self.base.execute("Select nom From Ingredients")
                for i in range(len(liste)):
                    liste_ingredient.insert(i, liste[i][0])

                liste_ingredient.bind("<Double-1>", lambda x : ajout_ingredient(liste_ingredient.get(liste_ingredient.curselection()[0])))

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"]).grid(row = 8, column = 0, columnspan = 4)
            elif self.onglet.get() == "Ingredient":                             ############################################################################################
                plus.iconbitmap("images/icone_ingredient.ico")
                # le nom
                Label(plus, text = "Nom", bg = self.option["color_bg"]).pack()
                nom = Entry(plus)
                nom.pack()

                # le poid
                Label(plus, text = "Poid de conditionnement :", bg = self.option["color_bg"]).pack()
                poid = Spinbox(plus, from_ = 0.001, to = 100.000, increment = 0.001)
                poid.pack()

                # le prix
                Label(plus, text = "Prix à l'unité de conditionnement :", bg = self.option["color_bg"]).pack()
                prix = Spinbox(plus, from_ = 0.01, to = 100.00, increment = 0.01)
                prix.pack()

                # la quantité restante
                Label(plus, text = "Stock :", bg = self.option["color_bg"]).pack()
                quantite = Spinbox(plus, from_ = 0.001, to = 100.000, increment = 0.001)
                quantite.pack()

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"]).pack()

            plus.mainloop()

    def show_information(self, texte):
        """
        on affiche les informations utiles dans self.informations selon self.onglet
        Les informations sont affiché sous la forme d'une liste
        En bas de cette liste, se trouve 2 boutons:
            Un pour modifier les informations
        si une information dépendait d'une autre, celle-ci est automatiquement changé (le prix d'une commande par exemple)
        """
        def clic_recherche(onglet, recherche):
            if onglet == "Client":
                self.commande()
            elif onglet == "Commande":
                self.gateau()
            elif onglet == "Gateau":
                self.brique()
            elif onglet == "Brique":
                self.ingredient()

            self.contenue_barre.set(recherche)

        self.clean_info()

        if self.onglet.get() == "Client":
            ID = texte.split("|")[0][:-1]

            Label(self.information, text = "Client : %s" %(texte), bg = self.option["color_bg"]).pack()
            info_base = self.base.execute("SELECT telephone, mail FROM Client WHERE ID='%s'" %(ID))[0]
            Label(self.information, text = "Tel : " + str(info_base[0]), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Mail : %s" %(info_base[1]), bg = self.option["color_bg"]).pack()

            def historique():
                historique_commande = Toplevel(self.root, bg = self.option["color_bg"])
                historique_commande.title("Historique de Commande")

                liste_commande = self.base.execute("SELECT date_dbt FROM Commandes WHERE ID_client=%s" %(ID))
                for commande in liste_commande:
                    Button(historique_commande, text = commande[0], command = lambda x="%s" %(commande[0]):clic_recherche("Client", x), bg = self.option["color_button"]).pack()

                historique_commande.mainloop()

            Button(self.information, text = "Historique", command = historique, bg = self.option["color_button"]).pack()

        elif self.onglet.get() == "Commande":
            ID = texte.split("|")[0][:-1]
            client = self.base.execute("SELECT Client.ID, nom, prenom FROM Client JOIN Commandes ON Client.ID = Commandes.ID_client WHERE Commandes.ID=%s" %(ID))[0]
            client = "%d | %s" %(client[0], client[1] + " " + client[2])
            info_base = self.base.execute("SELECT prix, livraison, date_dbt, date_fn, date_limite FROM Commandes WHERE ID=%s" %(ID))[0]

            Label(self.information, text = "Client commanditaire : %s" %(client), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Prix : %s €" %(info_base[0]), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Livraison : %s" %(info_base[1]), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Date de commande : %s" %(info_base[2]), bg = self.option["color_bg"]).pack()

            def finish():
                # on met la date actuelle
                date = datetime.datetime.now()
                date = "%d/%d/%d-%d:%d" %(date.day, date.month, date.year, date.hour, date.minute)
                self.base.execute("UPDATE Commandes SET date_fn='%s' WHERE ID=%s" %(date, ID))

                # on supprime les quantité d'ingrtedients utilisé
                liste_gateaux = self.base.execute("SELECT ID_gateaux, personnalisation FROM Composition WHERE ID_commandes=%s" %(ID))
                for i in range(len(liste_gateaux)):
                    liste_gateaux[i] = [*liste_gateaux[i]]
                    liste_gateaux[i][1] = int(liste_gateaux[i][1].split("|")[0].split(", ")[0].split("=")[1])
                    liste_gateaux[i] += [self.base.execute("SELECT nb_parts FROM Gateaux WHERE ID=%d" %(liste_gateaux[i][0]))[0][0]]

                    liste_briques = self.base.execute("SELECT ID_briques, poid_brique FROM Construction WHERE ID_gateaux=%d" %(liste_gateaux[i][0]))
                    for j in range(len(liste_briques)):
                        liste_briques[j] = [*liste_briques[j]]
                        liste_briques[j] += [self.base.execute("SELECT poid FROM Briques WHERE ID=%d" %(liste_briques[j][0]))[0][0]]

                        liste_ingredients = self.base.execute("SELECT ID_ingredients, poids FROM Recettes WHERE ID_briques=%d" %(liste_briques[j][0]))
                        for k in range(len(liste_ingredients)):
                            liste_ingredients[k] = [*liste_ingredients[k]]
                            liste_ingredients[k] += [self.base.execute("SELECT quantite FROM Ingredients WHERE ID=%d" %(liste_ingredients[k][0]))[0][0]]

                        liste_briques[j] += liste_ingredients

                    liste_gateaux[i] += liste_briques

                info = []

                for G in range(len(liste_gateaux)):
                    for B in range(3, len(liste_gateaux[G])):
                        for I in range(3, len(liste_gateaux[G][B])):
                            suppr_ = liste_gateaux[G][1] / liste_gateaux[G][2] # coefficient des briques
                            suppr_ = liste_gateaux[G][B][1] * suppr_
                            suppr_ = suppr_ / liste_gateaux[G][B][2]
                            suppr_ = liste_gateaux[G][B][I][1] * suppr_

                            q_restante = round(liste_gateaux[G][B][I][2] - suppr_, 3)
                            if q_restante < self.base.execute("SELECT poid_base FROM Ingredients WHERE ID=%d" %(liste_gateaux[G][B][I][0]))[0][0]:
                                info += [[self.base.execute("SELECT nom FROM Ingredients WHERE ID=%d" %(liste_gateaux[G][B][I][0])), str(q_restante)]]

                            self.base.execute("UPDATE Ingredients SET quantite=%s WHERE ID=%d" %(q_restante, liste_gateaux[G][B][I][0]))

                for danger in info:
                    showinfo(danger[0], "Quantité restante = %s kg" %(danger[1]))

                self.show_information(texte)

            if info_base[3] == None:
                Label(self.information, text = "Date limite : %s" %(info_base[4]), bg = self.option["color_bg"]).pack()
                """
                affiché temps restant
                """
                Button(self.information, text = "Commande terminé", command = finish, bg = self.option["color_button"]).pack()
            else:
                Label(self.information, text = "Date de fin : %s" %(info_base[3]), bg = self.option["color_bg"]).pack()


            def composition():
                """
                on affiche la liste de tous les gateaux nécessaires
                """
                compo_commande = Toplevel(self.root, bg = self.option["color_bg"])
                compo_commande.title("Composition de la Commande")

                liste_gateaux = self.base.execute("SELECT nom, personnalisation FROM Gateaux, Composition WHERE ID=ID_gateaux AND ID_commandes=%s" %(ID))
                for gateau in range(len(liste_gateaux)):
                    Button(compo_commande, text = liste_gateaux[gateau][0], command = lambda x="%s" %(liste_gateaux[gateau][0]):clic_recherche("Commande", x), bg = self.option["color_button"]).grid(row = gateau, column = 0)
                    Label(compo_commande, text = liste_gateaux[gateau][1], bg = self.option["color_bg"]).grid(row = gateau, column = 1)

                compo_commande.mainloop()

            Button(self.information, text = "Composition", command = composition, bg = self.option["color_button"]).pack()

        elif self.onglet.get() == "Gateau":
            ID = self.base.execute("SELECT ID FROM Gateaux WHERE nom='%s'" %(texte))[0][0]
            info_base = self.base.execute("SELECT type, nb_parts, prix_part, prix_assemblage, marge FROM Gateaux WHERE nom='%s'" %(texte))[0]

            Label(self.information, text = "Gateau : %s" %(texte), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Type : %s" %(info_base[0]), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Nombre de part : %s" %(info_base[1]), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Prix de la main d'oeuvre : " + str(info_base[3]) + " €", bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Prix de la part : " + str(info_base[2]) + " €", bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Marge : " + str(info_base[4]) + " points", bg = self.option["color_bg"]).pack()

            def construction():
                compo_gateau = Toplevel(self.root, bg = self.option["color_bg"])
                compo_gateau.title("Composition du Gateau")

                liste_briques = self.base.execute("SELECT nom, poid_brique FROM Briques, Construction WHERE ID=ID_briques AND ID_gateaux=%s" %(ID))
                for brique in range(len(liste_briques)):
                    Button(compo_gateau, text = liste_briques[brique][0], command = lambda x="%s" %(liste_briques[brique][0]):clic_recherche("Gateau", x), bg = self.option["color_button"]).grid(row = brique, column = 0)
                    Label(compo_gateau, text = "Poid : " + str(liste_briques[brique][1]) + " kg", bg = self.option["color_bg"]).grid(row = brique, column = 1)

                """
                liste de tout les ingredients necessaires
                nombres de gateau faisable
                """

                compo_gateau.mainloop()

            Button(self.information, text = "Construction", command = construction, bg = self.option["color_button"]).pack()

        elif self.onglet.get() == "Brique":
            ID = self.base.execute("SELECT ID FROM Briques WHERE nom='%s'" %(texte))[0][0]
            info_base = self.base.execute("SELECT prix, poid, recette FROM Briques WHERE nom='%s'" %(texte))[0]

            Label(self.information, text = "Nom : %s" %(texte), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Prix : " + str(info_base[0]) + " €", bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Poid : " + str(info_base[1]) + " kg", bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Recette :\n%s" %(info_base[2]), bg = self.option["color_bg"]).pack()

            def ingredient():
                """
                affichage de tous les ingrédients nécessaires
                """
                compo_brique = Toplevel(self.root, bg = self.option["color_bg"])
                compo_brique.title("Composition de la Recette")

                liste_ingredients = self.base.execute("SELECT nom, poids FROM Ingredients, Recettes WHERE ID=ID_ingredients AND ID_briques=%s" %(ID))
                for ingredient in range(len(liste_ingredients)):
                    Button(compo_brique, text = liste_ingredients[ingredient][0], command = lambda x="%s" %(liste_ingredients[ingredient][0]):clic_recherche("Brique", x), bg = self.option["color_button"]).grid(row = ingredient, column = 0)
                    Label(compo_brique, text = "Poid : " + str(liste_ingredients[ingredient][1]) + " kg", bg = self.option["color_bg"]).grid(row = ingredient, column = 1)

                """
                nombres de brique faisable
                """

                compo_brique.mainloop()

            Button(self.information, text = "Ingredients", command = ingredient, bg = self.option["color_button"]).pack()

        elif self.onglet.get() == "Ingredient":
            info_base = self.base.execute("SELECT prix_base, poid_base, quantite FROM Ingredients WHERE nom='%s'" %(texte))[0]

            Label(self.information, text = "Nom : %s" %(texte), bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Poid de conditionnement : " + str(info_base[0]) + " kg", bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Prix à l'unité : " + str(info_base[1]) + " €", bg = self.option["color_bg"]).pack()
            Label(self.information, text = "Quantité restante : " + str(info_base[2]) + " kg", bg = self.option["color_bg"]).pack()

        onglet = self.onglet.get()
        Button(self.information, text = "Modifier les informations", command = lambda x=[texte, onglet]: self.modification(*x), bg = self.option["color_button"]).pack()
        Button(self.information, text = "Supprimer les informations", command = lambda x=[texte, onglet]: self.suppression(*x), bg = self.option["color_button"]).pack()

    def modification(self, element, onglet):
        """
        cette fonction permet de modifier les informations d'un élément dans la base de données:
            info_actuelle   ==>     info_nouv

            VALIDER
            demander validation
        """
        def validation():
            info = []
            sous_info = {}
            taille = modif.grid_size()[1]

            for i in range(taille -1):
                element = modif.grid_slaves(row = i, column = 1)[0]
                if element == liste:
                    sous_taille = element.grid_size()[1]

                    for j in range(sous_taille):
                        sous_element = element.grid_slaves(row = j, column = 1)[0]
                        sous_nom = element.grid_slaves(row = j, column = 0)[0].get()

                        try:
                            sous_info[sous_nom] = sous_element.get("0.0", "end")
                        except:
                            try:
                                sous_info[sous_nom] = sous_element.get("0")
                            except:
                                sous_info[sous_nom] = sous_element.get()
                else:
                    try:
                        info += [element.get("0.0", "end")]
                    except:
                        try:
                            info += [element.get([0])]
                        except:
                            info += [element.get()]


            if onglet == "Client":
                self.base.execute("UPDATE Client SET nom='%s', prenom='%s', telephone=%s, mail='%s' WHERE ID=%s" %(*info, ID))
            elif onglet == "Commande":
                self.base.execute("UPDATE Commandes SET prix=%s, livraison='%s', date_limite='%s' WHERE ID=%s" %(*info, ID))
                # liste de personnalisation
                for nom, perso in sous_info.items():
                    ID_nom = self.base.execute("SELECT ID FROM Gateaux WHERE nom='%s'" %(nom))[0][0]
                    self.base.execute("UPDATE Composition SET personnalisation='%s' WHERE ID_gateaux=%s AND ID_commandes=%s" %(perso, ID_nom, ID))
            elif onglet == "Gateau":
                self.base.execute("UPDATE Gateaux SET type='%s', nom='%s', nb_parts=%s, prix_part=%s, prix_assemblage=%s WHERE ID=%s" %(*info, ID))
                # liste de poid_brique
                for nom, poid in sous_info.items():
                    ID_nom = self.base.execute("SELECT ID FROM Briques WHERE nom='%s'" %(nom))[0][0]
                    self.base.execute("UPDATE Construction SET poid_brique=%s WHERE ID_briques=%s AND ID_gateaux=%s" %(poid, ID_nom, ID))
            elif onglet == "Brique":
                self.base.execute("UPDATE Briques SET nom='%s', prix=%s, poid=%s, recette='%s' WHERE ID=%s" %(*info, ID))
                # liste de poids
                for nom, poid in sous_info.items():
                    ID_nom = self.base.execute("SELECT ID FROM Ingredients WHERE nom='%s'" %(nom))[0][0]
                    self.base.execute("UPDATE Recettes SET poids=%s WHERE ID_ingredients=%s AND ID_briques=%s" %(poid, ID_nom, ID))
            elif onglet == "Ingredient":
                self.base.execute("UPDATE Ingredients SET nom='%s', poid_base=%s, prix_base=%s, quantite=%s WHERE ID=%s" %(*info, ID))

            modif.destroy()
            self.clean_info()

        modif = Toplevel(self.root, bg = self.option["color_bg"])
        modif.title("Modification")
        liste = []


        if onglet == "Client":
            ID = element.split(" |")[0]
            info_base = self.base.execute("SELECT nom, prenom, telephone, mail FROM Client WHERE ID=%s" %(ID))[0]

            # nom
            Label(modif, text = "Nom : ", bg = self.option["color_bg"]).grid(row = 0, column = 0)
            nom = Entry(modif, width = 50)
            nom.insert("0", info_base[0])
            nom.grid(row = 0, column = 1)

            # prenom
            Label(modif, text = "Prenom : ", bg = self.option["color_bg"]).grid(row = 1, column = 0)
            prenom = Entry(modif, width = 50)
            prenom.insert("0", info_base[1])
            prenom.grid(row = 1, column = 1)

            # telephone
            Label(modif, text = "Numero de téléphone : ", bg = self.option["color_bg"]).grid(row = 2, column = 0)
            tel = Entry(modif, width = 50)
            tel.insert("0", info_base[2])
            tel.grid(row = 2, column = 1)

            # e-mail
            Label(modif, text = "Adresse E-mail : ", bg = self.option["color_bg"]).grid(row = 3, column = 0)
            mail = Entry(modif, width = 50)
            mail.insert("0", info_base[3])
            mail.grid(row = 3, column = 1)

            i = 4
        elif onglet == "Commande":
            ID = element.split(" |")[0]
            info_base = self.base.execute("SELECT prix, livraison, date_limite FROM Commandes WHERE ID=%s" %(ID))[0]

            # prix
            Label(modif, text = "Prix de la Commande :", bg = self.option["color_bg"]).grid(row = 0, column = 0)
            prix = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01)
            prix.delete("0", "end")
            prix.insert("0", info_base[0])
            prix.grid(row = 0, column = 1)

            # livraison
            Label(modif, text = "Adresse de livraison : ", bg = self.option["color_bg"]).grid(row = 1, column = 0)
            livraison = Entry(modif, width = 50)
            livraison.insert("0", info_base[1])
            livraison.grid(row = 1, column = 1)

            # date de limite
            Label(modif, text = "Date Limite : ", bg = self.option["color_bg"]).grid(row = 2, column = 0)
            date = Entry(modif, width = 50)
            date.insert("0", info_base[2])
            date.grid(row = 2, column = 1)

            # liste de gateau
            liste = Frame(modif)
            Label(modif, text = "Liste des Gateaux", bg = self.option["color_bg"]).grid(row = 3, column = 0)
            info_plus = self.base.execute("SELECT nom, personnalisation FROM Gateaux, Composition WHERE ID=ID_gateaux AND ID_commandes=%s" %(ID))
            for i in range(len(info_plus)):
                sous_nom = Entry(liste)
                sous_nom.insert("0", info_plus[i][0])
                sous_nom.configure(state = "readonly")
                sous_nom.grid(row = i, column = 0)
                perso = Text(liste, width = 50, height = 5)
                perso.insert("0.0", info_plus[i][1])
                perso.grid(row = i, column = 1)
            liste.grid(row = 3, column = 1)

            i = 4
        elif onglet == "Gateau":
            ID = self.base.execute("SELECT ID FROM Gateaux WHERE nom='%s'" %(element))[0][0]
            info_base = self.base.execute("SELECT type, nom, nb_parts, prix_part, prix_assemblage, marge FROM Gateaux WHERE nom='%s'" %(element))[0]

            # type de gateau
            Label(modif, text = "Type du gateau : ", bg = self.option["color_bg"]).grid(row = 0, column = 0)
            typ = Entry(modif, width = 50)
            typ.insert("0", info_base[0])
            typ.grid(row = 0, column = 1)

            # nom
            Label(modif, text = "Nom du gateau : ", bg = self.option["color_bg"]).grid(row = 1, column = 0)
            nom = Entry(modif, width = 50)
            nom.insert("0", info_base[1])
            nom.grid(row = 1, column = 1)

            # nombre de part
            Label(modif, text = "Nombre de part : ", bg = self.option["color_bg"]).grid(row = 2, column = 0)
            nb_parts = Spinbox(modif, from_ = 0, to = 100, increment = 1)
            nb_parts.delete("0", "end")
            nb_parts.insert("0", info_base[2])
            nb_parts.grid(row = 2, column = 1)

            # prix de l'assemblage
            Label(modif, text = "Prix de l'assemblage : ", bg = self.option["color_bg"]).grid(row = 3, column = 0)
            prix_assemblage = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01)
            prix_assemblage.delete("0", "end")
            prix_assemblage.insert("0", info_base[4])
            prix_assemblage.grid(row = 3, column = 1)

            # prix de la part
            Label(modif, text = "Prix de la part : ", bg = self.option["color_bg"]).grid(row = 4, column = 0)
            prix_part = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01)
            prix_part.delete("0", "end")
            prix_part.insert("0", info_base[3])
            prix_part.grid(row = 4, column = 1)

            # marge
            Label(modif, text = "Marge : ", bg = self.option["color_bg"]).grid(row = 5, column = 0)
            prix_part = Spinbox(modif, from_ = 0.0, to = 1000.0, increment = 0.1)
            prix_part.delete("0", "end")
            prix_part.insert("0", info_base[5])
            prix_part.grid(row = 5, column = 1)

            # liste des briques
            liste = Frame(modif)
            Label(modif, text = "Liste des Briques", bg = self.option["color_bg"]).grid(row = 6, column = 0)
            info_plus = self.base.execute("SELECT Briques.nom, poid_brique FROM Briques, Construction JOIN Gateaux ON Gateaux.ID=ID_gateaux WHERE Briques.ID=ID_briques AND Gateaux.nom='%s'" %(element))
            for i in range(len(info_plus)):
                sous_nom = Entry(liste)
                sous_nom.insert("0", info_plus[i][0])
                sous_nom.configure(state = "readonly")
                sous_nom.grid(row = i, column = 0)
                perso = Spinbox(liste, from_ = 0.000, to = 100.000, increment = 0.001)
                perso.delete("0", "end")
                perso.insert("0", info_plus[i][1])
                perso.grid(row = i, column = 1)
            liste.grid(row = 6, column = 1)

            i = 7
        elif onglet == "Brique":
            ID = self.base.execute("SELECT ID FROM Briques WHERE nom='%s'" %(element))[0][0]
            info_base = self.base.execute("SELECT nom, prix, poid, recette FROM Briques WHERE nom='%s'" %(element))[0]

            # nom
            Label(modif, text = "Nom de la brique : ", bg = self.option["color_bg"]).grid(row = 0, column = 0)
            nom = Entry(modif, width = 50)
            nom.insert("0", info_base[0])
            nom.grid(row = 0, column = 1)

            # prix
            Label(modif, text = "Prix de la brique : ", bg = self.option["color_bg"]).grid(row = 1, column = 0)
            prix = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01)
            prix.delete("0", "end")
            prix.insert("0", info_base[1])
            prix.grid(row = 1, column = 1)

            # poid
            Label(modif, text = "Poid de la Brique :", bg = self.option["color_bg"]).grid(row = 2, column = 0)
            poid = Spinbox(modif, from_ = 0.000, to = 1000.000, increment = 0.001)
            poid.delete("0", "end")
            poid.insert("0", info_base[2])
            poid.grid(row = 2, column = 1)

            # recette
            Label(modif, text = "Recette : ", bg = self.option["color_bg"]).grid(row = 3, column = 0)
            recette = Text(modif, width = 50, height = 10)
            recette.insert("0.0", info_base[3])
            recette.grid(row = 3, column = 1)

            # liste des ingredients
            liste = Frame(modif)
            Label(modif, text = "Liste des Ingredients", bg = self.option["color_bg"]).grid(row = 4, column = 0)
            info_plus = self.base.execute("SELECT Ingredients.nom, poids FROM Ingredients, Recettes JOIN Briques ON Briques.ID=ID_briques WHERE Ingredients.ID=ID_ingredients AND Briques.nom='%s'" %(element))
            for i in range(len(info_plus)):
                sous_nom = Entry(liste)
                sous_nom.insert("0", info_plus[i][0])
                sous_nom.configure(state = "readonly")
                sous_nom.grid(row = i, column = 0)
                perso = Spinbox(liste, from_ = 0.000, to = 100.000, increment = 0.001)
                perso.delete("0", "end")
                perso.insert("0", info_plus[i][1])
                perso.grid(row = i, column = 1)
            liste.grid(row = 4, column = 1)

            i = 5
        elif onglet == "Ingredient":
            ID = self.base.execute("SELECT ID FROM Ingredients WHERE nom='%s'" %(element))[0][0]
            info_base = self.base.execute("SELECT nom, poid_base, prix_base, quantite FROM Ingredients WHERE nom='%s'" %(element))[0]

            # nom
            Label(modif, text = "Nom de l'ingrédient : ", bg = self.option["color_bg"]).grid(row = 0, column = 0)
            nom = Entry(modif, width = 50)
            nom.insert("0", info_base[0])
            nom.grid(row = 0, column = 1)

            # poid d'achat
            Label(modif, text = "Poid de conditionnement :", bg = self.option["color_bg"]).grid(row = 1, column = 0)
            poid = Spinbox(modif, from_ = 0.000, to = 1000.000, increment = 0.001)
            poid.delete("0", "end")
            poid.insert("0", info_base[1])
            poid.grid(row = 1, column = 1)

            # prix d'achat
            Label(modif, text = "Prix à l'unité : ", bg = self.option["color_bg"]).grid(row = 2, column = 0)
            prix = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01)
            prix.delete("0", "end")
            prix.insert("0", info_base[2])
            prix.grid(row = 2, column = 1)

            # quantite restante
            Label(modif, text = "Stock :", bg = self.option["color_bg"]).grid(row = 3, column = 0)
            poid = Spinbox(modif, from_ = 0.000, to = 1000.000, increment = 0.001)
            poid.delete("0", "end")
            poid.insert("0", info_base[3])
            poid.grid(row = 3, column = 1)

            i = 4

        Button(modif, text = "Valider", command = validation, bg = self.option["color_button"]).grid(row = i, column = 0, columnspan = 2)
        modif.mainloop()


    def suppression(self, element, onglet):
        if askyesno("Validation", "Êtes-vous sûr de vouloir supprimer ces informations et toutes celles qui lui sont associées ? (Pour une durée très longue, éternelle)"):
            if onglet == "Client":
                ID = element.split(" | ")[0]
                for id_commande in self.base.execute("SELECT ID FROM Commandes WHERE ID_client = %s" %(ID)):
                    self.base.execute("DELETE FROM Composition WHERE ID_commandes = %d" %(id_commande[0])) # on enleve dans composition
                    self.base.execute("DELETE FROM Commandes WHERE ID = %d" %(id_commande[0])) # on enleve la commande
                self.base.execute("DELETE FROM Client WHERE ID = %s" %(ID)) # on enleve le client de la base
                self.client() # on relance les elements affiché
            elif onglet == "Commande":
                ID = element.split(" | ")[0]
                self.base.execute("DELETE FROM Composition WHERE ID_commandes = %s" %(ID)) # on enleve dans composition
                self.base.execute("DELETE FROM Commandes WHERE ID = %s" %(ID)) # on enleve la commande
                self.commande() # on relance les elements affiché
            elif onglet == "Gateau":
                ID = self.base.execute("SELECT ID FROM Gateaux WHERE nom = '%s'" %(element))[0][0]
                self.base.execute("DELETE FROM Composition WHERE ID_gateaux = %s" %(ID)) # on enleve la composition du gateau
                self.base.execute("DELETE FROM Construction WHERE ID_gateaux = %s" %(ID)) # on enleve la construction du gateau
                self.base.execute("DELETE FROM Gateaux WHERE ID = %s" %(ID)) # on enleve le gateau
                self.gateau() # on relance l'affichage
            elif onglet == "Brique":
                ID = self.base.execute("SELECT ID FROM Briques WHERE nom = '%s'" %(element))[0][0]
                self.base.execute("DELETE FROM Construction WHERE ID_briques = %s" %(ID)) # on enleve la composition des gateaux avec la brique
                self.base.execute("DELETE FROM Recettes WHERE ID_briques = %s" %(ID)) # on enleve la composition des gateaux avec la brique
                self.base.execute("DELETE FROM Briques WHERE ID = %s" %(ID)) # on enleve la brique
                self.brique() # on relance l'affichage
            elif onglet == "Ingredient":
                ID = self.base.execute("SELECT ID FROM Ingredients WHERE nom = '%s'" %(element))[0][0]
                self.base.execute("DELETE FROM Recettes WHERE ID_ingredients = %s" %(ID)) # on enleve la composition des gateaux avec la brique
                self.base.execute("DELETE FROM Ingredients WHERE ID = %s" %(ID)) # on enleve l'ingredient
                self.ingredient() # on relance l'affichage
            self.clean_info()

    def clean_info(self):
        for elmt in self.information.winfo_children():
            elmt.destroy()


def vide(chaine):
    """
    fonction permettant de déterminer si une chaine de caractères est vide
    parametres:
        chaine, une chaine de caracteres
    renvoie un booléen indiquant si la chaine est vide
    """
    lettres = []

    for caractere in chaine:
        if caractere not in lettres:
            lettres += [caractere]

    i = 0
    while i < len(lettres):
        if lettres[i] in [" ", "\n", "\t", "\r"]:
            lettres = lettres[:i] + lettres[i+1:]
            i -= 1
        i += 1

    if lettres == []:
        return True
    else:
        return False

def grid(root, R, C):
    """
    fonction permettant de mettre les élements d'une grille dans un intervalle à l'espace maximum disponible
    parametres:
        root, le fenetre dans laquelle se strouve la grille
        R, un entier qui est l'indice de la dernière ligne a affecté
        C, un entier qui est l'indice de la derniere colonne a affecte
    """
    for i in range(R):
        root.grid_rowconfigure(i, weight=1)
    for i in range(C):
        root.grid_columnconfigure(i, weight=1)


if __name__ == "__main__":
    fenetre = SGBD("base_de_donnees\\DGourmandises.db", "preferences.txt")
    fenetre.lancement()