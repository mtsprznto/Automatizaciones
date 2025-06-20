
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
from config.settings import FACEBOOK_URL, FACEBOOK_GROUP_URL, SCROLL_PAUSE_TIME
import os
from dotenv import load_dotenv
from core.utils.file_handler import guardar_en_txt

load_dotenv()

class FacebookScraper:
    def __init__(self):
        self.options = Options()
        self.options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.driver = None

    def iniciar_session(self):
        """Inicia sesión en Facebook"""
        try:
            self.driver = webdriver.Firefox()
            self.driver.maximize_window()
            self.driver.get(FACEBOOK_URL)
            time.sleep(4)
            
            # Ingresar credenciales
            email_input = self.driver.find_element(By.ID, "email")
            email_input.send_keys(os.getenv('NUM_FB'))
            time.sleep(4)
            
            pass_input = self.driver.find_element(By.ID, 'pass')
            pass_input.send_keys(os.getenv('PASS_FB'))
            time.sleep(4)
            
            login_button = self.driver.find_element(By.NAME, "login") 
            login_button.click()
            time.sleep(7)
            
            return True
            
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False

    def navegar_a_grupo(self):
        """Navega al grupo de Facebook especificado"""
        try:
            self.driver.get(FACEBOOK_GROUP_URL)
            return True
        except Exception as e:
            print(f"Error al navegar al grupo: {e}")
            return False

    def scroll_pagina(self):
        """Realiza scroll en la página"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            return True
        except Exception as e:
            print(f"Error al hacer scroll: {e}")
            return False

    def obtener_elementos_feed(self):
        """Obtiene los elementos del feed"""
        try:
            elements = self.driver.find_elements(By.XPATH,
                '//div[@role="feed"]//div[contains(@class, "x1yztbdb") and contains(@class, "x1n2onr6") and contains(@class, "xh8yej3") and contains(@class, "x1ja2u2z")]')
            return elements
        except Exception as e:
            print(f"Error al obtener elementos del feed: {e}")
            return []

    def obtener_elementos_scroll(self, archivo_salida, num_elementos):
        """Obtiene elementos del feed con scroll"""
        try:
            elements = self.obtener_elementos_feed()
            last_height = self.scroll_pagina()
            for cont in range(1, num_elementos):
                time.sleep(SCROLL_PAUSE_TIME)
                print(elements[cont].text)
                guardar_en_txt(elements[cont].text, archivo_salida)
                time.sleep(SCROLL_PAUSE_TIME)
                self.scroll_pagina()
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = self.scroll_pagina()
                time.sleep(SCROLL_PAUSE_TIME)
            return True
            
        except Exception as e:
            print(f"Error al obtener elementos con scroll: {e}")
            return False

    def cerrar_session(self):
        """Cierra la sesión"""
        if self.driver:
            self.driver.quit()
