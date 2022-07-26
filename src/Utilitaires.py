from tkinter import messagebox
from datetime import datetime
from tkinter import *

#fontion de fin de programme
def end(window,username,score):
    #si le mode admin est activé on affiche le score sinon on stocke le score et on demande au pilote si il veut voir son historique
    if username: 
        with open(f"Users/{str(username)}.txt", "a") as file:
            file.write(datetime.now().strftime("%d/%m/%Y %H:%M")+ " : " + str(score) +"\n") #on ecrit le score dans le fichier
        if reponse := messagebox.askyesno("Fin de la partie", "Voulez-vous voir votre historique complet?"):
            window.destroy() #on detruit les fenetres
            with open(f"Users/{str(username)}.txt", "r") as file:
                window_end = resultf(file)
            window_end.mainloop()
        else:
            messagebox.showinfo("Fin de la partie", "Bravo ! Votre score est de {0} points".format(score)) #on affiche le score 
            window.destroy()
    else:
        messagebox.showinfo("Fin de la partie", "Bravo ! Votre score est de {0} points.".format(score)) 
        window.destroy()


# TODO Rename this here and in `end`
def resultf(file):
    next(file) #on passe la premiere ligne
    result = Tk()
    result.iconbitmap("images/plane.ico")
    result.title("Historique")
    text = Text(result, bg="#2d2d2d", fg="White", font="Roboto 15", width=30)
    text.pack(expand=True, fill=BOTH)
    text.insert(END, file.read())
    text.config(state='disabled')
    return result



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