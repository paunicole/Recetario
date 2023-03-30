import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from modulos.logica import devuelve_str_ingredientes_2, devuelve_str_preparacion_2, devuelve_str_etiquetas

class VerMas(ttk.Frame):

    """Clase que muestra detalladamente una receta ya creada anteriormente."""

    def __init__(self, parent, receta):
        super().__init__(parent, padding=(10))
        self.parent = parent                                 # referencia a la ventana ppal
        parent.title("Ver Receta")                           # titulo de la ventana
        parent.iconbitmap('imagenes/logo.ico')               # cambiamos el icono

        # Imagen
        ruta_imagen = receta['imagen']
        img = Image.open(ruta_imagen)
        img = img.resize((300, 200), Image.ANTIALIAS)
        imagen = ImageTk.PhotoImage(img)
        label_imagen = ttk.Label(self, image=imagen)
        label_imagen.img_ref = imagen # Nunca te olvides de mantener una referencia
        label_imagen.grid(row=0, column=0, rowspan=6, sticky='W')
        
        # Nombre
        ttk.Label(self, text=receta['nombre'], padding=3, font=("Helvetica", 30)).grid(row=0, column=1, sticky='W')

        # Favorita: si no es favorita no muestra nada
        if receta['es_favorita']:
            ttk.Label(self, text="Favorita", padding=3, font=("Dubai", 10), background="yellow", relief="raised").grid(row=1, column=1, sticky='W')

        # Tiempo de preparación
        ttk.Label(self, text="Tiempo de Preparación:", padding=3).grid(row=2, column=1, sticky='W')
        ttk.Label(self, text=f"{receta['tiempo_preparacion']} min", padding=3, font=("Berlin Sans FB", 15)).grid(row=3, column=1, sticky='W')
        
        # Tiempo de Coción
        ttk.Label(self, text="Tiempo de Cocción:", padding=3).grid(row=4, column=1, sticky='W')
        ttk.Label(self, text=f"{receta['tiempo_coccion']} min", padding=3, font=("Berlin Sans FB", 15)).grid(row=5, column=1, sticky='W')
        
        # Etiquetas
        list_etiquetas = receta['etiquetas']
        str_etiquetas = devuelve_str_etiquetas(list_etiquetas)
        ttk.Label(self, text=str_etiquetas, padding=3, foreground='green').grid(row=6, column=0, sticky='EW')

        # Lista de Ingredientes
        ttk.Label(self, text="Ingredientes", padding=3, font=("Arial Black", 15)).grid(row=7, column=0, sticky='W')
        
        list_ingredientes = receta["lista_ingredientes"]
        str_ingredientes = devuelve_str_ingredientes_2(list_ingredientes)
        ttk.Label(self, text=str_ingredientes, padding=3).grid(row=8, column=0, sticky='NW')

        # Preparación
        ttk.Label(self, text="Preparación", padding=3, font=("Arial Black", 15)).grid(row=7, column=1, sticky='W')
        
        list_preparacion = receta["preparacion"]
        str_preparacion = devuelve_str_preparacion_2(list_preparacion)
        ttk.Label(self, text=str_preparacion, padding=3, wraplength=450).grid(row=8, column=1, sticky='NW')

        # Fecha creación
        ttk.Label(self, text=f"Fecha creación: {receta['fecha_creacion']}", padding=3).grid(row=10, column=0, sticky='W')

        # Boton Salir
        boton_salir = tk.Button(self, text="Salir", bg="orange", fg="black", width=10, command=self.salir)
        boton_salir.grid(row=10, column=2)

        parent.bind('<Return>', lambda e: boton_salir.invoke()) # para ejecutar el btn al presionar enter
        

    def salir(self):
        """Método para salir de la ventana."""
        self.parent.destroy() # Terminamos el programa al destruir la ventana ppal                                          