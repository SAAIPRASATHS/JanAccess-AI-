"""
Speech Service — Whisper (STT) and gTTS (TTS) integration.
"""
import os
import uuid
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Audio output directory
AUDIO_DIR = Path("backend/static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


async def transcribe_audio(file_path: str) -> str:
    """Uses OpenAI Whisper API to transcribe audio file to text."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key == "your_openai_api_key_here":
        logger.warning("No OpenAI API key — returning mock transcription.")
        return "I would like to know about government housing schemes."

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        logger.error(f"Whisper transcription error: {e}")
        return "Sorry, I could not transcribe the audio. Please try again or type your question."


def text_to_speech(text: str, lang: str = 'en') -> str:
    """Converts text to speech using gTTS and returns the file path."""
    try:
        from gtts import gTTS

        tts = gTTS(text=text[:500], lang=lang, slow=False)  # Limit text length
        filename = f"{uuid.uuid4()}.mp3"
        filepath = AUDIO_DIR / filename
        tts.save(str(filepath))
        return str(filepath)
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return ""
