from .client import get_client
import os

client = get_client()

current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(current_dir, "prompt_system.txt")

with open(prompt_path, "r", encoding="utf-8") as file:
    system_prompt = file.read()


def agente_llm(input_file: str):
    """
    Procesa un archivo de texto y utiliza el agente de IA para ordenar su contenido.

    Args:
        input_file (str): Ruta al archivo .txt que contiene el texto desordenado.

    Returns:
        str: Respuesta generada por el agente de IA.
    """
    # Leer el contenido del archivo de entrada
    with open(input_file, "r", encoding="utf-8") as file:
        user_content = file.read()


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_content,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    resultado = chat_completion.choices[0].message.content
    print(resultado)
    return resultado

