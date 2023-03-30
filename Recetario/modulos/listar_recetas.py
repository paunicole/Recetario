import tkinter as tk
import json

from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk 
from modulos.ver_mas import VerMas
from modulos.editar_receta import EditarReceta
from modulos.logica import deserializar, serializar

class ListarRecetas(ttk.Frame):
    """Clase para listar las recetas."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent                            # referencia a la ventana ppal
        parent.title("Listar Receta")                   # titulo de la ventana
        parent.iconbitmap('imagenes/logo.ico')          # cambiamos el icono
        parent.geometry("700x500+100+100")

        self.tree = self.crear_tree()
        self.insertar_datos()
        self.crear_botones()

        # ---- FRAME FILTRAR ----
        self.frame_filtro = ttk.Frame(self)
        self.frame_filtro = ttk.Labelframe(self, text='Filtrar')
        self.frame_filtro.grid(row=0, column=0)
        
        self.lb_filtro = ttk.Label(self.frame_filtro, text='Filtrar por: ').grid(row=0, column=0, sticky='E', pady=10, padx=(15,0))
        
        self.combo_lista = tk.StringVar()
        self.combo_elementos = tk.StringVar()
        
        self.lista_filtro=ttk.Combobox(self.frame_filtro,textvariable=self.combo_lista)
        self.lista_filtro["values"] = ('Nombre', 'Etiqueta', 'Tiempo de Preparación', 'Ingrediente')
        self.lista_filtro["state"] = "readonly"        
        self.lista_filtro.grid(row=0,column=1,pady=10,padx=(0,15))
        print(self.combo_lista.get())
        self.lista_filtro.bind('<<ComboboxSelected>>', self.elementos_lista)
        
        self.lb_seleccion=ttk.Label(self.frame_filtro,text='Elegir opción: ').grid(row=1,column=0,sticky='E',pady=10,padx=(15,0))

        self.lista_filtro=ttk.Combobox(self.frame_filtro,textvariable=self.combo_elementos)
        self.lista_filtro["state"] = "readonly"        
        self.lista_filtro.grid(row=1,column=1,pady=10,padx=(0,15))
        
        self.btn_filtrar=ttk.Button(self.frame_filtro,text='Filtrar',command=self.filtrar).grid(row=2,column=0,columnspan=2,pady=10)

        boton_salir = tk.Button(self, text="Salir", bg="orange", fg="black", width=10, command=self.salir)
        boton_salir.grid(row=10, column=10)

    def crear_tree(self):
        """Crea el treeview widget que contendra las recetas."""

        # Id y nombre de la receta
        columns = ('ID', 'Nombre')
        
        # crea el widget
        tree = ttk.Treeview(self, columns=columns, show='headings')
        
        # definimos el ancho de cada fila
        tree.column('ID', width=80)

        # insertamos en la grilla
        tree.grid(row=2, column=0, sticky=(tk.NSEW), pady=10, padx=5, columnspan=5)
        
        # insertamos el encabezado
        tree.heading('ID', text='ID')
        tree.heading('Nombre', text='Nombre')

        # agregamos scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=5, sticky=tk.NS, pady=10)

        return tree

    def insertar_datos(self):
        """Lee el fichero csv e inserta los datos en el treeview"""
        self.recetas = deserializar()
        for i, values in enumerate(self.recetas):
            data = [i, values["nombre"]]
            self.tree.insert('', tk.END, values=data)

    def crear_botones(self):
        """Crea los botones y los ubica en la grilla"""

        # Boton Ver mas
        tk.Button(self, text="Ver", bg="orange", fg="black", width=10, command=self.ver_mas).grid(row=1, column=1, padx=10, pady=5, sticky=(tk.NSEW))
        
        # Boton Editar
        tk.Button(self, text="Editar", bg="orange", fg="black", width=10, command=self.editar_receta).grid(row=1, column=2, padx=10, pady=5, sticky=(tk.NSEW))

        # Boton Eliminar
        tk.Button(self, text="Eliminar", bg="orange", fg="black", width=10, command=self.eliminar_receta).grid(row=1, column=3, padx=10, pady=5, sticky=(tk.NSEW))
        
    def retornar_id(self):
        """Guarda el ID del item seleccionado al presionar un boton."""
        item_seleccionados = self.tree.focus()
        return self.tree.item(item_seleccionados)['values'][0]

    def ver_mas(self):
        """Método para ver una receta."""
        toplevel = tk.Toplevel(self)
        id = self.retornar_id()
        VerMas(toplevel, self.recetas[id]).grid()

    def editar_receta(self):
        """Método para editar una receta."""
        toplevel = tk.Toplevel(self)
        id = self.retornar_id()
        EditarReceta(toplevel, self.recetas[id], id).grid()

    def eliminar_receta(self):
        """Método para eliminar una receta."""
         # Obtener el índice del elemento seleccionado
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar receta", "Seleccione una receta para eliminar.")
            return

        index = int(self.tree.index(seleccion[0]))

        # Obtener el nombre de la receta seleccionada
        nombre_receta = self.tree.item(seleccion[0])["values"][1]

        # Confirmar la eliminación
        confirmar_eliminar = messagebox.askyesno(title="Eliminar Receta", message=f"Desea eliminar la receta {nombre_receta}?")
        if confirmar_eliminar:
             # Eliminar la receta correspondiente de la lista
            lista_recetas = deserializar()
            receta_eliminar = lista_recetas.pop(index)

            # Escribir la lista actualizada en el archivo
            serializar(lista_recetas)

            # Actualizar la vista de la Treeview para reflejar la eliminación
            self.tree.delete(seleccion)

            messagebox.showinfo("Eliminar receta", f"La receta '{receta_eliminar['nombre']}' ha sido eliminada.")
    
    def elementos_lista(self, evento):
        elemento_a_filtrar=self.combo_lista.get()
        lista_recetas = deserializar()
        lista=[]
        self.combo_elementos.set('')
        if elemento_a_filtrar == 'Nombre':
            for r in lista_recetas:
                lista.append(r['nombre'])
        if elemento_a_filtrar == 'Etiqueta':
            conjunto = set()
            for r in lista_recetas:
                etiquetas = r['etiquetas']
                for eti in etiquetas:
                    conjunto.add(eti)
            lista = list(conjunto)        
        if elemento_a_filtrar == 'Tiempo de Preparación':
            conjunto = set()
            for r in lista_recetas:
                conjunto.add(str(r['tiempo_preparacion']))
            lista = list(conjunto)    
        if elemento_a_filtrar == 'Ingrediente':
            conjunto = set()
            for r in lista_recetas:
                for ing in r['lista_ingredientes']:
                    conjunto.add(ing['nombre'])
            lista=list(conjunto)            
        lista.sort()
        self.lista_filtro["values"] = tuple(lista)    
    
    def filtrar(self):
        elemento_a_filtrar = self.combo_lista.get()
        lista_recetas = deserializar()
        for i in self.tree.get_children():
            self.tree.delete(i)
        if elemento_a_filtrar == 'Nombre':
            for i, values in enumerate(lista_recetas):
                if values['nombre'] == self.combo_elementos.get():
                    data = [i, values["nombre"]]
                    self.tree.insert('', tk.END, values=data)        

        if elemento_a_filtrar == 'Etiqueta':
            for i, values in enumerate(lista_recetas):
                if self.combo_elementos.get() in values['etiquetas']:
                    data = [i, values["nombre"]]
                    self.tree.insert('', tk.END, values=data)       
      
        if elemento_a_filtrar == 'Tiempo de Preparación':
            for i, receta in enumerate(lista_recetas):
                if str(receta['tiempo_preparacion'])==self.combo_elementos.get():
                    data = [i, receta["nombre"]]
                    self.tree.insert('', tk.END, values=data)       
   
        if elemento_a_filtrar == 'Ingrediente':
            for i, receta in enumerate(lista_recetas):
                for ing in receta['lista_ingredientes']:
                    if ing['nombre'] == self.combo_elementos.get():
                        data = [i, receta["nombre"]]
                        self.tree.insert('', tk.END, values=data)    

    def salir(self):
        """Método para salir de la ventana."""
        self.parent.destroy() # Terminamos el programa al destruir la ventana ppal  