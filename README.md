# 🚀 Automatizaciones con Python

Este repositorio contiene una colección de proyectos de automatización y scraping desarrollados en Python. Cada proyecto está diseñado para optimizar procesos específicos y extraer datos de manera eficiente.

## 📁 Estructura del Proyecto

El repositorio está organizado en los siguientes directorios principales:

### 🏠 Automatización Airbnb
- Sistema automatizado para la gestión de propiedades en Airbnb
- Incluye scripts para descarga de datos y actualización automática
- Utiliza FastAPI para la API backend

### 🕸️ Scraping Facebook Arriendos
- Sistema de scraping para grupos de Facebook especializados en arriendos
- Extrae información de arriendos de cabañas y departamentos
- Almacena datos en formato CSV para análisis posterior
- Implementa validación geográfica para Puerto Varas

### 📈 Scraping Web
- Sistema general de scraping con integración de IA
- Utiliza Selenium para la automatización web
- Procesamiento de datos con GPT/Llama 2
- Sistema de limpieza y organización de datos
- Manejo de sesiones y autenticación

## 🛠️ Tecnologías Principales

- **Python**: Lenguaje principal
- **Selenium**: Para la automatización web
- **GPT/Llama 2**: Procesamiento de lenguaje natural
- **Pandas**: Análisis de datos
- **FastAPI**: API backend

## 📦 Requisitos

- Python 3.8+
- Firefox WebDriver (para Selenium)
- Variables de entorno configuradas (.env)
- API keys necesarias (Groq/GPT)

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/mtsprznto/Automatizaciones.git
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## 📝 Documentación de Proyectos

### Automatización Airbnb


[`automatización_airbnb`](https://github.com/mtsprznto/Automatizaciones/tree/main/automatizacion_airbnb)

- Sistema automatizado para descarga de datos de Airbnb
- Actualización automática mediante API
- Sistema de backup y versionado

### Scraping Facebook Arriendos

[`scraping_fb_arriendos`](https://github.com/mtsprznto/Automatizaciones/tree/main/scraping_fb_arriendos)



- Extracción de datos de grupos de Facebook
- Validación geográfica para Puerto Varas
- Almacenamiento en CSV
- Sistema de limpieza de datos

### Scraping Web

[`scraping_web`](https://github.com/mtsprznto/Automatizaciones/tree/main/scraping_web)

- Sistema general de scraping
- Integración con IA para análisis
- Sistema de limpieza avanzada
- Manejo de sesiones y autenticación

## 🤝 Contribución
¡Contribuciones son bienvenidas! Por favor, crea un issue o pull request con tus mejoras.

## 📞 Contacto
Para cualquier consulta o sugerencia, por favor, abre un issue en el repositorio.

## 📋 Notas Importantes
- Respetar las políticas de uso de las plataformas
- Usar perfiles dedicados para scraping
- Mantener actualizado el WebDriver
- Respetar tiempos de espera para evitar bloqueos
- Mantener seguras las credenciales y API keys

## 📊 Estructura de Datos
Los datos extraídos se almacenan en formatos estructurados y pueden ser procesados posteriormente mediante las funciones de IA incluidas en cada proyecto.

## 🔐 Seguridad
- Las credenciales se manejan a través de variables de entorno
- Nunca compartir el archivo `.env`
- Usar perfiles dedicados para scraping
- Mantener actualizadas las API keys

## 📈 Estadísticas del Proyecto
- 3 proyectos principales
- +1000 líneas de código
- +10 scripts automatizados
- +5 integraciones con servicios externos

## 🔍 Próximas Mejoras
- Implementación de tests unitarios
- Mejora de la documentación
- Optimización de rendimiento
- Implementación de logging avanzado
- Sistema de monitoreo

## 📚 Recursos Adicionales
- Documentación de Selenium
- Documentación de FastAPI
- Documentación de GPT/Llama 2
- Best practices de scraping
- Guías de seguridad en scraping

## 📢 Aviso Legal
Este repositorio se proporciona "TAL CUAL" y cualquier uso que se haga de él es responsabilidad del usuario. Se recomienda revisar las políticas de uso de las plataformas antes de implementar cualquier sistema de scraping.

