from .conn import get_groq_client

def obtener_respuesta(pregunta: str) -> str:
    """
    Envía una pregunta al modelo de Groq y devuelve la respuesta.
    
    Args:
        pregunta (str): La pregunta o mensaje para el modelo
        modelo (str, optional): El modelo a utilizar. Por defecto es "meta-llama/llama-4-scout-17b-16e-instruct"
        
    Returns:
        str: La respuesta generada por el modelo
    """
    client = get_groq_client()
    respuesta_completa = ""
    
    try:


        # Preparar la solicitud
        messages = [
            {
                "role": "system", 
                "content": f"""
                Te entregare una expresión que tiene un id de youtube, me puedes dar la url de este elemento:
                ~~~
                {pregunta}
                ~~~
                La quiero de esta forma: https://www.youtube.com/watch?v="id_elemento"

                En "id_elemento" quiero que coloques la id que encuentras, quiero que solo me entreges la url, no quiero que me entregues nada mas.
                """
            },
            {
                "role": "user", 
                "content": pregunta
            }
        ]

        # Hacer la solicitud a Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        return response.choices[0].message.content

        
        
    except Exception as e:
        return f"Error al obtener respuesta: {str(e)}"

# Ejemplo de uso
# if __name__ == "__main__":
#     pregunta = 'if(typeof(video_iframe_params) == "undefined") video_iframe_params = []; video_iframe_params[50175] = [\"<iframe title=\"Recreating the sun with Touchdesigner GLSL particles\" width=\"1280\" height=\"720\" src=\"https:\/\/www.youtube.com\/embed\/EKjCGIErOz4?feature=oembed&amp;autoplay=1&amp;wmode=opaque&amp;rel=0&amp;showinfo=0&amp;iv_load_policy=3&amp;modestbranding=0\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen\/<\/iframe>\"];'
#     respuesta = obtener_respuesta(pregunta)
#     print("Pregunta:", pregunta)
#     print("\nRespuesta:", respuesta)