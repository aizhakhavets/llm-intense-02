# Funny Recipe Bot

An LLM-powered Telegram bot that generates entertaining and surprising recipe combinations rooted in ancient fusion traditions! 🌟✨

## 🎯 What It Does

Creates funny culinary experiments by combining your ingredients in impossible-but-delicious ways with local/regional surprises. Through natural conversation, it gathers your preferences, discovers cultural context, and generates safe but surprising recipes with humor and cultural storytelling.

## ✨ Key Features

- 🤖 **Conversational Intelligence** - Natural step-by-step ingredient gathering with context awareness
- 🍳 **Cultural Recipe Generation** - LLM-powered recipes with historical background stories  
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

### 1-Minute Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd llm-intense-01

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
# Required - Get from @BotFather and OpenRouter
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional - Sensible defaults provided
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=1000
MAX_CONTEXT_MESSAGES=20
```

## 🎭 How It Works

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
Telegram → handlers.py → llm_client.py → OpenRouter (Claude 3.5 Haiku)
    ↑         ↓             ↓                    ↓
   User   State Mgmt   Local Intel        Recipe Generation
          + Memory    + Cultural           + Surprise Scoring
                      Context             + Enhancement
```

### Smart Recipe Generation
1. **Ingredient Intelligence**: Parses user ingredients + selects local surprises
2. **Cultural Context**: Integrates historical cooking traditions 
3. **Surprise Verification**: Ensures recipes score >0.5 surprise factor + humor
4. **Auto-Enhancement**: Improves failed recipes with targeted hints
5. **Proactive Variations**: Offers 2-3 humorous regional adaptations

## 🏗️ Architecture

### Technology Stack
- **Runtime**: Python 3.13 + functional programming (no OOP)
- **Bot Framework**: aiogram 3.x (async Telegram API)
- **LLM Provider**: OpenRouter API (Claude 3.5 Haiku - fast & cost-effective)
- **Deployment**: Docker + Docker Compose (single container)
- **Dependencies**: uv (modern Python package manager)
- **Storage**: In-memory (no database needed)

### Project Structure
```
llm-intense-01/
├── main.py                      # 🚀 Entry point & logging setup (40 lines)
├── config.py                    # ⚙️ Environment management (25 lines)  
├── handlers.py                  # 💬 Message processing & state (300 lines)
├── llm_client.py               # 🧠 LLM integration & prompts (260 lines)
├── ingredient_intelligence.py   # 🌍 Local ingredients (15 regions, 120 lines)
├── surprise_verification.py    # ✅ Quality assurance (310 lines)
├── docker-compose.yml          # 🐳 Deployment config
├── Dockerfile                  # 📦 Container definition
├── Makefile                    # 🔧 Automation (run, stop, logs, build)
├── logs/                       # 📝 Rotating logs (Docker volume)
└── doc/
    ├── documentation.md         # 📚 Complete technical docs
    ├── vision.md               # 🎯 Architecture & principles
    └── product_idea.md         # 💡 Product requirements
```

### Core Modules

| Module | Purpose | Key Features |
|--------|---------|-------------|
| `handlers.py` | Message routing & conversation management | State machine, context extraction, memory management |
| `llm_client.py` | LLM integration & dynamic prompts | Cultural context, conversation vs recipe modes |
| `ingredient_intelligence.py` | Local ingredient selection | 15-country database, cultural storytelling |
| `surprise_verification.py` | Recipe quality assurance | Surprise scoring, humor detection, enhancement |

## 🎪 Supported Regions

**15 Culinary Regions with Local Ingredients & Cultural Context**:

🇮🇹 **Italy**: Parmigiano-reggiano, balsamic vinegar, prosciutto → *"Ancient Roman spice routes meet Renaissance creativity"*

🇲🇽 **Mexico**: Lime, cilantro, jalapeños, avocado → *"Aztec traditions meet Spanish conquistador influences"*

🇯🇵 **Japan**: Miso paste, nori, mirin, sesame oil → *"Zen Buddhist simplicity meets samurai precision"*

🇫🇷 **France**: Butter, thyme, shallots, crème fraîche → *"Medieval guild techniques refined by royal chefs"*

🇮🇳 **India**: Curry leaves, tamarind, cumin, coconut → *"Silk Road spices meet Mughal imperial kitchens"*

*+ 10 more regions (Thailand, Greece, Morocco, China, Spain, Lebanon, Peru, Korea, Turkey, Brazil)*

## 🛠️ Management Commands

```bash
# Deployment
make build    # Build and start bot
make run      # Start with existing image  
make stop     # Stop bot
make clean    # Complete cleanup

# Monitoring  
make logs     # Real-time log streaming
tail -f logs/recipe_bot.log    # Direct log access

# Development
docker-compose up --build -d   # Manual build
docker-compose logs -f recipe-bot  # Manual logs
```

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
