from openai import OpenAI
from config import OLLAMA_CONFIG
from search import search_similar_videos
import logging

openai_client = OpenAI(
    base_url=OLLAMA_CONFIG["base_url"],
    api_key=OLLAMA_CONFIG["api_key"]
)

def generate_ai_answer(query):
    """Uses RAG (Retrieval-Augmented Generation) to answer questions."""
    results = search_similar_videos(query)

    context = "\n\n".join([f"Title: {r[0]}\nURL: {r[1]}\nTranscript: {r[2][:300]}..." for r in results])

    prompt = f"""
    Based on the following research findings:
    {context}

    Answer the user query: "{query}"
    """

    try:
        response = openai_client.chat.completions.create(
            model="deepseek-r1:1.5b",
            messages=[{"role": "user", "content": prompt}]
        )
        logging.info("✅ AI response generated")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"🚨 Error generating AI response: {e}")
        return "Sorry, I couldn't generate an answer."