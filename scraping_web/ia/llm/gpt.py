from config.settings import IA_PROMPT_PATH
import os
from dotenv import load_dotenv
from groq import Groq
from config.settings import IA_PROMPT_PATH

load_dotenv()

class GPTAgent:
    def __init__(self):
        self.prompt_path = IA_PROMPT_PATH
        self.client = self.get_client()

    def get_client(self):
        """Obtiene el cliente Groq"""
        return Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def procesar_texto(self, texto):
        """Procesa el texto usando Groq"""
        try:
            # Leer el prompt del archivo
            with open(self.prompt_path, 'r', encoding='utf-8') as file:
                prompt = file.read()

            # Preparar la solicitud
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": texto}
            ]

            # Hacer la solicitud a Groq
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error al procesar texto con Groq: {e}")
            return None
