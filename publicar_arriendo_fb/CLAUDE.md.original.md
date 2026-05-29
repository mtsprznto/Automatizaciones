# CLAUDE.md — publicar_arriendo_fb

## Protocolo Obligatorio
**SIEMPRE iniciar con `/caveman`** antes de cualquier tarea.
Actualizar este archivo cada vez que se descubra una ruta nueva, se resuelva un error o se confirme un patrón técnico.

---

## Proyecto
Bot Selenium que publica avisos de arriendo de departamento en grupos de Facebook.
Automatiza: login → escribir texto → subir imágenes → publicar en múltiples grupos.

**Propiedad:** Departamento de Margarita, Puerto Varas.
**Contacto propietaria:** +56 9 99479312

---

## Stack
- Python 3.x + Selenium + webdriver-manager + python-dotenv
- Chrome con perfil persistente (`perfil_fb/`) → evita re-login
- Credenciales en `.env` (nunca comitear)

## Estructura
```
publicar_arriendo_fb/
├── publicar_arriendo.py   # ✅ SCRIPT PRINCIPAL (usar este)
├── main.py                # versión antigua — headless, 1 solo grupo, driver version hardcodeada
├── main_actions.py        # versión Firefox — async innecesario, NO usar en producción
├── publicar_foco.py       # script para otro producto (focos LED)
├── utils/
│   └── iniciar_session.py # login FB + detección de checkpoint
├── image/                 # imágenes a subir: 1.png 2.png 3.png 4.png
├── perfil_fb/             # perfil Chrome persistente (no comitear — enorme)
├── .env                   # NUM_FB, PASS_FB — NUNCA comitear
└── requirements.txt       # selenium, python-dotenv, webdriver-manager
```

## Cómo Ejecutar
```bash
# Activar venv
.venv\Scripts\activate

# Correr script principal
python publicar_arriendo.py
```

---

## Variables de Entorno (.env)
```
NUM_FB=<numero o email de facebook>
PASS_FB=<contraseña>
```

---

## Errores Conocidos

### Pantalla "Continuar como usuario" reemplaza el form de login ✅ RESUELTO
- **Síntoma:** Email input nunca encontrado → timeout — NO es que FB cambió el HTML del form
- **Causa real:** Con perfil persistente (`perfil_fb/`), FB detecta la sesión guardada y muestra botón "Continuar como Margarita Nauto" en lugar del form email/password
- **Fix aplicado:** Paso 2.6/5 en `iniciar_session.py`:
  1. Detecta botón "Continuar" → `//div[@role='button' and contains(@aria-label,'Continuar')]`
  2. Click → espera 3s → chequea si aparece campo `name="pass"` (FB pide confirmación de contraseña)
  3. Si aparece → llena con `PASS_FB` del `.env` → submit (botón o ENTER fallback)
  4. Espera 10s → verifica login
- **XPath correcto del botón Continuar:** `aria-label="Continuar Margarita Nauto"` — el texto está en `<span>` anidado, hay que buscar por `@aria-label` del div padre
- **Flujo post-Continuar:** FB muestra campo password de confirmación (`name="pass"`, `type="password"`) antes de completar el login
- **Regla:** Siempre manejar los 3 estados posibles de `facebook.com/login`: (1) ya logueado en home, (2) pantalla "Continuar", (3) form email/password

### Email input timeout en login FB ✅ RESUELTO
- **Síntoma:** `Timeout esperando 'input email/teléfono' (intento 1/2)` → `(intento 2/2)` → fallo
- **Causa 1:** Facebook muestra un **cookie consent dialog** ANTES del login form. Sin dismissarlo, el form nunca es visible
- **Causa 2:** `--window-position=-32000,-32000` (fuera de pantalla) → FB no renderiza el formulario
- **Causa 3:** XPaths de email demasiado simples (`@name='email'` solo)
- **Fix aplicado:**
  - `_dismiss_cookie_consent()` en `iniciar_session.py` busca 8 variantes del botón "Aceptar cookies"
  - Llamado en Paso 2.5/5 (entre navegar y buscar el email) + `sleep(2)` tras cerrar
  - `_XPATH_EMAIL` ampliado: `@autocomplete='username'`, `@type='email'`, `@placeholder` en ES/EN
  - `--window-position=0,0` en ambos scripts
- **Regla:** Siempre llamar `_dismiss_cookie_consent()` antes de interactuar con cualquier form de FB

### `GetHandleVerifier` + `Message:` vacío durante login — causa real ✅ RESUELTO
- **Síntoma:** Chrome NO muere — sigue procesando grupos. Solo falla `iniciar_session`
- **Causa real:** `WebDriverWait.poll()` empieza a buscar el email input MIENTRAS Facebook todavía ejecuta redirects internos en `/login`. El DOM se invalida mid-poll → `WebDriverException` con `Message:` vacío (no es timeout, no es elemento no encontrado)
- **Fix aplicado en `utils/iniciar_session.py`:**
  - `time.sleep(3)` después de `driver.get('/login')` antes de cualquier `wait.until()`
  - `_wait_for_element()` wrapper con retry + `driver.refresh()` si detecta redirect-exception
  - `_is_redirect_exception()` detecta el patrón: `WebDriverException` con `Message:\n` vacío
  - Logging granular por paso (Paso 1/5 ... Paso 5/5) para aislar futura rotura
  - XPaths de botón login ampliados con `data-testid='royal_login_button'`
  - Fallback URL: si `/login` falla, intenta `/login/?next=%2F`
- **Regla:** NUNCA hacer `wait.until()` sin `sleep()` previo después de `driver.get()` en FB

### Chrome crash → `Message:` vacío + stacktrace `GetHandleVerifier` ✅ RESUELTO
- **Síntoma:** `ERROR: ❌ Error crítico en login: Message: \n Stacktrace: chromedriver!GetHandleVerifier...`
- **Causa real:** `--headless` + `user-data-dir` en Chrome 112+ (new headless) crashea al navegar con perfil existente. El perfil fue creado en modo GUI y es incompatible con new-headless.
- **Causa secundaria:** `perfil_fb/SingletonLock` residual después de `taskkill /F` (también se limpia en setup_driver)
- **Fix definitivo:** Usar `--headless=new` + `--disable-gpu` + `--window-size=1280,800`. El crash original NO era por headless — era por el timeout del email input (botón "Continuar" no manejado)
- **Regla:** NUNCA usar `--headless` a secas en Chrome 112+. Usar `--headless=new` explícitamente.

### `pdb.set_trace()` en iniciar_session.py bloquea automation ✅ RESUELTO
- **Archivos:** `utils/iniciar_session.py` (líneas 76, 83, 88), `publicar_foco.py` (línea 220), `publicar_arriendo.py`
- **Causa:** Debugger interactivo dejado en producción — cuelga el proceso esperando input de teclado
- **Fix aplicado:** Removidos todos. Reemplazados con `logger.error(...)` + `return 0`

### XPath con clases CSS hardcodeadas se rompen
- **Ejemplo:** `lista_checkbox_grupos` en `main.py` y `main_actions.py` — usa clases CSS de FB que cambian con cada deploy
- **Fix preferido:** Usar `@type='checkbox'` dentro de contexto de modal, sin clases CSS

### `main_actions.py` tiene `async def main()` pero Selenium es síncrono
- **Causa:** Selenium no es async-compatible de forma nativa
- **Fix:** Convertir a función normal `def main()` o eliminar `asyncio.run()`

### ChromeDriver version hardcodeada en main.py
- **Línea:** `ChromeDriverManager(driver_version="143.0.7499.170").install()`
- **Fix:** Usar `ChromeDriverManager().install()` sin version fija (auto-detecta)

### Imágenes con ruta relativa fallan si CWD no es raíz del proyecto
- **Archivo:** `main.py` línea 168 — usa `os.path.abspath(ruta_relativa)`
- **Fix (aplicado en publicar_arriendo.py):** `Path(__file__).resolve().parent / "image/1.png"`

### Facebook Checkpoint bloquea login headless
- **Causa:** FB detecta nuevo dispositivo/IP → pide confirmación en celular
- **Síntoma:** `"checkpoint" in driver.current_url` es True
- **Fix actual:** `pdb.set_trace()` para autorizar manual (OK para uso personal, NO para CI)
- **Fix definitivo:** Usar perfil persistente (`perfil_fb/`) para mantener sesión activa

---

## Patrones Aprendidos

### Perfil persistente Chrome
`publicar_arriendo.py` guarda sesión en `perfil_fb/`. Una vez logueado manualmente, 
los runs siguientes saltan el login automáticamente.

### Click vía JS para overlays FB
FB tiene muchos overlays. Preferir `driver.execute_script("arguments[0].click();", el)` 
sobre `.click()` nativo para evitar `ElementClickInterceptedException`.

### Xpath bilingüe (ES/EN)
FB puede estar en español o inglés. Siempre usar `or` en XPath:
```python
"//div[@role='button']//span[contains(text(), 'Escribe algo') or contains(text(), 'Write something')]"
```

### Grupos inaccessibles
Verificar `"Contenido no encontrado" in driver.page_source` antes de intentar publicar.
Si inaccessible → `continue` al siguiente grupo.

### Upload de imágenes — método directo
En `publicar_arriendo.py` se envía al `input[@type='file' and @multiple]` directamente,
más confiable que el flujo de botones Foto/video → agregar.

---

## Grupos FB Activos (publicar_arriendo.py)
30 grupos de arriendo/turismo en Puerto Varas y alrededores.
Ver lista completa en `publicar_arriendo.py` → variable `LINK_GROUPS`.
