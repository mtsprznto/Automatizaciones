# 🏨 Airbnb Automatización  

Este proyecto es una automatización que interactúa con la plataforma **Airbnb**. Su propósito principal es descargar y procesar datos relacionados con **reservas**, almacenarlos en un repositorio local y luego subir los cambios a un repositorio remoto de **Git**.  

## 📂 Estructura del Proyecto  

- **`automatic_down_csv.py`** – Script que utiliza **Selenium** para automatizar el inicio de sesión en Airbnb, descargar un archivo de reservas y procesarlo. También emplea **pywinauto** para interactuar con ventanas del sistema operativo y **dotenv** para cargar credenciales desde un archivo `.env`.  
- **`gitupdate.py`** – Script que usa **gitpython** para agregar archivos al índice de **Git**, realizar un commit y subir los cambios al repositorio remoto.  
- **`go_dl.bat`** – Script por lotes que automatiza la ejecución de los scripts Python (`automatic_down_csv.py` y `gitupdate.py`) y gestiona procesos relacionados con **Python**.  
- **`.env` y `envexample`** – Archivos para almacenar **credenciales sensibles** como el correo y la contraseña de inicio de sesión en Airbnb.  
- **`requirements.txt`** – Lista de **dependencias** necesarias para ejecutar el proyecto, como Selenium, pywinauto y python-dotenv.  

## 🔄 Flujo de Trabajo  

### 🏁 Inicio de Sesión y Descarga  
1. **`automatic_down_csv.py`** inicia sesión en Airbnb utilizando credenciales almacenadas en `.env`.  
2. Descarga un **archivo de reservas** desde Airbnb y lo guarda en la ubicación `temp_calendar/reservations_all.csv`.  

### 📦 Procesamiento del Archivo  
3. El archivo descargado **se renombra** y **se mueve** a una carpeta específica.  
4. Se utiliza **pywinauto** para interactuar con ventanas del sistema operativo durante el proceso de descarga.  

### 🚀 Subida al Repositorio  
5. **`gitupdate.py`** agrega el archivo procesado y otros archivos relevantes al **índice de Git**, realiza un commit y sube los cambios al **repositorio remoto**.  

### 🔄 Automatización Completa  
6. **`go_dl.bat`** coordina la ejecución de los scripts y gestiona procesos relacionados con **Python**.  

## 🛠️ Dependencias Clave  

- **Selenium** – Para la **automatización del navegador**.  
- **pywinauto** – Para **interactuar con ventanas** del sistema operativo.  
- **python-dotenv** – Para **cargar variables de entorno** desde un archivo `.env`.  
- **gitpython** – Para **interactuar con Git** desde Python.  

## 🎯 Propósito  

El proyecto está diseñado para **automatizar la gestión de reservas de Airbnb**, descargando datos, procesándolos y asegurando que estén sincronizados en un **repositorio remoto**. Esto permite mantener un registro actualizado de las reservas y posibilita la integración con otros sistemas.  

---

Este formato optimiza la estructura y claridad del documento, facilitando su lectura y comprensión. ¿Quieres que agregue algún otro detalle? 🚀  