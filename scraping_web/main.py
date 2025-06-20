from scraping.facebook import FacebookScraper
from core.utils.file_handler import guardar_en_txt, obtener_slug, crear_ruta_salida
from ia.llm.gpt import GPTAgent
from config.settings import ARCHIVO_BLOQUES, IA_RESPONSE_DIR, SCROLL_PAUSE_TIME,FACEBOOK_GROUP_URL
import time

def main():
    # Inicializar el scraper
    scraper = FacebookScraper()
    
    try:
        # Iniciar sesión
        if not scraper.iniciar_session():
            print("No se pudo iniciar sesión")
            return
            
        # Navegar al grupo
        if not scraper.navegar_a_grupo():
            print("No se pudo navegar al grupo")
            return
            
        # Obtener elementos con scroll
        if not scraper.obtener_elementos_scroll(ARCHIVO_BLOQUES, 11):
            print("Error al obtener elementos con scroll")
            pass
            
        # Procesar con IA
        gpt_agent = GPTAgent()
        with open(ARCHIVO_BLOQUES, 'r', encoding='utf-8') as file:
            contenido = file.read()

        respuesta = gpt_agent.procesar_texto(contenido)
        
        # # Crear ruta de salida
        try:
            fecha_formato = crear_ruta_salida()
            # Usar el ID del grupo como slug
            #slug = FACEBOOK_GROUP_ID
            url_scraping = FACEBOOK_GROUP_URL
            #print(url_scraping)
            slug = obtener_slug(url_scraping)
            #print(slug)
            archivo_salida = f"{IA_RESPONSE_DIR}/{fecha_formato}_{slug}.md"
            
            # Guardar resultado en markdown
            guardar_en_txt(respuesta, archivo_salida)
        except Exception as e:
            print(f"Error al crear la ruta de salida: {e}")
            return
    
    except Exception as e:
        print(f"Error en el proceso principal: {e}")
    finally:
        scraper.cerrar_session()

if __name__ == "__main__":
    main()
