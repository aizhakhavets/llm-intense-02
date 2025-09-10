# Development Task List

*Iterative development plan for Funny Recipe Bot following @vision.md and @conventions.md*

## Progress Report

**Current Status:** Iteration 3 Complete  
**Last Updated:** September 10, 2025  
**Completed Iterations:** 3/7  
**Next Step:** Conversation Memory  

### Completion Summary:
- [x] Iterations completed: 3
- [x] Core functionality working: Yes (Bot behaves as recipe assistant)
- [ ] Ready for user testing: Partial (single-message recipe responses work)

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

### Iteration 4: Conversation Memory
**Goal:** Add in-memory conversation history per chat_id  
**Test:** Bot remembers previous messages in same conversation

- [ ] Implement conversation storage in `handlers.py`
  - [ ] In-memory dict: `conversations[chat_id] = list[dict]`
  - [ ] Store last 20 relevant messages per @vision.md
- [ ] Update LLM integration
  - [ ] Pass full conversation history to LLM
  - [ ] Auto-trim old messages when limit exceeded
- [ ] Test: Multi-message conversation with context memory

### Iteration 5: Recipe Generation
**Goal:** Generate actual funny recipes with proper formatting  
**Test:** Bot creates complete recipes with names, ingredients, steps

- [ ] Enhance system prompt for recipe output
  - [ ] Recipe format specification from @product_idea.md
  - [ ] Funny names, surprising combinations, simple steps
- [ ] Test comprehensive recipe scenarios
  - [ ] Input: "I have chicken and chocolate"
  - [ ] Output: Complete formatted funny recipe
- [ ] Test: Various ingredient combinations produce creative recipes

### Iteration 6: Enhanced Personality & Variations
**Goal:** Add bot personality and proactive recipe variations  
**Test:** Bot offers multiple recipe options and cultural context

- [ ] Implement enhanced personality from @vision.md
  - [ ] Emoji-rich responses with cultural context
  - [ ] Historical/cultural recipe backgrounds
  - [ ] Proactive variation suggestions
- [ ] Add recipe complexity handling
  - [ ] 3-7 steps based on user confidence
  - [ ] Cooking skill level awareness
- [ ] Test: Bot provides recipe variations and cultural stories

### Iteration 7: Docker Deployment & Final Polish
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
Each iteration includes specific testable outcomes. Manual testing sufficient for MVP per @conventions.md - no complex test automation required initially.

---

*This plan follows KISS principles: each iteration builds working functionality, allows immediate testing, and adds single clear improvement.*
