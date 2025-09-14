# Development Task List

*Iterative development plan for Funny Recipe Bot following @vision.md and @conventions.md*

## Progress Report

**Current Status:** Phase 2 Refactoring Started
**Last Updated:** September 13, 2025
**Completed Iterations:** 12/12
**Next Step:** Rework solution to align with latest @vision.md and KISS principles

### Completion Summary:
- [x] Iterations completed: 10
- [x] Core functionality working: Yes (Bot generates formatted recipes with enhanced personality)
- [x] Conversational flow improvements: Complete (Step-by-step questions with cultural intelligence)
- [x] Local ingredient intelligence: Complete (Automatic selection of 1-2 regional ingredients)  
- [x] Ready for user testing: Yes (Full conversational flow with cultural surprise strategy)
- [x] Post-recipe conversation flow: Complete (Dynamic LLM responses, off-topic handling)
- [x] Surprise verification: Complete (Ensures recipes meet surprise criteria with regeneration loop)
- [x] Production deployment: Complete (Docker containerization with logging)
- [x] Language switching bug fix: Complete (Bidirectional English↔Russian detection fixed)
- [x] Conversation context fix: Complete (Enhanced context window and user response acknowledgment)
- [x] Language persistence fix: Complete (Strong language indicators prevent auto-switching)

---

## Phase 2: Refactoring for Simplicity and Alignment

*This phase reworks the existing solution to align with the updated @vision.md, focusing on KISS principles, simplification, and removing over-engineered components.*

### Iteration 13: Align Configuration & Context Management ✅
**Goal:** Synchronize the application with the 30-message context window from @vision.md
**Test:** The bot maintains a coherent conversation over 30 interactions
**Completed:** September 13, 2025

- [x] Update configuration to support 30 messages
  - [x] Set `MAX_CONTEXT_MESSAGES=30` in `config.py`
  - [ ] **ACTION REQUIRED:** Create `.env.example` manually and set `MAX_CONTEXT_MESSAGES=30`. The agent cannot create this file due to security restrictions.
- [x] Simplify context management in `handlers.py`
  - [x] Remove the token-saving logic (8 messages in request, 12 in storage) from Iteration 12
  - [x] Implement a simple list that stores the last 30 messages per chat_id
- [x] Test: Conversation history is accurately maintained up to the new 30-message limit

### Iteration 14: Unify Language Model & System Prompts ✅
**Goal:** Consolidate all LLM logic and prompts to strictly follow `vision.md`
**Test:** Bot uses the new system prompt correctly, including multi-language support for English, Russian, Dutch, and French
**Completed:** September 13, 2025

- [x] Update `llm_client.py` with the new unified system prompt
  - [x] Replace all previous system prompts with the single, definitive prompt from `vision.md`
- [x] Remove hardcoded language detection from `handlers.py`
  - [x] Rely entirely on the LLM's capability to detect and respond in the user's language as guided by the new prompt
- [x] Test: The bot successfully identifies and responds in the four specified languages based on user input

### Iteration 15: Implement Conversation Cycle Logic ✅
**Goal:** Implement the 30-interaction limit to re-tune user needs per @product_idea.md
**Test:** After 30 interactions, the bot prompts the user to refresh their preferences
**Completed:** September 13, 2025

- [x] Add an interaction counter in `handlers.py`
  - [x] Track the number of user/assistant message pairs for each chat_id
- [x] Implement the re-tuning mechanism
  - [x] When the counter reaches 30, trigger a message to ask the user for new preferences
  - [x] Reset the conversation context (partially or fully) to start a fresh exploration
- [x] Test: Bot initiates the re-tuning dialogue automatically after the 30th interaction

### Iteration 16: Implement Pre-Recipe User Confirmation ✅
**Goal:** Add a confirmation step where the bot summarizes collected user preferences before generating a recipe, as per the updated @vision.md.
**Test:** The bot summarizes the user's ingredients and preferences, asks for confirmation, and waits for approval before generating the recipe.
**Completed:** September 13, 2025

- [x] Update the system prompt in `llm_client.py` to reflect the new confirmation flow from @vision.md.
- [x] Modify `handlers.py` to introduce logic that can identify when it's time to ask for confirmation based on the conversation context.
- [x] Implement the confirmation handling logic:
  - [x] When the LLM generates a summary and confirmation request, the bot should handle the user's response.
  - [x] If the user confirms, the next LLM call should be to generate the recipe.
  - [x] If the user provides changes, the conversation should continue to refine preferences.
- [x] Test: A full conversation flow where the bot summarizes preferences, user confirms, and recipe is generated.

### Iteration 17: Conversational Flow & Language Consistency Fix ✅
**Goal:** Fix mixed-language responses and ensure the bot asks questions one-by-one to create a more natural, engaging conversation.
**Test:** Bot consistently responds in a single language and asks clarifying questions individually.
**Completed:** September 14, 2025

- [x] Enhance system prompt in `llm_client.py` for stricter language control.
  - [x] Add explicit rules to *never* mix languages in a single response.
  - [x] Reinforce that the bot must *always* reply in the language the user last used.
- [x] Update system prompt in `llm_client.py` to enforce a one-question-at-a-time conversational flow.
  - [x] Add instructions to break down information gathering into a friendly, step-by-step dialogue.
  - [x] Emphasize acknowledging the user's previous message before asking the next question.
- [x] Test:
  - [x] Switch to Russian and verify the bot responds *only* in Russian for the entire conversation.
  - [x] Start a new conversation and confirm the bot asks for ingredients, preferences, etc., in separate messages.

### Iteration 18: Contextual Summaries in Every Message ✅
**Goal:** Fix conversation context loss by including a summary of collected information in every bot message.
**Test:** The bot maintains context throughout the conversation by summarizing known facts, and asks for recipe confirmation when enough information is gathered.
**Completed:** September 14, 2025

- [x] Update system prompt in `llm_client.py` to enforce a new conversational flow.
  - [x] Add a rule: In every response, first acknowledge the user's message, then provide a bulleted list summarizing all gathered information (e.g., ingredients, preferences, mood).
  - [x] Add a rule: When the summary contains 4 or more items, ask the user for confirmation to generate the recipe or add more details.
  - [x] Reinforce the rule to generate a recipe only after explicit user confirmation.
- [x] Test:
  - [x] Start a new conversation and provide 2-3 pieces of information. Verify each bot response contains an updated summary.
  - [x] Provide a 4th piece of information. Verify the bot asks for confirmation to proceed.
  - [x] Confirm, and verify a recipe is generated.
  - [x] In a separate test, ask to add more details and verify the conversation continues.

### Iteration 19: Enhance System Prompt with Jokes, Mandatory Info, and Storytelling ✅
**Goal:** Update the system prompt to make the bot more engaging and gather necessary information consistently.
**Test:** The bot includes a joke in its messages, always asks for user location and cooking level, and uses storytelling in recipes.
**Completed:** September 14, 2025

- [x] Update system prompt in `llm_client.py` with new rules:
  - [x] Add rule: Include a joke in each message, playing with ingredients, mood, or context.
  - [x] Add rule: Make asking for user location and cooking level a mandatory step in information gathering.
  - [x] Add rule: Use historical, legendary, or fairy tale references in the final recipe description.
- [x] Test:
  - [x] Start a new conversation and verify the bot tells a joke.
  - [x] Verify the bot asks for location and cooking level before generating a recipe.
  - [x] Generate a recipe and check for storytelling elements in the description.

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

### Iteration 8: Post-Recipe Conversational Intelligence ✅
**Goal:** Transform bot from predefined responses to dynamic LLM-powered conversation flow after recipe generation  
**Test:** Bot engages naturally after recipe delivery, handles user reactions, offers follow-ups, and redirects off-topic questions with chef personality  
**Completed:** September 12, 2025

- [x] Replace predefined responses with LLM-generated contextual responses
  - [x] Remove hardcoded `get_next_question()` responses in `handlers.py`
  - [x] Implement `generate_contextual_response()` using LLM for dynamic answers
  - [x] Add conversation state-aware system prompts in `llm_client.py`
- [x] Add post-recipe conversation states and flow
  - [x] New states: `post_recipe_reaction`, `post_recipe_followup`
  - [x] State transitions for ongoing recipe conversations
  - [x] Context tracking for 20 messages as per requirements
- [x] Implement reaction discovery and follow-up offers
  - [x] Ask about user reaction to generated recipe (one question at a time)
  - [x] Offer new recipe ideas, ingredient additions, recipe adjustments
  - [x] Add light humor and jokes in responses when appropriate
- [x] Add off-topic question handling with chef personality
  - [x] Detect non-cooking related questions via system prompt
  - [x] Respond with "chef lens" worldview humor
  - [x] Redirect naturally back to cooking conversation
- [x] Test comprehensive post-recipe conversation scenarios
  - [x] User asks for recipe changes/improvements
  - [x] User requests completely new recipes
  - [x] User asks off-topic questions (weather, politics, etc.)
  - [x] User expresses positive/negative reactions to recipes

### Iteration 9: Surprise Verification & Humor Enhancement ✅
**Goal:** Add surprise verification layer to ensure recipes meet surprise criteria and include humor  
**Test:** Bot evaluates and enhances recipes for surprise factor and humor before delivery  
**Completed:** September 12, 2025

- [x] Create surprise verification system
  - [x] Implement `surprise_verification.py` module
  - [x] Define surprise scoring algorithm based on ingredient combinations
  - [x] Add humor verification to ensure recipes include jokes
- [x] Enhance recipe pipeline
  - [x] Add verification step between generation and delivery
  - [x] Implement automatic enhancement for low-surprise recipes
  - [x] Add joke injection for recipes lacking humor
  - [x] Add regeneration loop: if surprise verification fails, regenerate recipe (max 3 attempts)
- [x] Update recipe flow in handlers
  - [x] Modify `should_generate_recipe()` to include verification
  - [x] Update response pipeline with verification step
- [x] Test comprehensive verification scenarios
  - [x] Test with common vs. unusual ingredient combinations
  - [x] Verify humor enhancement works correctly
  - [x] Confirm recipe quality improves after verification

### Iteration 10: Docker Deployment & Final Polish ✅
**Goal:** Production-ready deployment with Docker  
**Test:** Bot runs in Docker container and handles real user load  
**Completed:** September 12, 2025

- [x] Create Docker configuration
  - [x] `Dockerfile` per @vision.md
  - [x] `docker-compose.yml` with logging volume
  - [x] `Makefile` for deployment automation
  - [x] `.env.example` configuration template
- [x] Add logging infrastructure
  - [x] Rotating file handler (10MB, 3 backups)
  - [x] Console output for Docker logs
  - [x] Enhanced main.py with setup_logging()
- [x] Final testing & documentation
  - [x] End-to-end user journey testing
  - [x] Update README.md with comprehensive deployment instructions
  - [x] Production-ready project status
- [x] Test: Full Docker deployment configuration verified

### Iteration 11: Context-Aware Conversational Intelligence ✅
**Goal:** Transform from rigid state-driven responses to context-aware conversational flow  
**Test:** Bot naturally reacts to user answers, asks follow-up questions based on responses, maintains conversational coherence  
**Completed:** September 12, 2025

- [x] Enhanced system prompt strategy in `llm_client.py`
  - [x] Replace rigid state-specific instructions with context-aware guidelines
  - [x] Add conversational flow examples and natural response patterns
  - [x] Focus on acknowledging user responses before asking follow-ups
- [x] Conversation context management in `handlers.py`
  - [x] Add `get_conversation_context_summary()` function for better LLM understanding  
  - [x] Add `should_ask_for_missing_info()` for intelligent information gathering
  - [x] Enhanced conversation history with context summaries
- [x] Smart state management
  - [x] Replace rigid state transitions with information-completeness based logic
  - [x] Context-aware state decisions rather than script-following
  - [x] Improved logging for conversation flow tracking
- [x] Test: Bot now acknowledges user answers and builds natural conversation flow

### Iteration 12: Token Starvation Fix & Enhanced Features ✅
**Goal:** Fix "running out of words" issue with token-efficient architecture and multilingual support  
**Test:** Bot generates full recipes without truncation and supports multiple languages with conversation recovery  
**Completed:** September 13, 2025

- [x] Fix token starvation by increasing LLM_MAX_TOKENS to 10000
  - [x] Update config.py with 10x token budget increase
  - [x] Ensure full recipe generation without truncation
- [x] Streamline system prompt following KISS principles
  - [x] Replace complex 500+ token prompt with lean 200-token version
  - [x] Generate recipes with 1 initial variation, offer more on-demand
  - [x] Add dedicated prompts for recipe generation, conversation, and variations
- [x] Add multilingual support with language detection
  - [x] Detect user language from message keywords (Russian, Spanish, French, German, Dutch, Italian, Portuguese)
  - [x] Respond in detected language for all content (recipes, jokes, cultural references)
  - [x] Store language preference in user profile
- [x] Add conversation recovery logic to re-engage users
  - [x] Detect conversation ending patterns (short responses, dismissive language)
  - [x] Generate recovery prompts asking about missing information
  - [x] Reset conversation state to re-gather user preferences
- [x] Implement on-demand recipe variations
  - [x] Add variation request detection in multiple languages
  - [x] Create separate LLM call for generating 2-3 recipe variations
  - [x] Maintain conversation context for variation requests
- [x] Optimize context management for token efficiency
  - [x] Reduce conversation history from 20 to 8 messages in requests
  - [x] Keep 12 messages in storage for context preservation
  - [x] Remove complex context summaries that consumed tokens
- [x] Simplify recipe generation pipeline
  - [x] Remove complex surprise verification loop (temporary)
  - [x] Focus on core functionality with lean prompt structure
  - [x] Maintain local ingredient intelligence integration
- [x] Test comprehensive functionality
  - [x] Configuration test: LLM_MAX_TOKENS = 10000 ✅
  - [x] Import test: All new functions working ✅
  - [x] Language detection test: Spanish detection working ✅
  - [x] Variation detection test: Request recognition working ✅

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
