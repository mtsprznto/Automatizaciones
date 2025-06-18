import os
from limpiar_text import limpiar_texto_avanzado, eliminar_duplicados, organizar_datos

# Ruta del archivo
archivo_txt = "./data_scraping/bloques_extraidos.txt"

# Leer el contenido del archivo
if os.path.exists(archivo_txt):
    with open(archivo_txt, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
else:
    print(f"❌ Error: El archivo {archivo_txt} no existe.")
    contenido = ""

# Aplicar las funciones de limpieza y organización
datos_limpios = organizar_datos(contenido)
datos_sin_duplicados = eliminar_duplicados(datos_limpios.split("\n"))

# Guardar el resultado en un nuevo archivo
archivo_limpio = "./data_scraping/bloques_limpios.txt"
with open(archivo_limpio, "w", encoding="utf-8") as archivo:
    archivo.write("\n".join(datos_sin_duplicados))

print(f"✅ Datos limpios guardados en {archivo_limpio}")