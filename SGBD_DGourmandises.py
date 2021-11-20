
# SGBD DGourmandises
# fait par Didier Mathias

from tkinter import Tk, Button, Scrollbar, Frame, Entry, Listbox, StringVar, Label, Checkbutton, BooleanVar, Text, Scale, ttk, Spinbox, Toplevel, PhotoImage, Menu
from tkinter.messagebox import showerror, showinfo, askyesno, showwarning, askokcancel
from tkinter.font import Font, families
from tkinter.colorchooser import askcolor
import datetime

import module_database as db
import module_lecture_fichier as read

class SGBD:
    """
    Gestionnaire de la base de données de patisserie
    """
    def __init__(self, base, option, aide):
        """
        constructeur de la classe
        parametres:
            base, une chaine de caracteres, indique le chemin vers la base de données
            option, une chaine de caracteres, indique le chemin vers le fichier des options de l'utilisateur
            aide, une chaine de caracteres, indique le chemin vers le fichier d'aide, la documentation 
        """
        self.base = Base_Gateau(db.database(base))
        self.fichierHelp = aide
        
        self.fichierOpt = option
        option = read.lire_fichier(option)
        dico = {}
        for ligne in option:
            ligne = ligne.split(":")
            dico[ligne[0]] = ligne[1].split("\r")[0]

        self.option = dico

        self.listeButton = []
        self.listeButtonEph = []
        self.listeBg = []
        self.listeBgEph = []

    def ChoiceColor(self, type_):
        color = askcolor()[1]
        if color == None: return False

        self.option[type_] = color # on change la couleur dans le dico

        # update couleur dans fichier
        texte = "%s:%s" %(type_, color)
        if type_ == "color_button":
            texte += "\rcolor_bg:%s\rcolor_txt:%s" %(self.option["color_bg"], self.option["color_txt"])
            for b in self.listeButton: b.configure(bg = color)
            for b in self.listeButtonEph: b.configure(bg = color)
        elif type_ == "color_bg":
            texte += "\rcolor_button:%s\rcolor_txt:%s" %(self.option["color_button"], self.option["color_txt"])
            for b in self.listeBg: b.configure(bg = color)
            for b in self.listeBgEph: b.configure(bg = color)
        elif type_ == "color_txt":
            texte += "\rcolor_button:%s\rcolor_bg:%s" %(self.option["color_button"], self.option["color_bg"])
            for b in self.listeBg: 
                if type(b) not in [Tk, Frame]: b.configure(fg = color)
            for b in self.listeBgEph: b.configure(foreground = color)
            for b in self.listeButton: b.configure(fg = color)
            for b in self.listeButtonEph: b.configure(fg = color)
            self.list.configure(fg = color)
            self.barre.configure(fg = color)

        # ajout option font
        texte += "\rfont_style:%s\rfont_size:%d" %(self.option["font_style"], self.option["font_size"])
        # enregistrement dans fichier
        read.suppr_fichier(self.fichierOpt, False)
        read.add_fichier("", self.fichierOpt, texte)
        return True

    def ChoiceFont(self):

        def FontChange(event):
            if not vide(lbFonts.get()): self.font.configure(family = lbFonts.get())
            if not vide(lbSize.get()): self.font.configure(size = int(lbSize.get()))
            return True

        def Valider():
            self.option["font_style"] = lbFonts.get()
            self.option["font_size"] = lbSize.get()
            texte = "color_bg:%s\rcolor_txt:%s\rcolor_button:%s" %(self.option["color_bg"], self.option["color_txt"], self.option["color_button"])
            texte += "\rfont_style:%s\rfont_size:%s" %(self.option["font_style"], self.option["font_size"])
            
            read.suppr_fichier(self.fichierOpt, False)
            read.add_fichier("", self.fichierOpt, texte)
            fontSelector.destroy()
            return True

        def Annuler():
            self.font.configure(family = self.option["font_style"])
            self.font.configure(size = int(self.option["font_size"]))
            fontSelector.destroy()
            return True

        # initialisation fenetre
        fontSelector = Toplevel(self.root)
        fontSelector.title("Police d'écriture")
        fontSelector.iconbitmap("images/icone_font.ico")
        #placement des font
        available_fonts = [i for i in families()] + ["Helvetica"]
        self.root.option_add("*TCombobox*Listbox*Foreground", self.option["color_txt"])
        lbFonts = MyCombobox(fontSelector, values = available_fonts, state = "readonly", font = self.font)
        lbSize = MyCombobox(fontSelector, values = [i for i in range(5, 31)], state = "readonly", font = self.font)

        for i in range(len(available_fonts)):
            if available_fonts[i] == self.option["font_style"] :
                lbFonts.current(i)
                break
        lbSize.current(int(self.option["font_size"]) - 5) 

        lbFonts.bind('<<ComboboxSelected>>', FontChange)
        lbSize.bind('<<ComboboxSelected>>', FontChange)

        lbFonts.grid(row = 0, column = 0)
        lbSize.grid(row = 0, column = 1)
        Button(fontSelector, command = Valider, text = "Ok", bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 0, sticky = "NSEW")
        Button(fontSelector, command = Annuler, text = "Annuler", bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 1, sticky = "NSEW")

        fontSelector.resizable(width=False, height=False)
        fontSelector.protocol("WM_DELETE_WINDOW", Annuler)
        fontSelector.mainloop()
        return True

    def Help(self):
        read.openFile(self.fichierHelp)
        return True

    def lancement(self):
        # on initialise la fenêtre
        self.root = Tk()
        self.root.title("SGBD DGourmandises")
        self.root.iconbitmap("images/icone.ico")
        self.root.configure(bg = self.option["color_bg"])
        self.listeBg += [self.root]
        self.menu = Frame(self.root)

        self.font = Font(family = self.option["font_style"], size = int(self.option["font_size"]))

        # création menu
        barremenu = Menu(self.root)
        # creation de l'aide
        barremenu.add_command(label = "Aide", underline = 0, command = self.Help)
        # creation du menu de préférences des couleurs
        choiceColor = Menu(barremenu, tearoff=0)
        barremenu.add_cascade(label = "Couleur", underline = 0, menu = choiceColor)
        choiceColor.add_command(label = "Bouton", underline = 0, command = lambda : self.ChoiceColor("color_button"))
        choiceColor.add_command(label = "Background", underline = 0, command = lambda : self.ChoiceColor("color_bg"))
        choiceColor.add_command(label = "Texte", underline = 0, command = lambda : self.ChoiceColor("color_txt"))
        # création du choix de police
        barremenu.add_command(label = "Police", underline = 0, command = self.ChoiceFont)
        # afficher le menu
        self.root.config(menu = barremenu)

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
        b1 = Button(self.menu, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font, anchor = "n", text = "Client", image = image_client, compound = "bottom", command = self.client)
        b2 = Button(self.menu, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font, anchor = "n", text = "Commandes", image = image_commande, compound = "bottom", command = self.commande)
        b3 = Button(self.menu, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font, anchor = "n", text = "Gateaux", image = image_gateau, compound = "bottom", command = self.gateau)
        b4 = Button(self.menu, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font, anchor = "n", text = "Recettes", image = image_recette, compound = "bottom", command = self.brique)
        b5 = Button(self.menu, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font, anchor = "n", text = "Ingrédients", image = image_ingredient, compound = "bottom", command = self.ingredient)

        self.listeButton += [b1, b2, b3, b4, b5]
        for i in range(len(self.listeButton)): self.listeButton[i].grid(row = 0, column = i, sticky="NSEW")

        self.menu.grid(row = 0, column = 0, columnspan = 3, sticky="NSEW")

        # on crée la barre de recherche
        self.contenue_barre = StringVar()

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

        self.barre = Entry(self.root, textvariable = self.contenue_barre, 
                           fg = self.option["color_txt"], font = self.font)
        self.barre.bind("<Return>", recherche)
        self.barre.grid(row = 1, column = 0, columnspan = 2, sticky="EW")

        # on crée la liste des éléments avec la scrollbar
        scrollbar = Scrollbar(self.root, orient = "vertical", width = 20)
        scrollbar.grid_propagate(0)
        scrollbar.grid(row = 2, column = 0, sticky="NSW")

        self.list = Listbox(self.root, yscrollcommand = scrollbar.set, 
                            fg = self.option["color_txt"], font = self.font)
        self.list.grid(row = 2, column = 1, sticky="NSEW")

        scrollbar.config(command = self.list.yview)

        # on crée la variable de sélection (savoir dans quoi on est)
        self.onglet = StringVar()
        self.onglet.set("None")

        # bouton d'ajout
        self.addButton = Button(self.root, text = "(+) Ajout", command = lambda x=self.onglet: self.ajout(x), 
                   bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
        self.addButton.grid(row = 3, column = 0, columnspan = 2, sticky="NSEW")
        self.listeButton += [self.addButton]

        # frame des informations complémentaires
        self.information = Frame(self.root, bg = self.option["color_bg"])
        self.information.grid(row = 1, column = 2, rowspan = 3, sticky="NSEW")
        self.listeBg += [self.information]

        # on gère l'adaptabilité à la fenêtre
        grid(self.menu, 1, 4)
        grid(self.root, 4, 3)
        self.root.grid_columnconfigure(0, weight = 0)
        self.root.grid_rowconfigure(1, weight = 0)
        self.root.grid_columnconfigure(2, weight = 2)

        # on gère le double-clic sur un élément de la liste
        self.list.bind("<Double-1>", lambda x :  self.show_information(self.list.get(self.list.curselection()[0])))
        self.root.mainloop()
        return True

    def GetNum(self, chaine):
        return int(chaine.split(" |")[0])

    def client(self):
        """
        méthode permettant d'afficher la liste des clients dans la listbox
        """
        self.onglet.set("Client")
        self.list.delete(0,'end')

        liste = self.base.GetClients()
        if liste == []:
            self.list.insert(0, "Aucun client n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = str(liste[i][0]) + " | " + liste[i][1] + " " + liste[i][2]
                self.list.insert(i, texte)
        self.addButton.configure(text = "(+) Ajout d'un Client")
        return True

    def commande(self):
        """
        méthode permettant d'afficher la liste des commandes dans la listbox
        """
        self.onglet.set("Commande")
        self.list.delete(0,'end')

        liste = self.base.GetCommandes()
        plus_proche = []
        if liste == []:
            self.list.insert(0, "Aucune commandes n'as été enregistré")
        else:
            demain = datetime.datetime.now() + datetime.timedelta(1)

            for i in range(len(liste)):
                self.list.insert(i, str(liste[i][0]) + " | " + liste[i][1]) # ajout dans listbox

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
        self.addButton.configure(text = "(+) Ajout d'une Commande")
        return True

    def gateau(self):
        """
        méthode permettant d'afficher la liste des gâteaux dans la listbox
        """
        self.onglet.set("Gateau")
        self.list.delete(0,'end')

        liste = self.base.GetGateaux()
        if liste == []:
            self.list.insert(0, "Aucun gateau n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = str(liste[i][0]) + " | " + liste[i][1]
                self.list.insert(i, texte)
        self.addButton.configure(text = "(+) Ajout d'un Gâteau")
        return True

    def brique(self):
        """
        méthode permettant d'afficher la liste des 'briques' dans la listbox
        """
        self.onglet.set("Brique")
        self.list.delete(0,'end')

        liste = self.base.GetBriques()
        if liste == []:
            self.list.insert(0, "Aucune recette n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = str(liste[i][0]) + " | " + liste[i][1]
                self.list.insert(i, texte)
        self.addButton.configure(text = "(+) Ajout d'une Recette")
        return True

    def ingredient(self):
        """
        méthode permettant d'afficher la liste des ingrédients dans la listbox
        """
        self.onglet.set("Ingredient")
        self.list.delete(0,'end')

        liste = self.base.GetIngredients()
        if liste == []:
            self.list.insert(0, "Aucun ingredient n'as été enregistré")
        else:
            for i in range(len(liste)):
                texte = str(liste[i][0]) + " | " + liste[i][1]
                self.list.insert(i, texte)
        self.addButton.configure(text = "(+) Ajout d'un Ingrédient")
        return True

    def ajout(self, onglet):
        """
        méthode permettant d'ajouter un éléments quel qu'il soit
        """
        if self.onglet.get() != "None":
            plus = Toplevel(self.root, bg = self.option["color_bg"])
            if onglet.get() == "Brique" : plus.title("Ajout Recette")
            else: plus.title("Ajout " + onglet.get())
            note = None

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
                liste = []

                if self.onglet.get() == "Client":
                    if not self.base.AddClient(nom.get(), prenom.get(), telephone.get(), email.get()): showerror("Erreur Formulaire", "Oups, il semble qu'il manque des informations, veuillez vérifier les conditions suivantes :\n\t- il y a un nom\n\t- il y a un prénom\n\t- il y a un numéro de téléphone ou un e-mail\n\t- s'il y a un numéro de téléphone, celui-ci est possible")
                    else:
                        plus.destroy()
                        self.client()
                elif self.onglet.get() == "Commande":
                    nbr_gateau = note.grid_size()[1]
                    for ligne in range(1, nbr_gateau): 
                        i = note.grid_slaves(row = ligne, column = 0)
                        if i != []: liste += [[self.GetNum(i[0].get()), note.grid_slaves(row = ligne, column = 3)[0].get(), note.grid_slaves(row = ligne, column = 4)[0].get(), note.grid_slaves(row = ligne, column = 1)[0].get(), note.grid_slaves(row = ligne, column = 2)[0].get("0.0", "end")]]
                    if vide(clients.get()):
                        showerror("Erreur Formulaire", "Oups, il semble qu'il manque des informations, veuillez vérifier les conditions suivantes :\n\t- il y a un client\n\t- il y a un prix non-nul\n\t- il y a au moins un gâteau")
                    elif not self.base.AddCommande(self.GetNum(clients.get()), prix_total.get(), "%s/%s/%s-%s:%s" %(jour.get(), mois.get(), annee.get(), heure.get(), minute.get()), livraison.get(), soldes.get(), liste): 
                        showerror("Erreur Formulaire", "Oups, il semble qu'il manque des informations, veuillez vérifier les conditions suivantes :\n\t- il y a un client\n\t- il y a un prix non-nul\n\t- il y a au moins un gâteau")
                    else:
                        plus.destroy()
                        self.commande()
                elif self.onglet.get() == "Gateau":
                    nbr_brique = espace_brique.grid_size()[1]
                    for ligne in range(1, nbr_brique): 
                        i = espace_brique.grid_slaves(row = ligne, column = 0)
                        if i !=[]: liste += [[self.GetNum(i[0].get()), espace_brique.grid_slaves(row = ligne, column = 1)[0].get()]]
                    if not self.base.AddGateau(type_.get(), nom.get(), nbr_part.get(), prix_part.get()[:-2], prix_assemblage.get(), marge.get()[:3], liste):
                        showerror("Erreur Formulaire", "Oups, il semble qu'il manque des informations, veuillez vérifier les conditions suivantes :\n\t- il y a un type\n\t- il y a un nom\n\t- le nom n'existe pas en double\n\t- il y a au moins une recette")
                    else:
                        plus.destroy()
                        self.gateau()
                elif self.onglet.get() == "Brique":
                    nbr_ingredient = espace_ingredient.grid_size()[1] -1
                    for ligne in range(1, nbr_ingredient): 
                        i = espace_ingredient.grid_slaves(row = ligne, column = 0)
                        if i != []: liste += [[self.GetNum(i[0].get()), espace_ingredient.grid_slaves(row = ligne, column = 1)[0].get()]]
                    if not self.base.AddBrique(nom.get(), prix.get(), poid.get(), recette.get("0.0", "end"), liste): showerror("Erreur Formulaire", "Oups, il semble qu'il manque des informations, veuillez vérifier les conditions suivantes :\n\t- il y a un nom\n\t- le nom n'existe pas en double\n\t- il y a au moins un ingredient")
                    else:
                        plus.destroy()
                        self.brique()
                elif self.onglet.get() == "Ingredient":
                    if not self.base.AddIngredient(nom.get(), poid.get(), prix.get(), quantite.get()): showerror("Erreur Formulaire", "Oups, il semble qu'il manque des informations, veuillez vérifier les conditions suivantes :\n\t- il y a un nom\n\t- le nom n'existe pas en double")
                    else:
                        plus.destroy()
                        self.ingredient()
                return True


            if self.onglet.get() == "Client":
                plus.iconbitmap("images/icone_client.ico")
                # champ nom
                Label(plus, text = "Nom :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
                nom = Entry(plus, fg = self.option["color_txt"], font = self.font)
                nom.grid(row = 1, column = 0, sticky = "NSEW")

                # champ prenom
                Label(plus, text = "Prénom :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
                prenom = Entry(plus, fg = self.option["color_txt"], font = self.font)
                prenom.grid(row = 3, column = 0, sticky = "NSEW")

                # champ numero de telephone
                Label(plus, text = "Numéro de téléphone :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 4, column = 0, sticky = "NSEW")
                telephone = Entry(plus, fg = self.option["color_txt"], font = self.font)
                telephone.grid(row = 5, column = 0, sticky = "NSEW")

                # champ addresse e-mail
                Label(plus, text = "Addresse E-mail :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 6, column = 0, sticky = "NSEW")
                email = Entry(plus, fg = self.option["color_txt"], font = self.font)
                email.grid(row = 7, column = 0, sticky = "NSEW")

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = 8, column = 0, sticky = "NSEW")
                grid(plus, 9, 1)
            elif self.onglet.get() == "Commande":
                plus.iconbitmap("images/icone_commande.ico")
                # on choisit le client
                Label(plus, text = "Client commanditaire :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, columnspan = 5, sticky = "NSEW")

                liste_clients = []
                liste_compose = self.base.GetClients()
                for elmt in liste_compose:
                    liste_clients += [str(elmt[0]) + " | " + elmt[1] + " " + elmt[2]]

                self.root.option_add("*TCombobox*Listbox*Foreground", self.option["color_txt"])
                clients = MyCombobox(plus, values = liste_clients, state = "readonly", font = self.font)
                clients.grid(row = 1, column = 0, columnspan = 5, sticky = "NSEW")

                # on met la possibilité d'une livraison
                Label(plus, text = "Addresse de Livraison :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, columnspan = 4, sticky = "NSW")
                livraison = Entry(plus, fg = self.option["color_txt"], font = self.font)
                livraison.insert("0", "Boutique")
                livraison.grid(row = 3, column = 0, columnspan = 4, sticky = "NSW")

                # on demande une date de fin prévu
                Label(plus, text = "Date de livraison :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 4, column = 0, columnspan = 5, sticky = "NSEW")
                Label(plus, text = "Heure :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 5, column = 0, sticky = "NSEW")
                Label(plus, text = "minute :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 5, column = 1, sticky = "NSEW")
                Label(plus, text = "Jour :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 5, column = 2, sticky = "NSEW")
                Label(plus, text = "Mois :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 5, column = 3, sticky = "NSEW")
                Label(plus, text = "Année :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 5, column = 4, sticky = "NSEW")
                date = datetime.datetime.now()
                jour = Spinbox(plus, from_ = 00, to = 31, increment = 1, width = 3, fg = self.option["color_txt"], font = self.font)
                jour.delete("0", "end")
                jour.insert("0", date.day)
                mois = Spinbox(plus, from_ = 00, to = 12, increment = 1, width = 3, fg = self.option["color_txt"], font = self.font)
                mois.delete("0", "end")
                mois.insert("0", date.month)
                annee = Spinbox(plus, from_ = date.year, to = date.year + 10, width = 4, fg = self.option["color_txt"], font = self.font)
                heure = Spinbox(plus, from_ = 00, to = 23, width = 4, fg = self.option["color_txt"], font = self.font)
                heure.delete("0", "end")
                heure.insert("0", date.hour)
                minute = Spinbox(plus, from_ = 00, to = 59, width = 5, fg = self.option["color_txt"], font = self.font)
                minute.delete("0", "end")
                minute.insert("0", date.minute)

                heure.grid(row = 6, column = 0, sticky = "NSEW")
                minute.grid(row = 6, column = 1, sticky = "NSEW")
                jour.grid(row = 6, column = 2, sticky = "NSEW")
                mois.grid(row = 6, column = 3, sticky = "NSEW")
                annee.grid(row = 6, column = 4, sticky = "NSEW")

                # on affiche les gateaux
                Label(plus, text = "Gâteaux disponibles :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 7, column = 0, columnspan = 5, sticky = "NSEW")
                scroll_gateau = Scrollbar(plus, orient = "vertical", width = 20)
                scroll_gateau.grid_propagate(0)
                scroll_gateau.grid(row = 8, column = 0, sticky = "NSEW")

                liste_gateau = Listbox(plus, yscrollcommand = scroll_gateau.set, height = 20, fg = self.option["color_txt"], font = self.font)
                liste_gateau.grid(row = 8, column = 1, columnspan = 4, sticky = "NSEW")

                scroll_gateau.config(command = liste_gateau.yview)
                    # on insere les gateaux dans la liste
                liste = self.base.GetGateaux()
                for i in range(len(liste)):
                    liste_gateau.insert(i, str(liste[i][0]) + " | " + liste[i][1])

                # Frame de note de fin
                note = Frame(plus, width = 500, bg = self.option["color_bg"])
                note.grid(row = 0, column = 5, rowspan = 8, sticky = "NSEW")

                # on met le prix total
                prix_total = StringVar()
                prix_total.set("0.0")
                Label(note, text = "Gateau :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
                Label(note, text = "Nbr de part :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 1, sticky = "NSEW")
                Label(note, text = "personnalisation :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 2, sticky = "NSEW")
                Label(note, text = "Prix (€):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 3, sticky = "NSEW")
                Label(note, text = "Supplément (€):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 4, sticky = "NSEW")

                Label(note, text = "Prix Total : " + prix_total.get() + " €", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 3, columnspan = 2, sticky = "SE")

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
                    Label(note, text = "Prix Total : " + prix_total.get() + " €", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = nbr_ligne, column = 3, columnspan = 2, sticky = "NSEW")
                    return True

                # on met la case de solde
                Label(plus, text = "Soldes (%):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 4, sticky = "NSE")
                soldes = Spinbox(plus, from_ = 0, to = 100, increment = 1, width = 5, command = lambda x=None : change_prix(), fg = self.option["color_txt"], font = self.font)
                soldes.grid(row = 3, column = 4, sticky = "NSE")

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
                        prix_part = float(self.base.GetGateau(self.GetNum(selection))[4])
                        prix_assemblage = float(self.base.GetGateau(self.GetNum(selection))[3])
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
                        return True

                    def delete_ligne(ligne):
                        """
                        sous-sous-fonction permettant de supprimer une ligne de la commande
                        """
                        for elmt in note.grid_slaves(row = ligne):
                            elmt.destroy()

                        change_prix()
                        return True

                    # regarder si le gateau n'est pas déjà dans note, si c'est le cas, on affiche une erreur = "gateau déjà présent"
                    if note.grid_size()[1] > 2:
                        for i in range(1, note.grid_size()[1] -1):
                            if note.grid_slaves(row = i, column = 0) != []:
                                if note.grid_slaves(row = i, column = 0)[0].get() == gateau:
                                    showerror("Présence", "Le gâteau que vous souhaitez ajoutez et déjà présent dans la commande")
                                    return None

                    # on enlève la dernière ligne contenant le prix total
                    taille = note.grid_size()[1]
                    note.grid_slaves(row = taille -1)[0].destroy()

                    # on insère la ligne
                        # nom du gateau (pour être récupérer)
                    nouv_ligne = Entry(note, fg = self.option["color_txt"], font = self.font)
                    nouv_ligne.insert("0", gateau)
                    nouv_ligne.configure(state = "readonly")
                    nouv_ligne.grid(row = taille -1, column = 0, sticky = "NSEW")
                        # nombre de parts
                    Spinbox(note, command = lambda x=int("%d" %(taille-1)) :change_prix_ligne(x), from_ = 1, to = 50, increment = 1, width = 5, 
                            fg = self.option["color_txt"], font = self.font).grid(row = taille-1, column = 1, sticky = "NSEW")
                        # personnalisation
                    Text(note, height = 2, width = 20, fg = self.option["color_txt"], font = self.font).grid(row = taille-1, column = 2, sticky = "NSEW")
                        # prix du gateau
                    nouv_prix = Entry(note, fg = self.option["color_txt"], font = self.font)
                    nouv_prix.insert("0", "0.00")
                    nouv_prix.configure(state = "readonly")
                    nouv_prix.grid(row = taille -1, column  = 3, sticky = "NSEW")
                        # prix supplémentaires
                    Spinbox(note, command = lambda x=int("%d" %(taille-1)) :change_prix_ligne(x), from_ = 0.00, to = 100.00, increment = 0.01, width = 10, 
                            fg = self.option["color_txt"], font = self.font).grid(row = taille-1, column = 4, sticky = "NSEW")
                        # bouton de suppression
                    Button(note, text = "X", command = lambda x=int("%d" %(taille-1)) : delete_ligne(x), 
                           bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = taille-1, column = 5, sticky = "NSEW")

                    # on met la dernière ligne contenant le prix total
                    Label(note, text = "Prix Total : " + prix_total.get() + " €", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = taille, column = 3, columnspan = 3, sticky = "NSEW")
                    change_prix_ligne(taille -1)
                    return True

                liste_gateau.bind("<Double-1>", lambda x :  ajout_gateau(liste_gateau.get(liste_gateau.curselection()[0])))

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = 9, column = 0, columnspan = 6, sticky = "NSEW")
                grid(plus, 10, 7)
            elif self.onglet.get() == "Gateau":
                plus.iconbitmap("images/icone_gateau.ico")
                espace_brique = Frame(plus, width = 200, bg = self.option["color_bg"])
                Label(espace_brique, text = "Nom :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
                Label(espace_brique, text = "Poid (g):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 1, sticky = "NSEW")

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
                        i = espace_brique.grid_slaves(row = ligne, column = 0)
                        if i != []:
                            prix_poid = self.base.GetBrique(self.GetNum(i[0].get()))
                            poid_choisi = float(espace_brique.grid_slaves(row = ligne, column = 1)[0].get())
                            prix += (poid_choisi * prix_poid[1] / prix_poid[2])

                    cout_ingredient = prix
                    prix += float(prix_assemblage.get())
                    if cout_ingredient != 0: point_marge = prix / cout_ingredient
                    else: point_marge = 0
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
                    return True

                def ajout_brique(brique):
                    taille = espace_brique.grid_size()[1] # on détermine la taille de la grille

                    if espace_brique.grid_size()[1] > 1:
                        for i in range(1, taille):
                            if brique == espace_brique.grid_slaves(row = i, column = 0)[0].get():
                                showerror("Présence", "La recette que vous souhaitez ajoutez et déjà présente dans le gateau")
                                return None

                    # on ajoute le nom
                    name = Entry(espace_brique, fg = self.option["color_txt"], font = self.font)
                    name.insert("0", brique)
                    name.configure(state = "readonly")
                    name.grid(row = taille, column = 0, sticky = "NSEW")

                    # on ajoute le poids
                    Spinbox(espace_brique, from_ = 1, to = 1000000, increment = 1, command = changer_prix, 
                            fg = self.option["color_txt"], font = self.font).grid(row = taille, column = 1, sticky = "NSEW")

                    # on ajoute le bouton
                    Button(espace_brique, text = "X", command = lambda x=int("%d" %(taille)) : delete_ligne(x), 
                           bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = taille, column = 2, sticky = "NSEW")

                    changer_prix()
                    return True

                def delete_ligne(ligne):
                    for elmt in espace_brique.grid_slaves(row = ligne):
                        elmt.destroy()

                    changer_prix()
                    return True

                # le type de gateau
                Label(plus, text = "Type de Gateau :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
                type_ = Entry(plus, fg = self.option["color_txt"], font = self.font)
                type_.grid(row = 1, column = 0, sticky = "NSEW")

                # le nom du gateau
                Label(plus, text = "Nom du Gateau :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
                nom = Entry(plus, fg = self.option["color_txt"], font = self.font)
                nom.grid(row = 3, column = 0, sticky = "NSEW")

                # le nombre de part
                Label(plus, text = "Nombre de part :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 4, column = 0, sticky = "NSEW")
                nbr_part = Spinbox(plus, from_ = 1, to = 100, increment = 1, command = changer_prix, fg = self.option["color_txt"], font = self.font)
                nbr_part.grid(row = 5, column = 0, sticky = "NSEW")

                # le prix de l'assemblage
                Label(plus, text = "Prix de la main d'oeuvre (€):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 6, column = 0, sticky = "NSEW")
                prix_assemblage = Spinbox(plus, from_ = 0.00, to = 100.00, increment = 0.01, command = changer_prix, fg = self.option["color_txt"], font = self.font)
                prix_assemblage.grid(row = 7, column = 0, sticky = "NSEW")

                # Le prix de la part
                Label(plus, text = "Prix de la part (€):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 8, column = 0, sticky = "NSW")
                prix_part = Entry(plus, width = 10, fg = self.option["color_txt"], font = self.font)
                prix_part.insert("0", "0.0 €")
                prix_part.configure(state = "readonly")
                prix_part.grid(row = 9, column = 0, sticky = "NSW")

                # la marge
                Label(plus, text = "marge :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 8, column = 0, sticky = "NSE")
                marge = Entry(plus, width = 10, fg = self.option["color_txt"], font = self.font)
                marge.insert("0", "0.0 points")
                marge.configure(state = "readonly")
                marge.grid(row = 9, column = 0, sticky = "NSE")

                # les briques
                    # l'espace necessaires
                espace_brique.grid(row = 0, column = 3, rowspan = 10, sticky = "NSEW")
                    # l'affichage des briques avec une scrollbar
                Label(plus, text = "Recettes disponibles :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 1, columnspan = 2, sticky = "NSEW")
                        # scrollbar
                scroll_brique = Scrollbar(plus, orient = "vertical", width = 20)
                scroll_brique.grid_propagate(0)
                scroll_brique.grid(row = 1, column = 1, rowspan = 9, sticky = "NSEW")
                        # listbox
                liste_brique = Listbox(plus, yscrollcommand = scroll_brique.set, height = 10, fg = self.option["color_txt"], font = self.font)
                liste_brique.grid(row = 1, column = 2, rowspan = 9, sticky = "NSEW")
                        # configuration scrollbar
                scroll_brique.config(command = liste_brique.yview)
                    # on insere les briques dans la liste
                liste = self.base.GetBriques()
                for i in range(len(liste)):
                    liste_brique.insert(i, str(liste[i][0]) + " | " + liste[i][1])

                liste_brique.bind("<Double-1>", lambda x : ajout_brique(liste_brique.get(liste_brique.curselection()[0])))

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = 12, column = 0, columnspan = 4, sticky = "NSEW")
                grid(plus, 13, 5)
            elif self.onglet.get() == "Brique":
                plus.iconbitmap("images/icone_recette.ico")
                # le nom de la brique
                Label(plus, text = "Nom de la Recette :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
                nom = Entry(plus, fg = self.option["color_txt"], font = self.font)
                nom.grid(row = 1, column = 0, sticky = "NSEW")

                # le poid de la brique
                Label(plus, text = "Poids de la préparation (g):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
                poid = Spinbox(plus, from_ = 1, to = 1000000, increment = 1, fg = self.option["color_txt"], font = self.font)
                poid.grid(row = 3, column = 0, sticky = "NSEW")

                # espace ingrédients
                espace_ingredient = Frame(plus, bg = self.option["color_bg"])
                espace_ingredient.grid(row = 0, column = 3, rowspan = 8, sticky = "NSEW")
                Label(espace_ingredient, text = "Nom :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
                Label(espace_ingredient, text = "Poids (g):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 1, sticky = "NSEW")
                Label(espace_ingredient, text = "Prix (€):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 2, sticky = "NSEW")

                # le prix
                prix = StringVar()
                prix.set("0.00")
                Label(espace_ingredient, text = "Prix total : %s €" %(prix.get()), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 2, columnspan = 2, sticky = "NSEW")

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
                    Label(espace_ingredient, text = "Prix total : %s €" %(prix.get()), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = taille-1, column = 2, columnspan = 2, sticky = "NSEW")
                    return True

                def changer_prix_ligne(ligne):
                    prix_poid = self.base.GetIngredient(self.GetNum(espace_ingredient.grid_slaves(row = ligne, column = 0)[0].get()))
                    poid = float(espace_ingredient.grid_slaves(row = ligne, column = 1)[0].get())
                    prix_ = poid * prix_poid[2] / prix_poid[1]
                    prix_ = round(prix_, 2)

                    emplacement = espace_ingredient.grid_slaves(row = ligne, column = 2)[0]
                    emplacement.configure(state = "normal")
                    emplacement.delete("0", "end")
                    emplacement.insert("0", prix_)
                    emplacement.configure(state = "readonly")

                    changer_prix()
                    return True 

                def ajout_ingredient(ingredient):
                    taille = espace_ingredient.grid_size()[1] # on détermine la taille de la grille

                    if espace_ingredient.grid_size()[0] > 2:
                        for i in range(1, taille -1):
                            if espace_ingredient.grid_slaves(row = i, column = 0) != []:
                                if ingredient == espace_ingredient.grid_slaves(row = i, column = 0)[0].get():
                                    showerror("Présence", "L'ingrédient que vous souhaitez ajoutez et déjà présent dans la recette")
                                    return None

                    espace_ingredient.grid_slaves(row = taille-1, column = 2)[0].destroy() # on enlève le précédent prix

                    # on ajoute le nom
                    name = Entry(espace_ingredient, fg = self.option["color_txt"], font = self.font)
                    name.insert("0", ingredient)
                    name.configure(state = "readonly")
                    name.grid(row = taille -1, column = 0, sticky = "NSEW")
                    
                    # on ajoute le poids
                    Spinbox(espace_ingredient, from_ = 1, to = 1000000, increment = 1, command = lambda x = int("%d" %(taille-1)): changer_prix_ligne(x), 
                            fg = self.option["color_txt"], font = self.font).grid(row = taille -1, column = 1, sticky = "NSEW")

                    # on affiche le prix
                    prix = Entry(espace_ingredient, fg = self.option["color_txt"], font = self.font)
                    prix.insert("0", "0.00")
                    prix.configure(state = "readonly")
                    prix.grid(row = taille -1, column = 2, sticky = "NSEW")

                    # on ajoute le bouton
                    Button(espace_ingredient, text = "X", command = lambda x=int("%d" %(taille -1)) : delete_ligne(x), 
                           bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = taille -1, column = 3, sticky = "NSEW")

                    # le prix
                    Label(espace_ingredient, text = "Prix total : %s €" %(prix.get()), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = taille, column = 2, columnspan = 2, sticky = "NSEW")

                    changer_prix_ligne(taille-1)
                    return True

                def delete_ligne(ligne):
                    for elmt in espace_ingredient.grid_slaves(row = ligne):
                        elmt.destroy()

                    changer_prix()
                    return True

                # prix assemblage
                Label(plus, text = "Prix de la main d'oeuvre (€):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 4, column = 0, sticky = "NSEW")
                prix_assemblage = Spinbox(plus, from_ = 0.00, to = 100.00, increment = 0.01, command = lambda x=None: changer_prix(), fg = self.option["color_txt"], font = self.font)
                prix_assemblage.grid(row = 5, column = 0, sticky = "NSEW")

                # recette
                Label(plus, text = "Recette :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 6, column = 0, sticky = "NSEW")
                recette = Text(plus, width = 50, height = 20, fg = self.option["color_txt"], font = self.font)
                recette.grid(row = 7, column = 0, sticky = "NSEW")

                # liste des ingrédients
                Label(plus, text = "Ingrédients disponibles :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 1, columnspan = 2, sticky = "NSEW")
                        # scrollbar
                scroll_ingredient = Scrollbar(plus, orient = "vertical", width = 20)
                scroll_ingredient.grid_propagate(0)
                scroll_ingredient.grid(row = 1, column = 1, rowspan = 7, sticky = "NSEW")
                        # listbox
                liste_ingredient = Listbox(plus, yscrollcommand = scroll_ingredient.set, height = 20, fg = self.option["color_txt"], font = self.font)
                liste_ingredient.grid(row = 1, column = 2, rowspan = 7, sticky = "NSEW")
                        # configuration scrollbar
                scroll_ingredient.config(command = liste_ingredient.yview)
                    # on insere les briques dans la liste
                liste = self.base.GetIngredients()
                for i in range(len(liste)):
                    liste_ingredient.insert(i, str(liste[i][0]) + " | " + liste[i][1])

                liste_ingredient.bind("<Double-1>", lambda x : ajout_ingredient(liste_ingredient.get(liste_ingredient.curselection()[0])))

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = 8, column = 0, columnspan = 4, sticky = "NSEW")
                grid(plus, 9, 4)
            elif self.onglet.get() == "Ingredient":                             ############################################################################################
                plus.iconbitmap("images/icone_ingredient.ico")
                # le nom
                Label(plus, text = "Nom :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
                nom = Entry(plus, fg = self.option["color_txt"], font = self.font)
                nom.grid(row = 1, column = 0, sticky = "NSEW")

                # le poid
                Label(plus, text = "Poid de conditionnement (g):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
                poid = Spinbox(plus, from_ = 1, to = 1000000, increment = 1, fg = self.option["color_txt"], font = self.font)
                poid.grid(row = 3, column = 0, sticky = "NSEW")

                # le prix
                Label(plus, text = "Prix à l'unité de conditionnement (€):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 4, column = 0, sticky = "NSEW")
                prix = Spinbox(plus, from_ = 0.01, to = 100.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
                prix.grid(row = 5, column = 0, sticky = "NSEW")

                # la quantité restante
                Label(plus, text = "Stock (g):", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 6, column = 0, sticky = "NSEW")
                quantite = Spinbox(plus, from_ = 1, to = 1000000, increment = 1, fg = self.option["color_txt"], font = self.font)
                quantite.grid(row = 7, column = 0, sticky = "NSEW")

                Button(plus, text = "Valider", command = validation, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = 8, column = 0, sticky = "NSEW")
                grid(plus, 9, 1)

            plus.protocol("WM_DELETE_WINDOW", lambda : on_closing(plus))
            plus.mainloop()
            return True
    
    def show_information(self, texte):
        """
        on affiche les informations utiles dans self.informations selon self.onglet
        Les informations sont affiché sous la forme d'une liste
        En bas de cette liste, se trouve 2 boutons:
            Un pour modifier les informations
        si une information dépendait d'une autre, celle-ci est automatiquement changé (le prix d'une commande par exemple)
        """
        def clic_recherche(onglet, recherche):
            if onglet == "Client": self.commande()
            elif onglet == "Commande": self.gateau()
            elif onglet == "Gateau": self.brique()
            elif onglet == "Brique": self.ingredient()
            self.contenue_barre.set(recherche)
            return True

        self.clean_info()
        self.listeButtonEph = []
        self.listeBgEph = []
        
        ID = self.GetNum(texte)
        if self.onglet.get() == "Client":
            info_base = self.base.GetClient(ID)
            # affichage informations
            c = Label(self.information, text = "Client : %s %s" %(info_base[0], info_base[1]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            t = Label(self.information, text = "Tel : " + str(info_base[2]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            m = Label(self.information, text = "Mail : %s" %(info_base[3]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            self.listeBgEph += [c, t, m]
            # gestion du bouton pour l'historique
            def historique():
                historique_commande = Toplevel(self.root, bg = self.option["color_bg"])
                historique_commande.iconbitmap("images/icone_information.ico")
                historique_commande.title("Historique de Commande")

                liste_commande = self.base.GetHistorique(ID)
                for i in range(len(liste_commande)):
                    Button(historique_commande, text = liste_commande[i][0], command = lambda x="%s" %(liste_commande[i][0]):clic_recherche("Client", x), 
                           bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = i, column = 0, sticky = "NSEW")
                grid(historique_commande, len(liste_commande), 1)
                historique_commande.mainloop()
                return True

            h = Button(self.information, text = "Historique", command = historique, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
            self.listeButtonEph += [h]
        elif self.onglet.get() == "Commande":
            info_base = self.base.GetCommande(ID)
            info_client = self.base.GetClient(info_base[0])
            client = "%d | %s" %(info_base[0], info_client[0] + " " + info_client[1])

            c1 = Label(self.information, text = "Client commanditaire : %s" %(client), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            p = Label(self.information, text = "Prix : %s €" %(info_base[1]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            l = Label(self.information, text = "Livraison : %s" %(info_base[2]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            d = Label(self.information, text = "Date de commande : %s" %(info_base[3]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            self.listeBgEph += [c1, p, l, d]

            def finish():
                info = self.base.FinishCommande(ID)
                for danger in info:
                    showinfo(danger[0], "Quantité restante = %s g" %(danger[1]))

                self.show_information(texte)
                return True
                
            def composition():
                """
                on affiche la liste de tous les gateaux nécessaires
                """
                compo_commande = Toplevel(self.root, bg = self.option["color_bg"])
                compo_commande.iconbitmap("images/icone_information.ico")
                compo_commande.title("Composition de la Commande")

                liste_gateaux = self.base.GetCompositionCommande(ID)
                for gateau in range(len(liste_gateaux)):
                    Button(compo_commande, text = liste_gateaux[gateau][1], command = lambda x="%s" %(liste_gateaux[gateau][1]):clic_recherche("Commande", x), 
                           bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = gateau, column = 0, sticky = "NSEW")
                    Label(compo_commande, text = "Prix : " + str(liste_gateaux[gateau][2]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = gateau, column = 1, sticky = "NSEW")
                    Label(compo_commande, text = "Supplément : " + str(liste_gateaux[gateau][3]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = gateau, column = 2, sticky = "NSEW")
                    Label(compo_commande, text = "Nb de parts : " + str(liste_gateaux[gateau][4]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = gateau, column = 3, sticky = "NSEW")
                    Label(compo_commande, text = "Personnalisation : " + str(liste_gateaux[gateau][5]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = gateau, column = 4, sticky = "NSEW")

                grid(compo_commande, len(liste_gateaux), 4)
                compo_commande.mainloop()
                return True

            # on affiche selon la présence d'une date de fin
            if info_base[4] == None:
                d1 = Label(self.information, text = "Date limite : %s" %(info_base[5]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
                c = Button(self.information, text = "Commande terminé", command = finish, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
                self.listeButtonEph += [c]
            else:
                d1 = Label(self.information, text = "Date de fin : %s" %(info_base[4]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            self.listeBgEph += [d1]

            c1 = Button(self.information, text = "Composition", command = composition, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
            self.listeButtonEph += [c1]
        elif self.onglet.get() == "Gateau":
            info_base = self.base.GetGateau(ID)

            g = Label(self.information, text = "Gateau : %s" %(info_base[1]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            t = Label(self.information, text = "Type : %s" %(info_base[0]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            n = Label(self.information, text = "Nombre de part : %s" %(info_base[2]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            pm = Label(self.information, text = "Prix de la main d'oeuvre : " + str(info_base[3]) + " €", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            pp = Label(self.information, text = "Prix de la part : " + str(info_base[4]) + " €", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            m = Label(self.information, text = "Marge : " + str(info_base[5]) + " points", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            self.listeBgEph += [g, t, n, pm, pp, m]

            # gestion des éléments du gateau
            def construction():
                compo_gateau = Toplevel(self.root, bg = self.option["color_bg"])
                compo_gateau.iconbitmap("images/icone_information.ico")
                compo_gateau.title("Composition du Gateau")

                liste_briques = self.base.GetConstructionGateau(ID)
                for brique in range(len(liste_briques)):
                    Button(compo_gateau, text = liste_briques[brique][1], command = lambda x="%s" %(liste_briques[brique][1]):clic_recherche("Gateau", x), 
                           bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = brique, column = 0, sticky = "NSEW")
                    Label(compo_gateau, text = "Poid : " + str(liste_briques[brique][2]) + " g", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = brique, column = 1, sticky = "NSEW")
                grid(compo_gateau, len(liste_briques), 2)
                compo_gateau.mainloop()
                return True

            c = Button(self.information, text = "Construction", command = construction, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
            self.listeButtonEph += [c]
        elif self.onglet.get() == "Brique":
            info_base = self.base.GetBrique(ID)

            n = Label(self.information, text = "Nom : %s" %(info_base[0]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            pr = Label(self.information, text = "Prix : " + str(info_base[1]) + " €", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            po = Label(self.information, text = "Poid : " + str(info_base[2]) + " g", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            r = Label(self.information, text = "Recette :\n%s" %(info_base[3]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            self.listeBgEph += [n, pr, po, r]

            def ingredient():
                """
                affichage de tous les ingrédients nécessaires
                """
                compo_brique = Toplevel(self.root, bg = self.option["color_bg"])
                compo_brique.iconbitmap("images/icone_information.ico")
                compo_brique.title("Composition de la Recette")

                liste_ingredients = self.base.GetContenuBrique(ID)
                for ingredient in range(len(liste_ingredients)):
                    Button(compo_brique, text = liste_ingredients[ingredient][1], command = lambda x="%s" %(liste_ingredients[ingredient][1]):clic_recherche("Brique", x), 
                           bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = ingredient, column = 0, sticky = "NSEW")
                    Label(compo_brique, text = "Poid : " + str(liste_ingredients[ingredient][2]) + " g", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = ingredient, column = 1, sticky = "NSEW")
                grid(compo_brique, len(liste_ingredients), 2)
                compo_brique.mainloop()
                return True

            i = Button(self.information, text = "Ingredients", command = ingredient, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
            self.listeBgEph += [i]
        elif self.onglet.get() == "Ingredient":
            info_base = self.base.GetIngredient(ID)

            n = Label(self.information, text = "Nom : %s" %(info_base[0]), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            po = Label(self.information, text = "Poid de conditionnement : " + str(info_base[1]) + " g", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            pr = Label(self.information, text = "Prix à l'unité : " + str(info_base[2]) + " €", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            q = Label(self.information, text = "Quantité restante : " + str(info_base[3]) + " g", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            u = Label(self.information, text = "Unité de conditionnement restantes : " + str(round(info_base[3] / info_base[1], 2)), bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font)
            self.listeBgEph += [n, po, pr, q, u]

        onglet = self.onglet.get()
        m = Button(self.information, text = "Modifier les informations", command = lambda x=[texte, onglet]: self.modification(*x), bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
        s = Button(self.information, text = "Supprimer les informations", command = lambda x=[texte, onglet]: self.suppression(*x), bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font)
        self.listeButtonEph += [m, s]
        
        for elmt in self.listeBgEph: elmt.pack()
        for elmt in self.listeButtonEph: elmt.pack()
        return True

    def modification(self, element, onglet):
        """
        cette fonction permet de modifier les informations d'un élément dans la base de données:
            info_actuelle   ==>     info_nouv

            VALIDER
            demander validation
        """
        def validation():
            info = []
            taille = modif.grid_size()[1]

            for i in range(taille -1):
                element = modif.grid_slaves(row = i, column = 1)[0]
                if element == liste:
                    sous_taille = element.grid_size()[1]
                    sousListe = []
                    for j in range(sous_taille):
                        sous_element = element.grid_slaves(row = j, column = 1)[0]
                        if not(onglet == "Commande" and j == 0):
                            sous_nom = self.GetNum(element.grid_slaves(row = j, column = 0)[0].get())

                            if onglet == "Commande":
                                sousListe += [[sous_nom, sous_element.get(), element.grid_slaves(row = j, column = 2)[0].get(), element.grid_slaves(row = j, column = 3)[0].get(), element.grid_slaves(row = j, column = 4)[0].get("0.0", "end")]]
                            else:
                                if type(sous_element) == Text:
                                    sousListe += [[sous_nom, sous_element.get("0.0", "end")]]
                                elif type(sous_element) == Entry:
                                    sousListe += [[sous_nom, sous_element.get("0")]]
                                else:
                                    sousListe += [[sous_nom, sous_element.get()]]
                    info += [sousListe]
                else:
                    if type(element) == Text:
                        info += [element.get("0.0", "end")]
                    else:
                        info += [element.get()]


            if onglet == "Client": self.base.ModifClient(ID, *info)
            elif onglet == "Commande": self.base.ModifCommande(ID, *info)
            elif onglet == "Gateau": self.base.ModifGateau(ID, *info)
            elif onglet == "Brique": self.base.ModifBrique(ID, *info)
            elif onglet == "Ingredient": self.base.ModifIngredient(ID, *info)

            modif.destroy()
            self.clean_info()
            return True

        modif = Toplevel(self.root, bg = self.option["color_bg"])
        modif.iconbitmap("images/icone_modification.ico")
        modif.title("Modification")
        liste = []

        ID = self.GetNum(element)
        if onglet == "Client":
            info_base = self.base.GetClient(ID)

            # nom
            Label(modif, text = "Nom : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
            nom = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            nom.insert("0", info_base[0])
            nom.grid(row = 0, column = 1, sticky = "NSEW")

            # prenom
            Label(modif, text = "Prenom : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 0, sticky = "NSEW")
            prenom = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            prenom.insert("0", info_base[1])
            prenom.grid(row = 1, column = 1, sticky = "NSEW")

            # telephone
            Label(modif, text = "Numero de téléphone : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
            tel = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            if info_base[2] != None: tel.insert("0", str(info_base[2]))
            tel.grid(row = 2, column = 1, sticky = "NSEW")

            # e-mail
            Label(modif, text = "Adresse E-mail : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 3, column = 0, sticky = "NSEW")
            mail = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            if info_base[3] != None: mail.insert("0", str(info_base[3]))
            mail.grid(row = 3, column = 1, sticky = "NSEW")

            i = 4
        elif onglet == "Commande":
            info_base = self.base.GetCommande(ID)

            # prix
            Label(modif, text = "Prix de la Commande :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
            prix = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
            prix.delete("0", "end")
            prix.insert("0", info_base[1])
            prix.grid(row = 0, column = 1, sticky = "NSEW")

            # livraison
            Label(modif, text = "Adresse de livraison : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 0, sticky = "NSEW")
            livraison = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            livraison.insert("0", info_base[2])
            livraison.grid(row = 1, column = 1, sticky = "NSEW")

            # date de limite
            Label(modif, text = "Date Limite : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
            date = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            date.insert("0", info_base[5])
            date.grid(row = 2, column = 1, sticky = "NSEW")

            # liste de gateau
            liste = Frame(modif, bg = self.option["color_bg"])
            Label(modif, text = "Liste des Gateaux", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 3, column = 0, sticky = "NSEW")
            Label(liste, text = "Nom :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
            Label(liste, text = "Prix :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 1, sticky = "NSEW")
            Label(liste, text = "Supplément :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 2, sticky = "NSEW")
            Label(liste, text = "Nb de parts :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 3, sticky = "NSEW")
            Label(liste, text = "Personnalisation :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 4, sticky = "NSEW")
            info_plus = self.base.GetCompositionCommande(ID)
            for i in range(len(info_plus)):
                # nom
                sous_nom = Entry(liste, fg = self.option["color_txt"], font = self.font)
                sous_nom.insert("0", str(info_plus[i][0]) + " | " + info_plus[i][1])
                sous_nom.configure(state = "readonly")
                sous_nom.grid(row = i+1, column = 0, sticky = "NSEW")
                # prix
                prix = Spinbox(liste, from_ = 0.00, to = 1000.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
                prix.delete("0", "end")
                prix.insert("0", info_plus[i][2])
                prix.grid(row = i+1, column = 1, sticky = "NSEW")
                # supplement
                suppl = Spinbox(liste, from_ = 0.00, to = 1000.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
                suppl.delete("0", "end")
                suppl.insert("0", info_plus[i][3])
                suppl.grid(row = i+1, column = 2, sticky = "NSEW")
                # nbr_parts
                nbrParts = Spinbox(liste, from_ = 0, to = 1000, increment = 1, fg = self.option["color_txt"], font = self.font)
                nbrParts.delete("0", "end")
                nbrParts.insert("0", info_plus[i][4])
                nbrParts.grid(row = i+1, column = 3, sticky = "NSEW")
                # personnalisation
                perso = Text(liste, width = 50, height = 5, fg = self.option["color_txt"], font = self.font)
                perso.insert("0.0", info_plus[i][5])
                perso.grid(row = i+1, column = 4, sticky = "NSEW")
            liste.grid(row = 3, column = 1)
            grid(liste, len(info_plus), 5)

            i = 4
        elif onglet == "Gateau":
            info_base = self.base.GetGateau(ID)

            # type de gateau
            Label(modif, text = "Type du gateau : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
            typ = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            typ.insert("0", info_base[0])
            typ.grid(row = 0, column = 1, sticky = "NSEW")

            # nom
            Label(modif, text = "Nom du gateau : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 0, sticky = "NSEW")
            nom = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            nom.insert("0", info_base[1])
            nom.grid(row = 1, column = 1, sticky = "NSEW")

            # nombre de part
            Label(modif, text = "Nombre de part : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
            nb_parts = Spinbox(modif, from_ = 0, to = 100, increment = 1, fg = self.option["color_txt"], font = self.font)
            nb_parts.delete("0", "end")
            nb_parts.insert("0", info_base[2])
            nb_parts.grid(row = 2, column = 1, sticky = "NSEW")

            # prix de l'assemblage
            Label(modif, text = "Prix de l'assemblage : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 3, column = 0, sticky = "NSEW")
            prix_assemblage = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
            prix_assemblage.delete("0", "end")
            prix_assemblage.insert("0", info_base[4])
            prix_assemblage.grid(row = 3, column = 1, sticky = "NSEW")

            # prix de la part
            Label(modif, text = "Prix de la part : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 4, column = 0, sticky = "NSEW")
            prix_part = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
            prix_part.delete("0", "end")
            prix_part.insert("0", info_base[3])
            prix_part.grid(row = 4, column = 1, sticky = "NSEW")

            # marge
            Label(modif, text = "Marge : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 5, column = 0, sticky = "NSEW")
            prix_part = Spinbox(modif, from_ = 0.0, to = 1000.0, increment = 0.1, fg = self.option["color_txt"], font = self.font)
            prix_part.delete("0", "end")
            prix_part.insert("0", info_base[5])
            prix_part.grid(row = 5, column = 1, sticky = "NSEW")

            # liste des briques
            liste = Frame(modif, bg = self.option["color_bg"])
            Label(modif, text = "Liste des Briques", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 6, column = 0, sticky = "NSEW")
            info_plus = self.base.GetConstructionGateau(ID)
            for i in range(len(info_plus)):
                # le nom
                sous_nom = Entry(liste, fg = self.option["color_txt"], font = self.font)
                sous_nom.insert("0", str(info_plus[i][0]) + " | " + info_plus[i][1])
                sous_nom.configure(state = "readonly")
                sous_nom.grid(row = i, column = 0, sticky = "NSEW")
                # la personnalisation
                perso = Spinbox(liste, from_ = 0, to = 1000000, increment = 1, fg = self.option["color_txt"], font = self.font)
                perso.delete("0", "end")
                perso.insert("0", info_plus[i][2])
                perso.grid(row = i, column = 1, sticky = "NSEW")
            liste.grid(row = 6, column = 1, sticky = "NSEW")
            grid(liste, len(info_plus), 2)

            i = 7
        elif onglet == "Brique":
            info_base = self.base.GetBrique(ID)

            # nom
            Label(modif, text = "Nom de la brique : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
            nom = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            nom.insert("0", info_base[0])
            nom.grid(row = 0, column = 1, sticky = "NSEW")

            # prix
            Label(modif, text = "Prix de la brique : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 0, sticky = "NSEW")
            prix = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
            prix.delete("0", "end")
            prix.insert("0", info_base[1])
            prix.grid(row = 1, column = 1, sticky = "NSEW")

            # poid
            Label(modif, text = "Poid de la Brique :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
            poid = Spinbox(modif, from_ = 1, to = 100000, increment = 1, fg = self.option["color_txt"], font = self.font)
            poid.delete("0", "end")
            poid.insert("0", info_base[2])
            poid.grid(row = 2, column = 1, sticky = "NSEW")

            # recette
            Label(modif, text = "Recette : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 3, column = 0, sticky = "NSEW")
            recette = Text(modif, width = 50, height = 10, fg = self.option["color_txt"], font = self.font)
            recette.insert("0.0", info_base[3])
            recette.grid(row = 3, column = 1, sticky = "NSEW")

            # liste des ingredients
            liste = Frame(modif, bg = self.option["color_bg"])
            Label(modif, text = "Liste des Ingredients", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 4, column = 0, sticky = "NSEW")
            info_plus = self.base.GetContenuBrique(ID)
            for i in range(len(info_plus)):
                # le nom
                sous_nom = Entry(liste, fg = self.option["color_txt"], font = self.font)
                sous_nom.insert("0", str(info_plus[i][0]) + " | " + info_plus[i][1])
                sous_nom.configure(state = "readonly")
                sous_nom.grid(row = i, column = 0, sticky = "NSEW")
                # le poid
                perso = Spinbox(liste, from_ = 0, to = 1000000, increment = 1, fg = self.option["color_txt"], font = self.font)
                perso.delete("0", "end")
                perso.insert("0", info_plus[i][2])
                perso.grid(row = i, column = 1, sticky = "NSEW")
            liste.grid(row = 4, column = 1, sticky = "NSEW")
            grid(liste, len(info_plus), 2)

            i = 5
        elif onglet == "Ingredient":
            info_base = self.base.GetIngredient(ID)

            # nom
            Label(modif, text = "Nom de l'ingrédient : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 0, column = 0, sticky = "NSEW")
            nom = Entry(modif, width = 50, fg = self.option["color_txt"], font = self.font)
            nom.insert("0", info_base[0])
            nom.grid(row = 0, column = 1, sticky = "NSEW")

            # poid d'achat
            Label(modif, text = "Poid de conditionnement :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 1, column = 0, sticky = "NSEW")
            poid = Spinbox(modif, from_ = 1, to = 1000000, increment = 1, fg = self.option["color_txt"], font = self.font)
            poid.delete("0", "end")
            poid.insert("0", info_base[1])
            poid.grid(row = 1, column = 1, sticky = "NSEW")

            # prix d'achat
            Label(modif, text = "Prix à l'unité : ", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 2, column = 0, sticky = "NSEW")
            prix = Spinbox(modif, from_ = 0.00, to = 1000.00, increment = 0.01, fg = self.option["color_txt"], font = self.font)
            prix.delete("0", "end")
            prix.insert("0", info_base[2])
            prix.grid(row = 2, column = 1, sticky = "NSEW")

            # quantite restante
            Label(modif, text = "Stock :", bg = self.option["color_bg"], fg = self.option["color_txt"], font = self.font).grid(row = 3, column = 0, sticky = "NSEW")
            poid = Spinbox(modif, from_ = 1, to = 1000000, increment = 1, fg = self.option["color_txt"], font = self.font)
            poid.delete("0", "end")
            poid.insert("0", info_base[3])
            poid.grid(row = 3, column = 1, sticky = "NSEW")

            i = 4

        Button(modif, text = "Valider", command = validation, bg = self.option["color_button"], fg = self.option["color_txt"], font = self.font).grid(row = i, column = 0, columnspan = 2, sticky = "NSEW")
        grid(modif, i, 2)
        modif.protocol("WM_DELETE_WINDOW", lambda : on_closing(modif))
        modif.mainloop()
        return True

    def suppression(self, element, onglet):
        if askyesno("Validation", "Êtes-vous sûr de vouloir supprimer ces informations et toutes celles qui lui sont associées ? (Pour une durée très longue, éternelle)"):
            ID = self.GetNum(element)
            if onglet == "Client":
                self.base.SupprClient(ID)
                self.client() # on relance les elements affiché
            elif onglet == "Commande":
                self.base.SupprCommande(ID)
                self.commande() # on relance les elements affiché
            elif onglet == "Gateau":
                self.base.SupprGateau(ID)
                self.gateau() # on relance l'affichage
            elif onglet == "Brique":
                self.base.SupprBrique(ID)
                self.brique() # on relance l'affichage
            elif onglet == "Ingredient":
                self.base.SupprIngredient(ID)
                self.ingredient() # on relance l'affichage
            self.clean_info()
        return True

    def clean_info(self):
        for elmt in self.information.winfo_children(): elmt.destroy()
        return True

def on_closing(window):
    if askokcancel("Quit", "Êtes-vous sûr ? Toutes les données renseignées seront effacées ..."): window.destroy()
    return True


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

    return lettres == []

def grid(root, R, C):
    """
    fonction permettant de mettre les élements d'une grille dans un intervalle à l'espace maximum disponible
    parametres:
        root, le fenetre dans laquelle se trouve la grille
        R, un entier qui est l'indice de la dernière ligne a affecté
        C, un entier qui est l'indice de la derniere colonne a affecte
    """
    for i in range(R):
        root.grid_rowconfigure(i, weight=1)
    for i in range(C):
        root.grid_columnconfigure(i, weight=1)
    return True


class Base_Gateau:
    def __init__(self, base):
        assert type(base) == db.database, "Base : Init() base doit être de type database"
        self.base = base

    # Ingredient
    def AddIngredient(self, name, mass, price, stock):
        if vide(name) or name in [x[0] for x in self.base.execute("SELECT nom FROM Ingredients")]:
            return False

        self.base.execute("INSERT INTO Ingredients(nom, poid_base, prix_base, quantite) VALUES('%s', %s, %s, %s)" %(name, mass, price, stock))
        return True

    def SupprIngredient(self, id):
        self.base.execute("DELETE FROM Recettes WHERE ID_ingredients = %s" %(id)) # on enleve la composition des gateaux avec la brique
        self.base.execute("DELETE FROM Ingredients WHERE ID = %s" %(id)) # on enleve l'ingredient
        return True
    
    def ModifIngredient(self, id, name, mass, price, stock):
        self.base.execute("UPDATE Ingredients SET nom='%s', poid_base=%s, prix_base=%s, quantite=%s WHERE ID=%s" %(name, mass, price, stock, id))
        return True

    def GetIngredient(self, id):
        return self.base.execute("SELECT nom, poid_base, prix_base, quantite FROM Ingredients WHERE ID=%s" %(id))[0]

    def GetIngredients(self):
        return self.base.execute("Select ID, nom From Ingredients")


    # Client
    def AddClient(self, name, surname, phone, mail):
        if vide(name) or name in [x[0] for x in self.base.execute("SELECT nom FROM Clients")]:
            return False
        elif vide(surname):
            return False
        elif vide(phone) and vide(mail):
            return False
        elif not vide(phone):
            for c in phone:
                if c not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    return False

        if vide(phone):
            self.base.execute("INSERT INTO Clients(nom, prenom, mail) VALUES('%s', '%s', '%s')" %(name, surname, mail))
        elif vide(mail):
            self.base.execute("INSERT INTO Clients(nom, prenom, telephone) VALUES('%s', '%s', %s)" %(name, surname, phone))
        else:
            self.base.execute("INSERT INTO Clients(nom, prenom, telephone, mail) VALUES('%s', '%s', %s, '%s')" %(name, surname, phone, mail))
        return True
                
    def SupprClient(self, id):
        for id_commande in self.base.execute("SELECT ID FROM Commandes WHERE ID_client = %s" %(id)):
            self.base.execute("DELETE FROM Compositions WHERE ID_commandes = %d" %(id_commande[0])) # on enleve dans composition
            self.base.execute("DELETE FROM Commandes WHERE ID = %d" %(id_commande[0])) # on enleve la commande
        self.base.execute("DELETE FROM Clients WHERE ID = %s" %(id)) # on enleve le client de la base
        return True

    def ModifClient(self, id, name, surname, phone, mail):
        if vide(phone): self.base.execute("UPDATE Clients SET nom='%s', prenom='%s', mail='%s' WHERE ID=%s" %(name, surname, mail, id))
        elif vide(mail): self.base.execute("UPDATE Clients SET nom='%s', prenom='%s', telephone=%s WHERE ID=%s" %(name, surname, phone, id))
        else: self.base.execute("UPDATE Clients SET nom='%s', prenom='%s', telephone=%s, mail='%s' WHERE ID=%s" %(name, surname, phone, mail, id))
        return True

    def GetClient(self, id):
        return self.base.execute("SELECT nom, prenom, telephone, mail FROM Clients WHERE ID=%s" %(id))[0]

    def GetClients(self):
        return self.base.execute("Select ID, nom, prenom From Clients")

    def GetHistorique(self, idClient):
        return self.base.execute("SELECT date_dbt FROM Commandes WHERE ID_client=%s" %(idClient))
    

    # Commande
    def AddCommande(self, idClient, price, dateLimite, livraison, solde, ListeGateaux):
        if idClient == -1 or price == "0.0" or ListeGateaux == []:
            return False

        date = datetime.datetime.now()
        dateDbt = "%d/%d/%d-%d:%d:%d" %(date.day, date.month, date.year, date.hour, date.minute, date.second) # on détermine la date exacte de commande
        self.base.execute("INSERT INTO Commandes(prix, livraison, date_dbt, date_limite, soldes, ID_client) VALUES(%s, '%s', '%s', '%s', %s, %s)" %(price, livraison, dateDbt, dateLimite, solde, idClient)) # On crée la commande

        id = self.base.execute("SELECT ID FROM Commandes WHERE date_dbt = '%s'" %(dateDbt))[0][0] # on détermine l'ID de commande grâce à l'heure qui est unique
        # insertion de la liste de gateaux dans composition
        for cake in ListeGateaux:
            self.base.execute("INSERT INTO Compositions VALUES(%d, %d, %s, %s, %s, '%s')" %(id, cake[0], cake[1], cake[2], cake[3], cake[4]))
        return True
                
    def SupprCommande(self, id):
        self.base.execute("DELETE FROM Compositions WHERE ID_commandes = %s" %(id)) # on enleve dans composition
        self.base.execute("DELETE FROM Commandes WHERE ID = %s" %(id)) # on enleve la commande
        return True

    def ModifCommande(self, id, price, livraison, dateLimite, ListeGateaux):
        self.base.execute("UPDATE Commandes SET prix=%s, livraison='%s', date_limite='%s' WHERE ID=%s" %(price, livraison, dateLimite, id))
        # liste de personnalisation
        for cake in ListeGateaux:
            self.base.execute("UPDATE Compositions SET prix=%s, supplement=%s, nbr_parts=%s, personnalisation='%s' WHERE ID_commandes=%s AND ID_gateaux=%s" %(cake[1], cake[2], cake[3], cake[4], id, cake[0]))
        return True

    def GetCommande(self, id):
        return self.base.execute("SELECT ID_client, prix, livraison, date_dbt, date_fn, date_limite, soldes FROM Commandes WHERE ID=%s" %(id))[0]

    def GetCommandes(self):
        return self.base.execute("Select ID, date_dbt, date_limite, date_fn From Commandes")

    def FinishCommande(self, id):
        # on met la date actuelle
        date = datetime.datetime.now()
        dateFn = "%d/%d/%d-%d:%d" %(date.day, date.month, date.year, date.hour, date.minute)
        self.base.execute("UPDATE Commandes SET date_fn='%s' WHERE ID=%s" %(dateFn, id))

        ingredientsDanger = []
        # on supprime les quantité d'ingredients utilisé
        liste_gateaux = self.base.execute("SELECT ID_gateaux, nbr_parts FROM Compositions WHERE ID_commandes=%s" %(id))
        for i in liste_gateaux:
            nbParts_Gateau = self.base.execute("SELECT nb_parts FROM Gateaux WHERE ID=%d" %(i[0]))[0][0]
            liste_briques = self.base.execute("SELECT ID_briques, poid_brique FROM Constructions WHERE ID_gateaux=%d" %(i[0]))
            for j in liste_briques:
                poid_Brique = self.base.execute("SELECT poid FROM Briques WHERE ID=%d" %(j[0]))[0][0]
                liste_ingredients = self.base.execute("SELECT ID_ingredients, poids FROM Recettes WHERE ID_briques=%d" %(j[0]))
                for k in liste_ingredients:
                    useQuantity = (nbParts_Gateau / ((j[1] / poid_Brique) * k[1])) * i[1]
                    stockQuantity = self.base.execute("SELECT quantite FROM Ingredients WHERE ID=%d" %(k[0]))[0][0]
                    self.base.execute("UPDATE Ingredients SET quantite=%d WHERE ID=%s" %(stockQuantity - useQuantity, k[0]))
                    stockQuantity = self.base.execute("SELECT quantite FROM Ingredients WHERE ID=%d" %(k[0]))[0][0]
                    name = self.base.execute("SELECT nom FROM Ingredients WHERE ID=%d" %(k[0]))[0][0]
                    if stockQuantity < self.base.execute("SELECT poid_base FROM Ingredients WHERE ID=%d" %(k[0]))[0][0] and name not in ingredientsDanger:
                        ingredientsDanger += [[name, stockQuantity]]
        # on décrémente les quantite des ingredients
        # on ajoute les ingredient dont quantite < poid_base
        return ingredientsDanger

    def GetCompositionCommande(self, id):
        return self.base.execute("SELECT ID, nom, prix, supplement, Compositions.nbr_parts, personnalisation FROM Gateaux, Compositions WHERE ID=ID_gateaux AND ID_commandes=%s" %(id))

    # Brique
    def AddBrique(self, name, price, mass, recette, ListeIngredients):
        if vide(name) or name in [x[0] for x in self.base.execute("SELECT nom FROM Briques")]:
            return False
        elif price == "0.0":
            return False
        elif mass == 0:
            return False
        elif ListeIngredients == []:
            return False
        
        self.base.execute('INSERT INTO Briques(nom, prix, poid, recette) VALUES("%s", %s, %s, "%s")' %(name, price, mass, recette))
        id = self.base.execute("SELECT ID FROM Briques WHERE nom='%s'" %(name))[0][0]
        for ingredient in ListeIngredients:
            self.base.execute("INSERT INTO Recettes VALUES(%d, %s, %s)" %(id, ingredient[0], ingredient[1]))
        return True

    def SupprBrique(self, id):
        self.base.execute("DELETE FROM Constructions WHERE ID_briques = %s" %(id)) # on enleve la composition des gateaux avec la brique
        self.base.execute("DELETE FROM Recettes WHERE ID_briques = %s" %(id)) # on enleve la composition des gateaux avec la brique
        self.base.execute("DELETE FROM Briques WHERE ID = %s" %(id)) # on enleve la brique
        return True

    def ModifBrique(self, id, name, price, mass, recette, ListeIngredients):
        self.base.execute('UPDATE Briques SET nom="%s", prix=%s, poid=%s, recette="%s" WHERE ID=%d' %(name, price, mass, recette, id))
        # liste de poids
        for ingredient in ListeIngredients:
            self.base.execute("UPDATE Recettes SET poids=%s WHERE ID_ingredients=%d AND ID_briques=%d" %(ingredient[1], ingredient[0], id))
        return True

    def GetBrique(self, id):
        return self.base.execute("SELECT nom, prix, poid, recette FROM Briques WHERE ID=%d" %(id))[0]

    def GetBriques(self):
        return self.base.execute("SELECT ID, nom From Briques")

    def GetContenuBrique(self, id):
        return self.base.execute("SELECT Ingredients.ID, Ingredients.nom, poids FROM Ingredients, Recettes WHERE ID=ID_ingredients AND ID_briques=%s" %(id))

    # Gateau
    def AddGateau(self, type_, name, nbParts, pricePart, priceBuild, marge, ListeBriques):
        if vide(type_):
            return False
        elif vide(name) or name in [x[0] for x in self.base.execute("SELECT nom FROM Gateaux")]:
            return False
        elif ListeBriques == []:
            return False

        self.base.execute("INSERT INTO Gateaux(type, nom, nb_parts, prix_part, prix_assemblage, marge) VALUES('%s', '%s', %s, %s, %s, %s)" %(type_, name, nbParts, pricePart, priceBuild, marge))
        id = self.base.execute("SELECT ID FROM Gateaux WHERE nom='%s'" %(name))[0][0]
        
        for brique in ListeBriques:
            self.base.execute("INSERT INTO Constructions VALUES(%d, %d, %s)" %(id, brique[0], brique[1]))
        return True

    def SupprGateau(self, id):
        self.base.execute("DELETE FROM Compositions WHERE ID_gateaux = %s" %(id)) # on enleve la composition du gateau
        self.base.execute("DELETE FROM Constructions WHERE ID_gateaux = %s" %(id)) # on enleve la construction du gateau
        self.base.execute("DELETE FROM Gateaux WHERE ID = %s" %(id)) # on enleve le gateau
        return True

    def ModifGateau(self, id, type_, name, nbParts, pricePart, priceBuild, marge, ListeBriques):
        self.base.execute("UPDATE Gateaux SET type='%s', nom='%s', nb_parts=%s, prix_part=%s, prix_assemblage=%s, marge=%s WHERE ID=%s" %(type_, name, nbParts, pricePart, priceBuild, marge, id))
        # liste de poid_brique
        for brique in ListeBriques:
            self.base.execute("UPDATE Constructions SET poid_brique=%s WHERE ID_briques=%s AND ID_gateaux=%s" %(brique[1], brique[0], id))
        return True

    def GetGateau(self, id):
        return self.base.execute("SELECT type, nom, nb_parts, prix_assemblage, prix_part, marge FROM Gateaux WHERE ID=%d" %(id))[0]

    def GetGateaux(self):
        return self.base.execute("Select ID, nom From Gateaux")

    def GetConstructionGateau(self, id):
        return self.base.execute("SELECT ID_briques, nom, poid_brique FROM Briques, Constructions WHERE ID=ID_briques AND ID_gateaux=%s" %(id))


class MyCombobox(ttk.Combobox):
    def config_popdown(self, **kwargs):
        self.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure {}'.format(self, ' '.join(self._options(kwargs))))


if __name__ == "__main__":
    fenetre = SGBD("base_de_donnees\\DGourmandises.db", "data\\preferences.txt", "data\\help.pdf")
    fenetre.lancement()