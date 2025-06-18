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



#-------------------------
# Primero iniciar session
#-------------------------



try:
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox()
    driver.maximize_window()
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
except Exception as e: 
    print(f"Error inesperado: {e}")



try:
    SCROLL_PAUSE_TIME = 5
    last_height = driver.execute_script("return document.body.scrollHeight")

    #-------------------------
    url = 'https://web.facebook.com/groups/692338427471692'
    driver.get(url)

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


    time.sleep(SCROLL_PAUSE_TIME)
    print(elements[1].text)
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    time.sleep(SCROLL_PAUSE_TIME)
    print(elements[2].text)
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    time.sleep(SCROLL_PAUSE_TIME)
    print(elements[3].text)
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    time.sleep(SCROLL_PAUSE_TIME)
    print(elements[4].text)
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")




    driver.quit()
except Exception as e:
    print(f"Error inesperado: {e}")
    driver.quit()

    

