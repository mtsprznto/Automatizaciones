import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_client():
    client = Groq(
        api_key = os.getenv("GROQ_API_KEY")
    )

    return client