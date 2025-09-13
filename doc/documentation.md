# Funny Recipe Bot - Complete Documentation

## Overview

The Funny Recipe Bot is an LLM-powered Telegram bot that creates entertaining and surprising recipe combinations using real food and drink products. It follows a conversational approach to gather user preferences and generates culturally-aware recipes with humor and unexpected ingredient combinations.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [Bot Setup & Deployment](#bot-setup--deployment)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Development](#development)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

### Core Architecture Pattern
**Linear Pipeline Architecture**: Simple request → process → response flow

```
User Message → Telegram API → handlers.py → llm_client.py → OpenRouter API
     ↑                                                               ↓
     ↓                                                         LLM Response
User receives recipe ← Telegram API ← handlers.py ←──────────────────┘
```

### Technology Stack

- **Runtime**: Python 3.13+ with functional programming approach
- **Telegram Bot**: aiogram 3.x (modern async Telegram Bot API)
- **LLM Provider**: OpenRouter API (Claude 3.5 Haiku)
- **Deployment**: Docker + Docker Compose
- **Dependency Management**: uv (modern Python package manager)
- **Storage**: In-memory (no database required)

### Design Principles

- **KISS (Keep It Simple, Stupid)**: Minimal abstractions, direct solutions
- **Functional Approach**: No OOP, pure functions as building blocks
- **Stateless Design**: Each conversation independent, minimal state
- **MVP Mindset**: Focus on core functionality over features

## System Components

### 1. Entry Point (`main.py`)
**Purpose**: Application initialization and startup

**Key Functions**:
- Bot initialization with aiogram
- Logging configuration (rotating file handler)
- Handler registration and polling startup

**Code Structure**:
```python
async def main():
    setup_logging()          # Configure rotating logs
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)  # Register message handlers
    await dp.start_polling(bot)
```

### 2. Configuration (`config.py`)
**Purpose**: Environment variable management and validation

**Environment Variables**:
- `TELEGRAM_BOT_TOKEN` - Bot API token from @BotFather (required)
- `OPENROUTER_API_KEY` - OpenRouter API key (required)
- `OPENROUTER_MODEL` - LLM model (default: anthropic/claude-3.5-haiku)
- `LLM_TEMPERATURE` - Response creativity (default: 0.8)
- `LLM_MAX_TOKENS` - Response length limit (default: 1000)
- `MAX_CONTEXT_MESSAGES` - Conversation memory (default: 20)

**Validation**: Fails fast on missing required variables

### 3. Message Handlers (`handlers.py`)
**Purpose**: Telegram message processing and conversation management

**Core Components**:

#### Conversation Storage
```python
# In-memory storage per chat_id
conversations: dict[int, list[dict]] = {}        # Message history
user_states: dict[int, str] = {}                 # Conversation state
user_profiles: dict[int, dict] = {}              # User preferences
```

#### Conversation States
- `waiting_for_ingredients` → `discovering_location` → `asking_mood` → `checking_skill_level` → `ready_for_recipe` → `recipe_generated` → `post_recipe_followup`

#### Key Functions:
- `add_to_conversation()` - Message history management with auto-trimming
- `extract_user_info()` - Context-aware information extraction
- `should_generate_recipe()` - Recipe generation trigger logic
- Message routing for `/start` command and general messages

#### Recipe Generation Process:
1. **Verification Loop**: Up to 3 attempts to generate surprising recipes
2. **Surprise Scoring**: Verification of humor and surprise factors
3. **Enhancement**: Automatic recipe improvement if verification fails

### 4. LLM Client (`llm_client.py`)
**Purpose**: OpenRouter API integration and system prompt management

**Core Functions**:

#### Dynamic System Prompt Builder
```python
def build_dynamic_system_prompt(user_profile, local_ingredients, 
                               conversation_state, for_recipe_generation)
```
- Context-aware prompt generation
- Cultural context integration
- Recipe vs. conversation mode switching
- Local ingredient incorporation

#### Recipe Generation Pipeline
```python
async def generate_recipe_with_local_ingredients(chat_id, user_profile, hints)
```
- User ingredient parsing
- Local surprise ingredient selection
- Cultural context integration
- Recipe generation with regeneration hints

#### Contextual Conversation
```python
async def generate_contextual_response(chat_id, user_profile, 
                                     conversation_history, current_state)
```
- State-aware conversation flow
- Natural response generation
- Information gathering guidance

### 5. Ingredient Intelligence (`ingredient_intelligence.py`)
**Purpose**: Local ingredient selection and cultural context

**Regional Database**: 15 supported regions with local ingredients
- Italy: "parmigiano-reggiano", "balsamic vinegar", "prosciutto"...
- Mexico: "lime", "cilantro", "jalapeños", "avocado"...
- India: "curry leaves", "tamarind", "cumin seeds"...
- [13 more regions with 8 ingredients each]

**Cultural Context Database**: Historical cooking context per region
- Italy: "Ancient Roman spice routes meet Renaissance creativity"
- Japan: "Zen Buddhist simplicity meets samurai precision"
- Morocco: "Berber nomad traditions meet Arabic palace cuisine"

**Key Functions**:
- `select_surprise_ingredients()` - Intelligent local ingredient selection
- `normalize_location()` - Location string processing
- `get_cultural_context()` - Cultural storytelling context

### 6. Surprise Verification (`surprise_verification.py`)
**Purpose**: Recipe quality assurance and enhancement

**Surprise Scoring Algorithm**:
- Ingredient category analysis (meats, sweets, dairy, etc.)
- Combination surprise scoring (sweet + savory = high surprise)
- Normalization and capping (max 2.0 surprise score)

**Humor Detection**:
- Keyword analysis for humor indicators
- Emoji presence checking
- Content structure analysis

**Enhancement Pipeline**:
```python
async def verify_recipe_surprise() → dict  # Verification results
def get_regeneration_hints() → str         # Improvement guidance  
async def enhance_recipe() → str           # Recipe improvement
```

## Bot Setup & Deployment

### Prerequisites
- Docker and Docker Compose installed
- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- OpenRouter API Key from [OpenRouter](https://openrouter.ai/)

### Quick Setup

#### 1. Environment Configuration
Create `.env` file with your credentials:
```bash
# Required API tokens
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional LLM Settings (with defaults)
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=1000
MAX_CONTEXT_MESSAGES=20
```

#### 2. Docker Deployment
```bash
# Build and start the bot
make build

# Or run with existing image
make run

# View real-time logs
make logs

# Stop the bot
make stop

# Clean up completely
make clean
```

#### 3. Manual Docker Commands
```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f recipe-bot

# Stop
docker-compose down
```

### System Requirements
- **CPU**: 1 vCPU (any modern processor)
- **RAM**: 512MB (lightweight Python application)
- **Storage**: 1GB (Docker images + rotating logs)
- **Network**: Internet access for Telegram API and OpenRouter API

### Security Considerations
- **Never commit `.env` files** to version control
- **API keys** must be kept secure and rotated regularly
- **Environment variables** are the only configuration method
- **Container isolation** provides additional security

## How It Works

### Conversation Flow

#### 1. Initial Contact (`/start` command)
```
🌟✨ Welcome, culinary adventurer! I'm your funny recipe wizard who creates 
impossible-but-delicious combinations rooted in ancient fusion traditions!

Let's start our culinary detective work... What ingredients are currently 
lurking in your fridge or pantry? Tell me what you have available! 🥘🔍
```

#### 2. Information Gathering Phase
**Smart State Management**: Context-aware transitions based on information completeness

- **Ingredients**: "I have chicken and chocolate"
  - Bot: Acknowledges specific ingredients, shows enthusiasm
  - Extracts: `{'ingredients': 'chicken and chocolate'}`

- **Location Discovery**: "I'm from Italy" 
  - Bot: Cultural enthusiasm, local ingredient hints
  - Extracts: `{'location': 'Italy'}`
  - Activates: Italian ingredient database

- **Mood & Preferences**: "Feeling adventurous"
  - Bot: Adjusts recipe complexity and style
  - Extracts: `{'mood': 'adventurous'}`

- **Skill Level**: "Pretty confident in kitchen"
  - Bot: Determines recipe step complexity
  - Extracts: `{'skill_level': 'confident'}`

#### 3. Recipe Generation Phase
When sufficient information is gathered:

**Local Ingredient Intelligence**:
```python
user_ingredients = ["chicken", "chocolate"]
user_location = "Italy"
local_surprises = select_surprise_ingredients("Italy", user_ingredients)
# Returns: ["balsamic vinegar", "mascarpone"]
```

**Cultural Context Integration**:
```python
cultural_context = get_cultural_context("Italy")
# Returns: "Ancient Roman spice routes meet Renaissance creativity"
```

**Recipe Generation with Verification**:
1. **Generate**: Create recipe with local ingredients + cultural context
2. **Verify**: Check surprise score (>0.5) and humor presence
3. **Enhance**: Improve recipe if verification fails
4. **Retry**: Up to 3 attempts with regeneration hints

#### 4. Recipe Output Format
```markdown
# Sultani Chocolate Chicken (Ottoman-Inspired) 🏺✨

**The Story:** Ottoman sultans loved complex sweet-savory combinations...

**Ingredients:**
- 2 chicken thighs
- 50g dark chocolate (70%+)
- [Local surprise ingredients with cultural notes]

**Steps:**
1. [Cultural technique] - [Clear instruction with humor]
2. [3-7 steps based on skill level]

**Result:** [Sensory description with cultural metaphors]

**Plot twist time! 🎭 Want to shake things up even more?**
🌊 **Greek Islander Version**: [Regional adaptation with humor]
🌮 **Aztec Revenge**: [Historical timeline twist]
🍷 **French Rebellion**: [Cultural adaptation with wit]
```

### Data Flow Architecture

#### Memory Management
```python
# Per chat_id storage
conversations[chat_id] = [
    {"role": "system", "content": "System prompt..."},
    {"role": "user", "content": "I have chicken and chocolate"},
    {"role": "assistant", "content": "Recipe response..."},
    # Auto-trimmed to last 20 relevant messages
]
```

#### LLM Integration Flow
```python
1. build_dynamic_system_prompt(user_profile, local_ingredients)
2. Enhanced conversation history with context summary
3. OpenRouter API call via openai client
4. Response processing and logging
5. Conversation history update
```

#### State Persistence
- **In-Memory Only**: No database required
- **Session-Based**: State cleared on bot restart
- **Chat Isolation**: Each `chat_id` maintains independent state
- **Auto-Cleanup**: Old messages automatically trimmed

## Conversation Flow Schema & Logical Dependencies

### Complete Conversation State Machine

#### State Transition Flow
```
/start → waiting_for_ingredients → discovering_location → asking_mood → 
checking_skill_level → ready_for_recipe → recipe_generated → post_recipe_followup ⟲
```

#### Conversation States Mapping (`handlers.py`)
```python
conversation_states = {
    "waiting_for_ingredients": "discovering_location",
    "discovering_location": "asking_mood", 
    "asking_mood": "checking_skill_level",
    "checking_skill_level": "ready_for_recipe",
    "ready_for_recipe": "recipe_generated",
    "recipe_generated": "post_recipe_reaction",
    "post_recipe_reaction": "post_recipe_followup",
    "post_recipe_followup": "post_recipe_followup"  # Loop in followup
}
```

#### State-Specific Information Extraction Logic
Each state has targeted information extraction in `extract_user_info()`:

- **`waiting_for_ingredients`**: Extracts ingredient list, filters out greetings
- **`discovering_location`**: Uses regex patterns + fallback for location detection  
- **`asking_mood`**: Captures cooking preferences and adventurousness
- **`checking_skill_level`**: Determines recipe complexity level
- **`ready_for_recipe`**: Triggers recipe generation pipeline
- **`post_recipe_*`**: Maintains conversation context for follow-ups

### Function Call Dependency Map

#### Per-Message Processing Sequence (`handlers.py::message_handler`)
```
message_handler(message: Message) →
├── 1. STATE LOOKUP
│   └── current_state = user_states.get(chat_id, "waiting_for_ingredients")
│
├── 2. INFORMATION EXTRACTION
│   ├── extract_user_info(user_message, current_state) → dict
│   │   ├── Regex patterns for location (6 patterns)
│   │   ├── State-specific filtering logic
│   │   └── Validation and sanitization
│   └── user_profiles[chat_id].update(user_info)
│
├── 3. CONVERSATION HISTORY
│   └── add_to_conversation(chat_id, "user", user_message)
│       ├── conversations[chat_id].append({"role": "user", "content": message})
│       └── Auto-trim if > MAX_CONTEXT_MESSAGES (20)
│
├── 4. DECISION BRANCH: Recipe vs Conversation
│   └── should_generate_recipe(chat_id) → bool
│       ├── profile.get('ingredients') exists
│       └── current_state == "ready_for_recipe"
│
├── 5A. RECIPE GENERATION PATH
│   └── [See Recipe Generation Pipeline below]
│
└── 5B. CONVERSATION PATH
    └── [See Contextual Conversation Flow below]
```

### Recipe Generation Pipeline

#### Multi-Attempt Verification Loop (Max 3 Attempts)
```python
# handlers.py::message_handler() - Recipe Generation Branch
for attempt in range(1, max_attempts + 1):
    
    # STEP 1: Recipe Generation with Context
    current_recipe = await generate_recipe_with_local_ingredients(
        chat_id, user_profiles[chat_id], regeneration_hints
    ) →
    ├── user_ingredients = parse_ingredients(user_profile['ingredients'])
    ├── local_ingredients = select_surprise_ingredients(location, user_ingredients, count=2) →
    │   ├── normalize_location(user_location) → standardized_location
    │   ├── LOCAL_INGREDIENTS[standardized_location] → available_ingredients
    │   ├── Filter out user_ingredients (avoid duplicates)
    │   └── random.sample(surprise_candidates, 2)
    ├── cultural_context = get_cultural_context(location) → cultural_story
    ├── system_prompt = build_dynamic_system_prompt(
    │       user_profile, local_ingredients, for_recipe_generation=True
    │   ) →
    │   ├── Base personality + cultural context
    │   ├── User context (location, ingredients, mood, skill)
    │   ├── Recipe generation instructions
    │   └── Mandatory format + proactive variations
    └── OpenRouter API call with enhanced prompt

    # STEP 2: Surprise Verification
    verification_result = await verify_recipe_surprise(current_recipe, user_profile) →
    ├── Ingredient category analysis (meats, sweets, dairy, etc.)
    ├── Combination surprise scoring (cross-category combinations)
    ├── Humor detection (keywords, emojis, structure)
    └── {"surprise_score": float, "has_humor": bool, "analysis": dict}

    # STEP 3: Quality Check
    surprise_threshold = 0.5
    meets_criteria = (
        verification_result["surprise_score"] >= surprise_threshold AND 
        verification_result["has_humor"] == True
    )

    if meets_criteria:
        # SUCCESS: Use current recipe
        final_recipe = current_recipe
        user_states[chat_id] = "recipe_generated"
        break
    elif attempt == max_attempts:
        # FALLBACK: Enhance recipe instead of regenerating
        final_recipe = await enhance_recipe(current_recipe, verification_result)
        user_states[chat_id] = "recipe_generated"
    else:
        # RETRY: Get regeneration hints for next attempt
        regeneration_hints = get_regeneration_hints(verification_result, attempt)
        continue
```

### Contextual Conversation Flow

#### Smart State Transition Logic (`handlers.py::message_handler`)
```python
# Conversation Path - Context-Aware Response Generation
conversation_history = get_conversation_history(chat_id)
user_profile = user_profiles.get(chat_id, {})

# STEP 1: Context Summary Generation
context_summary = get_conversation_context_summary(conversation_history, user_profile) →
├── Extract known user info (ingredients, location, mood, skill_level)
├── Get recent user messages (last 2)
└── Format: "User has ingredients: X; User is from: Y; Recent: Z"

# STEP 2: Information Gap Analysis
missing_info = should_ask_for_missing_info(user_profile) →
├── Check required fields: ingredients, location, mood, skill_level
└── Return first missing field or None

# STEP 3: Enhanced Context for LLM
enhanced_conversation_history = conversation_history.copy()
enhanced_conversation_history.append({
    "role": "system", 
    "content": f"CONVERSATION CONTEXT: {context_summary}"
})
if missing_info:
    enhanced_conversation_history.append({
        "role": "system",
        "content": f"MISSING INFO: Still need {missing_info}. Work naturally into conversation."
    })

# STEP 4: Contextual Response Generation
response = await generate_contextual_response(
    chat_id, user_profile, enhanced_conversation_history, current_state
) →
├── system_prompt = build_dynamic_system_prompt(
│       user_profile, conversation_state=current_state, for_recipe_generation=False
│   ) →
│   ├── Base personality + current user context
│   ├── Conversational approach guidelines
│   ├── Context-aware conversation rules
│   └── Information gathering priority
├── messages = [{"role": "system", "content": system_prompt}] + conversation_history
└── OpenRouter API call with conversation context

# STEP 5: Smart State Transitions
if missing_info is None and current_state not in ["post_recipe_reaction", "post_recipe_followup"]:
    user_states[chat_id] = "ready_for_recipe"  # All info collected
elif current_state in ["post_recipe_reaction", "post_recipe_followup"]:
    user_states[chat_id] = "post_recipe_followup"  # Stay in post-recipe mode
elif user_info:
    # Continue gathering information - no state change
elif no new information extracted:
    # Stay in current state - no state change
```

### Data Flow Architecture

#### Memory Management per `chat_id`
```python
# Global state containers (handlers.py)
conversations: dict[int, list[dict]] = {}    # Message history per chat
user_states: dict[int, str] = {}             # Current state per chat  
user_profiles: dict[int, dict] = {}          # Extracted info per chat

# Data Flow Pattern per chat_id:
user_message → extract_user_info() → user_profiles[chat_id].update() →
add_to_conversation() → should_generate_recipe() → [BRANCH] →
generate_response() → add_to_conversation() → telegram.answer()
```

#### LLM Integration Data Flow
```python
# Recipe Generation Data Flow:
user_profile + user_location →
select_surprise_ingredients() + get_cultural_context() →
build_dynamic_system_prompt(for_recipe_generation=True) →
OpenRouter API Call →
verify_recipe_surprise() + enhance_recipe() →
final_recipe

# Conversation Data Flow:
user_profile + conversation_history + current_state →
get_conversation_context_summary() + should_ask_for_missing_info() →
build_dynamic_system_prompt(for_recipe_generation=False) →
OpenRouter API Call →
contextual_response
```

### System Prompt Dynamic Assembly

#### Context-Aware Prompt Building (`llm_client.py::build_dynamic_system_prompt`)
```python
def build_dynamic_system_prompt(
    user_profile: dict = None,
    local_ingredients: list = None, 
    conversation_state: str = None,
    for_recipe_generation: bool = False,
    surprise_focus: bool = False
) → str:

# STEP 1: Base Personality (Always included)
base_prompt = "Joyful, culturally-aware recipe wizard..." + personality_traits

# STEP 2: User Context Integration (If available)
if user_profile:
    if user_profile.get('location'):
        cultural_context = get_cultural_context(location)
        base_prompt += f"User location: {location} ({cultural_context})"
    if user_profile.get('ingredients'):
        base_prompt += f"User ingredients: {ingredients}"
    if local_ingredients:
        base_prompt += f"Local surprise ingredients: {local_ingredients}"
    if user_profile.get('mood'):
        base_prompt += f"User mood: {mood}"
    if user_profile.get('skill_level'):
        base_prompt += f"Cooking skill level: {skill_level}"

# STEP 3: Task-Specific Instructions
if for_recipe_generation:
    base_prompt += RECIPE_GENERATION_TASK + RECIPE_FORMAT + MANDATORY_VARIATIONS
else:
    base_prompt += CONVERSATIONAL_APPROACH + CONTEXT_AWARE_GUIDELINES + FLOW_EXAMPLES

return base_prompt
```

### Ingredient Intelligence System

#### Location-Based Surprise Selection (`ingredient_intelligence.py`)
```python
# Data Structure: 15 Regional Databases
LOCAL_INGREDIENTS = {
    "italy": ["parmigiano-reggiano", "balsamic vinegar", ...],
    "mexico": ["lime", "cilantro", "jalapeños", ...],
    # ... 13 more regions with 8 ingredients each
}

CULTURAL_CONTEXTS = {
    "italy": "Ancient Roman spice routes meet Renaissance creativity",
    "mexico": "Aztec traditions meet Spanish conquistador influences",
    # ... corresponding cultural contexts
}

# Selection Algorithm:
select_surprise_ingredients(user_location, user_ingredients, count=2) →
├── normalize_location(user_location) → standardized_location
│   ├── Direct lookup in LOCAL_INGREDIENTS
│   ├── Alias mapping (italian→italy, mexican→mexico, etc.)
│   └── Substring matching for variations
├── available_ingredients = LOCAL_INGREDIENTS[standardized_location]
├── Filter duplicates:
│   └── For each available_ingredient:
│       └── Check if already in user_ingredients (smart matching)
├── surprise_candidates = filtered_ingredients
└── random.sample(surprise_candidates, min(count, len(candidates)))
```

### Error Handling & Logging Schema

#### Operation Tracking Points
```python
# Recipe Generation Metrics:
RECIPE_ATTEMPT chat_id={chat_id} attempt={attempt}/{max_attempts}
VERIFY_START chat_id={chat_id} attempt={attempt} - checking surprise factor and humor  
RECIPE_VERIFIED chat_id={chat_id} surprise_score={score} has_humor={bool}
RECIPE_FAILED_VERIFICATION chat_id={chat_id} surprise_score={score} has_humor={bool}
MAX_ATTEMPTS_REACHED chat_id={chat_id} - enhancing recipe

# Conversation Flow Metrics:
SMART_TRANSITION chat_id={chat_id} -> ready_for_recipe (all info collected)
CONTEXT_CONTINUE chat_id={chat_id} state={state} - new info: {keys}
CONTEXT_STAY chat_id={chat_id} state={state} - no new information

# LLM API Metrics:
LLM_SUCCESS tokens={tokens} time={duration}s cost=${cost}
RECIPE_SUCCESS chat_id={chat_id} location={location} local_ingredients={count} tokens={tokens}
CONTEXT_SUCCESS chat_id={chat_id} state={state} tokens={tokens}
```

This schema provides complete visibility into every function call, data dependency, and logical flow in the bot's conversation system, enabling precise debugging and system understanding.

## Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | Bot API token from @BotFather |
| `OPENROUTER_API_KEY` | ✅ | - | OpenRouter API key |
| `OPENROUTER_MODEL` | ❌ | `anthropic/claude-3.5-haiku` | LLM model selection |
| `LLM_TEMPERATURE` | ❌ | `0.8` | Response creativity (0.0-2.0) |
| `LLM_MAX_TOKENS` | ❌ | `1000` | Max response length |
| `MAX_CONTEXT_MESSAGES` | ❌ | `20` | Conversation memory limit |

### Model Options
Popular OpenRouter models for recipe generation:
- `anthropic/claude-3.5-haiku` - Fast, cost-effective (recommended)
- `anthropic/claude-3.5-sonnet` - Higher quality, slower
- `openai/gpt-4o-mini` - Alternative option
- `meta-llama/llama-3.1-8b-instruct` - Budget option

### Cost Optimization
- **Default Model**: Claude 3.5 Haiku (~$0.25/1M input + $1.25/1M output tokens)
- **Token Limits**: 1000 max tokens per response
- **Context Management**: Auto-trim to 20 messages
- **Monitoring**: Automatic cost tracking in logs

## Development

### Project Structure Explained
```
llm-intense-01/
├── main.py                    # Entry point - 40 lines
├── config.py                  # Configuration - 25 lines  
├── handlers.py                # Message handling - 300 lines
├── llm_client.py             # LLM integration - 260 lines
├── ingredient_intelligence.py # Local ingredients - 120 lines
├── surprise_verification.py   # Quality assurance - 310 lines
├── docker-compose.yml        # Deployment config
├── Dockerfile                # Container definition
├── Makefile                  # Automation commands
├── pyproject.toml            # Dependencies (uv)
├── logs/                     # Persistent logs
└── doc/                      # Documentation
```

### Code Organization Philosophy

**Functional Layers**:
- **Entry Layer**: `main.py` - initialization only
- **Handler Layer**: `handlers.py` - message processing and state
- **Client Layer**: `llm_client.py` - external API integration
- **Intelligence Layer**: `ingredient_intelligence.py`, `surprise_verification.py` - business logic

**No Object-Oriented Programming**:
- Pure functions as building blocks
- Simple data structures (dict, list, str)
- Avoid classes and complex inheritance
- Pass data as parameters, avoid global state

### Adding New Features

#### Adding New Regions
1. **Update `ingredient_intelligence.py`**:
```python
LOCAL_INGREDIENTS["new_country"] = ["local", "ingredients", "list"]
CULTURAL_CONTEXTS["new_country"] = "Cultural description"
```

2. **Update location normalization**:
```python
location_mappings["new_country_alias"] = "new_country"
```

#### Extending Conversation States
1. **Update `handlers.py`**:
```python
conversation_states["new_state"] = "next_state"
```

2. **Add state-specific logic**:
```python
def extract_user_info(user_message: str, current_state: str) -> dict:
    if current_state == "new_state":
        # Add extraction logic
```

#### Modifying System Prompts
1. **Update `llm_client.py`**:
```python
def build_dynamic_system_prompt():
    # Modify base_prompt or add new sections
```

### Testing Strategy
**Simple Unit Testing**:
- Test core functions in isolation
- Mock external API calls
- Focus on business logic (ingredient selection, surprise scoring)
- Manual testing with real Telegram bot

## Monitoring & Logging

### Log Configuration
**Rotating File Handler**:
```python
RotatingFileHandler(
    "logs/recipe_bot.log",
    maxBytes=10*1024*1024,  # 10MB files
    backupCount=3           # Keep 3 backups
)
```

**Log Levels**:
- `INFO` - Normal operations, user interactions, LLM metrics
- `ERROR` - API failures, processing errors
- `DEBUG` - Detailed conversation flow (set LOG_LEVEL=DEBUG)

### Key Metrics Logged

#### LLM Operations
```
LLM_SUCCESS tokens=450 time=1.23s cost=$0.0012
RECIPE_SUCCESS chat_id=123 location=Italy local_ingredients=2 tokens=850 time=2.15s cost=$0.0025
CONTEXT_SUCCESS chat_id=123 state=asking_mood tokens=320 time=0.89s cost=$0.0008
```

#### Recipe Generation
```
RECIPE_ATTEMPT chat_id=123 attempt=1/3
VERIFY_START chat_id=123 attempt=1 - checking surprise factor and humor
RECIPE_VERIFIED chat_id=123 attempt=1 surprise_score=0.8 has_humor=true
RECIPE_FAILED_VERIFICATION chat_id=123 attempt=2 surprise_score=0.3 has_humor=false
MAX_ATTEMPTS_REACHED chat_id=123 - enhancing recipe
```

#### Conversation Flow
```
SMART_TRANSITION chat_id=123 -> ready_for_recipe (all info collected)
CONTEXT_CONTINUE chat_id=123 state=asking_mood - new info: ['mood']
CONTEXT_STAY chat_id=123 state=waiting_for_ingredients - no new information
```

### Log Access
```bash
# Real-time logs
make logs

# Direct file access
tail -f logs/recipe_bot.log

# Search logs
grep "ERROR" logs/recipe_bot.log
grep "chat_id=123" logs/recipe_bot.log

# Log rotation
ls -la logs/
# recipe_bot.log, recipe_bot.log.1, recipe_bot.log.2, recipe_bot.log.3
```

### Cost Monitoring
**Automatic Cost Estimation**:
- Token usage tracking per request
- Rough cost calculation for Claude 3.5 Haiku
- Daily/weekly cost aggregation via log analysis

**Cost Analysis Example**:
```bash
# Daily cost estimation
grep "$(date +%Y-%m-%d)" logs/recipe_bot.log | grep "cost=" | \
awk -F'cost=\\$' '{sum+=$2} END {print "Daily cost: $" sum}'
```

## Troubleshooting

### Common Issues

#### 1. Bot Not Responding
**Symptoms**: No response to messages, bot appears offline

**Diagnosis**:
```bash
make logs  # Check for errors
docker ps  # Verify container is running
```

**Solutions**:
- Check `.env` file for correct `TELEGRAM_BOT_TOKEN`
- Verify internet connectivity
- Restart bot: `make stop && make run`

#### 2. LLM API Errors
**Symptoms**: "Sorry, I'm having trouble generating recipes" messages

**Log Patterns**:
```
LLM_ERROR: 401 Unauthorized
RECIPE_ERROR chat_id=123: API key invalid
CONTEXT_ERROR chat_id=123 state=asking_mood: Rate limit exceeded
```

**Solutions**:
- Verify `OPENROUTER_API_KEY` in `.env`
- Check API key permissions and balance
- Reduce `LLM_TEMPERATURE` or `LLM_MAX_TOKENS` for rate limits

#### 3. Recipe Generation Failures
**Symptoms**: Recipes not meeting surprise criteria, repeated regeneration

**Log Patterns**:
```
RECIPE_FAILED_VERIFICATION chat_id=123 attempt=3 surprise_score=0.2 has_humor=false
MAX_ATTEMPTS_REACHED chat_id=123 - enhancing recipe
```

**Solutions**:
- Check ingredient intelligence data for user's location
- Verify surprise verification thresholds
- Review system prompts for surprise emphasis

#### 4. Memory Issues
**Symptoms**: Bot becomes unresponsive, memory usage grows

**Solutions**:
- Check `MAX_CONTEXT_MESSAGES` setting (default: 20)
- Monitor container memory: `docker stats`
- Restart bot regularly in production

#### 5. Location Not Recognized
**Symptoms**: No local ingredients suggested, generic responses

**Log Patterns**:
```
RECIPE_SUCCESS chat_id=123 location=unknown local_ingredients=0
```

**Solutions**:
- Check `ingredient_intelligence.py` for supported locations
- Add location mapping or aliases
- User can try alternative location names

### Debug Mode
**Enable Detailed Logging**:
```bash
# Add to .env
LOG_LEVEL=DEBUG

# Restart bot
make stop && make run
```

**Debug Output**:
- Complete conversation history
- Detailed state transitions
- LLM request/response details
- Ingredient selection process

### Performance Monitoring
**Container Resource Usage**:
```bash
docker stats recipe-bot
# Monitor CPU%, MEM USAGE, NET I/O
```

**Log File Management**:
```bash
# Check log size
ls -lh logs/

# Manual log rotation if needed
mv logs/recipe_bot.log logs/recipe_bot.log.backup
systemctl restart recipe-bot  # Or make stop && make run
```

### Backup and Recovery
**Configuration Backup**:
```bash
# Backup environment configuration
cp .env .env.backup

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

**Disaster Recovery**:
1. Restore `.env` configuration
2. Rebuild container: `make build`
3. Restore logs if needed
4. Verify bot functionality with test message

---

## Summary

The Funny Recipe Bot is a lightweight, efficient Telegram bot that demonstrates modern Python development practices with functional programming, containerized deployment, and intelligent LLM integration. Its modular architecture makes it easy to extend and maintain while providing an entertaining user experience through culturally-aware, surprising recipe generation.

**Key Strengths**:
- Simple architecture with clear separation of concerns
- Robust conversation management with state persistence
- Intelligent local ingredient integration
- Comprehensive surprise verification and enhancement
- Production-ready containerized deployment
- Detailed monitoring and logging

The bot successfully balances technical simplicity with functional sophistication, making it an excellent example of KISS principles applied to LLM-powered applications.
