import time
import json
import logging
import shutil
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import pyperclip

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

TEXTO_DESCRIPCION = """ARRIENDO DEPARTAMENTO AMOBLADO VILLA LOS PRESIDENTES, PUERTO VARAS

Acogedor departamento amoblado en segundo piso de una casa, con entrada independiente y mucha privacidad. Ideal para pareja o grupo de hasta 4 personas (mismo precio).

- $550.000 mensuales 
- incluye internet y agua (Luz y gas por cuenta del arrendatario)

Distribución: 🛏️ 2 dormitorios
- 1 con cama matrimonial
- 1 con 2 camas de plaza 🚿 Baño 🛋️ Completamente amoblado, listo para llegar a vivir

Equipamiento:
- Calefacción Toyotomi a parafina y estufa a leña (leña no incluida) — abrigado para el invierno del sur 
Lavadora
- Muebles incluidos
- Estacionamiento en la calle (sector tranquilo, todos los vecinos dejan sus autos afuera)
- Muy buena iluminación natural
- A 5 minutos del centro de Puerto Varas en vehículo

Condiciones:
- Requisitos: 6 últimas cotizaciones de AFP o contrato de trabajo
- 1 mes de garantía
- No se aceptan mascotas

Contacto directo:
Dueña: Margarita — +56 9 9947 9312

Interesados, llamar directamente al número telefónico.
"""


COOKIES_FILE = Path(__file__).resolve().parent / "fb_cookies.json"


def setup_driver():
    chrome_options = Options()

    # Perfil temporal fresco cada run — cero problemas de lock entre runs
    temp_dir = tempfile.mkdtemp(prefix="fb_selenium_")

    chrome_options.add_argument(f"user-data-dir={temp_dir}")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280,800')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-first-run')

    driver = webdriver.Chrome(options=chrome_options)
    driver._temp_dir = temp_dir
    logger.info("✅ Driver iniciado con perfil temporal.")
    return driver


def cargar_cookies(driver) -> bool:
    if not COOKIES_FILE.exists():
        return False
    driver.get("https://www.facebook.com/")
    time.sleep(2)
    cookies = json.loads(COOKIES_FILE.read_text(encoding='utf-8'))
    for c in cookies:
        c.pop('sameSite', None)
        try:
            driver.add_cookie(c)
        except Exception:
            pass
    driver.refresh()
    time.sleep(4)
    logged = 'login' not in driver.current_url and 'facebook.com' in driver.current_url
    if logged:
        logger.info("✅ Sesión restaurada desde fb_cookies.json")
    else:
        logger.warning("⚠️ Cookies expiradas o inválidas.")
    return logged


def guardar_cookies(driver):
    try:
        cookies = driver.get_cookies()
        COOKIES_FILE.write_text(json.dumps(cookies, ensure_ascii=False), encoding='utf-8')
        logger.info(f"💾 Cookies actualizadas ({len(cookies)} cookies).")
    except Exception as e:
        logger.warning(f"No se pudieron guardar cookies: {e}")

def publicar_en_grupos():
    load_dotenv()
    
    # 1. Configuración de Rutas (Mejor práctica que usar strings planos)
    BASE_DIR = Path(__file__).resolve().parent
    
    URL_LIST = [
        BASE_DIR / "image/arriendo_mensual/2.png",
        BASE_DIR / "image/arriendo_mensual/3.png",
        BASE_DIR / "image/arriendo_mensual/4.png"
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
        # Intentar restaurar sesión desde cookies guardadas
        if not cargar_cookies(driver):
            logger.info("Sin cookies válidas — haciendo login completo...")
            iniciar_session(driver)
            guardar_cookies(driver)
            time.sleep(5)
        else:
            guardar_cookies(driver)  # actualizar cookies con los tokens frescos

        logger.info("Esperando 5 segundos para que la sesión se estabilice...")
        time.sleep(5)
        
        for link in LINK_GROUPS:
            try:
                link_clean = link.replace("web.facebook.com", "www.facebook.com")

                logger.info(f"Procesando grupo: {link}")
                driver.get(link_clean)

                if "Contenido no encontrado" in driver.page_source or "Content not found" in driver.page_source:
                    logger.warning(f"❌ Grupo inaccesible o eliminado: {link}. Omitiendo...")
                    continue


                wait_fast = WebDriverWait(driver, 5)
                xpath_escribe = "//div[@role='button']//span[contains(text(), 'Escribe algo') or contains(text(), 'Write something')]"
                
                try:
                    elemento = wait_fast.until(EC.element_to_be_clickable((By.XPATH, xpath_escribe)))
                    driver.execute_script("arguments[0].click();", elemento)
                except Exception:
                    logger.warning(f"⚠️ Formato incompatible (posible grupo de venta) en {link}. Omitiendo...")
                    continue # <--- AQUÍ SALTA AL SIGUIENTE LINK SIN DETENERSE

                time.sleep(5)  # esperar que modal cargue completamente

                # 3. INSERTAR TEXTO
                # Buscar con find_elements directo — WebDriverWait falla con contenteditable=""
                # porque el XPath @contenteditable='true' no matchea el atributo vacío del HTML.
                editor = None
                KEYWORDS_PLACEHOLDER = ['publicaci', 'public post', 'public post', 'crea una']
                for intento in range(3):
                    candidatos = driver.find_elements(By.XPATH, "//div[@role='textbox']")
                    for el in candidatos:
                        ph = (el.get_attribute('aria-placeholder') or '').lower()
                        if any(k in ph for k in KEYWORDS_PLACEHOLDER):
                            editor = el
                            break
                    if editor:
                        break
                    logger.info(f"Textbox no encontrado aún (intento {intento+1}/3), esperando 2s...")
                    time.sleep(2)

                if editor is None:
                    logger.error(f"❌ Imposible encontrar campo de texto en {link}. Saltando grupo...")
                    continue

                try:
                    # Clipboard: preserva emojis (BMP) Y saltos de línea
                    pyperclip.copy(TEXTO_DESCRIPCION)
                    driver.execute_script("arguments[0].click();", editor)
                    time.sleep(1)
                    from selenium.webdriver.common.action_chains import ActionChains
                    from selenium.webdriver.common.keys import Keys
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                    time.sleep(0.5)
                    logger.info("✅ Texto insertado correctamente.")
                except Exception as e:
                    logger.error(f"❌ Error insertando texto: {e}. Saltando grupo...")
                    continue
                #-------------------------------------
                # Paso 3: Subir Imágenes (Directo al input oculto)
                # Facebook suele tener un input tipo file oculto. Es más rápido enviarlo ahí.
                wait_modal = WebDriverWait(driver, 10)
                input_file = wait_modal.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @multiple]")))
                rutas_validas = [str(p) for p in URL_LIST if p.exists()]
                if rutas_validas:
                    # Se pueden enviar todas juntas separadas por un salto de línea en Windows
                    input_file.send_keys("\n".join(rutas_validas))
                    logger.info(f"✅ {len(rutas_validas)} imágenes cargadas.")
                
                time.sleep(5) # Esperar a que carguen las miniaturas

                # Paso 4: Publicar
                btn_publicar = "//div[@role='button' and @aria-label='Publicar']"
                boton = wait_modal.until(EC.element_to_be_clickable((By.XPATH, btn_publicar)))
                driver.execute_script("arguments[0].click();", boton)
                
                logger.info("🚀 Publicación enviada.")
                time.sleep(10) # Cooldown preventivo

            except Exception as e:
                logger.error(f"❌ Error en grupo {link}: {e}")
                continue

    finally:
        try:
            driver.quit()
        except Exception:
            pass
        try:
            shutil.rmtree(driver._temp_dir, ignore_errors=True)
        except Exception:
            pass

if __name__ == "__main__":
    publicar_en_grupos()