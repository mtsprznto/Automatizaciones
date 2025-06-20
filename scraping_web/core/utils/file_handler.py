import os
from datetime import datetime
import re

def guardar_en_txt(texto, nombre_archivo):
    """Guarda el texto en un archivo .txt, agregándolo al final."""
    with open(nombre_archivo, "a", encoding="utf-8") as archivo:
        archivo.write(texto + "\n\n")




def obtener_slug(url):
    try:
        match = re.search(r'/groups/(\d+)', url)
        if match:
            grupo_id = match.group(1)
            print(grupo_id)  # Output: 692338427471692
    
        return grupo_id
    except Exception as e:
        print(f"Error al obtener el slug: {e}")
        return None

def crear_ruta_salida():
    """Crea la ruta de salida para los archivos de IA"""
    fecha_formato = datetime.now().strftime("%d%m%y")
    return fecha_formato
