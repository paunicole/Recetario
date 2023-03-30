import tkinter as tk
import json
import shutil

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import INSERT
from modulos.global_var import DESTINO
from modulos.logica import deserializar, serializar
from modulos.logica import devuelve_str_preparacion
from modulos.logica import retornar_posiciones_seleccionadas

class EditarReceta(ttk.Frame):

    """Clase que modifica una receta ya creada anteriormente y guarda los cambios en un archivo JSON."""

    def __init__(self, parent, receta, pos):
        super().__init__(parent, padding=(10))
        self.parent = parent
        parent.title("Editar Receta")
        parent.iconbitmap('imagenes/logo.ico')

        self.receta = receta
        self.pos = pos

        # Inicializo Variables
        self.fecha_creacion = self.receta['fecha_creacion'] # No se modifica al editar receta
        self.nombre = tk.StringVar()
        self.nombre_ingrediente = tk.StringVar()
        self.cantidad = tk.IntVar()
        self.medida = tk.StringVar()
        self.tiempo_preparacion = tk.StringVar()
        self.tiempo_coccion = tk.StringVar()
        self.ruta_imagen = self.receta['imagen']
        self.etiquetas = self.receta['etiquetas']
        self.es_favorita = tk.BooleanVar()

        # EDITAR RECETA
        ttk.Label(self, text="Editar receta", font=("HelveticaNeueLT Std Med", 20), padding=30).grid(row=0, column=2)

        # Nombre
        ttk.Label(self, text="Nombre", padding=3).grid(row=1, column=1, sticky='E')
        entry_nombre = ttk.Entry(self, textvariable=self.nombre)
        entry_nombre.grid(row=1, column=2, sticky='EW')
        entry_nombre.insert(0, self.receta['nombre'])

        # Lista de Ingredientes
        #ttk.Label(self, text="Lista de Ingredientes", padding=3).grid(row=2, column=1, sticky='E')
        
        self.frame_ing = ttk.Frame(self)
        self.frame_ing.grid(row=2, column=2, columnspan=3)

        ttk.Label(self.frame_ing, text='Ingrediente', padding=3).grid(row=2, column=2, sticky='W')
        ttk.Label(self.frame_ing, text='Cantidad', padding=3).grid(row=2, column=3, sticky='W')
        ttk.Label(self.frame_ing, text='Medida', padding=3).grid(row=2, column=4, sticky='W')

        ttk.Entry(self.frame_ing, textvariable=self.nombre_ingrediente).grid(row=3, column=2, sticky='EW')
        ttk.Entry(self.frame_ing, textvariable=self.cantidad).grid(row=3, column=3, sticky='EW')
        medidas = ['miligramos', 'gramos', 'kilogramos', 'litros', 'cucharadas', 'cucharaditas', 'unidades', 'tazas']
        ttk.Combobox(self.frame_ing, textvariable=self.medida, values=medidas).grid(row=3, column=4, sticky='EW')
        
        tk.Button(self.frame_ing, text='Agregar', bg="yellow", fg="black", command=lambda:self.agregar_ingrediente()).grid(row=4, column=2, sticky='EW')
        tk.Button(self.frame_ing, text='Eliminar', bg="yellow", fg="black", command=lambda:self.eliminar_ingrediente()).grid(row=4, column=3, sticky='EW')

        columnas = ('Nombre', 'Cantidad', 'Medida')     
        tree_scroll_ing = ttk.Scrollbar(self.frame_ing, orient='vertical')
        tree_scroll_ing.grid(row=6, column=5, sticky='NS')
        self.tree_ing = ttk.Treeview(self.frame_ing, columns=tuple(columnas), style=None, yscrollcommand=tree_scroll_ing.set, selectmode='browse', show='headings', height=4)
        self.tree_ing.grid(row=6, column=2, columnspan=3, sticky='EW')
        tree_scroll_ing.config(command=self.tree_ing.yview)
        
        self.tree_ing.column('Nombre', width=70, anchor='center')
        self.tree_ing.column('Cantidad', width=70, anchor='center')
        self.tree_ing.column('Medida', width=70, anchor='center')
        
        self.tree_ing.heading('Nombre', text='Nombre')
        self.tree_ing.heading('Cantidad', text='Cantidad')
        self.tree_ing.heading('Medida', text='Medida')
        
        self.insertar_datos()

        # Preparación
        ttk.Label(self, text="Preparación", padding=3).grid(row=7, column=1, sticky='NE')
        
        scroll_prep = ttk.Scrollbar(self, orient='vertical')
        scroll_prep.grid(row=7, column=5, sticky='NS')
        
        self.preparacion = tk.Text(self, height=8, width=50, yscrollcommand=scroll_prep.set)
        self.preparacion.grid(row=7, column=2, sticky='EW')
        str_preparacion = devuelve_str_preparacion(self.receta['preparacion'])
        self.preparacion.insert(INSERT, str_preparacion)
        self.preparacion.bind("<Return>", lambda event: self.preparacion.insert(tk.END, ''))

        # Imagen
        ttk.Label(self, text="Imagen", padding=3).grid(row=8, column=1, sticky='E')
        tk.Button(self, text="Seleccionar", bg="yellow", fg="black", command=self.seleccionar_imagen).grid(row=8, column=2, sticky='W')
        ttk.Label(self, text=self.ruta_imagen, padding=3, wraplength=400).grid(row=9, column=2, sticky='W')

        # Tiempo de preparación
        ttk.Label(self, text="Tiempo de Preparación (min)", padding=3).grid(row=10, column=1, sticky='E')
        entry_tiempo_preparacion = ttk.Entry(self, textvariable=self.tiempo_preparacion)
        entry_tiempo_preparacion.grid(row=10, column=2, sticky='EW')
        entry_tiempo_preparacion.insert(0, self.receta['tiempo_preparacion'])

        # Tiempo de Coción
        ttk.Label(self, text="Tiempo de Cocción (min)", padding=3).grid(row=11, column=1, sticky='E')
        entry_tiempo_cocion = ttk.Entry(self, textvariable=self.tiempo_coccion)
        entry_tiempo_cocion.grid(row=11, column=2, sticky='EW')
        entry_tiempo_cocion.insert(0, self.receta['tiempo_coccion'])

        # Etiquetas
        ttk.Label(self, text="Etiquetas", padding=3).grid(row=12, column=1, sticky='NE')
        opciones_etiquetas = ('PlatoSalado', 'PlatoAgridulce', 'Tortas', 'Postre', 'Light', 'Vegano', 'Horno', 'Frito')
        var = tk.Variable(value=opciones_etiquetas)
        self.listbox = tk.Listbox(self, listvariable=var, height=4, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=12, column=2, sticky='EW')
       
        scroll_etiq = ttk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        scroll_etiq.grid(row=12, column=5, sticky='NS')
        self.listbox.config(yscrollcommand=scroll_etiq.set)

        seleccionadas = self.receta['etiquetas']
        posiciones_seleccionadas = retornar_posiciones_seleccionadas(list(opciones_etiquetas), seleccionadas)
        for p in posiciones_seleccionadas:
            self.listbox.select_set(p)
        self.listbox.bind('<<ListboxSelect>>', self.items_seleccionados)
        
        # Favorita
        ttk.Label(self, text="Favorita", padding=3).grid(row=13, column=1, sticky='E')
        check_favorita = tk.Checkbutton(self, variable=self.es_favorita, onvalue=1, offvalue=0)
        check_favorita.grid(row=13, column=2, sticky='W')
        if self.receta['es_favorita']:  # Si es True entonces el check aparece seleccionado por defecto 
            check_favorita.select()

        # Boton Guardar
        btn_guardar = tk.Button(self, text="Guardar", bg="orange", fg="black", command=self.guardar_receta)
        btn_guardar.grid(row=20, column=6, sticky='EW')

        # Boton Salir
        btn_salir = tk.Button(self, text="Salir", bg="orange", fg="black", width=12, command=parent.destroy)
        btn_salir.grid(row=21, column=6, sticky='EW')


    def seleccionar_imagen(self):
        """Guarda en la variable 'ruta_imagen' la ruta de la imagen seleccionada."""
        self.ruta_imagen = filedialog.askopenfilename(filetypes=(('imagenes jpg', '*.jpg'), ('Todos los archivos', '*.*')))
        if self.ruta_imagen != None:
            messagebox.showinfo(message='Imagen cargada!')
            ttk.Label(self, text=self.ruta_imagen, padding=3, wraplength=400).grid(row=9, column=2, sticky='W')


    def obtener_ruta(self):
        """Copia la imagen seleccionada a la carpeta de imagenes y devuelve la ruta donde se copió. Si imagen no contiene nada, devuelve la imagen especificada por defecto."""
        if self.ruta_imagen != None:
            try:
                #copia el archivo de origen a la ruta de destino
                shutil.copy(self.ruta_imagen, DESTINO)           # el archivo de la ruta se copiará en el directorio especificado por DESTINO. Si el archivo de destino ya existe, se sobrescribirá con el archivo de origen. Si el directorio de destino no existe, se creará automáticamente.
            except shutil.SameFileError:
                #El archivo de origen y de destino son iguales, muestra una ventana de confirmacion donde el usuario decide si sobreescribirlo
                ventana_confirmacion= VentanaConfirmacion(self.master,self.ruta_imagen)
                ventana_confirmacion.mostrar()
   
            nombre_imagen = self.ruta_imagen.split('/')[-1]  # ruta_imagen contiene una cadena con la ruta "carpeta/carpeta/imagen.png". Con split dividimos la cadena por el delimitador '/', es decir ['carpeta', 'carpeta', 'imagen.png']. Con el slicing [-1] accedemos al último elemento de la lista resultante, que es el nombre del archivo.
            return 'imagenes/' + nombre_imagen               # devolvemos la ruta 'imagenes/imagen.png' que es donde se encuentra ahora mismo nuestra imagen.
        
        else:
            return 'imagenes/por_defecto.png' # si ruta_imagen es igual a None quiere decir que no seleccionamos ninguna imagen asi que retornamos la ruta de la imagen por defecto que se debera mostrar siempre que mostremos la receta.
    
    def items_seleccionados(self, event):
        """"Metodo que guarda en una lista las etiqueta seleccionadas."""
        indices_seleccionados = self.listbox.curselection()
        self.etiquetas = [self.listbox.get(i) for i in indices_seleccionados]

    def insertar_datos(self):
        """Inserta los datos en el treeview."""
        list_ingredientes = self.receta['lista_ingredientes']
        for dict in list_ingredientes:
            data = [dict["nombre"], dict["cantidad"], dict["medida"]]
            self.tree_ing.insert('', tk.END, values=data)

    def agregar_ingrediente(self):
        try:
            if self.nombre_ingrediente.get()!='' and self.cantidad.get()!=0 and self.medida.get()!='':
                nombre = self.nombre_ingrediente.get()
                cantidad = self.cantidad.get()
                medida = self.medida.get()
                self.tree_ing.insert("","end", values=(nombre, cantidad, medida))
                self.nombre_ingrediente.set('')
                self.cantidad.set(0)
                self.medida.set('')
            else:
                messagebox.showinfo(message="Los campos deben de tener algun valor") 
        except:    
            messagebox.showinfo(message="Ingrese valores correctos a los campos") 

    def eliminar_ingrediente(self):
        seleccion = self.tree_ing.selection()
        if seleccion:
            item = self.tree_ing.item(seleccion) 
            for item in seleccion:
                self.tree_ing.delete(item)
        else:
            messagebox.showinfo(message="Debe elegir un elemento primero...")    

    def get_ingredientes(self):
        items = self.tree_ing.get_children()
        lista_ing = []
        for item in items:
            uno = self.tree_ing.item(item)
            ing, cant, med = uno['values']
            lista_ing.append({"nombre" : ing, "cantidad" : cant, "medida" : med})
        return lista_ing 

    def guardar_receta(self):
        """Metodo para guardar los datos introducidos en el formulario en un archivo JSON."""

        # Obtenemos los datos de la receta que se ingresó en el formulario
        receta_actualizada = {
            "fecha_creacion" : self.fecha_creacion,
            "nombre" : self.nombre.get(),
            "lista_ingredientes" : self.get_ingredientes(),
            "preparacion" : self.preparacion.get('1.0','end').split('\n')[:-2],
            "imagen" : self.obtener_ruta(),
            "tiempo_preparacion" : self.tiempo_preparacion.get(),
            "tiempo_coccion" : self.tiempo_coccion.get(),
            "etiquetas" : self.etiquetas,
            "es_favorita" : self.es_favorita.get()
            }
        
        # Obtengo la lista de recetas del archivo JSON
        lista_recetas = deserializar()
        
        # Guarda la receta actualizada en la posicion i
        lista_recetas[self.pos] = receta_actualizada

        # Guardo la lista de recetas actualizada en el archivo JSON
        serializar(lista_recetas)

        # Informamos que la receta ha sido guardada
        messagebox.showinfo(title='Información', message='Receta actualizada') 

        # Terminamos el programa al destruir la ventana ppal
        self.parent.destroy()              

import shutil
import tkinter as tk

class VentanaConfirmacion(tk.Toplevel):
    def __init__(self, master, archivo):
        super().__init__(master)
        self.archivo = archivo

        mensaje = tk.Label(self, text="El archivo ya existe en la ruta de destino. ¿Desea sobrescribirlo?")
        mensaje.pack()
        
        boton_sobrescribir = tk.Button(self, text="Sobrescribir", command=self.sobrescribir)
        boton_sobrescribir.pack(side=tk.LEFT)
        
        boton_no_sobrescribir = tk.Button(self, text="No sobrescribir", command=self.no_sobrescribir)
        boton_no_sobrescribir.pack(side=tk.RIGHT)
        
    def sobrescribir(self):
        # Cierra la ventana y copia el archivo de origen a la ruta de destino sobreescribiendo el archivo existente
        self.destroy()
        shutil.copy(self.archivo, DESTINO)
        
    def no_sobrescribir(self):
        # Cierra la ventana sin copiar el archivo de origen
        self.destroy()
    
    def mostrar(self):
        # Muestra la ventana de confirmación
        self.grab_set()
        self.wait_window()
    
    def cerrar(self):
        # Cierra la ventana
        self.destroy()                                 
        

