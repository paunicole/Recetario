"""Autoras: Nicole Cardozo Gómez - Daniela Gutierrez Aliaga"""

import tkinter as tk

from tkinter import ttk
from PIL import ImageTk, Image
from modulos.ver_mas import VerMas
from modulos.crear_receta import CrearReceta
from modulos.listar_recetas import ListarRecetas
from modulos.logica import receta_aleatoria

class App(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent                      
        parent.title("Cocina Conmigo")
        #parent.geometry("700x500")
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.resizable(False, False)
        parent.iconbitmap('imagenes/logo.ico')

        # ------- FRAME COCINA CONMIGO -------
        titulo = tk.Frame(self, width=700, height=100, background='black')
        titulo.grid(row=0, column=0, columnspan=2, sticky='EW')

        photo = tk.PhotoImage(file='imagenes/cocina_conmigo.png')
        photo = photo.subsample(5)

        title = tk.Label(self,
                        text='¡Bienvenidos a Cocina Conmigo!',
                        image=photo,
                        font=('Arial', 25, 'bold'), 
                        bg='black', 
                        fg='#FFFFFF',
                        compound='left' # Muestra la imagen a la izquierda del texto.
                        )
        title.img_ref = photo
        title.grid(row=0, column=0, columnspan=2) 


        # -------- FRAME RECETA DEL DIA -------

        cuadro = tk.Frame(self, width=390, height=180,  background='yellow', highlightbackground='black', highlightthickness=2, borderwidth=10)
        cuadro.grid(row=1, column=0, padx=5, pady=5, ipady=5)

        # titulo
        ttk.Label(cuadro, text="RECETA DEL DIA:", font=("Cambria", 15), background='yellow').grid(row=1, column=0, sticky='W') # etiqueta "RECETA DEL DIA"
        
        # Obtengo una receta aleatoria
        self.receta = receta_aleatoria()
        
        # imagen
        ruta_imagen = self.receta['imagen']
        img = Image.open(ruta_imagen)
        img = img.resize((300, 200), Image.ANTIALIAS)
        imagen = ImageTk.PhotoImage(img)
        label_imagen = ttk.Label(cuadro, image=imagen)
        label_imagen.img_ref = imagen  # Nunca te olvides de mantener una referencia
        label_imagen.grid(row=2, column=0, rowspan=5, sticky='W')
        
        # nombre
        ttk.Label(cuadro, text=self.receta['nombre'], background='yellow', font=('Britannic Bold', 20)).grid(row=2, column=1, sticky='W')

        # tiempo preparacion
        ttk.Label(cuadro, text="Preparación:", background='yellow').grid(row=3, column=1, sticky='W')
        preparacion = str(self.receta['tiempo_preparacion']) + ' min'
        ttk.Label(cuadro, text=preparacion, background='yellow', font=('Berlin Sans FB', 15)).grid(row=4, column=1, sticky='W')

        # tiempo coccion
        ttk.Label(cuadro, text="Cocción:", background='yellow').grid(row=5, column=1, sticky='W')
        coccion = str(self.receta['tiempo_coccion']) + ' min'
        ttk.Label(cuadro, text=coccion, background='yellow', font=('Berlin Sans FB', 15)).grid(row=6, column=1, sticky='W')

        tk.Button(cuadro, text="Ver más", bg="orange", fg="black", width=10, command=self.ver_mas).grid(row=7, column=1, sticky='E')

        # -------- FRAME BOTONES -------

        cuadro2 = tk.Frame(self)
        cuadro2.grid(row=1, column=1)

        tk.Button(cuadro2, text="Crear receta", bg="orange", fg="black", width=10, command=self.crear_receta).grid(row=0, column=0, sticky='N')
        tk.Button(cuadro2, text="Listar recetas", bg="orange", fg="black", width=10, command=self.listar_recetas).grid(row=1, column=0) 

    def ver_mas(self):
        toplevel = tk.Toplevel(self.parent)
        VerMas(toplevel, self.receta).grid()

    def crear_receta(self):
        toplevel = tk.Toplevel(self.parent)
        CrearReceta(toplevel).grid()

    def listar_recetas(self):
        toplevel = tk.Toplevel(self.parent)
        ListarRecetas(toplevel).grid()


root = tk.Tk()
App(root).grid()
root.mainloop()