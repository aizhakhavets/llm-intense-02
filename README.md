# Funny Recipe Bot

An LLM-powered Telegram bot that generates entertaining and surprising recipe combinations rooted in ancient fusion traditions! 🌟✨

## 🎯 What It Does

Creates funny culinary experiments by combining your ingredients in impossible-but-delicious ways with local/regional surprises. Through natural conversation, it gathers your preferences, discovers cultural context, and generates safe but surprising recipes with humor and cultural storytelling.

## ✨ Key Features

- 🤖 **Conversational Intelligence** - Natural step-by-step ingredient gathering with context awareness
- 🍳 **Cultural Recipe Generation** - LLM-powered recipes with historical background stories
- 📸 **Photo Ingredient Recognition** - Identify ingredients from your photos.
- 🎤 **Voice Message Transcription** - Talk to the bot with your ingredient lists.
- 💾 **Persistent User Profiles** - Remembers your preferences across conversations.
- 🌍 **Local Ingredient Surprise** - Automatic selection of regional ingredients (15 countries supported)
- 😄 **Humor & Personality** - Joyful responses with cultural commentary and witty variations
- 🔄 **Quality Assurance** - Automatic surprise verification and recipe enhancement (up to 3 attempts)
- 📝 **Memory Management** - Remembers conversation context across 20 messages per chat
- 🏛️ **Cultural Storytelling** - References ancient culinary traditions (Silk Road, Ottoman Empire, Aztec fusion)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- [Telegram Bot Token](https://t.me/botfather) from @BotFather
- [OpenRouter API Key](https://openrouter.ai/) for LLM access
- [OpenAI API Key](https://platform.openai.com/api-keys) for audio transcription

### 1-Minute Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd llm-intense-02

# 2. Configure environment
cp .env.example .env
# Edit .env with your tokens

# 3. Deploy with one command
make build

# 4. View logs
make logs
```

### Environment Configuration

Create `.env` file with your credentials:
```bash
# Required - Get from @BotFather, OpenRouter, and OpenAI
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Sensible defaults provided
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
OPENROUTER_VISION_MODEL=google/gemini-pro-vision
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=10000
MAX_CONTEXT_MESSAGES=30
```

## 🎭 How It Works

### How to Use
- **Start a conversation**: Use the `/start` command.
- **Text**: Simply chat with the bot and tell it what ingredients you have.
- **Photo**: Send a photo of your ingredients, and the bot will identify them for you. Use `/photo_help` for tips.
- **Voice**: Send a voice message listing your ingredients.

### User Experience Flow
```
👤 User: /start
🤖 Bot: "Welcome, culinary adventurer! What's lurking in your fridge? 🥘"

👤 User: "I have chicken and chocolate"  
🤖 Bot: "Ooh, ancient Aztec vibes! 🍫🐔 Where are you located?"

👤 User: "Italy"
🤖 Bot: "Perfect! Italian fusion possibilities... What's your cooking mood?"

👤 User: "Adventurous"
🤖 Bot: Generates → "Medici Chocolate Chicken (Renaissance-Inspired) 🏺✨"
```

### Technical Architecture
```
Telegram → handlers.py → llm_client.py   → OpenRouter
              ↑ ↓           (LLM & Vision)
              ↑ ↓
   (User) → database.py   → audio_processor.py → OpenAI (Whisper)
           (User Profiles
         & Conv. History)
```

## 🏗️ Architecture

### Technology Stack
- **Runtime**: Python 3.13
- **Bot Framework**: aiogram 3.x (async Telegram API)
- **LLM Provider**: OpenRouter API (Claude 3.5 Haiku, etc.)
- **Deployment**: Docker + Docker Compose (single container)
- **Dependencies**: uv (modern Python package manager)
- **Storage**: SQLite for user profiles and conversation history.

### Project Structure
```
llm-intense-02/
├── main.py               # 🚀 Entry point & bot startup
├── config.py             # ⚙️ Environment variable management
├── handlers.py           # 💬 Message routing & core bot logic
├── llm_client.py         # 🧠 LLM chat integration
├── image_processor.py    # 🖼️ Image analysis (Vision API)
├── audio_processor.py    # 🎤 Audio transcription (Whisper API)
├── database.py           # 🗄️ SQLite database operations
├── docker-compose.yml    # 🐳 Deployment configuration
├── Dockerfile            # 📦 Container definition
├── Makefile              # 🔧 Automation (run, stop, logs)
└── logs/                 # 📝 Log files
```

### Core Modules

| Module | Purpose |
|--------|---------|
| `handlers.py` | Handles incoming Telegram messages (text, photo, voice) and manages conversation flow. |
| `llm_client.py` | Generates text responses using a Large Language Model. |
| `image_processor.py` | Identifies ingredients from user-sent photos using a Vision model. |
| `audio_processor.py` | Transcribes voice messages into text. |
| `database.py` | Manages storing and retrieving user data and conversation history from an SQLite database. |

## 🛠️ Bot Management Commands

A set of convenient commands are available to manage the bot's lifecycle. You can use either `make` (on Linux/macOS) or the `run.ps1` script (on Windows with PowerShell).

| Command           | Makefile      | PowerShell        | Description                                                                 |
|-------------------|---------------|-------------------|-----------------------------------------------------------------------------|
| **Build & Start** | `make build`  | `.\run.ps1 build` | Builds the Docker image (if needed) and starts the bot in detached mode.    |
| **Start**         | `make run`    | `.\run.ps1 run`   | Starts the bot using the existing image.                                    |
| **Stop**          | `make stop`   | `.\run.ps1 stop`  | Stops and removes the bot's container.                                      |
| **View Logs**     | `make logs`   | `.\run.ps1 logs`  | Streams the live logs from the bot container.                               |
| **Full Cleanup**  | `make clean`  | `.\run.ps1 clean` | Stops the bot, removes the container, and deletes the log volume.           |
| **Direct Logs**   | `tail -f logs/recipe_bot.log` | `Get-Content -Path logs\recipe_bot.log -Wait` | Directly monitor the log file on the host machine. |

## 📊 Monitoring & Performance

### Automatic Logging
- **LLM Metrics**: Token usage, response time, cost estimation
- **Recipe Quality**: Surprise scores, verification attempts, enhancement triggers  
- **User Flow**: State transitions, information extraction, conversation context
- **System Health**: API errors, performance bottlenecks, memory usage

### Log Examples
```
LLM_SUCCESS tokens=450 time=1.23s cost=$0.0012
RECIPE_VERIFIED chat_id=123 attempt=1 surprise_score=0.8 has_humor=true  
SMART_TRANSITION chat_id=123 -> ready_for_recipe (all info collected)
```

### Cost Optimization
- **Efficient Model**: Claude 3.5 Haiku (~$0.75 per 1M tokens average)
- **Smart Context**: Auto-trimmed to 20 relevant messages
- **Token Limits**: 1000 max tokens per response
- **Cost Tracking**: Real-time estimation in logs

## 📈 System Requirements

**Production Ready**:
- **CPU**: 1 vCPU (any modern processor)
- **RAM**: 512MB (lightweight Python application) 
- **Storage**: 1GB (Docker images + rotating logs)
- **Network**: Internet access for Telegram + OpenRouter APIs

**Development Principles**:
- **KISS**: Simple, direct solutions over clever abstractions
- **Functional**: Pure functions, no OOP complexity
- **Stateless**: Each conversation independent
- **MVP Focus**: Core functionality over feature creep

## 📚 Documentation

- **[Complete Documentation](doc/documentation.md)** - Comprehensive technical guide
- **[Technical Vision](doc/vision.md)** - Architecture principles and design decisions  
- **[Product Requirements](doc/product_idea.md)** - Feature specifications and system prompts

## 🔧 Development

**Built with KISS principles**:
- ✅ Functional programming approach (no classes)
- ✅ Simple data structures (dict, list, str)
- ✅ Linear architecture (request → process → response)
- ✅ Minimal dependencies (only essential libraries)
- ✅ Docker deployment (single container)

**Contributing**:
1. Follow functional programming patterns
2. Add comprehensive logging for new features
3. Update documentation for architectural changes
4. Test with real Telegram bot before submitting

## 🎉 Status

**✅ Production Ready**
- All core features implemented and tested
- Docker deployment with persistent logging  
- 15 regional ingredient databases
- Comprehensive surprise verification system
- Real-world user testing completed
- Cost-optimized LLM integration

---

**🌟 Ready to create some culinary chaos? Deploy your bot and start the adventure! 🚀**
