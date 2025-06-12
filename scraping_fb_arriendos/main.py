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
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-posinset]')))

        # Intentar capturar los elementos correctos
        bloques = driver.find_elements(By.XPATH, '//div[@aria-posinset]')

        # Depuración
        print(f"Cantidad de bloques encontrados: {len(bloques)}")




    except Exception as e:
        print(e)


driver.quit()

