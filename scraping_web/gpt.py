import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# Configuración del navegador
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(options=options)
driver.maximize_window()

def iniciar_sesion():
    try:
        driver.get("https://web.facebook.com/?locale=es_LA&_rdc=1&_rdr")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(os.getenv('NUM_FB'))
        driver.find_element(By.ID, 'pass').send_keys(os.getenv('PASS_FB'))
        driver.find_element(By.NAME, "login").click()
        WebDriverWait(driver, 15).until(EC.url_contains("facebook.com"))
        print("✅ Sesión iniciada correctamente.")
    except Exception as e:
        print(f"❌ Error al iniciar sesión: {e}")
        driver.quit()

def scroll_y_extraer_bloques(url, max_iteraciones=10):
    try:
        driver.get(url)
        time.sleep(5)

        for i in range(max_iteraciones):
            # Scroll hacia abajo
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # Extraer elementos después de cada scroll
            elementos = driver.find_elements(
                By.XPATH,
                '//div[@role="feed"]//div[contains(@class, "x1yztbdb") and contains(@class, "x1n2onr6") and contains(@class, "xh8yej3") and contains(@class, "x1ja2u2z")]'
            )

            if elementos:
                print(f"\n🔍 Iteración {i+1}: {len(elementos)} elementos encontrados")
                for idx, elemento in enumerate(elementos[:5]):  # Limitar a los primeros 5 por iteración
                    print(f"🧩 Bloque {idx+1}: {elemento.text.strip()}")

            time.sleep(3)

        print("\n✅ Scroll y extracción completados.")
    except Exception as e:
        print(f"❌ Error durante el scraping: {e}")
    finally:
        driver.quit()

# Ejecución
iniciar_sesion()
scroll_y_extraer_bloques("https://web.facebook.com/groups/692338427471692", max_iteraciones=10)