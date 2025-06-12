from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import time

from utils.iniciar_session import iniciar_session


load_dotenv()

driver = webdriver.Chrome()
driver.get('https://web.facebook.com/?_rdc=1&_rdr')



iniciar_session(driver)


grupos_arriendos = [
    "https://web.facebook.com/groups/309255821890411/",
    # "https://web.facebook.com/groups/arriendospuertovaras/",
    # "https://web.facebook.com/groups/1026824829038999/",
    # "https://web.facebook.com/groups/1222821132423278/",
    # "https://web.facebook.com/groups/692338427471692/"
]

for grupo in grupos_arriendos:
    print(f"Accediendo a: {grupo}")
    driver.get(grupo)
    time.sleep(5)
    
    try:
        driver.maximize_window()
        #-------------
        # XPATH PARA EL TITULO
        # .//strong[contains(@class, "xdj266r")]/span 
        #

        #-------------
        # XPATH PARA DESCRIPCION
        # .//div[@dir="auto" and @style="text-align: start;"]
        #

        #-----------
        # XPATH DE IMAGENES
        # .//img[@class="xz74otr x15mokao x1ga7v0g x16uus16 xbiv7yw x1ey2m1c xtijo5x x5yr21d x10l6tqk x1o0tod x13vifvy xh8yej3"]
        #

        # Esperar a que el contenedor `feed` esté presente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
        contenedor_feed = driver.find_element(By.XPATH, '//div[@role="feed"]')

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Esperar unos segundos para la carga

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/div[contains(@class, "x1yztbdb")]')))

        # Buscar los bloques dentro del contenedor `feed`
        bloques = driver.find_elements(By.XPATH, './/div[contains(@class, "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")]')
        resultado_nombres = driver.find_elements(By.XPATH,'.//strong[contains(@class, "xdj266r")]/span')
        for i, bloque in enumerate(bloques):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                # Buscar dentro del bloque el contenido de texto
                nombre_contenedor = resultado_nombres[i]
                print(f"Resultado: {nombre_contenedor.text}")


                
                #lineas = bloque.find_elements(By.XPATH, './/div[@dir="auto" and contains(@style, "text-align")]')
            
            except Exception as e:
                print(f"❌ Error en bloque {i+1}: {e}")






        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        nombre_contenedor = driver.find_element(By.XPATH,'.//strong[contains(@class, "xdj266r")]/span')
        nombre_text= nombre_contenedor.text.strip()
        time.sleep(3)
        descripcion_contenedor = driver.find_element(By.XPATH,'.//div[@dir="auto" and contains(@style, "text-align")]')
        descripcion_text= descripcion_contenedor.text.strip()

        print(descripcion_text)

       
        # nombre_elemento = bloques.find_element(By.XPATH, './/strong[contains(@class, "xdj266r")]/span')

        # print("Nombres encontrados:", nombre_elemento)
        time.sleep(3)
        # **Scroll para cargar más elementos**
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    except Exception as e:
        print(e)


driver.quit()

