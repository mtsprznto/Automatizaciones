@echo off
echo 🔄 Activando entorno virtual...


REM Activa el entorno virtual (.venv)
call .venv\Scripts\activate

echo 🚀 Ejecutando main.py...
python main.py

REM Opcional: pausa para ver errores si ocurre alguno
REM pause