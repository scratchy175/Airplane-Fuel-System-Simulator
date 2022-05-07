
import random
from tkinter import messagebox
from Config import *
from Composants import *


from tkinter import *
import os


def login_menu():
    global root
    
    if admin_mode:
        
        create_window(dico)
    else:
        
        
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
        root.mainloop()

def connexion(event):
    connexion_username = username_entry.get()
    connexion_password = password_entry.get()
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    if os.path.isdir("Users"):
        liste_files = os.listdir("Users")
        if connexion_username and connexion_password:
            if str(connexion_username) + ".txt" in liste_files:
                file = open("Users/" + str(connexion_username) + ".txt", "r")
                lines = file.readline().split(":")
                if lines[1].strip("\n") == str(connexion_password):
                    logged = Label(root, text="Connexion réussie.", fg="green",bg="#2d2d2d", font=("Arial",10))
                    logged.place(x=100, y=400)
                    root.after(500, lambda: create_window(dico))
                    return
    login_error = Label(root, text="Nom d'utilisateur ou mot de passe incorrect.", fg="red",bg="#2d2d2d", font=("Arial",10))
    login_error.place(x=100, y=400)
    login_error.after(1000, login_error.destroy)

def inscription():
    inscription_username = username_entry.get()
    inscription_password = password_entry.get()
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    if not os.path.isdir("Users"):
        os.mkdir("Users")
    liste_files = os.listdir("Users")
    if inscription_username and inscription_password:
        if not str(inscription_username) + ".txt" in liste_files:
            file = open("Users/" + str(inscription_username) + ".txt", "w")
            file.write("Mot de passe:" + str(inscription_password)+"\n")
            file.close()
            sucess = Label(root, text="Inscription réussie.", fg="green",bg="#2d2d2d", font=("Arial",10))
            sucess.place(x=100, y=400)
            sucess.after(1000, sucess.destroy)
        else:
            already_used = Label(root, text="Ce nom d'utilisateur est déjà utilisé.", fg="red",bg="#2d2d2d", font=("Arial",10))
            already_used.place(x=100, y=400)
            already_used.after(1000, already_used.destroy)
    else:
        entry_empty = Label(root, text="Veuillez remplir tous les champs.", fg="red",bg="#2d2d2d", font=("Arial",10))
        entry_empty.place(x=100, y=400)
        entry_empty.after(1000, entry_empty.destroy)

def create_window(dico):
    if not admin_mode:
        root.destroy()
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
    window2 = Toplevel(window)
    window2.title("Etat du système de carburant")
    window2.geometry("600x600+1500+250")
    window2.iconbitmap("images/plane.ico")
    global canvas
    canvas = Canvas(window2, width=600, height=600, bg="#0269A4")
    canvas.pack(expand=True)



    global Tank1,Tank2,Tank3,P11,P12,P21,P22,P31,P32,VT12,VT23,V12,V13,V23,M1,M2,M3
    global liste_flux
    Tank1 = Tank(canvas,"Tank1",dico,"Orange")
    Tank2 = Tank(canvas,"Tank2",dico,"DarkGreen")
    Tank3 = Tank(canvas,"Tank3",dico,"Yellow")
    P11 = Pompe(canvas,frame2,"P11",dico,"Normal")
    P12 = Pompe(canvas,frame2,"P12",dico,"Secours")
    P21 = Pompe(canvas,frame2,"P21",dico,"Normal")
    P22 = Pompe(canvas,frame2,"P22",dico,"Secours")
    P31 = Pompe(canvas,frame2,"P31",dico,"Normal")
    P32 = Pompe(canvas,frame2,"P32",dico,"Secours")
    VT12 = Vanne(canvas,frame,"VT12",dico)
    VT23 = Vanne(canvas,frame,"VT23",dico)
    V12 = Vanne(canvas,frame3,"V12",dico)
    V13 = Vanne(canvas,frame3,"V13",dico)
    V23 = Vanne(canvas,frame3,"V23",dico)
    M1 = Moteur(canvas,"M1",dico)
    M2 = Moteur(canvas,"M2",dico)
    M3 = Moteur(canvas,"M3",dico)
    liste_tank = [Tank1,Tank2,Tank3]
    liste_pompe = [P11,P12,P21,P22,P31,P32]
    liste_vanne = [VT12,VT23,V12,V13,V23]
    liste_moteur = [M1,M2,M3]
    liste_flux = [Flux(canvas,"L"+str(i),dico) for i in range(1,len(dico["F"])+1)]

    for i in range(8):
        liste_flux[i].change_etat()

    """Tank3.vider()
    P31.en_panne(event=None)
    P12.en_panne(event=None)
    M3.eteindre()"""
    genere_panne(liste_tank,liste_pompe,liste_flux)
    for i in range(len(liste_pompe)):
        pass
        #print(liste_pompe[i].get_etat())
    
    #M1.change_etat()

    compteur = 0
    window.after(500, lambda: boucle(window,compteur, liste_moteur,liste_tank,liste_pompe,liste_vanne,liste_flux))
    window.mainloop()

def eteindre_flux_moteur():
    if not Tank1.get_etat() or P11.get_etat()== -1 or (P12.get_etat()== 0 and P11.get_etat() == -1):
        M1.eteindre()
        liste_flux[0].eteindre()
        liste_flux[1].eteindre()
        liste_flux[2].eteindre()
    
    if not Tank2.get_etat() or P21.get_etat()== -1 or (P22.get_etat()== 0 and P21.get_etat() == -1):
        M2.eteindre()
        liste_flux[3].eteindre()
        liste_flux[4].eteindre()

    if not Tank3.get_etat() or P31.get_etat()== -1 or (P32.get_etat()== 0 and P31.get_etat() == -1):
        M3.eteindre()
        liste_flux[5].eteindre()
        liste_flux[6].eteindre()
        liste_flux[7].eteindre()


def genere_panne(liste_tank,liste_pompe, liste_flux):#remettre par defaut a chaque panne resolu /boucle
    panne_tank = random.choice(liste_tank)
    rand_int = random.randint(1,3)
    liste_panne = random.sample(range(0,len(liste_pompe)-1),rand_int)
    for val in liste_panne:
        liste_pompe[val].en_panne(event=None)
        print(liste_pompe[val].get_name())
    panne_tank.vider()
    eteindre_flux_moteur()



def boucle (window,compteur, liste_moteur, liste_tank, liste_pompe,liste_vanne,liste_flux):
    if compteur != 10:
        if M1.get_etat() and M2.get_etat() and M3.get_etat():
            compteur+=1
            #genere_panne(liste_tank,liste_pompe,liste_flux)
            return
            #window.after(500, boucle, window,compteur, liste_moteur, liste_tank, liste_pompe,liste_vanne,liste_flux)
        else:
            """print("Moteur {0} {1} {2}".format(M1.get_etat(),M2.get_etat(),M3.get_etat()))
            print("Tank {0} {1} {2}".format(Tank1.get_etat(),Tank2.get_etat(),Tank3.get_etat()))
            print("Pompe {0} {1} {2}".format(P11.get_etat(),P12.get_etat(),P21.get_etat(),P22.get_etat(),P31.get_etat(),P32.get_etat()))"""
            eteindre_flux_moteur()
            reparer()
            allumer_vanne()
            
            window.after(500, boucle, window,compteur, liste_moteur, liste_tank, liste_pompe,liste_vanne,liste_flux)
    else:
        messagebox.showinfo("Fin", "Fin du programme")
        #print(username_entry)
        #ajouter la note 
        #prendre le temps au debut du programme et comparé au temps a la fin et en fonction attribuer une note de 0 a 10
        #ecrire la note dans le .txt


def allumer_vanne():
    if VT12.get_etat():
        liste_flux[14].allumer()
        liste_flux[15].allumer()
        if not Tank1.get_etat() and Tank2.get_etat():
            Tank1.remplir()
            
        elif not Tank2.get_etat() and Tank1.get_etat():
            Tank2.remplir()
    else:
    
        liste_flux[14].eteindre()
        liste_flux[15].eteindre()
            
    if VT23.get_etat():
        liste_flux[16].allumer()
        liste_flux[17].allumer()
        
        if not Tank2.get_etat() and Tank3.get_etat():
            Tank2.remplir()
            
        elif not Tank3.get_etat() and Tank2.get_etat():
            Tank3.remplir()
    
    else:
        liste_flux[16].eteindre()
        liste_flux[17].eteindre()


def checkM1():
    if not M1.get_etat():
            if Tank1.get_etat():
                if P11.get_etat() == 1:
                    liste_flux[0].allumer()
                    liste_flux[1].allumer()
                    liste_flux[2].allumer()
                    print("1 M1")
                    M1.allumer()
                    return
                elif P11.get_etat() == -1:
                    if P12.get_etat() == 1:
                        liste_flux[0].allumer()
                        liste_flux[1].allumer()
                        liste_flux[2].allumer()
                        M1.allumer()
                        return
            if Tank2.get_etat():
                if P22.get_etat()== 1 and V12.get_etat():
                    liste_flux[3].allumer()
                    liste_flux[11].allumer()
                    liste_flux[10].allumer()
                    liste_flux[2].allumer()
                    M1.allumer()
                    return
            if Tank3.get_etat():
                if P32.get_etat() == 1 and V13.get_etat():
                    liste_flux[5].allumer()
                    liste_flux[9].allumer()
                    liste_flux[8].allumer()
                    liste_flux[1].allumer()
                    liste_flux[2].allumer()
                    M1.allumer()
                    return


def checkM2():
    if not M2.get_etat():
            if Tank2.get_etat():
                if P21.get_etat() == 1:
                    liste_flux[3].allumer()
                    liste_flux[4].allumer()
                    print("1 M2")
                    M2.allumer()
                    return
                elif P21.get_etat() == -1:
                    if P22.get_etat() == 1:
                        liste_flux[3].allumer()
                        liste_flux[4].allumer()
                        M2.allumer()
                        return
            if Tank1.get_etat():
                if P12.get_etat() == 1 and V12.get_etat():
                    liste_flux[0].allumer()
                    liste_flux[1].allumer()
                    liste_flux[10].allumer()
                    liste_flux[11].allumer()
                    liste_flux[4].allumer()
                    M2.allumer()
                    return
            if Tank3.get_etat():
                if P32.get_etat() == 1 and V23.get_etat():
                    liste_flux[5].allumer()
                    liste_flux[6].allumer()
                    liste_flux[13].allumer()
                    liste_flux[12].allumer()
                    liste_flux[4].allumer()
                    M2.allumer()
                    return


def checkM3():
    if not M3.get_etat():
            if Tank3.get_etat():
                if P31.get_etat() == 1:
                    liste_flux[5].allumer()
                    liste_flux[6].allumer()
                    liste_flux[7].allumer()
                    M3.allumer()
                    print("1 M3")
                    return
                elif P31.get_etat() == -1:
                    if P32.get_etat()== 1:
                        liste_flux[5].allumer()
                        liste_flux[6].allumer()
                        liste_flux[7].allumer()
                        M3.allumer()
                        print("2")
                        return
            if Tank1.get_etat():
                if P12.get_etat() == 1 and V13.get_etat():
                    liste_flux[0].allumer()
                    liste_flux[8].allumer()
                    liste_flux[9].allumer()
                    liste_flux[6].allumer()
                    liste_flux[7].allumer()
                    M3.allumer()
                    print("3")
                    return
            if Tank2.get_etat():
                if P22.get_etat() == 1 and V23.get_etat():
                    liste_flux[3].allumer()
                    liste_flux[12].allumer()
                    liste_flux[13].allumer()
                    liste_flux[7].allumer()
                    M3.allumer()
                    print("4")
                    return


def reparer():
    checkM1()
    checkM2()
    checkM3()
    


