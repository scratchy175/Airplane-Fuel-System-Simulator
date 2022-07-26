from Config import *
import math
from tkinter import *

# Classe mère de tous les composants
class Composant(object):
    def __init__(self,canvas,nom,points):
        self.canvas = canvas
        self.etat = 0
        self.nom = nom
        self.points = points[self.nom]

    def get_name(self):
        return self.nom

    def get_etat(self):
        return self.etat

# Classe permettant de créer un Tank
class Tank(Composant): #hérite de la classe Composant
    def __init__(self,canvas,nom,points,color,practice_mode):
        Composant.__init__(self,canvas,nom,points)
        self.practice_mode = practice_mode
        self.color = color
        self.etat = 1
        if self.nom == "Tank2": #permet de créer le Tank2 n'etant pas un polygone comme Tank1 et Tank3
            self.rectangle = self.canvas.create_rectangle(self.points["R"], fill=self.color, outline=self.color, width=3)
            self.forme= self.rectangle
        else:
            self.polygone = self.canvas.create_polygon(self.points["P"], fill=self.color, outline=self.color, width=3)
            self.forme= self.polygone
        if practice_mode: #si on est en mode pratique, permet de generer une panne de tank manuellement
            self.canvas.tag_bind(self.forme, "<Button-1>", self.change_etat)
            self.canvas.pack()
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, font=("Arial", 20,'bold'))
        self.rectangleP = self.canvas.create_rectangle(self.points["R2"], width=2)


    def change_etat(self,event): #permet de changer l'etat du tank
        if self.etat == 0:
            self.canvas.itemconfig(self.forme, fill=self.color)
            self.etat = 1
        elif self.etat == 1:
            self.canvas.itemconfig(self.forme, fill="#0269A4")
            self.etat = 0
    
    def remplir(self): #permet de remplir le tank
        self.canvas.itemconfig(self.forme, fill=self.color)
        self.etat = 1
    
    def vider(self): #permet de vider le tank
        self.canvas.itemconfig(self.forme, fill="#0269A4")
        self.etat = 0

# Classe permettant de créer une vanne
class Vanne(Composant): #hérite de la classe Composant
    def __init__(self,canvas,frame,nom,points):
        Composant.__init__(self,canvas,nom,points)
        self.frame = frame
        #affichage graphique de la vanne
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, font=("Arial",20,'bold'))
        self.cercle = self.canvas.create_oval(self.points["C"],fill="Black")
        self.polygone = self.canvas.create_polygon(self.points["P2"], fill="White")

        self.x1, self.y1 = self.points["P2"][0], self.points["P2"][1]
        self.x2, self.y2 = self.points["P2"][4], self.points["P2"][5]
        self.centre = ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        self.counter = 1

        #création du bouton de la vanne
        self.image_off = PhotoImage(file=f"images/{self.nom}_off.png")
        self.image_on = PhotoImage(file=f"images/{self.nom}_on.png")
        self.button = Button(self.frame, text=self.nom,image=self.image_off, borderwidth=0, bg="#202124",activebackground="#202124", command=self.change_etat)
        self.button.pack(side=LEFT,expand=True)
        
    
    def change_etat(self): #permet de changer l'etat de la vanne
        if self.etat == 0:
            self.button.config(image=self.image_on)
            self.rt()
            
            self.etat = 1
        elif self.etat == 1:
            self.rt()
            self.button.config(image=self.image_off)
            self.etat = 0
    
    def rotation(self, points, angle, centre): #permet de faire une rotation de points autour d'un centre
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = centre
        new_points = []
        for i in range (0,len(points),2):
            x_old = points[i]
            y_old = points[i+1]
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.extend((x_new + cx, y_new + cy))
        return new_points

    def rt(self,mode=None): #permet de faire une rotation de la vanne
        if mode == "reset" and self.etat == 0:
            self.new_square = self.rotation(self.points["P2"], -self.counter, self.centre)
            return
        if self.etat == 1:
            self.new_square = self.rotation(self.points["P2"], self.counter, self.centre)
        elif self.etat == 0:
            self.new_square = self.rotation(self.points["P2"], -self.counter, self.centre)
        self.canvas.coords(self.polygone, self.new_square)
        if self.counter<90:
            self.counter+=1
            self.canvas.after(1, self.rt)
        else:
            self.counter = 1
            self.points["P2"] = self.new_square

    #permet de renitialiser la vanne par défaut
    def reset_vanne(self):
        self.rt("reset")
        self.button.config(image=self.image_off)
        self.etat = 0

# Classe permettant de créer une pompe
class Pompe(Composant): #hérite de la classe Composant
    def __init__(self,canvas,practice_mode,frame,nom,points,nature="Normal"):
        Composant.__init__(self,canvas,nom,points)
        self.frame = frame
        self.nature = nature
        self.practice_mode = practice_mode
        #affichage graphique de la pompe
        self.cercle = self.canvas.create_oval(self.points["C"],fill="Black")
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, fill="White", font=("Arial",15,'bold'))
        if practice_mode: #si on est en mode pratique, permet de generer une panne de pompe manuellement
            self.canvas.tag_bind(self.text, "<Button-1>", self.en_panne)
            self.canvas.tag_bind(self.cercle, "<Button-1>", self.en_panne)


        if self.nature == "Secours": #si la pompe est une pompe de secours, on crée un bouton pour l'activer
            self.alimente = None
            self.image_off = PhotoImage(file=f"images/{self.nom}_off.png")
            self.image_on = PhotoImage(file=f"images/{self.nom}_on.png")
            self.button = Button(self.frame, text=self.nom,image=self.image_off, borderwidth=0, bg="#202124",activebackground="#202124", command=self.change_etat)
            self.button.pack(side=LEFT,expand=True,fill=BOTH)

        elif self.nature == "Normal": #si la pompe est une pompe normale, on l'allume par défaut
            self.allumer()

    #permet de changer l'etat de la pompe
    def change_etat(self):
        if self.etat == 0:
            self.canvas.itemconfig(self.cercle, fill="Green")
            self.button.config(image=self.image_on)
            self.etat = 1
        elif self.etat == 1:
            self.button.config(image=self.image_off)
            self.canvas.itemconfig(self.cercle, fill="Black")
            self.etat = 0

    
    #permet d'allumer la pompe
    def allumer(self):
        if self.nature == "Secours":
            self.button.config(image=self.image_on)
        self.canvas.itemconfig(self.cercle, fill="Green")
        self.etat = 1

    #permet d'eteindre la pompe
    def eteindre(self):
        if self.nature == "Secours":
            self.button.config(image=self.image_off)
        self.canvas.itemconfig(self.cercle, fill="Black")
        self.etat = 0

    #permet de definir quel moteur la pompe alimente
    def set_alimente(self,alimente):
        self.alimente = alimente

    #permet de recuperer quel moteur la pompe alimente
    def get_alimente(self):
        return self.alimente

    #permet de mettre la pompe en panne
    def en_panne(self,event):
        if self.etat in [0, 1]:
            if self.nature == "Secours":
                self.button.config(state=DISABLED)
            self.canvas.itemconfig(self.cercle, fill="Orange")
            self.etat = -1
        elif self.etat == -1:
            if self.nature == "Secours":
                self.button.config(image=self.image_off)
                self.button.config(state=NORMAL)
                self.canvas.itemconfig(self.cercle, fill="Black")
                self.etat = 0
            elif self.nature == "Normal":
                self.canvas.itemconfig(self.cercle, fill="Green")
                self.etat = 1
    
    #permet de renitialiser la pompe par défaut
    def reset_pompe(self):
        if self.nature == "Secours": 
            self.set_alimente(None)
            self.canvas.itemconfig(self.cercle, fill="Black")
            self.button.config(image=self.image_off, state=NORMAL)
            self.etat = 0
        elif self.nature == "Normal":
            self.canvas.itemconfig(self.cercle, fill="Green")
            self.etat = 1
    
# Classe permettant de créer un moteur
class Moteur(Composant): #hérite de la classe Composant
    def __init__(self,canvas,nom,points):
        Composant.__init__(self,canvas,nom,points)
        self.etat = 1
        #affichage graphique du moteur
        self.rectangle = self.canvas.create_rectangle(self.points["R"], fill="Green", outline="Grey", width=2)
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, font=("Arial",20,'bold'))

    #permet d'eteindre le moteur
    def eteindre(self):
        self.canvas.itemconfig(self.rectangle, fill="Grey")
        self.etat = 0

    #permet d'allumer le moteur
    def allumer(self):
        self.canvas.itemconfig(self.rectangle, fill="Green")
        self.etat = 1

    
# Classe permettant de créer un flux
class Flux(object):
    def __init__(self,canvas,nom,points):
        self.canvas = canvas
        self.etat = 0
        self.nom = nom
        self.nb_allumage = 0
        self.points = points["F"]
        self.line = self.canvas.create_line(self.points[self.nom], fill="Black", width=2)


    #permet de recuperer l'etat du flux
    def get_etat(self):
        return self.etat

    #permet d'eteindre le flux
    def eteindre(self):
        self.add_allumage(-1)
        if self.get_allumage() == 0:
            self.canvas.itemconfig(self.line, fill="Black", width=2)
            self.etat = 0
    
    #permet d'allumer le flux
    def allumer(self):
        if self.get_allumage() == 0:
            self.canvas.itemconfig(self.line, fill="Red", width=5)
            self.etat = 1
        self.add_allumage(1)

    #permet d'allumer le flux2 de la vanne VT12 et VT23
    def allumer2(self):
        self.canvas.itemconfig(self.line, fill="Red", width=5)
        self.etat = 1
    
    #permet d'eteindre le flux de la vanne VT12 et VT23
    def eteindre2(self):
        self.canvas.itemconfig(self.line, fill="Black", width=2)
        self.etat = 0

    #permet de recuperer le nombre d'allumage du flux
    def get_allumage(self):
        return self.nb_allumage

    #permet de mettre a jour le nombre d'allumage du flux
    def add_allumage(self,nb):
        self.nb_allumage += nb

    #permet de renitialiser les flux
    def reset_flux(self):
        self.nb_allumage = 0
        self.canvas.itemconfig(self.line, fill="Black", width=2)
        self.etat = 0

    