from db import initialize_db, store_video_data
from youtube import get_youtube_transcript
from embeddings import get_embedding
from rag import generate_ai_answer

if __name__ == "__main__":
    initialize_db()

    video_url = "https://www.youtube.com/watch?v=1N6hbRbyAeQ"
    title = "Meal Prep For The Week In Under An Hour | Sweet and Sour Chicken"

    video_id, transcript = get_youtube_transcript(video_url)
    if transcript:
        embedding = get_embedding(transcript)
        store_video_data(video_id, title, video_url, transcript, embedding)

    user_query = "why sky is blue?"
    print("\n🔍 AI Answer:\n", generate_ai_answer(user_query))