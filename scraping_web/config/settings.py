# Configuración global del proyecto
from pathlib import Path

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Tiempos de espera
SCROLL_PAUSE_TIME = 5

# Rutas
DATA_DIR = BASE_DIR / "data_scraping"
IA_RESPONSE_DIR = DATA_DIR / "ia_response"

# Configuración de Facebook
FACEBOOK_URL = "https://web.facebook.com/?locale=es_LA&_rdc=1&_rdr"
FACEBOOK_GROUP_URL = f"https://web.facebook.com/groups/692338427471692"

# Configuración de archivos
ARCHIVO_BLOQUES = DATA_DIR / "bloques_extraidos.txt"
# Configuración de IA
IA_PROMPT_PATH = BASE_DIR / "ia" / "prompts" / "prompt_system.txt"
