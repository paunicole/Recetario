import json
import random
from datetime import datetime

def deserializar():
    """Método para obtener el contenido del archivo JSON."""
    with open('recetas.json', 'r', encoding='UTF-8') as archivo:
        lista_recetas = json.load(archivo)
    return lista_recetas

def serializar(lista_recetas):
    """Método para guardar el contenido en el archivo JSON."""
    with open("recetas.json", 'w', encoding='UTF-8') as archivo:
        json.dump(lista_recetas, archivo, indent=2)

def receta_aleatoria():
    """Método para obtener una receta aleatoria de la lista de recetas."""
    lista_recetas = deserializar()
    posicion_aleatoria = random.randint(0, len(lista_recetas)-1)
    return lista_recetas[posicion_aleatoria]

def fecha_hoy():
    """Devuelve la fecha y hora de hoy con el formato indicado."""
    fecha_hoy = datetime.now()
    fecha_formato = fecha_hoy.strftime('%d/%m/%Y %X')
    return fecha_formato

def devuelve_str_preparacion(preparacion):
    """Método que recibe una lista de pasos y retorna la misma en formato string (para EditarReceta)."""
    str_preparacion = ''
    for i in preparacion:
        str_preparacion += i+'\n'
    return str_preparacion

def devuelve_str_ingredientes_2(lista_ingredientes):
    """Método que recibe una lista de ingredientes y retorna la misma en formato string (para VerReceta)."""
    str_lista_ingredientes = ''
    for dic in lista_ingredientes:
        str_lista_ingredientes += '- ' + dic['nombre'] + ' ' + str(dic['cantidad']) + ' ' + dic['medida'] + '\n\n'
    return str_lista_ingredientes

def devuelve_str_preparacion_2(lista_preparacion):
    """Método que recibe una lista de pasos y retorna la misma en formato string (para VerReceta)."""
    str_preparacion = ''
    for count, paso in enumerate(lista_preparacion):
        str_preparacion += f'{count+1}. '+paso+'\n\n'
    return str_preparacion

def devuelve_str_etiquetas(lista_etiquetas):
    """Método que recibe una lista de etiquetas y retorna la misma en formato string (para VerReceta)."""
    str_etiquetas = ''
    for i in lista_etiquetas:
        str_etiquetas += '#'+i+'  '
    return str_etiquetas

def retornar_posiciones_seleccionadas(opciones_etiquetas, seleccionadas):
    posiciones_seleccionadas = list()
    for pos, values in enumerate(opciones_etiquetas):
        if values in seleccionadas:
            posiciones_seleccionadas.append(pos)
    return posiciones_seleccionadas