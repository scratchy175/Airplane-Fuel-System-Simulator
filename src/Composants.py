import math
from tkinter import *


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

    """def setEtat(self,etat):
        self.etat = etat"""

class Tank(Composant):
    def __init__(self,canvas,nom,points,color):
        Composant.__init__(self,canvas,nom,points)
        self.color = color
        self.etat = 1
        if self.nom == "Tank2":
            self.rectangle = self.canvas.create_rectangle(self.points["R"], fill=self.color, outline=self.color, width=3)
            self.forme= self.rectangle
        else:
            self.polygone = self.canvas.create_polygon(self.points["P"], fill=self.color, outline=self.color, width=3)
            self.forme= self.polygone
        self.canvas.tag_bind(self.forme, "<Button-1>", self.change_etat)
        self.canvas.pack()
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, font=("Arial", 20,'bold'))
        self.rectangleP = self.canvas.create_rectangle(self.points["R2"], width=2)


    def change_etat(self,event):
        if self.etat == 0:
            self.canvas.itemconfig(self.forme, fill="#0269A4")
            self.etat = 1
        elif self.etat == 1:
            self.canvas.itemconfig(self.forme, fill=self.color)
            self.etat = 0
    
    def remplir(self):
        self.canvas.itemconfig(self.forme, fill=self.color)
        self.etat = 1
    
    def vider(self):
        self.canvas.itemconfig(self.forme, fill="#0269A4")
        self.etat = 0


class Vanne(Composant):
    def __init__(self,canvas,frame,nom,points):
        Composant.__init__(self,canvas,nom,points)
        self.frame = frame

        self.text = self.canvas.create_text(self.points["T"], text=self.nom, font=("Arial",20,'bold'))
        self.cercle = self.canvas.create_oval(self.points["C"],fill="Black")
        self.polygone = self.canvas.create_polygon(self.points["P2"], fill="White")

        self.x1, self.y1 = self.points["P2"][0], self.points["P2"][1]
        self.x2, self.y2 = self.points["P2"][4], self.points["P2"][5]
        self.centre = ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        self.counter = 1

        self.image_off = PhotoImage(file="images/" + self.nom + "_off.png")
        self.image_on = PhotoImage(file="images/" + self.nom + "_on.png")
        self.button = Button(self.frame, text=self.nom,image=self.image_off, borderwidth=0, bg="#202124",activebackground="#202124", command=self.change_etat)
        self.button.pack(side=LEFT,expand=True)
        
    
    """def get_etat(self):
        return self.etat"""

    def change_etat(self):
        if self.etat == 0:
            self.button.config(image=self.image_on)
            self.rt()
            
            self.etat = 1
        elif self.etat == 1:
            self.rt()
            self.button.config(image=self.image_off)
            self.etat = 0
    
    def rotation(self, points, angle, centre):
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
            new_points.append(x_new + cx)
            new_points.append(y_new + cy)
        return new_points

    def rt(self,mode=None):
        if mode == "reset":
            if self.etat == 0:
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

    """def ouvrir(self):
        self.etat = 1"""

    def reset_vanne(self):
        self.rt("reset")
        self.button.config(image=self.image_off)
        self.etat = 0


class Pompe(Composant):
    def __init__(self,canvas,frame,nom,points,nature="Normal"):
        Composant.__init__(self,canvas,nom,points)
        self.frame = frame
        self.nature = nature
        
        self.cercle = self.canvas.create_oval(self.points["C"],fill="Black")
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, fill="White", font=("Arial",15,'bold'))
        self.canvas.tag_bind(self.text, "<Button-1>", self.en_panne)
        self.canvas.tag_bind(self.cercle, "<Button-1>", self.en_panne)
    
        
        if self.nature == "Secours":
            self.alimente = None
            self.image_off = PhotoImage(file="images/" + self.nom + "_off.png")
            self.image_on = PhotoImage(file="images/" + self.nom + "_on.png")
            self.button = Button(self.frame, text=self.nom,image=self.image_off, borderwidth=0, bg="#202124",activebackground="#202124", command=self.change_etat)
            self.button.pack(side=LEFT,expand=True,fill=BOTH)
        
        elif self.nature == "Normal":
            self.allumer()


    """def get_nature(self):
        return self.nature"""

    def change_etat(self):
        if self.etat == 0:
            self.canvas.itemconfig(self.cercle, fill="Green")
            self.button.config(image=self.image_on)
            self.etat = 1
            self.clignoter()
        elif self.etat == 1:
            self.button.config(image=self.image_off)
            self.canvas.itemconfig(self.cercle, fill="Black")
            self.etat = 0
    
    def clignoter(self):
        if self.etat == 1:
            if self.canvas.itemcget(self.cercle, 'fill') == "Black":
                self.canvas.itemconfig(self.cercle, fill="Green")
            else:
                self.canvas.itemconfig(self.cercle, fill="Black")
            
            self.canvas.after(500, self.clignoter)

    def allumer(self):
        self.canvas.itemconfig(self.cercle, fill="Green")
        self.etat = 1

    def eteindre(self):
        self.canvas.itemconfig(self.cercle, fill="Black")
        self.etat = 0


    def set_alimente(self,alimente):
        self.alimente = alimente

    def get_alimente(self):
        return self.alimente


    def en_panne(self,event):
        if self.nature == "Secours":
            self.button.config(state=DISABLED)
        self.canvas.itemconfig(self.cercle, fill="Orange")
        self.etat = -1

    def reset_pompe(self):
        if self.nature == "Secours": 
            self.set_alimente(None)
            self.canvas.itemconfig(self.cercle, fill="Black")
            self.button.config(image=self.image_off, state=NORMAL)
            self.etat = 0
        elif self.nature == "Normal":
            self.canvas.itemconfig(self.cercle, fill="Green")
            self.etat = 1
    

class Moteur(Composant):
    def __init__(self,canvas,nom,points):
        Composant.__init__(self,canvas,nom,points)
        self.etat = 1
        self.rectangle = self.canvas.create_rectangle(self.points["R"], fill="Green", outline="Grey", width=2)
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, font=("Arial",20,'bold'))

    """def get_etat(self):
        return self.etat"""

    """def change_etat(self):
        if self.etat == 0:
            self.canvas.itemconfig(self.rectangle, fill="Green")
            self.etat = 1
        elif self.etat == 1:
            self.canvas.itemconfig(self.rectangle, fill="Grey")
            self.etat = 0"""

    def eteindre(self):
        self.canvas.itemconfig(self.rectangle, fill="Grey")
        self.etat = 0

    def allumer(self):
        self.canvas.itemconfig(self.rectangle, fill="Green")
        self.etat = 1

    

class Flux(object):
    def __init__(self,canvas,nom,points):
        self.canvas = canvas
        self.etat = 0
        self.nom = nom
        self.nb_allumage = 0
        self.points = points["F"]
        self.line = self.canvas.create_line(self.points[self.nom], fill="Black", width=2)

    def get_etat(self):
        return self.etat

    """def change_etat(self):
        if self.etat == 0:
            self.canvas.itemconfig(self.line, fill="Red", width=5)
            self.etat = 1
        elif self.etat == 1:
            self.canvas.itemconfig(self.line, fill="Black", width=2)
            self.etat = 0"""

    def eteindre(self):
        self.add_allumage(-1)
        if self.get_allumage() == 0:
            self.canvas.itemconfig(self.line, fill="Black", width=2)
            self.etat = 0
    
    def allumer(self):
        if self.get_allumage() == 0:
            self.canvas.itemconfig(self.line, fill="Red", width=5)
            self.etat = 1
        self.add_allumage(1)

    def allumer2(self):
        self.canvas.itemconfig(self.line, fill="Red", width=5)
        self.etat = 1
    
    def eteindre2(self):
        self.canvas.itemconfig(self.line, fill="Black", width=2)
        self.etat = 0

        
    def get_allumage(self):
        return self.nb_allumage

    def add_allumage(self,nb):
        self.nb_allumage += nb

    def reset_flux(self):
        self.nb_allumage = 0
        self.canvas.itemconfig(self.line, fill="Black", width=2)
        self.etat = 0

    