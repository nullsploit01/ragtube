from openai import OpenAI
from config import OLLAMA_CONFIG
import logging

openai_client = OpenAI(
    base_url=OLLAMA_CONFIG["base_url"],
    api_key=OLLAMA_CONFIG["api_key"]
)

def get_embedding(text):
    """Generates AI embeddings using DeepSeek R1 via Ollama."""
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="deepseek-r1:1.5b"
        )
        logging.info("✅ Embedding generated successfully")
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"🚨 Error generating embedding: {e}")
        return None