import time
import re

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import os
from dotenv import load_dotenv
load_dotenv()

#-------------------------
# UTILS
#-------------------------

nombre_archivo = "./data_scraping/bloques_extraidos.txt"

from utils.guardar_en_txt import guardar_en_txt
from utils.obtener_slug import obtener_slug



#-------------------------
# Primero iniciar session
#-------------------------



try:
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox()
    driver.maximize_window()
    url_iniciar_session = "https://web.facebook.com/?locale=es_LA&_rdc=1&_rdr"
    
    driver.get(url_iniciar_session)
    time.sleep(4)
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(os.getenv('NUM_FB'))
    time.sleep(4)
    pass_input= driver.find_element(By.ID,'pass')
    pass_input.send_keys(os.getenv('PASS_FB'))
    time.sleep(4)
    login_button = driver.find_element(By.NAME, "login") 
    login_button.click()
    time.sleep(7)
except Exception as e: 
    print(f"Error inesperado: {e}")

#-------------------------
# Scraping y guardado en archivo
#-------------------------


try:
    SCROLL_PAUSE_TIME = 5
    last_height = driver.execute_script("return document.body.scrollHeight")

    #-------------------------
    url_scraping = 'https://web.facebook.com/groups/692338427471692'
    driver.get(url_scraping)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_TIME)

    # FEED GENERAL
    elements = driver.find_elements(By.XPATH,'//div[@role="feed"]//div[contains(@class, "x1yztbdb") and contains(@class, "x1n2onr6") and contains(@class, "xh8yej3") and contains(@class, "x1ja2u2z")]')

    time.sleep(SCROLL_PAUSE_TIME)
    print(elements[0].text)
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    for cont in range(1, 11):
        time.sleep(SCROLL_PAUSE_TIME)
        print(elements[cont].text)
        guardar_en_txt(elements[cont].text, nombre_archivo)
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        

    driver.quit()
except Exception as e:
    print(f"Error inesperado: {e}")
    driver.quit()


#-------------------------
# IA organizar
#-------------------------
try:
    from ia.consultas import agente_llm
    from datetime import datetime


    #input_file = "./data_scraping/bloques_extraidos.txt"
    respuesta = agente_llm(nombre_archivo)
    #print(respuesta)
    fecha_formato = datetime.now().strftime("%d%m%y")
    slug = obtener_slug(url_scraping)
    print(slug)
    print(fecha_formato)

    ia_response = f"./data_scraping/ia_response/{fecha_formato}_{slug}.md"
    guardar_en_txt(respuesta, ia_response)
except Exception as e:
    print(f"Error inesperado: {e}")