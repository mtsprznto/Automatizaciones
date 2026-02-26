import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService 
# WebDriver Manager
from webdriver_manager.chrome import ChromeDriverManager

# Tu módulo personalizado
from utils.iniciar_session import iniciar_session

# Configuración de Logging para Debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TEXTO_DESCRIPCION = """Arriendo acogedor departamento interior tipo departamento en Puerto Varas
Ubicado en el segundo nivel, con entrada independiente, en un barrio tranquilo (Villa Los Presidentes), muy cerca del centro, clínica y Tur Bus. Ideal para quienes buscan comodidad y privacidad.
Características:
Máximo 4 pasajeros
A 5 min del centro en auto, con locomoción a la puerta
Entrada desde 14:00 hrs / Salida hasta 12:00 hrs
Equipamiento:
Calefacción eficiente: cuenta con Toyotomi y sistema de combustión lenta, incluye leña
Lavadora disponible en el departamento
Living-comedor acogedor con sofá cama y TV cable
Cocina equipada (microondas, loza y utensilios)

Dos dormitorios:
- 1 dormitorio con cama matrimonial
1 dormitorio con dos camas de plaza


Wifi disponible
Reja de protección en la entrada para niños pequeños

No se arrienda por año corrido

Tarifa: $50.000 por noche
Dueña: Margarita
Contacto: +56 9 99479312
Interesados, llamar directamente al número telefónico

Más información: https://dept.mtsprz.org
"""


def setup_driver():
    chrome_options = Options()
    
    # --- CAMBIO PARA ESCALABILIDAD Y PERSISTENCIA ---
    # Esto crea una carpeta 'perfil_fb' donde se guardará tu sesión
    # Así no te pedirá login cada vez que reinicies el script
    script_dir = Path(__file__).resolve().parent
    user_data_dir = script_dir / "perfil_fb"
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # IMPORTANTE: Para Docker/Binance necesitarás estos:
    chrome_options.add_argument('--headless') # Descomenta para Docker
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        logger.info("✅ Driver iniciado con perfil persistente.")
        return driver
    except Exception as e:
        logger.warning(f"Fallo auto-discovery, intentando Service: {e}")
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

def publicar_en_grupos():
    load_dotenv()
    
    # 1. Configuración de Rutas (Mejor práctica que usar strings planos)
    BASE_DIR = Path(__file__).resolve().parent
    
    URL_LIST = [
        BASE_DIR / "image/1.png",
        BASE_DIR / "image/2.png",
        BASE_DIR / "image/3.png",
        BASE_DIR / "image/4.png"
    ]

    LINK_GROUPS = [
        "https://www.facebook.com/groups/782773525842194/",
        "https://www.facebook.com/groups/avisopuertovaras/",
        "https://www.facebook.com/groups/524559424328298/",
        "https://www.facebook.com/groups/237181410725224/",
        "https://www.facebook.com/groups/906901732740560/",
        "https://www.facebook.com/groups/1049457588420905/",
        "https://www.facebook.com/groups/150106962013519/",
        "https://www.facebook.com/groups/150106962013519/",
        "https://www.facebook.com/groups/4162085083869640/",
        "https://www.facebook.com/groups/1547122495537305/",
        "https://www.facebook.com/groups/713786551040818/",
        "https://www.facebook.com/groups/252294063366985/",
        "https://www.facebook.com/groups/2370631826381694/",
        "https://www.facebook.com/groups/2436707279984605/",
        "https://www.facebook.com/groups/1103879840113888/",
        "https://www.facebook.com/groups/381256015925560/",
        "https://www.facebook.com/groups/vecinosdepuertovaras/",
        "https://www.facebook.com/groups/183900808755578/",
        "https://www.facebook.com/groups/1419693948298699/",
        "https://www.facebook.com/groups/696244649751164/",
        "https://www.facebook.com/groups/324525800948349/",
        "https://www.facebook.com/groups/894578011021666/",
        "https://www.facebook.com/groups/578352859763309/",
        "https://www.facebook.com/groups/246215055878294/",
        "https://www.facebook.com/groups/148151746044237/",
        "https://www.facebook.com/groups/283015253404012/",
        "https://www.facebook.com/groups/1050649785505128/",
        "https://www.facebook.com/groups/807265633391770/",
        "https://www.facebook.com/groups/1718059098671369/",
        "https://www.facebook.com/groups/1699865733653222/",
    ]


    #TEXTO_DESCRIPCION = os.getenv("TEXTO_PUBLICACION", "Foco Solar LED 1200W...") # Opcional usar .env para el texto

    driver = setup_driver()

    try:
        # Iniciar sesión (usa tu lógica de utils)
        iniciar_session(driver)
        logger.info("Esperando 10 segundos para que las cookies se estabilicen...")
        time.sleep(10)
        
        for link in LINK_GROUPS:
            try:
                link_clean = link.replace("web.facebook.com", "www.facebook.com")

                logger.info(f"Procesando grupo: {link}")
                driver.get(link_clean)

                if "Contenido no encontrado" in driver.page_source or "Content not found" in driver.page_source:
                    logger.warning(f"❌ Grupo inaccesible o eliminado: {link}. Omitiendo...")
                    continue

                if len(driver.find_elements(By.NAME, "email")) > 0:
                    logger.warning("⚠️ Sesión perdida al entrar al grupo. Reintentando login...")
                    iniciar_session(driver)
                    driver.get(link_clean)

                wait = WebDriverWait(driver, 20)

                # Paso 1: Click en "¿Qué estás pensando?"
                xpath_escribe = "//div[@role='button']//span[contains(text(), 'Escribe algo') or contains(text(), 'Write something')]"
                elemento = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_escribe)))
                driver.execute_script("arguments[0].click();", elemento)

                #_----------------------------------
                # Paso 2: Insertar Texto (Ajustado para evitar comentarios ajenos)
                # Buscamos el textbox que tenga el aria-placeholder correcto
                xpath_editor = "//div[@role='textbox' and (contains(@aria-placeholder, 'Crea una publicación') or contains(@aria-placeholder, 'Create a public post'))]"

                try:
                    # Aseguramos que el editor esté visible y sea el del modal
                    editor = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_editor)))
                    
                    # Hacemos click previo para ganar el foco
                    driver.execute_script("arguments[0].click();", editor)
                    time.sleep(1)
                    
                    # Insertar el texto
                    editor.send_keys(TEXTO_DESCRIPCION)
                    logger.info("✅ Texto insertado correctamente en el modal de publicación.")
                    
                except Exception as e:
                    logger.warning("No se encontró el textbox con aria-placeholder, intentando respaldo...")
                    # Respaldo: Buscar el textbox que NO esté dentro de un comentario (basado en clases de contenedor de post)
                    xpath_respaldo = "//div[@role='dialog']//div[@contenteditable='true' and @role='textbox']"
                    editor = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_respaldo)))
                    editor.send_keys(TEXTO_DESCRIPCION)
                #-------------------------------------
                # Paso 3: Subir Imágenes (Directo al input oculto)
                # Facebook suele tener un input tipo file oculto. Es más rápido enviarlo ahí.
                input_file = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @multiple]")))
                
                rutas_validas = [str(p) for p in URL_LIST if p.exists()]
                if rutas_validas:
                    # Se pueden enviar todas juntas separadas por un salto de línea en Windows
                    input_file.send_keys("\n".join(rutas_validas))
                    logger.info(f"✅ {len(rutas_validas)} imágenes cargadas.")
                
                time.sleep(5) # Esperar a que carguen las miniaturas

                # Paso 4: Publicar
                btn_publicar = "//div[@role='button' and @aria-label='Publicar']"
                boton = wait.until(EC.element_to_be_clickable((By.XPATH, btn_publicar)))
                driver.execute_script("arguments[0].click();", boton)
                
                logger.info("🚀 Publicación enviada.")
                time.sleep(10) # Cooldown preventivo

            except Exception as e:
                logger.error(f"❌ Error en grupo {link}: {e}")
                # DEBUGGER: Aquí entra en juego tu instrucción de añadir debugger
                import pdb; pdb.set_trace() 
                continue

    finally:
        driver.quit()

if __name__ == "__main__":
    publicar_en_grupos()