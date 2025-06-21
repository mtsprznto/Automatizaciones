# Web Scraping

Este proyecto es un sistema de web scraping diseñado para extraer información estructurada de artículos del sitio web AllTD.org, enfocándose específicamente en tutoriales y recursos relacionados con TouchDesigner.

## Características Principales

- Extracción automática de artículos
- Procesamiento de contenido dinámico con JavaScript
- Extracción de vídeos incrustados de YouTube
- Generación de datos estructurados en formato JSON
- Integración opcional con API de IA (Groq)

## Estructura del Proyecto

```
scraping_alltd/
├── data_scraping/          # Almacena los datos extraídos
│   └── articulos.json      # Archivo de salida con los datos estructurados
├── ia/                     # Módulos de IA
│   ├── conn.py             # Conexión a la API de Groq
│   └── preguntas.py        # Funciones para procesamiento con IA
├── .gitignore              # Archivo para ignorar archivos sensibles
├── envexample              # Plantilla para variables de entorno
└── main.py                 # Script principal de scraping
```

## Requisitos

- Python 3.x
- Selenium
- Firefox WebDriver (geckodriver)
- Groq API (opcional para funcionalidades de IA)

## Instalación

1. Clonar el repositorio
2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar las variables de entorno:
   - Copiar `envexample` a `.env`
   - Configurar la API key de Groq si se va a usar la funcionalidad de IA

## Uso

1. Ejecutar el script principal:
   ```bash
   python main.py
   ```

2. Los resultados se guardarán en `data_scraping/articulos.json`

## Estructura del JSON de Salida

Cada artículo extraído contendrá los siguientes campos:
- `id`: Identificador único del artículo
- `titulo`: Título del artículo
- `enlace_alltd`: URL completa del artículo en AllTD.org
- `imagen`: URL de la imagen destacada
- `url_video`: URL del vídeo de YouTube asociado (si existe)

## Variables de Entorno

- `api_qroq`: API key de Groq (opcional)

## Consideraciones Importantes

- El proyecto utiliza Selenium en modo headless para la automatización
- Se recomienda tener una conexión estable a internet
- Los tiempos de espera están configurados para evitar bloqueos
- El proyecto incluye manejo de errores básico

## Contribución

1. Fork del repositorio
2. Crear una rama para tu funcionalidad (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request


## Contacto

- Email: matiaspereznauto@gmail.com
- GitHub: https://github.com/mtsprznto

## Agradecimientos

- Selenium
- Groq
- AllTD.org
- Los desarrolladores que contribuyen a las bibliotecas utilizadas

