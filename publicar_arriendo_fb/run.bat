@echo off
echo 🔄 Activando entorno virtual...


REM Activa el entorno virtual (.venv)
call .venv\Scripts\activate

echo 🚀 Ejecutando publicar_arriendo.py...
python publicar_arriendo.py

REM Opcional: pausa para ver errores si ocurre alguno
REM pause