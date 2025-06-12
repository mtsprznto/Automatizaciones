from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import os
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
        # Esperar a que el contenedor `feed` esté presente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
        contenedor_feed = driver.find_element(By.XPATH, '//div[@role="feed"]')

        # **Scroll para cargar más elementos**
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Esperar unos segundos para la carga

        # Buscar los bloques dentro del contenedor `feed`
        bloques = contenedor_feed.find_elements(By.XPATH, './/div[contains(@class, "x1yztbdb")]')

        # Depuración: Mostrar la cantidad de bloques encontrados
        print(f"Cantidad de bloques encontrados dentro de 'feed': {len(bloques)}")

        nombres = []
        
        for i, bloque in enumerate(bloques):
            try:
                nombre_elemento = bloque.find_element(By.XPATH, './/strong[contains(@class, "xdj266r")]/span')
                nombre = nombre_elemento.text.strip()
                if nombre:
                    nombres.append(nombre)
            except Exception as e:
                print(f"Error al extraer nombre en bloque {i+1}: {e}")

        print("Nombres encontrados:", nombres)



    except Exception as e:
        print(e)


driver.quit()

