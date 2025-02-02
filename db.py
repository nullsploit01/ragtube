import psycopg2
import json
import logging
from config import DB_CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_db():
    """Connects to PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        logging.info("✅ Connected to PostgreSQL")
        return conn, cur
    except Exception as e:
        logging.error(f"🚨 Database connection error: {e}")
        exit(1)

def initialize_db():
    conn, cur = connect_db()
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
    logging.info("✅ Database initialized successfully")
    cur.close()
    conn.close()

def store_video_data(video_id, title, url, transcript, embedding):
    conn, cur = connect_db()
    try:
        cur.execute("""
            INSERT INTO youtube_transcripts (video_id, title, url, transcript, metadata, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING;
        """, (video_id, title, url, transcript, json.dumps({"tags": ["AI", "research"]}), embedding))
        conn.commit()
        logging.info("✅ Data inserted successfully")
    except Exception as e:
        logging.error(f"🚨 Error inserting data: {e}")
    finally:
        cur.close()
        conn.close()