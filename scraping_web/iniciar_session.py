import time
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





def iniciar_session():
    try:
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        driver = webdriver.Firefox()
        driver.get("https://web.facebook.com/?locale=es_LA&_rdc=1&_rdr")

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
        return driver
    except Exception as e: 
        print(f"Error inesperado: {e}")
        return 0

