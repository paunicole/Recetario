import os

def obtener_destino():
    """Metodo que obtiene la ruta del directorio actual del archivo.
    
    Explicación:
    __file__ es una variable especial que almacena la ruta del archivo
    en el que se está ejecutando el código actual.
    La función os.path.dirname() toma esta ruta de archivo como argumento y
    devuelve la ruta del directorio que lo contiene."""

    return os.path.dirname(__file__)