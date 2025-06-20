import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class CreadorGui(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x600")
        self.master.title("Este no es un virtus")
        self.pack()

        welcome_text = "Proyecto de programación, virus keylogger"
        mi_fuente = ("Arial", 16, "bold")
        welcome = ttk.Label(self, text=welcome_text, font=mi_fuente)
        welcome.pack (fill=X, pady=10)

        #Menu chapioya

        #Establecer conección

        boton_getConection = ttk.Button(self, text= "Establecer conección")
        boton_getConection.pack(side="left", padx=10, pady=0)

        #Ver lo leído 

        boton_getConection = ttk.Button(self, text= "Ver teclas leídas")
        boton_getConection.pack(side="left", padx=10, pady=30)

        #Abrir el fichero

        boton_getConection = ttk.Button(self, text= "Abrir fichero")
        boton_getConection.pack(side="left", padx=10, pady=10) 

        

        #boton = ttk.Button(root, text="Haz clic aquí", bootstyle=PRIMARY)
        #boton.pack(pady=20)#



if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = CreadorGui(root)
    root.mainloop()