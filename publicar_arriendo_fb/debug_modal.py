"""Debug: abre grupo FB, clickea 'Escribe algo', screenshot + dump HTML del modal."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--window-size=1280,900')
opts.add_argument('--no-first-run')
opts.add_argument('--disable-session-crashed-bubble')
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option('useAutomationExtension', False)

user_data = Path(__file__).resolve().parent / 'perfil_fb_ok'
opts.add_argument(f'user-data-dir={user_data}')

GROUP = "https://www.facebook.com/groups/782773525842194/"

d = webdriver.Chrome(options=opts)
try:
    d.get(GROUP)
    time.sleep(5)
    d.save_screenshot('debug_group_01.png')
    print("Screenshot grupo guardado")
    print("URL:", d.current_url)

    # Buscar el botón "Escribe algo"
    xpath_escribe = "//div[@role='button']//span[contains(text(), 'Escribe algo') or contains(text(), 'Write something')]"
    wait = WebDriverWait(d, 10)
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_escribe)))
        print("Botón 'Escribe algo' encontrado")
        d.execute_script("arguments[0].click();", btn)
        print("Click ejecutado")
    except Exception as e:
        print("NO encontrado 'Escribe algo':", e)
        # Buscar cualquier botón de publicar/crear
        btns = d.find_elements(By.XPATH, "//div[@role='button']//span")
        for b in btns[:20]:
            t = b.text.strip()
            if t:
                print("  Span en button:", repr(t))

    time.sleep(4)
    d.save_screenshot('debug_group_02_post_click.png')
    print("Screenshot post-click guardado")

    # Dump de todos los role=textbox y contenteditable
    print("\n=== TEXTBOX ELEMENTS ===")
    textboxes = d.find_elements(By.XPATH, "//*[@role='textbox']")
    print(f"Encontrados {len(textboxes)} elementos role=textbox")
    for i, tb in enumerate(textboxes):
        print(f"  [{i}] tag={tb.tag_name} aria-placeholder={tb.get_attribute('aria-placeholder')!r} contenteditable={tb.get_attribute('contenteditable')!r}")

    print("\n=== CONTENTEDITABLE ELEMENTS ===")
    ces = d.find_elements(By.XPATH, "//*[@contenteditable='true']")
    print(f"Encontrados {len(ces)} elementos contenteditable=true")
    for i, ce in enumerate(ces):
        print(f"  [{i}] tag={ce.tag_name} role={ce.get_attribute('role')!r} aria-placeholder={ce.get_attribute('aria-placeholder')!r}")

    print("\n=== DIALOG ELEMENTS ===")
    dialogs = d.find_elements(By.XPATH, "//*[@role='dialog']")
    print(f"Encontrados {len(dialogs)} dialogs")

    # HTML del primer dialog si existe
    if dialogs:
        inner = dialogs[0].get_attribute('innerHTML')
        with open('debug_dialog.html', 'w', encoding='utf-8') as f:
            f.write(inner)
        print("HTML del dialog guardado en debug_dialog.html")
    else:
        # Guardar body completo
        body = d.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')
        with open('debug_body.html', 'w', encoding='utf-8') as f:
            f.write(body[:50000])
        print("HTML body (primeros 50k chars) guardado en debug_body.html")

finally:
    d.quit()
    print("Done")
