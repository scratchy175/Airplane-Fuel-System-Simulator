from tkinter import messagebox
from datetime import datetime
from tkinter import *

#fontion de fin de programme
def end(window,username,score):
    #si le mode admin est activé on affiche le score sinon on stocke le score et on demande au pilote si il veut voir son historique
    if username: 
            file = open("Users/" + str(username) + ".txt", "a") #on ouvre le fichier en mode ajout
            file.write(datetime.now().strftime("%d/%m/%Y %H:%M")+ " : " + str(score) +"\n") #on ecrit le score dans le fichier
            file.close()
            reponse = messagebox.askyesno("Fin de la partie","Voulez-vous voir votre historique complet?") #on demande a l'utilisateur si il veut voir son historique
            if reponse:
                window.destroy() #on detruit les fenetres
                file = open("Users/" + str(username) + ".txt", "r") #on ouvre le fichier en mode lecture
                next(file) #on passe la premiere ligne
                window_end = Tk() #on cree une fenetre pour afficher l'historique
                window_end.iconbitmap("images/plane.ico")
                window_end.title("Historique")
                text = Text(window_end,bg="#2d2d2d",fg="White", font="Roboto 15", width=30) #on cree une zone de texte pour afficher l'historique
                text.pack(expand=True, fill=BOTH)
                text.insert(END, file.read()) 
                text.config(state='disabled')
                file.close()
                window_end.mainloop()
            else:
                
                messagebox.showinfo("Fin de la partie", "Bravo ! Votre score est de {0} points".format(score)) #on affiche le score 
                window.destroy()
    else:
        messagebox.showinfo("Fin de la partie", "Bravo ! Votre score est de {0} points.".format(score)) 
        window.destroy()



#fonction qui permet de renitialiser tout le systeme
def reset(liste_tank,liste_pompe,liste_moteur,liste_vanne,liste_flux):
    for i in range(len(liste_tank)):
        liste_tank[i].remplir()
    for i in range(len(liste_vanne)):
        liste_vanne[i].reset_vanne()

    for i in range(len(liste_pompe)):
        liste_pompe[i].reset_pompe()
    
    for i in range(len(liste_moteur)):
        liste_moteur[i].allumer()

    for i in range(len(liste_flux)):
        liste_flux[i].reset_flux()

    for i in range(8):
        liste_flux[i].allumer()