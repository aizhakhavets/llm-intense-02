import logging
from io import BytesIO
import openai
from config import OPENAI_API_KEY, OPENROUTER_AUDIO_MODEL

# Use the official OpenAI client for transcription
client = openai.AsyncClient(api_key=OPENAI_API_KEY)

async def transcribe_audio_message(chat_id: int, audio_data: BytesIO) -> str:
    """
    Transcribes an audio message using the official OpenAI Whisper API.
    """
    try:
        # Set the filename for the API, required for some audio formats
        audio_data.name = "voice_message.ogg"

        response = await client.audio.transcriptions.create(
            model=OPENROUTER_AUDIO_MODEL,
            file=audio_data
        )
        
        transcribed_text = response.text
        logging.info(f"Successfully transcribed audio for chat_id={chat_id}: '{transcribed_text}'")
        return transcribed_text

    except Exception as e:
        logging.error(f"Error transcribing audio for chat_id={chat_id}: {e}")
        return "Error: Could not transcribe the audio message."
