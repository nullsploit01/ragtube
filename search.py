from db import connect_db
from embeddings import get_embedding
import logging

SIMILARITY_THRESHOLD = 0.7 # Adjust threshold based on use case (0.7 = 70% similarity)

def search_similar_videos(query):
    """Finds similar videos based on embeddings, filtering out low similarity results."""
    query_embedding = get_embedding(query)
    conn, cur = connect_db()

    try:
        cur.execute("""
            SELECT title, url, transcript, embedding <=> %s::vector AS similarity
                FROM youtube_transcripts
                WHERE embedding <=> %s::vector > %s
                ORDER BY similarity DESC
                LIMIT 5;
        """, (query_embedding, query_embedding, SIMILARITY_THRESHOLD))

        results = cur.fetchall()
        
        if not results:
            logging.info("🔍 No relevant research found for query")
            return []

        logging.info("✅ Relevant research found")
        return results

    except Exception as e:
        logging.error(f"🚨 Error in search: {e}")
        return []
    finally:
        cur.close()
        conn.close()