from openai import OpenAI
import psycopg2
import json
from youtube_transcript_api import YouTubeTranscriptApi

openai_client = OpenAI(
base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

conn = psycopg2.connect("dbname=research_db user=admin password=secret host=localhost")
cur = conn.cursor()

cur.execute("""
    CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE IF NOT EXISTS youtube_transcripts (
        id SERIAL PRIMARY KEY,
        video_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        transcript TEXT NOT NULL,
        metadata JSONB,
        embedding VECTOR(1536),
        created_at TIMESTAMP DEFAULT NOW()
    );
""")
conn.commit()


def get_youtube_transcript(video_url):
    try:
        video_id = video_url.split("v=")[-1]  
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return video_id, transcript_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None, None


def get_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
         model="deepseek-r1:1.5b"
    )
    
    return response.data[0].embedding



def store_video_data(video_id, title, url, transcript):
    try:
        embedding = get_embedding(transcript)  
        cur.execute("""
            INSERT INTO youtube_transcripts (video_id, title, url, transcript, metadata, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING;
        """, (video_id, title, url, transcript, json.dumps({"tags": ["AI", "research"]}), embedding))
        conn.commit()
        print("✅ Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")


def search_similar_videos(query):
    query_embedding = get_embedding(query)  
    cur.execute("""
        SELECT title, url, transcript
        FROM youtube_transcripts
        LIMIT 5;
    """, (query_embedding,))

    results = cur.fetchall()
    return results


def generate_ai_answer(query):
    results = search_similar_videos(query)

    context = "\n\n".join([f"Title: {r[0]}\nURL: {r[1]}\nTranscript: {r[2][:300]}..." for r in results])

    prompt = f"""
    Based on the following research findings:
    {context}
    
    Answer the user query: "{query}"
    """

    response = openai_client.chat.completions.create(
        model="deepseek-r1:1.5b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=1K5oDtVAYzk"  
    title = "The Hidden Pattern in Post Codes"    

    video_id, transcript = get_youtube_transcript(video_url)
    if transcript:
        store_video_data(video_id, title, video_url, transcript)

    user_query = "So what is a postal code?"
    print("\n🔍 User Query:\n", user_query)
    print("\n🔍 AI Answer:\n", generate_ai_answer(user_query))