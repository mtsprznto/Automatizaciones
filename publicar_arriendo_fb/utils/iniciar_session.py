import time
import os
import logging
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    StaleElementReferenceException,
    NoSuchElementException,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# XPaths centralizados para fácil mantenimiento
_XPATH_EMAIL = (
    "//input[@name='email']"
    " | //input[@id='email']"
    " | //input[@autocomplete='username']"
    " | //input[@type='email']"
    " | //input[contains(@placeholder,'correo') or contains(@placeholder,'Correo')"
    "           or contains(@placeholder,'email') or contains(@placeholder,'Email')"
    "           or contains(@placeholder,'teléfono') or contains(@placeholder,'Teléfono')"
    "           or contains(@placeholder,'phone') or contains(@placeholder,'Phone')]"
)
_XPATH_PASS  = (
    "//input[@name='pass']"
    " | //input[@id='pass']"
    " | //input[@autocomplete='current-password']"
    " | //input[@type='password']"
)
_XPATH_BTN   = (
    "//button[@name='login']"
    " | //button[@id='loginbutton']"
    " | //button[@type='submit']"
    " | //button[contains(@data-testid,'login')]"
    " | //*[@data-testid='royal_login_button']"
    " | //div[@role='button' and (contains(@aria-label,'Iniciar') or contains(@aria-label,'Log in') or contains(@aria-label,'Log In'))]"
    " | //span[contains(text(),'Iniciar sesión') or contains(text(),'Log in') or contains(text(),'Log In')]/ancestor::*[@role='button'][1]"
    " | //input[@type='submit']"
    " | //div[@role='button'][.//span[contains(text(),'Iniciar') or contains(text(),'Log')]]"
)
# XPaths del dialog de cookies que FB muestra ANTES del login form
_XPATHS_COOKIE_CONSENT = [
    "//button[@data-cookiebanner='accept_button']",
    "//*[@data-testid='cookie-policy-manage-dialog-accept-button']",
    "//button[contains(text(),'Aceptar todo')]",
    "//button[contains(text(),'Accept All')]",
    "//button[contains(text(),'Allow all cookies')]",
    "//button[contains(text(),'Aceptar') and contains(text(),'cookie')]",
    "//button[contains(@title,'Accept')]",
    "//button[normalize-space()='OK']",
]
_LOGIN_URLS = [
    "https://www.facebook.com/login",
    "https://www.facebook.com/login/?next=%2F",
]


def _dismiss_cookie_consent(driver) -> bool:
    """
    Cierra el dialog de cookies de FB si aparece antes del login form.
    Devuelve True si encontró y cerró algún botón.
    """
    for xpath in _XPATHS_COOKIE_CONSENT:
        try:
            btns = driver.find_elements(By.XPATH, xpath)
            if btns:
                driver.execute_script("arguments[0].click();", btns[0])
                logger.info("✅ Cookie consent cerrado con: %s", xpath)
                time.sleep(1.5)
                return True
        except WebDriverException:
            pass
    logger.info("No se detectó dialog de cookies (o ya fue aceptado).")
    return False


def _is_redirect_exception(exc: Exception) -> bool:
    """
    Devuelve True cuando la excepción es la conocida WebDriverException con
    Message vacío provocada por un redirect mid-poll (GetHandleVerifier).
    """
    msg = str(exc)
    return isinstance(exc, WebDriverException) and (
        "Message:" not in msg or msg.strip().startswith("Message:\n")
    )


def esta_logueado(driver) -> bool:
    """Verifica si hay sesión activa comprobando elementos del feed autenticado."""
    indicadores = [
        "//div[@aria-label='Tu perfil']",
        "//div[@role='navigation']",
        "//div[@aria-label='Facebook']",
    ]
    for xpath in indicadores:
        try:
            if len(driver.find_elements(By.XPATH, xpath)) > 0:
                logger.debug("Indicador de sesión encontrado: %s", xpath)
                return True
        except WebDriverException as exc:
            # Si el DOM está en transición no levantamos la excepción,
            # simplemente ignoramos este indicador.
            logger.debug("WebDriverException en esta_logueado (xpath=%s): %s", xpath, exc)
    return False


def _wait_for_element(wait, condition, descripcion: str, driver=None, reintentos: int = 2):
    """
    Wrapper alrededor de wait.until() que:
    - Captura WebDriverException con Message vacío (redirect mid-poll).
    - Hace driver.refresh() + retry cuando corresponde.
    - Lanza TimeoutException si se agotan los reintentos.
    """
    for intento in range(1, reintentos + 1):
        try:
            logger.info("Esperando elemento: %s (intento %d/%d)", descripcion, intento, reintentos)
            return wait.until(condition)
        except TimeoutException:
            logger.warning("Timeout esperando '%s' (intento %d/%d)", descripcion, intento, reintentos)
            if intento == reintentos:
                raise
        except (StaleElementReferenceException, WebDriverException) as exc:
            if _is_redirect_exception(exc) and driver is not None and intento < reintentos:
                logger.warning(
                    "Redirect detectado mientras se esperaba '%s' — refrescando y reintentando...",
                    descripcion,
                )
                time.sleep(3)
                driver.refresh()
                time.sleep(3)
            else:
                raise
    # nunca debería llegar aquí, pero por seguridad:
    raise TimeoutException(f"No se pudo encontrar: {descripcion}")


def _navegar_a_login(driver) -> bool:
    """
    Intenta cargar la página de login con fallback de URL.
    Devuelve True si la carga fue exitosa.
    """
    for url in _LOGIN_URLS:
        try:
            logger.info("Navegando a: %s", url)
            driver.get(url)
            # Dar tiempo a que terminen los redirects internos de FB antes de
            # empezar a pollean el DOM. Este sleep es la corrección principal
            # del bug GetHandleVerifier.
            logger.info("Esperando 3s para que terminen los redirects de FB...")
            time.sleep(3)
            current = driver.current_url
            logger.info("URL actual tras carga: %s", current)
            # Si terminamos en /login o en una variante, la URL es válida
            if "login" in current or "facebook.com" in current:
                return True
        except WebDriverException as exc:
            logger.warning("Error navegando a %s: %s — probando URL alternativa...", url, exc)
    return False


def iniciar_session(driver) -> int:
    """
    Inicia sesión en Facebook.

    Retorna:
        1  — sesión iniciada correctamente
        0  — fallo (credenciales, checkpoint, o error irrecuperable)
    """
    wait = WebDriverWait(driver, 15)

    try:
        # ── Paso 1: verificar si ya hay sesión ────────────────────────────
        logger.info("Paso 1/5 — Verificando estado de sesión existente...")
        logger.info("Navegando a https://www.facebook.com/")
        driver.get("https://www.facebook.com/")
        logger.info("Esperando 4s para carga inicial...")
        time.sleep(4)

        if esta_logueado(driver):
            logger.info("Sesión ya activa — omitiendo login.")
            return 1

        # ── Paso 2: cargar la página de login ─────────────────────────────
        logger.info("Paso 2/5 — No hay sesión activa. Cargando página de login...")
        if not _navegar_a_login(driver):
            logger.error("No se pudo cargar ninguna URL de login de Facebook.")
            return 0

        # ── Paso 2.5: cerrar cookie consent si aparece ────────────────────
        logger.info("Paso 2.5/5 — Verificando cookie consent dialog...")
        _dismiss_cookie_consent(driver)
        time.sleep(2)

        # ── Paso 2.6: detectar pantalla "Continuar como [usuario]" ────────
        # Cuando el perfil tiene sesión guardada, FB muestra un botón "Continuar"
        # en lugar del formulario email/password. Hay que clickearlo.
        logger.info("Paso 2.6/5 — Verificando pantalla 'Continuar como usuario'...")
        _xpaths_continuar = [
            # aria-label contiene 'Continuar' (ej: "Continuar Margarita Nauto")
            "//div[@role='button' and contains(@aria-label,'Continuar')]",
            "//div[@role='button' and contains(@aria-label,'Continue')]",
            # span interno con texto exacto
            "//span[normalize-space()='Continuar']/ancestor::div[@role='button'][@tabindex='0']",
            "//span[normalize-space()='Continue']/ancestor::div[@role='button'][@tabindex='0']",
        ]
        for xpath in _xpaths_continuar:
            try:
                btns = driver.find_elements(By.XPATH, xpath)
                if btns:
                    logger.info("✅ Pantalla 'Continuar' detectada. Haciendo click...")
                    driver.execute_script("arguments[0].click();", btns[0])
                    time.sleep(3)

                    # FB puede pedir confirmación de contraseña tras el click
                    pass_fields = driver.find_elements(By.XPATH, _XPATH_PASS)
                    if pass_fields:
                        logger.info("🔑 Campo de contraseña detectado tras 'Continuar'. Ingresando...")
                        pass_fields[0].clear()
                        pass_fields[0].send_keys(os.getenv("PASS_FB", ""))
                        logger.info("Contraseña ingresada. Buscando botón submit...")
                        # Botón submit del formulario de confirmación
                        submit_btns = driver.find_elements(By.XPATH, _XPATH_BTN)
                        if submit_btns:
                            driver.execute_script("arguments[0].click();", submit_btns[0])
                            logger.info("Submit ejecutado. Esperando 10s...")
                        else:
                            # Fallback: Enter desde el campo password
                            from selenium.webdriver.common.keys import Keys
                            pass_fields[0].send_keys(Keys.RETURN)
                            logger.info("Submit vía ENTER. Esperando 10s...")
                        time.sleep(10)
                    else:
                        logger.info("No se requirió contraseña. Esperando 8s...")
                        time.sleep(8)

                    if esta_logueado(driver):
                        logger.info("✅ SESIÓN INICIADA vía 'Continuar'.")
                        return 1
                    logger.warning("Click en 'Continuar' ejecutado pero sesión no confirmada. URL: %s", driver.current_url)
                    break
            except WebDriverException:
                pass

        # ── Paso 3: ingresar email ─────────────────────────────────────────
        logger.info("Paso 3/5 — Localizando campo de email/teléfono...")
        email_input = _wait_for_element(
            wait,
            EC.visibility_of_element_located((By.XPATH, _XPATH_EMAIL)),
            "input email/teléfono",
            driver=driver,
        )
        logger.info("Campo email encontrado. Ingresando credencial...")
        email_input.clear()
        email_input.send_keys(os.getenv("NUM_FB", ""))
        logger.info("Credencial de email ingresada.")

        # ── Paso 4: ingresar contraseña ────────────────────────────────────
        logger.info("Paso 4/5 — Localizando campo de contraseña...")
        pass_input = _wait_for_element(
            wait,
            EC.visibility_of_element_located((By.XPATH, _XPATH_PASS)),
            "input contraseña",
            driver=driver,
        )
        logger.info("Campo contraseña encontrado. Ingresando contraseña...")
        pass_input.clear()
        pass_input.send_keys(os.getenv("PASS_FB", ""))
        logger.info("Contraseña ingresada.")

        # ── Paso 5: click en botón de login ───────────────────────────────
        logger.info("Paso 5/5 — Localizando botón de login...")
        time.sleep(2)  # esperar que FB habilite el botón después de llenar campos
        try:
            login_button = _wait_for_element(
                wait,
                EC.element_to_be_clickable((By.XPATH, _XPATH_BTN)),
                "botón login",
                driver=driver,
            )
            logger.info("Botón login encontrado. Ejecutando click via JS...")
            driver.execute_script("arguments[0].click();", login_button)
        except (TimeoutException, WebDriverException):
            logger.warning("Botón login no encontrado — enviando ENTER como fallback...")
            from selenium.webdriver.common.keys import Keys
            pass_input.send_keys(Keys.RETURN)
        logger.info("Submit ejecutado. Esperando 10s para procesamiento de login...")
        time.sleep(10)

        # ── Verificación post-login ────────────────────────────────────────
        current_url = driver.current_url
        logger.info("URL tras login: %s", current_url)

        if "checkpoint" in current_url:
            logger.warning("Facebook detectó inicio de sesión desde dispositivo nuevo.")
            logger.warning("Acepta la solicitud en tu celular y vuelve a ejecutar el script.")
            return 0

        if esta_logueado(driver):
            logger.info("SESION INICIADA correctamente.")
            return 1
        else:
            logger.error(
                "No se pudo confirmar el inicio de sesion. "
                "URL actual: %s — Verifica credenciales en .env",
                current_url,
            )
            return 0

    except TimeoutException as exc:
        logger.error("Timeout irrecuperable en login: %s", exc)
        return 0
    except WebDriverException as exc:
        logger.error("WebDriverException en login: %s", exc)
        return 0
    except Exception as exc:
        logger.error("Error critico inesperado en login: %s", exc)
        return 0
