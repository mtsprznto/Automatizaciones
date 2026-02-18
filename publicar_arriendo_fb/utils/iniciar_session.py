import time
import os
import logging
from dotenv import load_dotenv

# IMPORTS FALTANTES CLAVE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# Configuración de logger para que funcione el logger.info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def esta_logueado(driver):
    """Verifica si hay una sesión activa en el navegador."""
    # Buscamos elementos que solo aparecen con sesión iniciada
    # 1. El aria-label 'Tu perfil' o la barra de búsqueda
    indicadores_login = [
        "//div[@aria-label='Tu perfil']", 
        "//div[@role='navigation']",
        "//div[@aria-label='Facebook']" # El logo que lleva al inicio
    ]
    
    for xpath in indicadores_login:
        if len(driver.find_elements(By.XPATH, xpath)) > 0:
            return True
    return False

def iniciar_session(driver):
    wait = WebDriverWait(driver, 15)
    try:
        logger.info("Verificando estado de la sesión...")
        driver.get('https://www.facebook.com/')
        time.sleep(4) 

        if esta_logueado(driver):
            logger.info("✅ Usuario ya está logueado.")
            return 1

        logger.info("No hay sesión activa. Yendo a login directo...")
        # CAMBIO ESTRATÉGICO: En lugar de forzar modal en grupo, 
        # vamos a la página de login que es 100% estable para el bot.
        driver.get('https://www.facebook.com/login')

        # 2. Localizar Email
        # Usamos un selector más flexible por si cambian los IDs
        email_xpath = "//input[@name='email'] | //input[@id='email']"
        email_input = wait.until(EC.visibility_of_element_located((By.XPATH, email_xpath)))
        
        email_input.clear()
        email_input.send_keys(os.getenv('NUM_FB'))
        logger.info("Correo/Número ingresado.")

        # 3. Localizar Password
        pass_xpath = "//input[@name='pass'] | //input[@id='pass']"
        pass_input = wait.until(EC.visibility_of_element_located((By.XPATH, pass_xpath)))
        pass_input.clear()
        pass_input.send_keys(os.getenv('PASS_FB'))

        # 4. Botón Login
        # El botón en la página /login suele ser 'loginbutton' o name='login'
        btn_xpath = "//button[@name='login'] | //button[@id='loginbutton']"
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
        
        driver.execute_script("arguments[0].click();", login_button)
        
        # 5. Verificación de Seguridad (Checkpoint)
        logger.info("Esperando procesamiento de login...")
        time.sleep(10) 
        
        if "checkpoint" in driver.current_url:
            logger.warning("⚠️ Facebook detectó un inicio de sesión nuevo. Acepta en tu celular.")
            import pdb; pdb.set_trace() # Pausa para que autorices manualmente

        if esta_logueado(driver):
            logger.info("✅ SESIÓN INICIADA.")
            return 1
        else:
            logger.error("❌ No se pudo confirmar el inicio de sesión.")
            import pdb; pdb.set_trace()
            return 0

    except Exception as e:
        logger.error(f"❌ Error crítico en login: {e}")
        import pdb; pdb.set_trace() 
        return 0