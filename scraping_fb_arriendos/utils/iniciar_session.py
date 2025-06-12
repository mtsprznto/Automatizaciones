import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv

load_dotenv()

def iniciar_session(driver):
    try:
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
        return 1
    except Exception as e: 
        print(f"Error inesperado: {e}")
        return 0

