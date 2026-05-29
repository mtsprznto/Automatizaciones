from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import time, os
from dotenv import load_dotenv

load_dotenv()

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--window-size=1280,900')
opts.add_argument('--no-first-run')

user_data = Path(__file__).resolve().parent / 'perfil_fb_ok'
opts.add_argument(f'user-data-dir={user_data}')

d = webdriver.Chrome(options=opts)
try:
    d.get('https://www.facebook.com/login')
    time.sleep(4)
    d.save_screenshot('debug_01_landing.png')
    print('Title:', d.title)
    print('URL:', d.current_url)

    email = d.find_element('xpath', '//input[@name="email"]')
    email.send_keys(os.getenv('NUM_FB', ''))
    time.sleep(1)

    pw = d.find_element('xpath', '//input[@name="pass"]')
    pw.send_keys(os.getenv('PASS_FB', ''))
    time.sleep(2)

    d.save_screenshot('debug_02_filled.png')
    pw.send_keys(Keys.RETURN)
    time.sleep(10)

    d.save_screenshot('debug_03_post_login.png')
    print('URL post:', d.current_url)
    print('Title post:', d.title)

    # Buscar mensajes de error en pantalla
    for xpath in [
        '//*[contains(text(),"checkpoint")]',
        '//*[contains(text(),"verificar")]',
        '//*[contains(text(),"Verificar")]',
        '//*[contains(text(),"suspendida")]',
        '//*[contains(text(),"incorrecta")]',
        '//*[contains(text(),"deshabilitada")]',
    ]:
        els = d.find_elements('xpath', xpath)
        for e in els[:2]:
            t = e.text.strip()
            if t:
                print('Texto visible:', t[:300])
finally:
    d.quit()
    print('Done')
