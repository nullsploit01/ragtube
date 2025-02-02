from youtube_transcript_api import YouTubeTranscriptApi
import logging

def get_youtube_transcript(video_url):
    """Fetches the transcript of a YouTube video."""
    try:
        video_id = video_url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        logging.info(f"✅ Transcript fetched for video: {video_id}")
        return video_id, transcript_text
    except Exception as e:
        logging.error(f"🚨 Error fetching transcript: {e}")
        return None, None