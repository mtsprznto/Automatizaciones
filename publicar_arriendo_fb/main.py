from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

import sys
import time

from dotenv import load_dotenv
from utils.iniciar_session import iniciar_session
import os


load_dotenv()




chrome_options = Options()

# Si estás en entorno sin GUI (como GitHub Actions), activa headless
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)


#driver = webdriver.Chrome()
driver.get('https://web.facebook.com/?_rdc=1&_rdr')





LINK_GROUP = "https://web.facebook.com/groups/676990837721174/"

TEXTO_DESCRIPCION = """
Arriendo acogedor departamento interior tipo departamento en Puerto Varas
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
- 1 dormitorio con dos camas de plaza


Wifi disponible
Reja de protección en la entrada para niños pequeños

No se arrienda por año corrido

Tarifa: $50.000 por noche
Dueña: Margarita
Contacto: +56 9 99479312
Interesados, llamar directamente al número telefónico
"""


iniciar_session(driver)
print("INICIO EXITOSO")
driver.get(LINK_GROUP)
TS = 5
time.sleep(TS)

try:
    escribe_algo = "//div[@role='button' and descendant::span[contains(text(), 'Escribe algo') or contains(text(), 'Write something')]]"
    elemento = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, escribe_algo))
    )
    driver.execute_script("arguments[0].click();", elemento)  # Click vía JS por si hay overlays
except Exception as e:
    print(f"❌ Error al insertar texto [escribe_algo]: {e}")
    driver.quit()
    sys.exit(1)



time.sleep(TS)

try:
    crear_publicacion_publica = "//div[@contenteditable='true' and @role='textbox' and (@aria-placeholder='Crea una publicación pública...' or @aria-placeholder='Create a public post...')]"
    editor = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, crear_publicacion_publica))
    )
    editor.click()  # Activar el foco
    editor.send_keys(TEXTO_DESCRIPCION)
    print("✅ Texto insertado correctamente.")
except Exception as e:
    print(f"❌ Error al insertar texto [crear_publicacion_publica]: {e}")
    driver.quit()
    sys.exit(1)

time.sleep(TS)



# añadir imagenes


try:
    btn_agregar_a_publicacion="//div[@role='button' and (@aria-label='Agregar a tu publicación' or @aria-label='Add to your post')]"
    boton_agregar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, btn_agregar_a_publicacion))
    )
    driver.execute_script("arguments[0].click();", boton_agregar)
    print("✅ Botón 'Agregar a tu publicación' clickeado correctamente.")
except Exception as e:
    print(f"❌ Error al hacer clic en el botón [btn_agregar_a_publicacion]: {e}")
    driver.quit()
    sys.exit(1)

time.sleep(TS)




try:
    btn_foto_video = "//span[text()='Foto/video']/ancestor::div[@role='button']"
    boton_foto_video = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, btn_foto_video))
    )
    driver.execute_script("arguments[0].click();", boton_foto_video)
    print("✅ Botón 'Foto/video' clickeado correctamente.")
except Exception as e:
    print(f"❌ Error al hacer clic en 'Foto/video': {e}")
    driver.quit()
    sys.exit(1)


time.sleep(TS)



inputs = driver.find_elements(By.XPATH, "//input[@type='file' and contains(@accept, 'image')]")


URL_LIST = [
    "image/1.png",
    "image/2.png",
    "image/3.png",
    "image/4.png"
]

try:
    for i, ruta_relativa in enumerate(URL_LIST, start=1):
        ruta_absoluta = os.path.abspath(ruta_relativa)
        inputs[1].send_keys(ruta_absoluta)
        print(f"✅ Imagen {i} enviada: {ruta_absoluta}")
        time.sleep(2)  # Espera entre cargas para evitar saturación
except Exception as e:
    print(f"⚠️ Error al subir imágenes: {e}")
    driver.quit()
    sys.exit(1)


time.sleep(TS)



agregar_mas_grupos = "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u' and text()='Agregar grupos']"

try:
    boton_agregar_grupos = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, agregar_mas_grupos))
    )
    driver.execute_script("arguments[0].click();", boton_agregar_grupos)
    print("✅ Click en 'Agregar grupos' realizado correctamente.")
except Exception as e:
    print(f"❌ Error al hacer clic en 'Agregar grupos': {e}")
    driver.quit()
    sys.exit(1)

time.sleep(TS)

lista_checkbox_grupos = "//input[@class='x1i10hfl x9f619 xggy1nq xtpw4lu x1tutvks x1s3xk63 x1s07b3s x1ypdohk x5yr21d x1o0tod xdj266r x14z9mp xat24cr x1lziwak x1w3u9th x1a2a7pz xexx8yu xyri2b x18d9i69 x1c1uobl x10l6tqk x13vifvy xh8yej3' and @type='checkbox']"
try:
    checkboxes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, lista_checkbox_grupos))
    )
    # Slicing del 2 al 7 (índices 1 al 6)
    for i, checkbox in enumerate(checkboxes[1:7], start=2):
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"✅ Checkbox #{i} clickeado.")
  
except Exception as e:
    print(f"❌ Error al clickeear checkboxes del 2 al 7: {e}")
    driver.quit()
    sys.exit(1)
  
time.sleep(TS)

boton_listo_grupos = "//div[@role='button' and @aria-label='Listo']"
try:
    boton_listo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, boton_listo_grupos))
    )
    driver.execute_script("arguments[0].click();", boton_listo)
    print("✅ Botón 'Listo' clickeado correctamente.")
except Exception as e:
    print(f"❌ Error al hacer clic en el botón 'Listo': {e}")
    driver.quit()
    sys.exit(1)
time.sleep(TS)



# DARLE CLICK A PUBLICAR
btn_publicar = "//div[@role='button' and @aria-label='Publicar']"
try:
    boton_publicar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, btn_publicar))
    )
    driver.execute_script("arguments[0].click();", boton_publicar)
    print("🚀 Publicación enviada correctamente.")
except Exception as e:
    print(f"❌ Error al hacer clic en 'Publicar': {e}")
    driver.quit()
    sys.exit(1)

time.sleep(8)