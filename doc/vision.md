# Technical Vision: The Witty AI Cooking Companion

*An LLM-powered Telegram bot that guides users from fun, experimental recipes to healthier eating habits through an engaging, multi-modal experience.*

## Technologies

**Core Stack:**
- **Python 3.11+** - Simple, excellent LLM ecosystem, fast development
- **aiogram 3.x** - Modern async Telegram Bot API library  
- **OpenRouter API** - Access to various LLM models at competitive prices
- **openai** Python library - OpenRouter-compatible API client

**Multi-Modal Input Processing:**
- **Vision API** (e.g., OpenAI Vision, Google Cloud Vision) - To analyze images of ingredients.
- **Speech-to-Text API** (e.g., OpenAI Whisper, Google Cloud Speech-to-Text) - To transcribe audio messages.
- **python-telegram-bot** file handling - To download user-sent photos and audio.
- **Pillow** or **OpenCV-Python** - For basic image processing (if needed before sending to an API).

**Development & Tools:**
- **uv** - Modern Python dependency management and environment
- **pytest** - Testing framework
- **make** - Automation for build, run, deploy
- **python-dotenv** - Environment configuration

**Deployment:**
- **Docker** - Simple containerization
- **Docker Compose** - Local development and deployment

**Data Approach:**
- **Lightweight Database (SQLite)** - Both user profiles and conversation history (dialogs) will be stored in the database to ensure persistence.
- **Stateless Handlers** - The message handlers will be designed to be stateless, fetching all required context (user profile, dialog history) from the database for each incoming message.
- **Web search** - For real recipe inspiration when needed.

## Development Principles

**KISS - Keep It Simple, Stupid**
- Solve only the current problem - create an engaging, multi-modal recipe assistant that can evolve with the user.
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
├── llm_client.py        # LLM integration for text generation
├── vision_client.py     # Client for Vision API calls
├── speech_client.py     # Client for Speech-to-Text API calls
├── database.py          # Database interaction (user profiles & preferences)
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
- **handlers.py** - All Telegram message handling logic; calls appropriate clients for processing.
- **llm_client.py** - Manages communication with the text-generation LLM.
- **vision_client.py** - Handles communication with the Vision API to analyze images.
- **speech_client.py** - Handles communication with the Speech-to-Text API to transcribe audio.
- **database.py** - Manages storing and retrieving user profiles and preferences.
- **doc/** - All project documentation

## Project Architecture

**Type:** Simple Pipeline Architecture with Persistent State

**Data Flow:**
```
                                                  ┌─> vision_client.py ─> Vision API
                                                  │
User Message (Photo, Audio, Text) → Telegram API → handlers.py ┼─> speech_client.py ─> Speech-to-Text API
                                                  │
                                                  └─> llm_client.py ─> OpenRouter (Text LLM)

(Client results are processed by handlers.py, which then calls llm_client.py to generate a final response for the user)
```

**Core Components:**

1. **main.py** - Application entry point
   - Initialize aiogram bot
   - Register handlers
   - Start polling

2. **handlers.py** - Message processing layer
   - Receive user messages (text, photo, audio).
   - For photo/audio messages, download the file and call the appropriate client (`vision_client.py` or `speech_client.py`) to get a text description/transcription.
   - Fetch the current user profile and recent conversation history from the database.
   - Use the resulting text to interact with the main text LLM via `llm_client.py` to generate a response.
   - Save the new messages (user's and bot's) to the dialog history in the database.
   - Send final responses back to the user.

3. **llm_client.py** - LLM integration layer for text
   - Provides functions to interact with the text-generation LLM (via OpenRouter).
   - Prepares and sends prompts using system prompts that adapt to the user's journey stage.
   - Processes and returns text responses from the LLM.

4. **vision_client.py** - Vision processing layer
   - Provides a function to call Vision APIs (e.g., GPT-4 Vision) with an image file.
   - Returns a structured text description of the image content (e.g., a list of ingredients).

5. **speech_client.py** - Speech processing layer
   - Provides a function to call Speech-to-Text APIs (e.g., Whisper) with an audio file.
   - Returns the transcribed text from the user's voice message.

6. **database.py** - Persistence layer
   - CRUD operations for `users` table (profiles, preferences, goals, journey stage).
   - CRUD operations for `dialog_history` table (storing, retrieving, and trimming conversation history).

7. **config.py** - Configuration layer
   - Environment variables and basic settings

**Architecture Principles:**
- **Linear Flow** - Simple request→process→response
- **Persistent User State** - User profiles and preferences are stored in a database.
- **In-Memory Session Context** - Keep last 30 messages per user for the current conversation.
- **Single Responsibility** - Each layer has one clear job

## Data Model

**Principle:** Simple dialogue history per session, with a persistent user profile.

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

**2. User Profile Data (in database.py, e.g., SQLite):**
```python
# User Profile Table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    chat_id INTEGER UNIQUE,
    journey_stage TEXT DEFAULT 'new_user', -- e.g., new_user, familiar, health_focused
    preferences TEXT, -- JSON string for preferences like diet, cuisine, etc.
    goals TEXT -- JSON string for user goals
);
```

**3. Dialogue History Table (in database.py):**
```python
# Dialogue History Table
CREATE TABLE dialog_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    role TEXT NOT NULL, -- 'system', 'user', or 'assistant'
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES users (chat_id)
);
```

**What Gets Stored:**
- ✅ **In DB:**
    - `users` table: `user_id`, `chat_id`, `journey_stage`, `preferences`, `goals`.
    - `dialog_history` table: A record of all `system`, `user`, and `assistant` messages for context.
- ❌ **Not Stored:** Error messages, system notifications, or other non-dialogue events.

**Context Management:**
- Before calling the LLM, retrieve the last `MAX_CONTEXT_MESSAGES` (e.g., 30) messages for the current `chat_id` from the `dialog_history` table.
- The system prompt is adapted based on the user's `journey_stage` from the `users` table and prepended to the retrieved history.
- After a successful interaction, the new user message and the bot's response are saved to the `dialog_history` table.
- A periodic cleanup job could be implemented to trim very old dialogs if the database size becomes a concern.

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

**System Prompt**:

The full system prompt is defined as the `SYSTEM_PROMPT` constant within `llm_client.py`.

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

**The User Journey: From Fun to Healthy**

The following scenarios illustrate the bot's adaptive persona. It starts with a playful tone for new users and gradually becomes a supportive advisor as it learns their goals.

**1. Initial Conversation Invitation (New User)**
```
User: /start
Bot: Welcome, culinary adventurer! 🌟✨ I'm your funny recipe wizard who loves creating impossible-but-delicious combinations rooted in ancient fusion traditions! 

Tell me - what's lurking in your fridge right now? 🥘 Or maybe something's been on your mind ingredient-wise? Share whatever you have or whatever's calling to you! 

Also, what's your mood today - feeling adventurous? Nostalgic? Ready to surprise someone? 🎭
```

**2. Ingredient Gathering (Photo Input)**
```
User: [Sends a photo of a bell pepper, an onion, and some eggs]
Bot: Ah, a classic trio! 🫑🥚 I see bell pepper, onion, and eggs. A fantastic start for a culinary masterpiece... or a delightful disaster! 

What else are we working with? Any spices, proteins, or secret ingredients you're hiding from me? And what meal are we dreaming of?
```

**3. Profile & Mood Check**
```
User: I have some paprika and cheese. I want something for a quick lunch. My goal is to eat healthier.
Bot: A noble goal! And paprika and cheese are excellent sidekicks. Before I whip something up... 

I've noted your goal to eat healthier. I can definitely help with that! For today's lunch, are we leaning towards "tasty but healthy" or "let's have one last hurrah before the diet starts"? 😉
```

**4. Pre-flight Check & Confirmation**
```
User: Tasty but healthy please!
Bot: You got it! Let's confirm:
- **Ingredients:** Bell pepper, onion, eggs, paprika, cheese.
- **Vibe:** A quick, tasty, and healthy lunch.
- **Goal:** Healthy eating.

Ready to cook something amazing?
```

**5. Recipe Generation (Healthy Focus)**
```
User: Yes!
Bot: Excellent! Forget a boring omelette. Let's make...

# Shakshuka-light with a Cheesy Twist 🍳✨

**The Story:** A lighter, quicker take on the classic Middle Eastern dish. All the flavor, none of the fuss!

**Ingredients:**
- 1 bell pepper, sliced
- 1/2 onion, chopped
- 2 eggs
- 1 tsp paprika
- 2 tbsp crumbled feta or goat cheese (less is more!)
- 1/4 cup canned chopped tomatoes (optional, for more flavor)
- Olive oil, salt, and pepper

**Steps:**
1. Sauté the onion and bell pepper in a splash of olive oil until soft.
2. Stir in the paprika and canned tomatoes (if using) and let it simmer for 2 minutes.
3. Make two wells in the vegetable mixture and crack an egg into each.
4. Cover and cook until the egg whites are set but the yolks are still runny.
5. Sprinkle with cheese, salt, and pepper.

**Healthy Twist:** Serve with a side of whole-wheat toast or a fresh green salad instead of white bread. This is packed with protein and veggies to keep you energized!
```

**6. Follow-up & Goal Reinforcement**
```
Bot: How did your Shakshuka-light turn out? 

Since you mentioned you're focusing on healthier eating, I can keep suggesting more recipes like this. We can explore low-carb lunches, high-protein dinners, or even healthy-ish desserts! What sounds good for next time?
```

**7. Scenario: Voice Request**
```
User: [Sends a 10-second voice message]
Bot (internal action):
1. Downloads the audio file.
2. Sends it to the Speech-to-Text API.
3. Receives the transcription: "What can I make with avocados, tomatoes, and some lime?"

Bot (to user):
You've got avocados, tomatoes, and lime? Sounds like the start of a fiesta! 🥑🍅 Are we thinking of a guacamole, a fresh salad, or something more adventurous?
```

**8. Scenario: User Preferences Setup**
```
User: /settings
Bot: Let's fine-tune your culinary profile! This will help me give you the best recommendations. What are your preferences? You can tell me about:
- **Dietary restrictions:** (e.g., vegetarian, gluten-free, no dairy)
- **Favorite cuisines:** (e.g., Italian, Mexican, Thai)
- **Dislikes:** (e.g., no cilantro, not a fan of mushrooms)
- **Health goals:** (e.g., low-carb, high-protein)
```
```
User: I'm vegetarian, love spicy food, and I'm trying to eat low-carb. I hate olives.
Bot (internal action):
1. Parses the user's message.
2. Updates the database for this user:
   - preferences: {"diet": "vegetarian", "likes": "spicy", "dislikes": "olives"}
   - goals: {"nutrition": "low-carb"}

Bot (to user):
Got it! Profile updated: Vegetarian, spicy, low-carb, and a strict no-olive zone. I'll keep this in mind for all future delicious creations! ✨
```

**9. Scenario: Photo of Random Ingredients**
```
User: [Sends a photo of a can of tuna, a lemon, and a red onion]
Bot (internal action):
1. Downloads the image.
2. Sends it to the Vision API.
3. Receives the analysis: ["canned tuna", "lemon", "red onion"].

Bot (to user):
I see you have canned tuna, a lemon, and a red onion! A zesty combination. Are you in the mood for a quick tuna salad, a light pasta dish, or maybe some creative tuna patties? Let me know what you're thinking!
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
MAX_CONTEXT_MESSAGES=30

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
