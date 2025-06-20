


def guardar_en_txt(texto, nombre_archivo):
    """Guarda el texto en un archivo .txt, agregándolo al final."""
    with open(nombre_archivo, "a", encoding="utf-8") as archivo:
        archivo.write(texto + "\n\n")  # Agrega el texto con un salto de línea