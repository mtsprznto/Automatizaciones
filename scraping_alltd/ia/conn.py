import os
from dotenv import load_dotenv
from groq import Groq

# Cargar variables de entorno
load_dotenv()

# Obtener la API key de las variables de entorno
GROQ_API_KEY = os.getenv("api_qroq")

def get_groq_client():
    """
    Crea y retorna un cliente de Groq configurado con la API key.
    
    Returns:
        Groq: Cliente de Groq configurado
    """
    if not GROQ_API_KEY:
        raise ValueError("No se encontró la API key de Groq. Asegúrate de configurar api_qroq en tu archivo .env")
    
    return Groq(api_key=GROQ_API_KEY)

# Ejemplo de uso:
if __name__ == "__main__":
    try:
        client = get_groq_client()
        print("¡Conexión exitosa con Groq!")
    except Exception as e:
        print(f"Error al conectar con Groq: {e}")