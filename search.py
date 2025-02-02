from db import connect_db
from embeddings import get_embedding
import logging

def search_similar_videos(query):
    """Finds similar videos based on embeddings."""
    query_embedding = get_embedding(query)
    conn, cur = connect_db()

    try:
        cur.execute("""
            SELECT title, url, transcript
            FROM youtube_transcripts
            LIMIT 5;
        """, (query_embedding,))
        
        results = cur.fetchall()
        logging.info("✅ Similar research found")
        return results
    except Exception as e:
        logging.error(f"🚨 Error in search: {e}")
        return []
    finally:
        cur.close()
        conn.close()