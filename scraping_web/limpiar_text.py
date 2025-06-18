import re

def limpiar_texto_avanzado(texto):
    """Limpia el texto eliminando caracteres desordenados y palabras irrelevantes."""
    texto = texto.strip()
    texto = re.sub(r'\s+', ' ', texto)  # Reduce múltiples espacios
    texto = re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑ]', '', texto)  # Elimina caracteres especiales
    texto = re.sub(r'\b\d+\b', '', texto)  # Borra números aislados
    texto = re.sub(r'\b(?:Me gusta|Comentar|Enviar|Compartir|Ver más|Escribe un comentario público)\b', '', texto, flags=re.IGNORECASE)  # Filtra texto irrelevante de Facebook
    texto = re.sub(r'\b[a-zA-Z]\b', '', texto)  # Borra letras aisladas que no forman palabras
    return texto.strip()


def eliminar_duplicados(lista_textos):
    """Elimina bloques duplicados manteniendo la estructura."""
    textos_unicos = list(set(lista_textos))
    return textos_unicos

def organizar_datos(texto):
    """Divide los anuncios en secciones más claras."""
    bloques = texto.split("\n")
    datos_limpios = [limpiar_texto_avanzado(bloque) for bloque in bloques if bloque.strip()]
    return "\n-------\n".join(datos_limpios)



def eliminar_ruido(texto):
    """Elimina líneas con caracteres aleatorios que no forman palabras útiles."""
    lineas = texto.split("\n")
    resultado = []

    for linea in lineas:
        # Si una línea contiene más de un 70% de caracteres sueltos, se elimina
        caracteres_sueltos = re.findall(r'\b[a-zA-Z0-9]\b', linea)
        porcentaje_ruido = len(caracteres_sueltos) / len(linea) if len(linea) > 0 else 0
        
        if porcentaje_ruido < 0.7:  # Mantiene líneas con información útil
            resultado.append(linea.strip())

    return "\n".join(resultado)