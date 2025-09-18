import os
from dotenv import load_dotenv

if os.getenv("ENV") != "production":
    load_dotenv()

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# OpenRouter LLM
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-haiku")
OPENROUTER_VISION_MODEL = os.getenv("OPENROUTER_VISION_MODEL", "google/gemini-2.0-flash-exp:free")

# OpenAI Audio
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Separate key for Whisper
OPENROUTER_AUDIO_MODEL = os.getenv("OPENROUTER_AUDIO_MODEL", "whisper-1")

LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.8"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "10000"))

# Bot Behavior
MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", "30"))

# Validate required settings
required_vars = [TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, OPENAI_API_KEY]
if not all(required_vars):
    raise ValueError("Missing required environment variables! Make sure they are set in your environment or .env file.")
