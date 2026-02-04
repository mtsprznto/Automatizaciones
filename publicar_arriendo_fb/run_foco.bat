@echo off
echo 🔄 Activando entorno virtual...


REM Activa el entorno virtual (.venv)
call .venv\Scripts\activate

echo 🚀 Ejecutando publicar_foco.py...
python publicar_foco.py

REM Opcional: pausa para ver errores si ocurre alguno
REM pause