@echo off
echo 🧹 Limpiando procesos previos de Chrome para evitar bloqueos...

:: Usamos taskkill (nativo de CMD) para cerrar procesos huérfanos
:: /F fuerza el cierre, /IM es el nombre de la imagen, /T cierra procesos hijos
taskkill /F /IM chrome.exe /T >nul 2>&1
taskkill /F /IM chromedriver.exe /T >nul 2>&1

echo 🔄 Activando entorno virtual...
call .venv\Scripts\activate

echo 🚀 Ejecutando publicar_foco.py...
python publicar_foco.py

echo.
echo ✅ Proceso finalizado.