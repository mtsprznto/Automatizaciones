# Automatización de Web Scraping con IA

## Descripción
Este proyecto es una herramienta de automatización que combina web scraping con inteligencia artificial para extraer y procesar datos de Facebook. Utiliza Selenium para la automatización web y GPT para el procesamiento de texto.

## Estructura del Proyecto

### Directorios Principales
- `data_scraping/` - Almacena los datos extraídos
- `driver/` - Contiene los drivers del navegador
- `ia/` - Contiene el código relacionado con inteligencia artificial

### Archivos Principales
- `main.py` - Script principal que maneja la automatización
- `iniciar_session.py` - Gestión de sesiones y autenticación
- `limpiar_text.py` - Procesamiento y limpieza de texto
- `gpt.py` - Interfaz con GPT para procesamiento de lenguaje natural

## Requisitos
- Python 3.x
- Selenium
- Firefox WebDriver
- python-dotenv
- Otros paquetes Python (ver requirements.txt)

## Configuración
1. Crear archivo `.env` con las siguientes variables:
   ```
   NUM_FB=tu_email_facebook
   PASS_FB=tu_contraseña_facebook
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
1. Ejecutar el script principal:
   ```bash
   python main.py
   ```

2. El script iniciará sesión en Facebook y comenzará a extraer datos del grupo especificado.

## Funcionalidades
- Automatización de navegación web con Selenium
- Extracción de datos de Facebook
- Procesamiento y limpieza de texto
- Integración con IA para análisis de datos
- Manejo de sesiones y autenticación

## Notas Importantes
- El proyecto requiere credenciales de Facebook válidas
- Se recomienda usar un perfil dedicado para el scraping
- Respetar las políticas de uso de Facebook
- Mantener actualizado el WebDriver de Firefox

## Estructura de Datos
Los datos extraídos se almacenan en el directorio `data_scraping/` y pueden ser procesados posteriormente mediante las funciones de IA incluidas en el proyecto.

## Seguridad
- Las credenciales se manejan a través de variables de entorno
- Nunca compartir el archivo `.env`
- Usar un perfil de Facebook dedicado para el scraping

## Contribución
Si deseas contribuir al proyecto, por favor crea un issue o pull request con tus mejoras.