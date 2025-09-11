# Development Task List

*Iterative development plan for Funny Recipe Bot following @vision.md and @conventions.md*

## Progress Report

**Current Status:** Iteration 7 Complete  
**Last Updated:** September 11, 2025  
**Completed Iterations:** 7/8  
**Next Step:** Docker Deployment & Final Polish  

### Completion Summary:
- [x] Iterations completed: 7
- [x] Core functionality working: Yes (Bot generates formatted recipes with enhanced personality)
- [x] Conversational flow improvements: Complete (Step-by-step questions with cultural intelligence)
- [x] Local ingredient intelligence: Complete (Automatic selection of 1-2 regional ingredients)  
- [x] Ready for user testing: Yes (Full conversational flow with cultural surprise strategy)
- [ ] Production deployment: Pending (Docker containerization)

---

## Iterative Development Plan

### Iteration 1: Setup & Basic Bot
**Goal:** Create minimal bot that responds to /start  
**Test:** Bot connects to Telegram and responds with hello message

- [x] Create project structure per @vision.md
  - [x] `main.py` - bot startup and polling
  - [x] `config.py` - environment variables
  - [x] `handlers.py` - message handlers
  - [x] `pyproject.toml` - uv dependencies
- [x] Setup environment configuration
  - [x] Basic config validation in `config.py`
- [x] Implement basic Telegram bot
  - [x] aiogram 3.x integration in `main.py`
  - [x] Simple /start handler in `handlers.py`
- [x] Test: Dependencies install and imports work correctly

### Iteration 2: LLM Integration
**Goal:** Connect to OpenRouter API for basic LLM responses  
**Test:** Bot can generate simple text responses using LLM

- [x] Create `llm_client.py` per @vision.md
  - [x] OpenRouter API integration via openai client
  - [x] Basic error handling for LLM failures
  - [x] Simple logging for token usage
- [x] Implement basic LLM conversation
  - [x] Any user message → LLM → response flow
  - [x] No system prompt yet (just echo-style responses)
- [x] Test: Send any message, get LLM-generated response

### Iteration 3: System Prompt & Recipe Context ✅
**Goal:** Add recipe-focused system prompt from @product_idea.md  
**Test:** Bot behaves like a recipe assistant, not generic chatbot  
**Completed:** September 10, 2025

- [x] Implement system prompt in `llm_client.py`
  - [x] Full system prompt from @product_idea.md
  - [x] Recipe-focused personality and rules
- [x] Update response handling
  - [x] System prompt prepended to all conversations
  - [x] Focus on ingredient gathering and recipe generation
- [x] Test: Ask about ingredients, get recipe-focused questions back

### Iteration 4: Conversation Memory ✅
**Goal:** Add in-memory conversation history per chat_id  
**Test:** Bot remembers previous messages in same conversation  
**Completed:** September 10, 2025

- [x] Implement conversation storage in `handlers.py`
  - [x] In-memory dict: `conversations[chat_id] = list[dict]`
  - [x] Store last 20 relevant messages per @vision.md
- [x] Update LLM integration
  - [x] Pass full conversation history to LLM
  - [x] Auto-trim old messages when limit exceeded
- [x] Test: Multi-message conversation with context memory

### Iteration 5: Recipe Generation ✅
**Goal:** Generate actual funny recipes with proper formatting  
**Test:** Bot creates complete recipes with names, ingredients, steps  
**Completed:** September 10, 2025

- [x] Enhance system prompt for recipe output
  - [x] Recipe format specification from @product_idea.md
  - [x] Funny names, surprising combinations, simple steps
  - [x] Markdown formatting with clear structure
- [x] Test comprehensive recipe scenarios
  - [x] Input: "I have chicken and chocolate"
  - [x] Output: Complete formatted funny recipe template
- [x] Test: Various ingredient combinations produce creative recipes

### Iteration 6: Enhanced Personality & Variations ✅
**Goal:** Add bot personality and proactive recipe variations  
**Test:** Bot offers multiple recipe options and cultural context  
**Completed:** September 10, 2025

- [x] Implement enhanced personality from @vision.md
  - [x] Emoji-rich responses with cultural context
  - [x] Historical/cultural recipe backgrounds
  - [x] Proactive variation suggestions
- [x] Add recipe complexity handling
  - [x] 3-7 steps based on user confidence
  - [x] Cooking skill level awareness
- [x] Test: Bot provides recipe variations and cultural stories

### Iteration 7: Intelligent Conversational Flow with Local Ingredient Intelligence ✅
**Goal:** Transform bot from asking all questions at once to step-by-step conversation with cultural discovery and automatic local ingredient selection for maximum surprise  
**Test:** Bot asks one question at a time, discovers user location nicely, and creates recipes combining user ingredients with 1-2 locally available surprise ingredients  
**Completed:** September 11, 2025

- [x] Implement step-by-step conversation state management
  - [x] Simple conversation states in `handlers.py`
  - [x] One question per message flow
  - [x] State tracking per chat_id using simple dict
- [x] Add cultural background discovery
  - [x] Polite optional location inquiry with humor
  - [x] Store user location/cultural info in conversation context
  - [x] Explain why asking (to create better surprises)
- [x] Implement local ingredient intelligence
  - [x] Create local ingredient database by region/country (`ingredient_intelligence.py`)
  - [x] Function to select 1-2 local surprise ingredients
  - [x] Avoid duplicating user's provided ingredients
- [x] Enhanced system prompt with local knowledge
  - [x] Inject selected local ingredients into LLM context
  - [x] Guide LLM to create recipes using user + local ingredients
  - [x] Maintain surprise factor while ensuring accessibility
- [x] Test comprehensive conversational scenarios
  - [x] Multi-step conversation with cultural discovery
  - [x] Recipe generation with local ingredient additions
  - [x] Various locations and ingredient combinations

### Iteration 8: Docker Deployment & Final Polish
**Goal:** Production-ready deployment with Docker  
**Test:** Bot runs in Docker container and handles real user load

- [ ] Create Docker configuration
  - [ ] `Dockerfile` per @vision.md
  - [ ] `docker-compose.yml` with logging volume
  - [ ] `Makefile` for deployment automation
- [ ] Add logging infrastructure
  - [ ] Rotating file handler
  - [ ] Console output for Docker logs
- [ ] Final testing & documentation
  - [ ] End-to-end user journey testing
  - [ ] Update README.md with deployment instructions
- [ ] Test: Full deployment in Docker with log monitoring

---

## File References

**Core Implementation:**
- @vision.md - Complete technical architecture and design
- @product_idea.md - System prompt and recipe requirements  
- @conventions.md - Coding standards and KISS principles

**Implementation Files** (to be created):
- `main.py` - Bot startup and polling
- `config.py` - Environment configuration  
- `handlers.py` - Telegram message processing
- `llm_client.py` - OpenRouter API integration
- `pyproject.toml` - Dependencies via uv

**Testing Strategy:**
Each iteration includes specific testable outcomes. Manual testing sufficient for MVP per @conventions.md - no complex test automation required initially. Iteration 7 introduces conversational flow testing requiring multi-step user interaction scenarios.

---

*This plan follows KISS principles: each iteration builds working functionality, allows immediate testing, and adds single clear improvement.*
