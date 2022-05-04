
import math
from tkinter import *


class Composant(object):
    def __init__(self,canvas,nom,points):
        self.canvas = canvas
        self.etat = 0
        self.nom = nom
        self.points = points[self.nom]

    def getEtat(self):
        return self.etat

    """def setEtat(self,etat):
        self.etat = etat"""

class Tank(Composant):
    
    def __init__(self,canvas,nom,points,color):
        Composant.__init__(self,canvas,nom,points)
        self.color = color
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
        
        
    def get_etat(self):
        if self.etat == 0:
            return "vide"
        elif self.etat == 1:
            return "plein"

    def change_etat(self,event):
        if self.etat == 0:
            self.canvas.itemconfig(self.forme, fill="#0269A4")
            self.etat = 1
        elif self.etat == 1:
            self.canvas.itemconfig(self.forme, fill=self.color)
            self.etat = 0
    
    def remplir(self):
        self.etat = 1
    
    def vider(self):
        self.etat = 0
        print("bite")

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

        self.button = Button(self.frame, text=self.nom,font= ("Arial",20,"bold"),height = 2,width = 2, command=self.change_etat,bg="#880808")
        self.button.pack(fill=X, side=LEFT,expand=True, padx=50)
    
    def get_etat(self):
        if self.etat == 0:
            return "fermé"
        elif self.etat == 1:
            return "ouvert"

    def change_etat(self):
        #self.rt()
        if self.etat == 0:
            self.button.config(bg="Green")
            self.rt()
            self.etat = 1
        elif self.etat == 1:
            self.rt()
            self.button.config(bg="#880808")
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

    def rt(self):
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
        self.etat = 1

    def fermer(self):
        self.etat = 0"""

class Pompe(Composant):
    def __init__(self,canvas,frame,nom,points,nature="Normal"):
        Composant.__init__(self,canvas,nom,points)
        self.frame = frame
        self.nature = nature
        self.cercle = self.canvas.create_oval(self.points["C"],fill="Black")
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, fill="White", font=("Arial",15,'bold'))
        self.canvas.tag_bind(self.text, "<Button-1>", self.en_panne)
        self.canvas.tag_bind(self.cercle, "<Button-1>", self.en_panne)
        if nature == "Secours":
            self.button = Button(self.frame, text=self.nom,font= ("Arial",20,"bold"), height = 2,width = 2, command=self.change_etat,bg="#880808",activebackground="Green")
            self.button.pack(fill=X, side=LEFT,expand=True, padx=50)
    

    def get_etat(self):
        return self.etat

    def get_nature(self):
        return self.nature

    def change_etat(self): #que si pompe de secours

        if self.etat == 0:
            self.button.config(bg="Green",activebackground="#880808")
            self.etat = 1
            self.clignoter()
        elif self.etat == 1:
            self.button.config(bg="#880808")
            self.canvas.itemconfig(self.cercle, fill="Black")
            self.etat = 0
    
    def clignoter(self): #faire clignoter si pompe en panne
        if self.etat == 1:
            if self.canvas.itemcget(self.cercle, 'fill') == "Black":
                self.canvas.itemconfig(self.cercle, fill="Green")
            else:
                self.canvas.itemconfig(self.cercle, fill="Black")
            
            self.canvas.after(500, self.clignoter)

    def allumer(self):
        self.etat = 1

    def eteindre(self):
        self.etat = 0

    def en_panne(self,event):
        if self.etat == -1:
            self.button.config(bg="#880808",state=NORMAL)
            self.canvas.itemconfig(self.cercle, fill="Black")
            self.etat = 0
        else:
            self.button.config(bg="Grey",state=DISABLED)
            self.canvas.itemconfig(self.cercle, fill="Orange")
            self.etat = -1

class Moteur(Composant):
    def __init__(self,canvas,nom,points):
        Composant.__init__(self,canvas,nom,points)
        self.rectangle = self.canvas.create_rectangle(self.points["R"], fill="Grey", outline="Grey")
        self.text = self.canvas.create_text(self.points["T"], text=self.nom, font=("Arial",20,'bold'))

class Flux(object):
    def __init__(self,canvas,nom,points):
        self.canvas = canvas
        self.etat = 0
        self.nom = nom
        self.points = points["F"]
        self.line = self.canvas.create_line(self.points[self.nom], fill="Black", width=2)

    def change_etat(self):
        if self.etat == 0:
            self.canvas.itemconfig(self.line, fill="Yellow", width=5)
            self.etat = 1
        elif self.etat == 1:
            self.canvas.itemconfig(self.line, fill="Black", width=2)
            self.etat = 0

def create_window(root,dico):
    global liste_flux

    root.destroy()
    window = Tk()
    window.title("Tableau de bord du pilote")
    window.geometry("1000x500+300+300")
    window.iconbitmap("plane.ico")
    frame = Frame(window, bg="#0269A4")
    frame.pack(side= TOP, expand=True, fill=BOTH)
    frame2 = Frame(window, bg="#0269A4")
    frame2.pack(side= TOP, expand=True, fill=BOTH)
    frame3 = Frame(window, bg="#0269A4")
    frame3.pack(side= TOP, expand=True, fill=BOTH)
    window2 = Toplevel(window)
    window2.title("Etat du système de carburant")
    window2.geometry("600x600+1500+250")
    window2.iconbitmap("plane.ico")
    canvas = Canvas(window2, width=600, height=600, bg="#0269A4")
    canvas.pack(expand=True)

    Tank1 = Tank(canvas,"Tank1",dico,"Orange")
    Tank2 = Tank(canvas,"Tank2",dico,"Green")
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
    liste_flux = [Flux(canvas,"L"+str(i),dico) for i in range(1,len(dico["F"])+1)]

    for i in range(8):
        liste_flux[i].change_etat()
    """liste_flux[0].change_etat()
    liste_flux[1].change_etat()
    liste_flux[2].change_etat()"""
    window.mainloop()
    return liste_flux





if __name__ == "__main__":


    root = Tk()
    root.title("Login")
    root.geometry("500x500")
    root.iconbitmap("plane.ico")
    frame = Frame(root,width=500,height=500, bg="#0269A4")
    #frame.pack(side= TOP, expand=True, fill=BOTH)
    
    username = Label(frame, text="Username", bg="#0269A4", fg="Black", font=("Arial",20,'bold'))
    #username.grid(row=0, column=2)
    username.pack()
    
    #frame.pack(expand=True)
    username_entry = Entry(frame, bg="White", fg="Black", font=("Arial",20,'bold'))
    #username_entry.grid(row=1, column=2)
    username_entry.pack()
    password = Label(frame, text="Password", bg="#0269A4", fg="Black", font=("Arial",20,'bold'))
    password.pack()
    password_entry = Entry(frame, bg="White", fg="Black", font=("Arial",20,'bold'))
    password_entry.pack()
    login_button = Button(frame, text="Login", command= lambda:create_window(root,dico))
    login_button.pack()
    register_button = Button(frame, text="Login", command= lambda:create_window(root,dico))
    register_button.pack()
    frame.pack(expand=True)

    dico = {"Tank1":{"P":(25, 180, 25, 90, 145, 30, 145, 180),"T":(90,110),"R2":(50, 130, 145, 180)},
            "Tank2":{"R":(240, 30, 360, 180),"T":(300,110),"R2":(250, 130, 350, 180)},
            "Tank3":{"P":(575, 180, 575, 90, 455, 30, 455, 180),"T":(510,110),"R2":(455, 130, 550, 180)},

            "P11":{"C":(55,135, 95, 175),"T":(75,155)},
            "P12":{"C":(100,135, 140, 175),"T":(120,155)},
            "P21":{"C":(255,135, 295, 175),"T":(275,155)},
            "P22":{"C":(305,135, 345, 175),"T":(325,155)},
            "P31":{"C":(460,135, 500, 175),"T":(480,155)},
            "P32":{"C":(505,135, 545, 175),"T":(525,155)},

            "VT12":{"C":(162, 80, 222, 140),"T":(190,60),"P2":(187, 80, 197, 80, 197, 140, 187, 140)},
            "VT23":{"C":(378, 80, 438, 140),"T":(410,60),"P2":(403, 80, 413, 80, 413, 140, 403, 140)},
            "V12":{"C":(162, 330, 222, 390),"T":(190,310),"P2":(187, 330, 197, 330, 197, 390, 187, 390)},
            "V13":{"C":(328, 220, 388, 280),"T":(360,200),"P2":(353, 220, 363, 220, 363, 280, 353, 280)},
            "V23":{"C":(378, 330, 438, 390),"T":(410,310),"P2":(403, 330, 413, 330, 413, 390, 403, 390)},

            "M1":{"R":(60, 430, 110, 580),"T":(85,500)},
            "M2":{"R":(275, 430, 325, 580),"T":(300,500)},
            "M3":{"R":(490, 430, 540, 580),"T":(515,500)},

            "F":{"L1":(85, 180, 85, 250),"L2":(85, 250, 85, 360),"L3":(85, 360, 85, 430),
                "L4":(300, 180, 300, 360),"L5":(300, 360, 300, 430),
                "L6":(515, 180, 515, 250),"L7":(515, 250, 515, 360),"L8":(515, 360, 515, 430),
                "L9":(85, 250, 328, 250),"L10":(388, 250, 515, 250),
                "L11":(85, 360, 162, 360),"L12":(222, 360, 300, 360),
                "L13":(300, 360, 378, 360),"L14":(438, 360, 515, 360),
                "L15":(145, 110, 162, 110),"L16":(222, 110, 240, 110),
                "L17":(360, 110, 378, 110),"L18":(438, 110, 455, 110),}
            }
 
    ##panne pompes et vidange reservoirs aleatoires ou pas ?
    # Si oui alors faire un systeme de bouton qui genere une panne aleatoire d'une ou plusieurs pompes et d'un ou plusieurs reservoirs

    # voir pour utiliser une classe pour la creation de la nouvelle fenetre 
    #crée le menu de login
    #faire la gestion des flux
    #split en plusieurs fichiers

    #window.mainloop()
    root.mainloop()


