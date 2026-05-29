"""
Abre Chrome VISIBLE con perfil_fb_ok para hacer login manual una vez.
Después de completar login + CAPTCHA, el perfil queda con sesión guardada
y los scripts headless no necesitarán volver a hacer login.

Uso: python login_manual.py
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time

opts = Options()
# SIN --headless para que el usuario vea la pantalla y resuelva captcha
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option('useAutomationExtension', False)
opts.add_argument('--window-size=1280,900')
opts.add_argument('--no-first-run')
opts.add_argument('--disable-session-crashed-bubble')

user_data = Path(__file__).resolve().parent / 'perfil_fb_ok'
opts.add_argument(f'user-data-dir={user_data}')

print("Abriendo Chrome con perfil persistente...")
print("Completa el login + CAPTCHA en la ventana que aparece.")
print("Cuando estés en el feed de Facebook, presiona ENTER aquí para cerrar.")

d = webdriver.Chrome(options=opts)
d.get('https://www.facebook.com/')

input("\n>> Presiona ENTER cuando hayas iniciado sesión en Facebook: ")

url = d.current_url
if 'facebook.com' in url and 'login' not in url:
    print(f"✅ Sesión activa en: {url}")
else:
    print(f"⚠️  URL actual: {url} — asegúrate de estar logueado antes de cerrar")

d.quit()
print("✅ Sesión guardada en perfil_fb_ok. Los scripts headless ya no necesitarán login.")
