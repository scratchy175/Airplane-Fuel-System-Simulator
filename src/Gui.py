from turtle import pen
from Config import *
from Composants import *
from Manager import *


from tkinter import *
import os


is_on = False



#fonction permettant d'afficher une fenêtre de connexion a l'aide de tkinter et de l'interface graphique 
def login_menu():
    global root 
    if admin_mode: 
        #Passage directement à la fenêtre de simulation   
        create_window()
    else:
        #Création de la fenêtre de connexion
        #Generation de bouttons,zones d'entrées/textes, d'images, mise en place des éléments
        root = Tk()
        root.title("Connexion")
        root.geometry("500x600")
        root.iconbitmap("images/plane.ico")
        root.bind("<Return>",connexion)
        
        frame = Frame(root, bg="#2d2d2d", width=500, height=750)
        frame.place(x=0, y=0)

        login = Label(frame, text="Connexion",fg="White", font=("Roboto",25), bg="#2d2d2d")
        login.place(x=175, y=50)

        username = Label(frame, text="Nom d'utilisateur",bg="#2d2d2d",fg="White", font=("Roboto",15))
        username.place(x=100, y=150)

        user_image = PhotoImage(file="images/button.png")
        user_entry = Label(frame, image=user_image, bg="#2d2d2d", border=0)
        user_entry.place(x=100, y=190)
        global username_entry
        username_entry = Entry(frame, bg="#2d2d2d",fg="White", font=("Roboto",15), border=0, width=20)
        username_entry.place(x=110, y=203)

        password = Label(frame, text="Mot de passe", bg="#2d2d2d", fg="White", font=("Roboto",15))
        password.place(x=100, y=300)

        pass_entry = Label(frame, image=user_image, bg="#2d2d2d", border=0)
        pass_entry.place(x=100, y=340)
        global password_entry
        password_entry = Entry(frame, bg="#2d2d2d", fg="White", font=("Roboto",15), border=0, width=15, show="*")
        password_entry.place(x=110, y=355)

        login_image = PhotoImage(file="images/button_connexion.png")
        inscription_image = PhotoImage(file="images/button_inscription.png")
        login_button = Button(frame, text="Connexion",image=login_image, borderwidth=0,bg="#2d2d2d",activebackground="#2d2d2d", command= lambda: connexion(event = None))
        login_button.place(x=80, y=450)
        register_button = Button(frame, text="Inscription",image=inscription_image, borderwidth=0, bg="#2d2d2d",activebackground="#2d2d2d", command= inscription)
        register_button.place(x=260, y=450)


        #Création du texte et du bouton du mode practice
        practice_text = Label(frame, text="Practice Mode :", bg="#2d2d2d", fg="White", font=("Roboto",15))
        practice_text.place(x=100, y=549)
        global practice_on
        global practice_off
        practice_on=PhotoImage(file="images/On.png")
        practice_off=PhotoImage(file="images/Off.png")
        practice_button = Button(frame,image=practice_off, borderwidth=0, bg="#2d2d2d",activebackground="#2d2d2d", command=lambda: switch(practice_button))
        practice_button.place(x=250, y=550)
        root.mainloop()

#fonction permettant de changer le mode practice
def switch(practice_button):
    global is_on
    if is_on:
        practice_button.config(image=practice_off)
        practice_mode = False
        is_on=False    
    else:
        practice_button.config(image=practice_on)
        practice_mode = True
        is_on=True


#fonction exécuté par le boutton de connexion
# elle permet de vérifier si le nom d'utilisateur et le mot de passe sont corrects et si correcte, de lancer la fenêtre de simulation
def connexion(event):
    global connexion_username
    connexion_username = username_entry.get() #récupération du nom d'utilisateur
    connexion_password = password_entry.get()
    username_entry.delete(0, END) #suppression des données de l'entrée
    password_entry.delete(0, END)
    if os.path.isdir("Users"): #vérification de l'existence du dossier Users
        liste_files = os.listdir("Users") #récupération de la liste des fichiers
        if connexion_username and connexion_password: #vérification de l'existence des entrées
            if str(connexion_username) + ".txt" in liste_files: #vérification de l'existence du fichier
                file = open("Users/" + str(connexion_username) + ".txt", "r") #ouverture du fichier
                lines = file.readline().split(":") #récupération des lignes
                if lines[1].strip("\n") == str(connexion_password): #vérification du mot de passe
                    logged = Label(root, text="Connexion réussie.", fg="green",bg="#2d2d2d", font=("Arial",10)) #affichage du message de connexion
                    logged.place(x=100, y=400)
                    root.after(500, lambda: create_window()) #lancement de la fenêtre de simulation
                    return
    login_error = Label(root, text="Nom d'utilisateur ou mot de passe incorrect.", fg="red",bg="#2d2d2d", font=("Arial",10)) #affichage du message d'erreur
    login_error.place(x=100, y=400)
    login_error.after(1000, login_error.destroy) #suppression du message d'erreur


#fonction exécuté par le boutton d'inscription
# elle permet de créer un nouveau compte
def inscription():
    inscription_username = username_entry.get()
    inscription_password = password_entry.get()
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    if not os.path.isdir("Users"):
        os.mkdir("Users") #création du dossier Users
    liste_files = os.listdir("Users")
    if inscription_username and inscription_password:
        if not str(inscription_username) + ".txt" in liste_files:
            file = open("Users/" + str(inscription_username) + ".txt", "w") #création du fichier
            file.write("Mot de passe:" + str(inscription_password)+"\n") #écriture du mot de passe
            file.close()
            sucess = Label(root, text="Inscription réussie.", fg="green",bg="#2d2d2d", font=("Arial",10)) #affichage du message d'inscription
            sucess.place(x=100, y=400)
            sucess.after(1000, sucess.destroy)
        else:
            already_used = Label(root, text="Ce nom d'utilisateur est déjà utilisé.", fg="red",bg="#2d2d2d", font=("Arial",10)) #affichage du message d'erreur
            already_used.place(x=100, y=400)
            already_used.after(1000, already_used.destroy)
    else:
        entry_empty = Label(root, text="Veuillez remplir tous les champs.", fg="red",bg="#2d2d2d", font=("Arial",10)) #affichage du message d'erreur
        entry_empty.place(x=100, y=400)
        entry_empty.after(1000, entry_empty.destroy)



#genere la fenêtre de simulation
def create_window():
    if not admin_mode: #vérification si le mode admin est desactivé, si oui alors on detruit la fenêtre de connexion
        root.destroy()
    #création de la fenêtre contenant les bouttons
    window = Tk()
    window.title("Tableau de bord du pilote")
    window.geometry("500x300+300+300")
    window.iconbitmap("images/plane.ico")
    frame = Frame(window, bg="#202124")
    frame.pack(side= TOP, expand=True, fill=BOTH)
    frame2 = Frame(window, bg="#202124")
    frame2.pack(side= TOP, expand=True, fill=BOTH)
    frame3 = Frame(window, bg="#202124")
    frame3.pack(side= TOP, expand=True, fill=BOTH)
    #création de la fenêtre contenant le système de carburant
    window2 = Toplevel(window)
    window2.title("Etat du système de carburant")
    window2.geometry("600x600+1500+250")
    window2.iconbitmap("images/plane.ico")
    canvas = Canvas(window2, width=600, height=600, bg="#0269A4")
    canvas.pack(expand=True)

    #permet de recupérer le nom d'utilisateur si le mode admin est desactivé
    if admin_mode: 
        set_systeme(window,None,canvas,frame,frame2,frame3)
    else:
        set_systeme(window,connexion_username,canvas,frame,frame2,frame3)
    window.mainloop()