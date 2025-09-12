# Funny Recipe Bot

A Telegram bot powered by LLM that generates entertaining and surprising recipe combinations using real food and drink products.

## Overview

This bot creates funny culinary experiments by combining user's ingredients in unexpected ways with local/regional surprises. It uses conversational AI to gather preferences step-by-step, discovers cultural context, and generates safe but surprising recipes for entertaining cooking experiments.

## Key Features

- 🤖 **Interactive Telegram Bot** - Natural conversation flow with step-by-step ingredient gathering
- 🍳 **LLM-Powered Recipe Generation** - Contextual recipes with cultural background stories  
- 🌍 **Local Ingredient Intelligence** - Automatic selection of regional surprise ingredients
- 😄 **Humor & Personality** - Entertaining responses with cultural context and recipe variations
- 🔄 **Surprise Verification** - Ensures recipes meet surprise criteria with automatic enhancement
- 📝 **Conversation Memory** - Remembers context across 20 messages per chat

## Technologies

- **Python 3.11+** with functional programming approach
- **aiogram 3.x** - Modern async Telegram Bot API
- **OpenRouter API** - Access to various LLM models (Claude 3.5 Haiku)
- **Docker** - Containerized deployment
- **uv** - Modern Python dependency management

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Telegram Bot Token (from @BotFather)
- OpenRouter API Key

### Setup & Deployment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd llm-intense-01
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API tokens:
   # TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   # OPENROUTER_API_KEY=your_openrouter_api_key
   ```

3. **Deploy with Docker:**
   ```bash
   # Build and start the bot
   make build
   
   # Or simply run (uses existing image)
   make run
   
   # View logs
   make logs
   
   # Stop the bot
   make stop
   ```

### Manual Commands

```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f recipe-bot

# Stop
docker-compose down
```

## Configuration

All configuration is done via environment variables in `.env` file:

```bash
# Required API tokens
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LLM Settings (optional, with defaults)
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=1000

# Bot Behavior (optional)
MAX_CONTEXT_MESSAGES=20
```

## Project Structure

```
llm-intense-01/
├── main.py                  # Entry point - bot startup and logging
├── config.py                # Configuration and environment variables
├── handlers.py              # Telegram message handlers and conversation flow
├── llm_client.py            # LLM integration with system prompts
├── ingredient_intelligence.py   # Local ingredient selection logic
├── surprise_verification.py     # Recipe surprise scoring and enhancement
├── docker-compose.yml       # Docker deployment configuration  
├── Dockerfile               # Container definition
├── Makefile                 # Deployment automation commands
├── pyproject.toml           # Python dependencies (uv)
├── logs/                    # Persistent log files (Docker volume)
└── doc/                     # Complete project documentation
    ├── vision.md                # Technical architecture
    ├── product_idea.md          # Product requirements
    ├── conventions.md           # Development standards  
    └── tasklist.md              # Development iterations
```

## How It Works

1. **Conversation Flow:** Bot asks step-by-step questions to gather user ingredients and preferences
2. **Cultural Discovery:** Optionally discovers user location for regional ingredient surprises  
3. **Local Intelligence:** Automatically selects 1-2 local ingredients to enhance recipes
4. **Recipe Generation:** Creates entertaining recipes with cultural context and humor
5. **Surprise Verification:** Scores and enhances recipes to ensure maximum surprise factor
6. **Follow-up Engagement:** Continues conversation with variations and new recipe ideas

## Development

Built following KISS (Keep It Simple, Stupid) principles:
- **Functional approach** - No OOP, simple functions by domains
- **Minimal dependencies** - Only essential libraries  
- **Simple architecture** - Linear pipeline: User → Handlers → LLM → Response
- **In-memory storage** - No database, conversation history in memory
- **Docker deployment** - Single container with persistent logs

## Logging & Monitoring

- **Rotating logs:** `logs/recipe_bot.log` (10MB max, 3 backups)
- **Docker logs:** Console output via `make logs`
- **LLM monitoring:** Token usage, response time, estimated cost tracking

## System Requirements

- **CPU:** 1 vCPU
- **RAM:** 512MB  
- **Storage:** 1GB (Docker images + logs)
- **Network:** Internet access for Telegram + OpenRouter APIs

## Author

Andrei

## Status

✅ **Production Ready** - All 10 development iterations completed, Docker deployment available
