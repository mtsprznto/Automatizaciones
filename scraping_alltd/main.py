import time
import asyncio

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ia.preguntas import obtener_respuesta

import os

import json

async def main():
    try:
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        driver = webdriver.Firefox()
        driver.maximize_window()

        #-------------------------
        # Scraping y guardado en archivo
        #-------------------------
        TIME_SLEEP = 5

        URL_SCRAPING = 'https://alltd.org/category/featured/'
        driver.get(URL_SCRAPING)
        time.sleep(TIME_SLEEP)
        

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(TIME_SLEEP)
        # new_height = driver.execute_script("return document.body.scrollHeight")
        # time.sleep(TIME_SLEEP)

        bloque_contenedor = driver.find_elements(By.XPATH, '//article[@class="cactus-post-item hentry"]')
        time.sleep(TIME_SLEEP)


        #-------------------------
        # Procesamiento
        #-------------------------
        ITERACIONES = 90
        articulos = []
        for cont in range(0, ITERACIONES):
            #print(bloque_contenedor[0].text)
            primer_articulo = bloque_contenedor[cont]
            enlace = primer_articulo.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            #print(f"ENLACE: {enlace}")
            titulo = primer_articulo.find_element(By.CSS_SELECTOR, "a").get_attribute('title')
            #print(f"Titulo: {titulo}")
            imagen = primer_articulo.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
            #print(f"URL de la imagen: {imagen}")
            
            time.sleep(TIME_SLEEP)
            
            # Obtener el script que contiene el ID del video
            script_content = primer_articulo.find_element(By.CSS_SELECTOR, "div.ct-icon-video script").get_attribute('textContent')
            

            #print(script_content)


            respuesta = obtener_respuesta(script_content)
            #print(respuesta)
            articulo = {
                "id": str(cont),  # Convert to string to match your example
                "titulo": titulo,
                "enlace_alltd": enlace,
                "imagen": imagen,
                "url_video": respuesta
            }

            articulos.append(articulo)
            time.sleep(TIME_SLEEP)
        
        #print(articulos)
        # Guardar en archivo
        path_save = "./data_scraping/articulos.json"
        with open(path_save, "w", encoding="utf-8") as archivo:
            json.dump(articulos, archivo, indent=4, ensure_ascii=False)

        print(f"Articulos guardados en {path_save}")


        driver.quit()
    except Exception as e:
        print(f"Error inesperado: {e}")
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
