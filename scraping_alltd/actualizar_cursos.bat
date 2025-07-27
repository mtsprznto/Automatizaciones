@echo off
setlocal

:: Activar entorno virtual
call .venv\Scripts\activate
if errorlevel 1 (
    echo Error al activar entorno virtual
    exit /b 1
)

:: Ejecutar el script principal
python main.py
if errorlevel 1 (
    echo Error al ejecutar main.py
    exit /b 1
)

:: Verificar cambios y subir a GitHub
git add .
git commit -m "Actualización automática desde .bat"
git push origin main

echo Script completado exitosamente.
endlocal