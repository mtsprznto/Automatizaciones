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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager




load_dotenv()


chrome_options =  webdriver.ChromeOptions()

# Si estás en entorno sin GUI (como GitHub Actions), activa headless

chrome_options.add_argument('--headless')              # Corre en modo headless
chrome_options.add_argument('--disable-gpu')           # Previene errores en entorno CI
chrome_options.add_argument('--no-sandbox')   # Útil en contenedores

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager(driver_version="143.0.7499.170").install()),
    options=chrome_options
)


#driver = webdriver.Chrome()
driver.get('https://web.facebook.com/?_rdc=1&_rdr')




# Modificar esto para que sea un array de links
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

TEXTO_DESCRIPCION = """Foco Solar LED 1200W IP67 - Especial para Parcelas y Lluvia

Ilumina tu parcela o entrada sin gastar un peso en la cuenta de la luz. Este foco solar de 1200W está diseñado para resistir las condiciones climáticas de Puerto Varas, gracias a su certificación IP67 que lo protege totalmente de la lluvia y humedad.

Contacto Directo y WhatsApp: +56975475781
Haz clic aquí para escribirme: https://wa.me/56975475781

Características principales:
- Potencia: 1200W de alta luminosidad.
Autonomía: Se carga durante el día y se enciende automáticamente al anochecer.
Resistencia: Certificación IP67 (Totalmente resistente al agua).
Fácil Instalación: No requiere cables ni conexión eléctrica.
Control Remoto: Configura el tiempo de encendido y la intensidad a distancia.

¿Qué incluye el kit por $35.000?
- Foco LED 1200W con panel solar integrado.
Brazo de soporte metálico para poste o pared.
Control remoto con pilas incluidas.
Kit de pernos de anclaje.

Promociones:
- 1 unidad: $35.000
2 unidades por: $64.990
4 unidades por: $119.990

Entregas: Retiro en Puerto Varas. Realizamos envíos a domicilio (consultar recargo según zona) y envíos a regiones por pagar vía Starken o Blue Express.

Escríbeme para asegurar los tuyos. ¡Stock limitado!
"""


iniciar_session(driver)

for link in LINK_GROUPS:
    try:
        driver.get(link)
        TS = 5
        time.sleep(TS)

        try:
            escribe_algo = "//div[@role='button' and descendant::span[contains(., 'algo') or contains(., 'write')]]"
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
            "image/foco/foco.jpeg",
            "image/foco/foco_.jpeg",
            "image/foco/foco_posicion.jpeg",
            "image/foco/referencia_ia.jpeg",
            "image/foco/img_ia.jpeg",
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

    except Exception as e:
        print(f"❌ Error en el grupo {link}: {e}")
        # En caso de error, el debugger permite inspeccionar el estado del driver
        # pdb.set_trace() 
        continue # Salta al siguiente grupo

driver.quit()