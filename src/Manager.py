from webbrowser import get
from Composants import *
from Config import *
import random
from tkinter import messagebox
from datetime import datetime



#fonction qui permet de créer le systeme, de l'initialiser et demarrer l'exercice
def set_systeme(window,username,canvas,frame,frame2,frame3):
    global Tank1,Tank2,Tank3,P11,P12,P21,P22,P31,P32,VT12,VT23,V12,V13,V23,M1,M2,M3
    global liste_flux,liste_pompe,liste_tank,liste_vanne,liste_moteur
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
    liste_flux = [Flux(canvas,"L"+str(i),dico) for i in range(0,len(dico["F"]))]
    for i in range(8):
        liste_flux[i].allumer()

    compteur = 0
    score = 0
    if not practice_mode:
        genere_panne(liste_tank,liste_pompe) #genere une serie panne aléatoire
    window.after(500, lambda: boucle(window,username,compteur,score)) # permet de debuter la boucle

#fonction qui permet d'eteindre les flux et moteurs
def eteindre_flux_moteur2():
    if M1.get_etat() == 1 : #si le moteur 1 est allumé
        if P12.get_alimente() == "M1" and P12.get_etat()== 0: #si la pompe 12 alimente M1 et que la pompe 12 est eteinte
            if liste_flux[0].get_allumage() == 1:
                liste_flux[0].eteindre()
                

            if liste_flux[1].get_allumage() == 1:
                liste_flux[1].eteindre()
                

            if liste_flux[2].get_allumage() == 1:
                liste_flux[2].eteindre()
                
            P12.set_alimente(None) #P12 n'alimente plus rien
            M1.eteindre() #on eteint le moteur 1
            if debug_mode:
                print("1 M1 eteint")
        if (P22.get_alimente() == "M1" and P22.get_etat()== 0) or (P22.get_alimente() == "M1" and P22.get_etat()== 1 and V12.get_etat() == 0):
            if liste_flux[2].get_allumage() == 1:
                liste_flux[2].eteindre()
            
            if liste_flux[10].get_allumage() == 1:
                liste_flux[10].eteindre()
            
            if liste_flux[11].get_allumage() == 1:
                liste_flux[11].eteindre()
            
            if liste_flux[3].get_allumage() == 1:
                liste_flux[3].eteindre()
            P22.set_alimente(None)
            M1.eteindre()
            if debug_mode:
                print("2 M1 eteint")

        if (P32.get_alimente() == "M1" and P32.get_etat()== 0) or (P32.get_alimente() == "M1" and P32.get_etat()== 1 and V13.get_etat() == 0):
            if liste_flux[2].get_allumage() == 1:
                liste_flux[2].eteindre()
            
            if liste_flux[1].get_allumage() == 1:
                liste_flux[1].eteindre()
            
            if liste_flux[8].get_allumage() == 1:
                liste_flux[8].eteindre()
            
            if liste_flux[9].get_allumage() == 1:
                liste_flux[9].eteindre()

            if liste_flux[5].get_allumage() == 1:
                liste_flux[5].eteindre()
            P32.set_alimente(None)
            M1.eteindre()
            if debug_mode:
                print("3 M1 eteint")
    if M2.get_etat() == 1 : #pareil pour le moteur 2
        if (P12.get_alimente() == "M2" and P12.get_etat()== 0) or (P12.get_alimente() == "M2" and P12.get_etat()== 1 and V12.get_etat() == 0):
            if liste_flux[0].get_allumage() == 1:
                liste_flux[0].eteindre()
                
            if liste_flux[1].get_allumage() == 1:
                liste_flux[1].eteindre()
                
            if liste_flux[10].get_allumage() == 1:
                liste_flux[10].eteindre()

            if liste_flux[11].get_allumage() == 1:
                liste_flux[11].eteindre()
            
            if liste_flux[4].get_allumage() == 1:
                liste_flux[4].eteindre()
                
            P12.set_alimente(None)
            M2.eteindre()
            if debug_mode:
                print("1 M2 eteint")
        if P22.get_alimente() == "M2" and P22.get_etat()== 0:
            if liste_flux[3].get_allumage() == 1:
                liste_flux[3].eteindre()
            
            if liste_flux[4].get_allumage() == 1:
                liste_flux[4].eteindre()

            P22.set_alimente(None)
            M2.eteindre()
            if debug_mode:
                print("2 M2 eteint")

        if (P32.get_alimente() == "M2" and P32.get_etat()== 0) or (P32.get_alimente() == "M2" and P32.get_etat()== 1 and V23.get_etat() == 0):
            if liste_flux[5].get_allumage() == 1:
                liste_flux[5].eteindre()
            
            if liste_flux[6].get_allumage() == 1:
                liste_flux[6].eteindre()
            
            if liste_flux[13].get_allumage() == 1:
                liste_flux[13].eteindre()
            
            if liste_flux[12].get_allumage() == 1:
                liste_flux[12].eteindre()

            if liste_flux[4].get_allumage() == 1:
                liste_flux[4].eteindre()
            P32.set_alimente(None)
            M2.eteindre()
            if debug_mode:
                print("3 M2 eteint")
    
    if M3.get_etat() == 1 : #pareil pour le moteur 3
        if P12.get_alimente() == "M3" and P12.get_etat()== 0 or (P12.get_alimente() == "M3" and P12.get_etat()== 1 and V13.get_etat() == 0):
            if liste_flux[0].get_allumage() == 1:
                liste_flux[0].eteindre()
                
            if liste_flux[8].get_allumage() == 1:
                liste_flux[8].eteindre()
                
            if liste_flux[9].get_allumage() == 1:
                liste_flux[9].eteindre()

            if liste_flux[6].get_allumage() == 1:
                liste_flux[6].eteindre()
            
            if liste_flux[7].get_allumage() == 1:
                liste_flux[7].eteindre()
                
            P12.set_alimente(None)
            M3.eteindre()
            if debug_mode:
                print("1 M3 eteint")
        if P22.get_alimente() == "M3" and P22.get_etat()== 0 or (P22.get_alimente() == "M3" and P22.get_etat()== 1 and V23.get_etat() == 0):
            if liste_flux[3].get_allumage() == 1:
                liste_flux[3].eteindre()
            
            if liste_flux[12].get_allumage() == 1:
                liste_flux[12].eteindre()
            
            if liste_flux[13].get_allumage() == 1:
                liste_flux[13].eteindre()
            
            if liste_flux[7].get_allumage() == 1:
                liste_flux[7].eteindre()

            P22.set_alimente(None)
            M3.eteindre()
            if debug_mode:
                print("2 M3 eteint")

        if P32.get_alimente() == "M3" and P32.get_etat()== 0:
            if liste_flux[5].get_allumage() == 1:
                liste_flux[5].eteindre()
            
            if liste_flux[6].get_allumage() == 1:
                liste_flux[6].eteindre()
            
            if liste_flux[7].get_allumage() == 1:
                liste_flux[7].eteindre()
        
            P32.set_alimente(None)
            M3.eteindre()
            if debug_mode:
                print("3 M3 eteint")

    #permet de rallumer les pompes principales si les tanks se remplissent de nouveau
    if Tank1.get_etat() and P11.get_etat()== 0:
            P11.allumer()
            print("allume P11")
    if Tank2.get_etat() and P21.get_etat()== 0:
            P21.allumer()
            print("allume P21")
    if Tank3.get_etat() and P31.get_etat()== 0:
            P31.allumer()
            print("allume P31")
            
#fontion qui permet permet d'eteindre les flux et les moteurs lorsque on genere les pannes
def eteindre_flux_moteur():
        if not Tank1.get_etat() or P11.get_etat()== -1 or (P12.get_etat()== 0 and P11.get_etat() == -1):
            if liste_flux[0].get_allumage() == 1:
                liste_flux[0].eteindre()
            if liste_flux[1].get_allumage() == 1:
                liste_flux[1].eteindre()
            if liste_flux[2].get_allumage() == 1:
                liste_flux[2].eteindre()
            M1.eteindre()
            if debug_mode:
                    print("1 1 M1 eteint")
        if not Tank1.get_etat() and P11.get_etat()== 1:
            P11.eteindre()

        if not Tank2.get_etat() or P21.get_etat()== -1 or (P22.get_etat()== 0 and P21.get_etat() == -1):
            if liste_flux[3].get_allumage() == 1:
                liste_flux[3].eteindre()
            if liste_flux[4].get_allumage() == 1:
                liste_flux[4].eteindre()
            M2.eteindre()
            if debug_mode:
                    print("1 2 M2 eteint")
        if not Tank2.get_etat() and P21.get_etat()== 1:
            P21.eteindre()

        if not Tank3.get_etat() or P31.get_etat()== -1 or (P32.get_etat()== 0 and P31.get_etat() == -1): 
            if liste_flux[5].get_allumage() == 1:
                liste_flux[5].eteindre()
            if liste_flux[6].get_allumage() == 1:
                liste_flux[6].eteindre()
            if liste_flux[7].get_allumage() == 1:
                liste_flux[7].eteindre()
            M3.eteindre()
            if debug_mode:
                    print("1 3 M3 eteint")
        if not Tank3.get_etat() and P31.get_etat()== 1:
            P31.eteindre()

#fontion qui permet permet d'eteindre les flux et les moteurs lorsqu'on est en mode practice
def eteindre_flux_moteur_pratice():
    if (P22.get_alimente() != "M1" and P32.get_alimente() != "M1"):
        if not Tank1.get_etat() and (P11.get_etat() == 1 or P11.get_etat() == -1):
            if liste_flux[0].get_allumage() == 1:
                liste_flux[0].eteindre()
            if liste_flux[1].get_allumage() == 1:
                liste_flux[1].eteindre()
            if liste_flux[2].get_allumage() == 1:
                liste_flux[2].eteindre()
            M1.eteindre()
            if P11.get_etat()!= -1:
                P11.eteindre()
            if P12.get_etat()!= -1:
                P12.eteindre()
        elif P11.get_etat() == -1 and P12.get_etat()!= 1:
            if liste_flux[0].get_allumage() == 1:
                liste_flux[0].eteindre()
            if liste_flux[1].get_allumage() == 1:
                liste_flux[1].eteindre()
            if liste_flux[2].get_allumage() == 1:
                liste_flux[2].eteindre()
            M1.eteindre()
            if debug_mode:
                    print(P32.get_alimente())
                    print("prac 1 M1 eteint")
        elif Tank1.get_etat() and P11.get_etat() != -1:
            P11.allumer()
    if (P12.get_alimente() != "M2" and P32.get_alimente() != "M2"):
        if not Tank2.get_etat() and (P21.get_etat() == 1 or P21.get_etat() == -1):
            if liste_flux[3].get_allumage() == 1:
                liste_flux[3].eteindre()
            if liste_flux[4].get_allumage() == 1:
                liste_flux[4].eteindre()
            M2.eteindre()
            if P21.get_etat()!= -1:
                P21.eteindre()
            if P22.get_etat()!= -1:
                P22.eteindre()
        elif P21.get_etat() == -1 and P22.get_etat()!= 1:
            if liste_flux[3].get_allumage() == 1:
                liste_flux[3].eteindre()
            if liste_flux[4].get_allumage() == 1:
                liste_flux[4].eteindre()
            M2.eteindre()
            if debug_mode:
                    print(P22.get_alimente())
                    print("prac 2 M2 eteint")
        elif Tank2.get_etat() and P21.get_etat() != -1:
            P21.allumer()
    if (P22.get_alimente() != "M3" and P12.get_alimente() != "M3"):
        if not Tank3.get_etat() and (P31.get_etat() == 1 or P31.get_etat() == -1):
            if liste_flux[5].get_allumage() == 1:
                liste_flux[5].eteindre()
            if liste_flux[6].get_allumage() == 1:
                liste_flux[6].eteindre()
            if liste_flux[7].get_allumage() == 1:
                liste_flux[7].eteindre()
            M3.eteindre()
            if P31.get_etat()!= -1:
                P31.eteindre()
            if P32.get_etat()!= -1:
                P32.eteindre()
        elif P31.get_etat() == -1 and P32.get_etat()!= 1:
            if liste_flux[5].get_allumage() == 1:
                liste_flux[5].eteindre()
            if liste_flux[6].get_allumage() == 1:
                liste_flux[6].eteindre()
            if liste_flux[7].get_allumage() == 1:
                liste_flux[7].eteindre()
            M3.eteindre()
            if debug_mode:
                    print(P32.get_alimente())
                    print("prac 3 M3 eteint")
        elif Tank3.get_etat() and P31.get_etat() != -1:
            P31.allumer()

#fontion qui permet de generer une serie de pannes
def genere_panne(liste_tank,liste_pompe):
    rand_tank = random.randint(1,2) #nombre de tanks qui seront en panne
    rand_pompe = random.randint(1,3) #nombre de pompes qui seront en panne
    liste_panne = random.sample(range(0,len(liste_pompe)-1),rand_pompe)
    for val in liste_panne: #on met les pompes en panne
        liste_pompe[val].en_panne(event=None)
        if debug_mode:
            print(liste_pompe[val].get_name())
    liste_panne2 = random.sample(range(0,len(liste_tank)-1),rand_tank)
    for val in liste_panne2: #on met les tanks en panne
        liste_tank[val].vider()
        if debug_mode:
            print(liste_tank[val].get_name())
    eteindre_flux_moteur()


#fontion de la boucle principale
def boucle (window,username,compteur,score):
    if practice_mode:
        
        eteindre_flux_moteur2()
        eteindre_flux_moteur_pratice()
        reparer()
        allumer_vanne() 
        window.after(500, boucle, window,username,compteur,score)
    else:
        if compteur != nb_series: #on verifie que le compteur est inferieur au nombre de series de pannes
            if M1.get_etat() and M2.get_etat() and M3.get_etat(): #on verifie que les moteurs sont allumes(le pilote a resolu la pannne correctement ou non)
                compteur+=1
                score += resolution()
                reset()
                genere_panne(liste_tank,liste_pompe)
                if debug_mode:
                    print(score)
                window.after(500, boucle, window,username,compteur, score)
            else:
                eteindre_flux_moteur2()
                reparer()
                allumer_vanne() 
                window.after(500, boucle, window,username,compteur,score)
        else:
            end(window,username,score)
        
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

#fonction qui permet d'allumer les flux et de remplir les tanks avec les vannes VT12 et VT23
def allumer_vanne():
    if VT12.get_etat() and (not Tank1.get_etat() or not Tank2.get_etat()):
        liste_flux[14].allumer2()
        liste_flux[15].allumer2()
        if not Tank1.get_etat() and Tank2.get_etat():
            Tank1.remplir()
            
        elif not Tank2.get_etat() and Tank1.get_etat():
            Tank2.remplir()
    if not VT12.get_etat() and liste_flux[14].get_etat() and liste_flux[15].get_etat():
        liste_flux[14].eteindre2()
        liste_flux[15].eteindre2()
            
    if VT23.get_etat() and (not Tank3.get_etat() or not Tank2.get_etat()):
        liste_flux[16].allumer2()
        liste_flux[17].allumer2()
        
        if not Tank2.get_etat() and Tank3.get_etat():
            Tank2.remplir()
            
        elif not Tank3.get_etat() and Tank2.get_etat():
            Tank3.remplir()
    
    if not VT23.get_etat() and liste_flux[16].get_etat() and liste_flux[17].get_etat():
        liste_flux[16].eteindre2()
        liste_flux[17].eteindre2()

# permet d'allumer le moteur M1 et ses flux associés
def checkM1():  
    if M1.get_etat() == 0:
        if Tank1.get_etat():
            if P11.get_etat() == 1:
                liste_flux[0].allumer()
                liste_flux[1].allumer()
                liste_flux[2].allumer()
                if debug_mode:
                    print("1 M1")
                M1.allumer()
                return
            elif P11.get_etat() == -1:
                if P12.get_etat() == 1:
                    liste_flux[0].allumer()
                    liste_flux[1].allumer()
                    liste_flux[2].allumer()
                    if debug_mode:
                        print("2 M1")
                    M1.allumer()
                    P12.set_alimente("M1")
                    return
        if Tank2.get_etat():
            if P22.get_etat()== 1 and V12.get_etat() and P22.get_alimente() == None:
                liste_flux[3].allumer()
                liste_flux[11].allumer()
                liste_flux[10].allumer()
                liste_flux[2].allumer()
                if debug_mode:
                    print("3 M1")
                M1.allumer()
                P22.set_alimente("M1")
                return
        if Tank3.get_etat():
            if P32.get_etat() == 1 and V13.get_etat() and P32.get_alimente()== None:
                liste_flux[5].allumer()
                liste_flux[9].allumer()
                liste_flux[8].allumer()
                liste_flux[1].allumer()
                liste_flux[2].allumer()
                if debug_mode:
                    print("4 M1")
                M1.allumer()
                P32.set_alimente("M1")
                return

# permet d'allumer le moteur M2 et ses flux associés
def checkM2():
    if not M2.get_etat():
        if Tank2.get_etat():
            if P21.get_etat() == 1:
                liste_flux[3].allumer()
                liste_flux[4].allumer()
                if debug_mode:
                    print("1 M2")
                M2.allumer()
                return
            elif P21.get_etat() == -1:
                if P22.get_etat() == 1 and P22.get_alimente()== None:
                    liste_flux[3].allumer()
                    liste_flux[4].allumer()
                    if debug_mode:
                        print("2 M2")
                    M2.allumer()
                    P22.set_alimente("M2")
                    return
        if Tank1.get_etat():
            if P12.get_etat() == 1 and V12.get_etat() and P12.get_alimente() == None:
                liste_flux[0].allumer()
                liste_flux[1].allumer()
                liste_flux[10].allumer()
                liste_flux[11].allumer()
                liste_flux[4].allumer()
                if debug_mode:
                    print("3 M2")
                M2.allumer()
                P12.set_alimente("M2")
                return
        if Tank3.get_etat():
            if P32.get_etat() == 1 and V23.get_etat() and P32.get_alimente()== None:
                liste_flux[5].allumer()
                liste_flux[6].allumer()
                liste_flux[13].allumer()
                liste_flux[12].allumer()
                liste_flux[4].allumer()
                if debug_mode:
                    print("4 M2")
                M2.allumer()
                P32.set_alimente("M2")
                return

# permet d'allumer le moteur M3 et ses flux associés
def checkM3():
    if not M3.get_etat():
        if Tank3.get_etat():
            if P31.get_etat() == 1:
                liste_flux[5].allumer()
                liste_flux[6].allumer()
                liste_flux[7].allumer()
                M3.allumer()
                if debug_mode:
                    print("1 M3")
                return
            elif P31.get_etat() == -1:
                if P32.get_etat()== 1 and P32.get_alimente()== None:
                    liste_flux[5].allumer()
                    liste_flux[6].allumer()
                    liste_flux[7].allumer()
                    M3.allumer()
                    P32.set_alimente("M3")
                    if debug_mode:
                        print("2 M3")
                    return
        if Tank1.get_etat():
            if P12.get_etat() == 1 and V13.get_etat() and P12.get_alimente() == None:
                liste_flux[0].allumer()
                liste_flux[8].allumer()
                liste_flux[9].allumer()
                liste_flux[6].allumer()
                liste_flux[7].allumer()
                M3.allumer()
                P12.set_alimente("M3")
                if debug_mode:
                    print("3 M3")
                return
        if Tank2.get_etat():
            if P22.get_etat() == 1 and V23.get_etat() and P22.get_alimente() == None:
                liste_flux[3].allumer()
                liste_flux[12].allumer()
                liste_flux[13].allumer()
                liste_flux[7].allumer()
                M3.allumer()
                P22.set_alimente("M3")
                if debug_mode:
                    print("4")
                return

# permet de regrouper les fonctions checkM1, checkM2 et checkM3
def reparer():
    checkM1()
    checkM2()
    checkM3()


#fonction qui permet de verifier si le probleme a ete resolu correctement et qui attribue un point ou non au pilote
def resolution():
    if (P11.get_etat() == -1 and P12.get_etat() == 1 and P12.get_alimente() != "M1") or (P11.get_etat() == 1 and (P22.get_alimente() == "M1" or P32.get_alimente() == "M1")):
        return 0
    
    if (P21.get_etat() == -1 and P22.get_etat() == 1 and P22.get_alimente() != "M2") or (P21.get_etat() == 1 and (P12.get_alimente() == "M2" or P32.get_alimente() == "M2")):
        return 0
    
    if (P31.get_etat() == -1 and P32.get_etat() == 1 and P32.get_alimente() != "M3") or (P31.get_etat() == 1 and (P12.get_alimente() == "M3" or P22.get_alimente() == "M3")):
        return 0
    
    return 1


#fonction qui permet de renitialiser tout le systeme
def reset():
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

