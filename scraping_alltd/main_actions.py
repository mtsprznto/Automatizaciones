import time
import asyncio

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from ia.preguntas import obtener_respuesta


import json

async def main():
    try:
        options = Options()
        options.add_argument('--headless')              # Corre en modo headless
        options.add_argument('--disable-gpu')           # Previene errores en entorno CI
        options.add_argument('--no-sandbox')            # Útil en contenedores
        
        service = Service(executable_path="/usr/local/bin/geckodriver")

        driver = webdriver.Firefox(service=service,options=options)     # Usa opciones actualizadas

        driver.maximize_window()

        #-------------------------
        # Scraping y guardado en archivo
        #-------------------------
        TIME_SLEEP = 5

        FEATURED = "featured"
        TUTORIAL = "tutorial"
        
        POINT = [FEATURED, TUTORIAL]
        for p in POINT:
            print("-----------Inicio scraping-------------------")
            print(f"Web: {p}")
            URL_SCRAPING = f'https://alltd.org/category/{p}/'
            print(f"Go to {URL_SCRAPING}")
            driver.get(URL_SCRAPING)
            time.sleep(TIME_SLEEP)
            bloque_contenedor = driver.find_elements(By.XPATH, '//article[@class="cactus-post-item hentry"]')
            time.sleep(TIME_SLEEP)
            #-------------------------
            # Procesamiento
            #-------------------------
            ITERACIONES = 90
            articulos = []
            
            for cont in range(0, ITERACIONES):
                primer_articulo = bloque_contenedor[cont]
                enlace = primer_articulo.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                titulo = primer_articulo.find_element(By.CSS_SELECTOR, "a").get_attribute('title')
                autor = primer_articulo.find_element(By.CSS_SELECTOR,"span.fn").text
                date = primer_articulo.find_element(By.CSS_SELECTOR, "time.entry-date.updated").text
                imagen = primer_articulo.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
                time.sleep(TIME_SLEEP)
                # Obtener el script que contiene el ID del video
                script_content = primer_articulo.find_element(By.CSS_SELECTOR, "div.ct-icon-video script").get_attribute('textContent')
                respuesta = obtener_respuesta(script_content)
                articulo = {
                    "id": str(cont),  # Convert to string to match your example
                    "titulo": titulo,
                    "autor": autor,
                    "date":date,
                    "enlace_alltd": enlace,
                    "imagen": imagen,
                    "url_video": respuesta
                }
                articulos.append(articulo)
                time.sleep(TIME_SLEEP)
                print(f"Bloque {cont} Completado")
            # Guardar en archivo
            path_save = f"./data_scraping/articulos_{p}.json"
            with open(path_save, "w", encoding="utf-8") as archivo:
                json.dump(articulos, archivo, indent=4, ensure_ascii=False)
            print(f"Articulos guardados en {path_save}")
            print(f"Terminando SCRAPING: {p}")
            print("-"*80)
            articulos = []
        driver.quit()
    except Exception as e:
        print(f"Error inesperado: {e}")
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
