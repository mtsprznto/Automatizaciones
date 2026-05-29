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

TEXTO_DESCRIPCION = """FOCO SOLAR LED 1200W PROFESIONAL - SERIE ZHU - PROTECCIÓN CLIMÁTICA IP67

Asegure la visibilidad y seguridad de su parcela con tecnología de iluminación autónoma diseñada específicamente para resistir las condiciones extremas del sur de Chile. Este equipo industrial ofrece una solución definitiva contra la oscuridad, con costo operativo cero.

CERTIFICACIÓN Y GARANTÍA TÉCNICA
- Resistencia Sellada IP67: Blindaje total contra lluvia intensa, ráfagas de viento y humedad persistente.
Garantía de Fábrica: Respaldo de 2 años detallado en empaque oficial.
Stock Local: Entrega inmediata en Puerto Varas (Sin esperas de envío desde Santiago).

ESPECIFICACIONES DE ALTO RENDIMIENTO
- Potencia Lumínica: 1200W con tecnología LED de alta eficiencia.
Gestión Energética: Carga fotovoltaica automática durante el día y activación inteligente por sensor al anochecer.
Autonomía Reforzada: Batería interna de larga duración para funcionamiento ininterrumpido.
Instalación Simplificada: Sistema inalámbrico que no requiere cableados subterráneos ni técnicos eléctricos.

KIT DE INSTALACIÓN COMPLETO (LO QUE RECIBE)
1. Foco LED ZHU 1200W con panel solar integrado de alto impacto.
Brazo de soporte metálico estructural para poste o pared.
Control remoto de largo alcance para configuración de modos y potencia.
Kit de pernos de anclaje de alta resistencia.
Pilas incluidas para el mando a distancia.

PRECIOS COMPETITIVOS (INVERSIÓN ÚNICA)
- Valor Individual: $29.990 (Mejor precio garantizado en la zona).
Pack Seguridad (2 Unidades): $56.990.
Pack Perímetro Total (4 Unidades): $109.990.

GESTIÓN DE ENTREGA Y CONTACTO
- Retiro Presencial: Punto de entrega céntrico en Puerto Varas para su comodidad.
Despachos Locales: Consultar tarifa para entrega a domicilio en radio urbano y alrededores.
Envíos a Regiones: Despacho diario vía Starken o Blue Express (por pagar).

SOLICITE SU PEDIDO POR WHATSAPP:
Contacto: +56975475781
Enlace directo: https://wa.me/56975475781

Equipos probados y garantizados para el clima de la Región de Los Lagos. Stock limitado para entrega esta semana.
"""


def setup_driver():
    chrome_options = Options()

    # --- CAMBIO PARA ESCALABILIDAD Y PERSISTENCIA ---
    # Esto crea una carpeta 'perfil_fb' donde se guardará tu sesión
    # Así no te pedirá login cada vez que reinicies el script
    script_dir = Path(__file__).resolve().parent
    user_data_dir = script_dir / "perfil_fb"

    # Limpiar lock files residuales que crashean Chrome al reiniciar
    for lock in ["SingletonLock", "SingletonCookie", "SingletonSocket"]:
        lock_path = user_data_dir / lock
        if lock_path.exists():
            try:
                lock_path.unlink()
                logger.info(f"🔓 {lock} eliminado del perfil.")
            except Exception as ex:
                logger.warning(f"No se pudo eliminar {lock}: {ex}")

    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Headless: funciona correctamente ahora que el login maneja "Continuar" + password
    # Usar --headless=new (Chrome 112+). NO usar --headless a secas en versiones recientes.
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280,800')
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
        BASE_DIR / "image/foco/foco.jpeg",
        BASE_DIR / "image/foco/foco_.jpeg",
        BASE_DIR / "image/foco/foco_posicion.jpeg",
        BASE_DIR / "image/foco/referencia_ia.jpeg",
        BASE_DIR / "image/foco/img_ia.jpeg",
    ]

    LINK_GROUPS = [
        "https://www.facebook.com/groups/782773525842194/",
        "https://www.facebook.com/groups/906901732740560/",
        "https://www.facebook.com/groups/2370631826381694/",
        "https://www.facebook.com/groups/avisopuertovaras/",
        "https://www.facebook.com/groups/158758577866060/",
        "https://www.facebook.com/groups/1730316040537560/",
        "https://www.facebook.com/groups/4162085083869640/",
        "https://www.facebook.com/groups/150106962013519/",
        "https://www.facebook.com/groups/696244649751164/",
        "https://www.facebook.com/groups/1908909182683277/",
        "https://www.facebook.com/groups/237181410725224/",
        "https://www.facebook.com/groups/2436707279984605/",
        "https://www.facebook.com/groups/1264891191737598/",
        "https://www.facebook.com/groups/1443748286763818/",
        "https://www.facebook.com/groups/vecinosdepuertovaras/",
        "https://www.facebook.com/groups/252294063366985/",
        "https://www.facebook.com/groups/1586572161826458/",
        "https://www.facebook.com/groups/arriendosenpuertomontt/",
        "https://www.facebook.com/groups/409895557711702/",
        "https://www.facebook.com/groups/148151746044237/",
        "https://www.facebook.com/groups/1419693948298699/",
        "https://www.facebook.com/groups/578352859763309/",
        "https://www.facebook.com/groups/183900808755578/",
        "https://www.facebook.com/groups/470863470443485/",
        "https://www.facebook.com/groups/250188448518030/",
        "https://www.facebook.com/groups/381256015925560/",
        "https://www.facebook.com/groups/381256015925560/",
        "https://www.facebook.com/groups/483385337526073/",
        "https://www.facebook.com/groups/278126866643049/",
        "https://www.facebook.com/groups/2873980156107548/",
    ]



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

                wait = WebDriverWait(driver, 10)
                # Paso 1: Click en "¿Qué estás pensando?"
                xpath_escribe = "//div[@role='button']//span[contains(text(), 'Escribe algo') or contains(text(), 'Write something')]"
                
                try:
                    elemento = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_escribe)))
                    driver.execute_script("arguments[0].click();", elemento)
                except Exception:
                    logger.warning(f"⚠️ Formato incompatible u omitido en {link}")
                    continue
                

                wait_modal = WebDriverWait(driver, 10)
                xpath_editor = "//div[@role='textbox' and (contains(@aria-placeholder, 'Crea una publicación') or contains(@aria-placeholder, 'Create a public post'))]"
                
                try:
                    try:
                        # Plan A
                        editor = wait_modal.until(EC.element_to_be_clickable((By.XPATH, xpath_editor)))
                        driver.execute_script("arguments[0].click();", editor)
                        time.sleep(1)
                        editor.send_keys(TEXTO_DESCRIPCION)
                    except Exception:
                        # Plan B: Respaldo
                        logger.warning("Buscando textbox de respaldo...")
                        xpath_respaldo = "//div[@role='dialog']//div[@contenteditable='true' and @role='textbox']"
                        editor = wait_modal.until(EC.element_to_be_clickable((By.XPATH, xpath_respaldo)))
                        editor.send_keys(TEXTO_DESCRIPCION)
                except Exception:
                    logger.error(f"❌ No se pudo escribir en el modal de {link}. Saltando...")
                    continue

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
                continue

    finally:
        driver.quit()

if __name__ == "__main__":
    publicar_en_grupos()