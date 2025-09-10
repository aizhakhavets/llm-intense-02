# Technical Vision: Funny Recipe Bot

*LLM-powered Telegram bot for generating entertaining and surprising recipe combinations*

## Technologies

**Core Stack:**
- **Python 3.11+** - Simple, excellent LLM ecosystem, fast development
- **aiogram 3.x** - Modern async Telegram Bot API library  
- **OpenRouter API** - Access to various LLM models at competitive prices
- **openai** Python library - OpenRouter-compatible API client

**Development & Tools:**
- **uv** - Modern Python dependency management and environment
- **pytest** - Testing framework
- **make** - Automation for build, run, deploy
- **python-dotenv** - Environment configuration

**Deployment:**
- **Docker** - Simple containerization
- **Docker Compose** - Local development and deployment

**Data Approach:**
- **No database** - All necessary info in system prompt or retrieved from web
- **In-memory storage** - Simple Python dict/list for conversation history
- **Stateless design** - Each conversation independent
- **Web search** - For real recipe inspiration when needed

## Development Principles

**KISS - Keep It Simple, Stupid**
- Solve only the current problem - funny recipe generation
- Minimum abstractions - straightforward code
- If a function can be avoided - don't write it
- Direct approach over clever solutions

**No Object-Oriented Programming**
- Pure functional approach
- Functions as building blocks
- Simple data structures (dict, list, str)
- Avoid classes and complex inheritance

**Functional Approach by Layers**
- Organize by layer: handlers/, clients/ with minimal modules
- Each function does one thing well
- Pass data as parameters, avoid global state
- Pure functions where possible - easier to test

**Clean Code**
- Clear naming: `generate_funny_recipe()` not `gen_rec()`
- Comments for complex logic and business rules
- Simple documentation for functions
- Self-documenting code through good naming

**MVP Mindset**
- Build working recipe bot in 1-2 days
- Test with real users ASAP
- Focus on core: ingredient input → funny recipe output
- Simple unit tests for core logic

**Simple Everything**
- Simple testing: unit tests for core functions only
- Simple structure: as few modules as possible

## Project Structure

```
llm-intense-01/
├── main.py              # Entry point - bot startup and polling
├── config.py            # Configuration and environment variables only
├── handlers.py          # Telegram message handlers (layer)
├── llm_client.py        # LLM integration + system prompts
├── tests/
│   ├── test_handlers.py     # Simple handler tests
│   └── test_llm_client.py   # Simple LLM tests
├── doc/                 # All documentation
│   ├── vision.md            # This technical vision
│   └── product_idea.md      # Product description
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example         # Environment template
├── .gitignore
├── pyproject.toml       # uv configuration
├── Makefile             # Build/run automation
└── README.md
```

**Module Responsibilities:**
- **main.py** - Bot initialization, start polling
- **config.py** - Environment variables, API keys, basic settings
- **handlers.py** - All Telegram message handling logic
- **llm_client.py** - LLM communication + system prompts for recipe generation
- **doc/** - All project documentation

## Project Architecture

**Type:** Simple Linear Pipeline Architecture

**Data Flow:**
```
User Message → Telegram API → handlers.py → llm_client.py → OpenRouter API
     ↑                                                              ↓
     ↓                                                        LLM Response
User receives recipe ← Telegram API ← handlers.py ←─────────────────┘
```

**Core Components:**

1. **main.py** - Application entry point
   - Initialize aiogram bot
   - Register handlers
   - Start polling

2. **handlers.py** - Message processing layer
   - Receive user messages
   - Manage conversation context (last 20 messages in-memory dict)
   - Call LLM for recipe generation
   - Send responses back

3. **llm_client.py** - LLM integration layer
   - System prompts for funny recipe generation
   - OpenRouter API communication
   - Response processing

4. **config.py** - Configuration layer
   - Environment variables and basic settings

**Architecture Principles:**
- **Linear Flow** - Simple request→process→response
- **In-Memory Context** - Keep last 20 messages per user
- **Single Responsibility** - Each layer has one clear job

## Data Model

**Principle:** Simple dialogue history per chat_id with relevant messages only

**1. Configuration Data (loaded from .env):**
```python
TELEGRAM_BOT_TOKEN: str
OPENROUTER_API_KEY: str  
OPENROUTER_MODEL: str
LLM_TEMPERATURE: float
LLM_MAX_TOKENS: int
MAX_CONTEXT_MESSAGES: int
LOG_LEVEL: str
```

**2. Dialogue History (in-memory in handlers.py):**
```python
# Per chat_id conversation history
conversations: dict[int, list[dict]] = {}

# Only relevant messages stored:
conversations[chat_id] = [
    {"role": "system", "content": "You are a funny recipe bot..."},
    {"role": "user", "content": "I have chicken and chocolate"},
    {"role": "assistant", "content": "# Chocolate Chicken Surprise\n..."},
    {"role": "user", "content": "Make it spicier"},
    {"role": "assistant", "content": "# Spicy Chocolate Chicken Madness\n..."}
]
```

**What Gets Stored:**
- ✅ User ingredient requests
- ✅ Recipe generation responses
- ✅ Follow-up clarifications
- ❌ Error messages
- ❌ System notifications
- ❌ Bot status messages

**Context Management:**
- Keep last 20 relevant messages per chat_id
- Auto-trim oldest when limit exceeded
- System prompt always included (not counted)

## LLM Integration

**Approach:** OpenRouter API via openai client with full chat context

**Core Integration Function:**
```python
# llm_client.py
def generate_response(chat_messages: list[dict]) -> str:
    """Send full chat history + system prompt to LLM"""
    
    # Prepare messages: system prompt + chat history
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + chat_messages
    
    # OpenRouter via openai client
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-haiku",
            messages=messages,
            temperature=0.8,
            max_tokens=1000
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return "Sorry, I'm having trouble generating recipes right now. Please try again!"
```

**System Prompt** (from product_idea.md):
```python
SYSTEM_PROMPT = """You are an LLM assistant for generating funny and surprising recipes through Telegram.

Goal: Create entertaining culinary experiments by combining real food and drink products in impossible, surprising ways that can actually be cooked.

Rules:
- Ask one clarifying question at a time about preferences or available ingredients
- Only use real food and drink products that exist
- Create surprising combinations that are technically cookable
- Keep recipes simple and easy to follow
- Make the experience entertaining and fun

Recipe format:
- Creative funny name for the dish
- List of surprising ingredient combinations  
- Simple step-by-step instructions
- Expected funny/surprising result description
"""
```

**Simple LLM Answer Handling:**
- Direct text response from LLM → send to user
- No complex parsing or processing

**Context Flow:**
1. Get chat history for current chat_id
2. Add system prompt as first message
3. Send all to LLM via OpenRouter
4. Return LLM response directly

## LLM Monitoring

**Principle:** Simple text logging for cost control and debugging

**Basic Monitoring Implementation:**
```python
# llm_client.py
import logging
import time

def generate_response(chat_messages: list[dict]) -> str:
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(...)
        
        duration = time.time() - start_time
        tokens = response.usage.total_tokens
        
        # Estimate cost (approximate for claude-3.5-haiku: $0.25/1M input + $1.25/1M output tokens)
        estimated_cost = (tokens * 0.75) / 1_000_000  # Rough average
        
        logging.info(f"LLM_SUCCESS tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}")
        return response.choices[0].message.content
```

**What We Track:**
- ✅ Token usage per request
- ✅ Response time
- ✅ Estimated cost per request
- ✅ Simple text log format

**Tools:**
- Python standard logging
- Log rotation for large files
- No complex dashboards for MVP

## Work Scenarios

**Enhanced User Journey with Personality & Profile Matching:**

**1. Initial Conversation Invitation**
```
User: /start
Bot: Welcome, culinary adventurer! 🌟✨ I'm your funny recipe wizard who loves creating impossible-but-delicious combinations rooted in ancient fusion traditions! 

Tell me - what's lurking in your fridge right now? 🥘 Or maybe something's been on your mind ingredient-wise? Share whatever you have or whatever's calling to you! 

Also, what's your mood today - feeling adventurous? Nostalgic? Ready to surprise someone? 🎭
```

**2. Ingredient Gathering**
```
User: I have chicken, dark chocolate, and some random spices
Bot: Ooh, chicken and chocolate! 🍫🐔 That's actually an ancient Mesoamerican combination - the Aztecs were onto something magical! 

What spices are we talking about? And what type of meal speaks to your soul right now?
```

**3. Profile & Mood Check (Optional)**
```
User: I have paprika, cumin, cinnamon. Want something for dinner.
Bot: Perfect spice trinity! 🌶️ Before I craft your culinary surprise... 

Quick vibe check: Are you more of a "comfort food explorer" or "blow-my-mind adventurer"? Any cuisine regions that make your heart sing? (Mediterranean, Asian fusion, Middle Eastern, Latin American...) 

And cooking confidence level - kitchen ninja or cautious experimenter? 🥷👨‍🍳
```

**4. Recipe Generation with Historical Context**
```
User: Adventurous, love Middle Eastern flavors, pretty confident in kitchen
Bot: BRILLIANT! 🌅 I'm channeling ancient Silk Road vibes with a modern twist...

# Sultani Chocolate Chicken (Ottoman-Inspired) 🏺✨

**The Story:** Ottoman sultans loved complex sweet-savory combinations. This dish would've impressed Suleiman himself!

**Ingredients:**
- 2 chicken thighs
- 50g dark chocolate (70%+) 
- 1 tsp cumin, 1 tsp paprika, pinch cinnamon
- Pomegranate molasses, pistachios, fresh mint

**Steps:**
1. Toast spices until fragrant - this awakens their ancient souls 🔥
2. Create chocolate spice rub, massage into chicken (15 min)
3. Sear chicken skin-side down until golden 
4. Flip, add pomegranate molasses glaze
5. Finish with crushed pistachios & mint

**Result:** A dish that tastes like a sunset over Constantinople - rich, mysterious, and surprisingly harmonious! The chocolate becomes earthy, not sweet.
```

**5. Proactive Humorous Variations (Wrap-up)**
```
Bot: Plot twist time! 🎭 Want to shake things up even more?

🌊 **Greek Islander Version**: Swap pistachios for olives and feta - because why should Turkey have all the fun?

🌮 **Aztec Revenge**: Add chipotle and serve with corn tortillas - the chicken that traveled through time!

🍷 **French Rebellion**: Deglaze with red wine instead of pomegranate - because the French can't resist improving everyone's recipes! 

Which timeline calls to you? Or shall we explore completely different cosmic combinations? ✨
```

**Bot Personality Traits:**
- 🎭 Joyful, emoji-rich but never childish
- 🏛️ References ancient culinary history and fusion traditions  
- 🧠 Smart, nuanced suggestions with cultural context
- 🎪 Professional advice wrapped in playful presentation
- 🌍 Draws from global, lesser-known cuisine combinations
- 💫 Proactively offers creative variations with humor

**Recipe Complexity:** 3-7 steps based on user confidence and request complexity

## Deployment

**Principle:** Single Docker container for local deployment

**Docker Configuration:**
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync --frozen
CMD ["uv", "run", "python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  recipe-bot:
    build: .
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./logs:/app/logs
```

**Makefile for Automation:**
```makefile
.PHONY: run stop logs build

run:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f recipe-bot

build:
	docker-compose up --build -d
```

**Local Deployment:**
```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your tokens

# 2. Start bot
make run

# 3. Check logs
make logs
```

**Minimum Requirements:**
- **CPU**: 1 vCPU (any modern processor)
- **RAM**: 512MB (Python + bot is lightweight) 
- **Storage**: 1GB (for Docker images and logs)
- **Network**: Internet access for Telegram API + OpenRouter API
- **Software**: Docker + Docker Compose

## Configuration Approach

**Principle:** All configuration in .env file - simple and explicit

**Environment Setup (.env):**
```bash
# .env (all configuration here)
# Required API tokens
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LLM Settings
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=1000

# Bot Behavior
MAX_CONTEXT_MESSAGES=20

# Logging
LOG_LEVEL=INFO
```

**Config Module (config.py):**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Load all settings from .env - fail fast if missing required ones
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS"))
MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES"))
LOG_LEVEL = os.getenv("LOG_LEVEL")

# Validate required settings
required_vars = [TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, OPENROUTER_MODEL]
if not all(required_vars):
    raise ValueError("Missing required environment variables in .env file!")
```

**Local Development Flow:**
1. Copy `.env.example` to `.env`
2. Fill in all configuration values (no defaults in code)
3. Run `make run` - configuration loaded automatically
4. Change `.env` and restart container for updates

**Example .env.example template:**
```bash
# .env.example - template for developers
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=1000
MAX_CONTEXT_MESSAGES=20
LOG_LEVEL=INFO
```

## Logging Approach

**Principle:** Simple Python logging - INFO by default, DEBUG only when debugging

**Logging Setup:**
```python
# main.py - configure logging at startup
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=LOG_LEVEL,  # INFO by default, DEBUG when needed
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler("logs/recipe_bot.log", maxBytes=10*1024*1024, backupCount=3),
            logging.StreamHandler()  # Console for Docker logs
        ]
    )
```

**What We Log:**
- **INFO**: User interactions, successful recipe generations, LLM metrics
- **DEBUG**: Detailed conversation flow (only when LOG_LEVEL=DEBUG in .env)

**Log Management:**
- Rotate at 10MB, keep 3 backups
- Persist in Docker volume: `./logs:/app/logs`
- View with `make logs` or `tail -f logs/recipe_bot.log`

---

**Technical Vision Complete!** 🎉

*This document serves as the foundation for developing the Funny Recipe Bot following KISS principles and MVP mindset. All sections designed for rapid implementation and testing.*