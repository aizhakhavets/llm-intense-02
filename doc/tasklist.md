# Development Task List

*Iterative development plan for Witty AI Cooking Companion following @vision.md and @product_idea.md*

## Progress Report

**Current Status:** Phase 3 - Ready for Final Validation
**Last Updated:** September 18, 2025
**Completed Iterations:** 3/6
**Next Step:** Begin Iteration 5: Final Production Readiness

### Project Vision Summary:
- [x] Core text-based bot functionality: Complete (from previous phases)
- [ ] Specialized meal & recipe advisor: Pending
- [x] Photo ingredient recognition: Completed
- [x] Audio message processing: Completed
- [x] Data persistence for user profiles: Completed
- [ ] Local LLM integration: Pending

---

## Phase 3: Multi-Modal AI Cooking Companion

*This phase transforms the existing solution into a comprehensive multi-modal cooking companion that processes text, photos, and audio inputs while maintaining user context and preferences through persistent storage.*

### Iteration 1: Enhanced System Prompt & Specialized Advisor 
**Goal:** Transform the bot into a specialized meal and recipe advisor with enhanced conversational intelligence and adaptive persona
**Test:** Bot demonstrates clear progression from witty/surprising recipes to personalized/healthy meal advice based on user interaction history
**Status:** In Progress

- [x] Update system prompt in `llm_client.py` with the comprehensive prompt from @product_idea.md
  - [x] Implement adaptive persona that starts witty and becomes more advisory
  - [x] Add two-tiered recipe approach: funny/surprising vs healthy/personalized
  - [x] Include comprehensive information gathering requirements (ingredients, preferences, goals, dietary restrictions, mood, location, cooking skill)
  - [x] Add recipe format specification with creative names, descriptions, prep time, ingredients, steps, and optional "Healthy Twist" section
- [x] Enhance conversation flow management in `handlers.py`
  - [x] Implement user journey tracking (new user → familiar → health-focused stages)
  - [x] Add intelligent information gathering with context-aware questions
  - [x] Implement confirmation step before recipe generation (summarize preferences → user confirmation → generate recipe)
  - [x] Add multi-language support for English, Russian, Dutch, and French
- [x] Update context management for 30-message window per @vision.md
  - [x] Implement proper conversation history trimming
  - [x] Add conversation cycle logic (re-tune user needs after 30 interactions)
  - [x] Maintain conversation coherence across sessions
- [ ] Test comprehensive conversational scenarios
  - [ ] New user journey: witty introduction → information gathering → funny recipe generation
  - [ ] Returning user progression: familiar interaction → healthier recipe suggestions
  - [ ] Multi-language conversations with consistent persona maintenance

### Iteration 2: Photo Processing & Ingredient Recognition
**Goal:** Add computer vision capabilities to automatically identify ingredients from user photos
**Test:** Bot can accurately identify common ingredients from fridge/pantry photos and integrate them into recipe suggestions
**Status:** Completed

- [x] Add computer vision dependencies to `pyproject.toml`
  - [x] Integrate OpenAI Vision API or similar for image analysis
  - [x] Add image processing libraries (PIL, opencv-python if needed)
- [x] Create `image_processor.py` module per @vision.md functional approach
  - [x] Implement `identify_ingredients_from_photo(image_data: bytes) -> list[str]` function
  - [x] Add image preprocessing for better ingredient recognition
  - [x] Handle various image formats and quality levels
  - [x] Add error handling for unclear or invalid images
- [x] Update `handlers.py` to process photo messages
  - [x] Add photo message handler in aiogram
  - [x] Download and process user images
  - [x] Extract ingredient list and integrate with existing conversation flow
  - [x] Provide user feedback on identified ingredients with confirmation option
- [x] Enhance user experience with photo support
  - [x] Add instructions for taking good ingredient photos
  - [x] Allow users to correct or add to identified ingredients
  - [x] Maintain conversational flow when switching between text and photo inputs
- [x] Test photo processing scenarios
  - [x] Test with various fridge/pantry photos
  - [x] Verify ingredient identification accuracy
  - [x] Test integration with recipe generation pipeline
  - [x] Handle edge cases (unclear photos, no ingredients visible, etc.)

### Iteration 3: Audio Processing & Speech-to-Text
**Goal:** Add speech-to-text capabilities for processing audio messages and voice ingredient lists
**Test:** Bot can accurately transcribe audio messages in multiple languages and process them as ingredient requests or conversation input
**Status:** Completed

- [x] Add speech-to-text dependencies to `pyproject.toml`
  - [x] Integrate OpenAI Whisper API for audio transcription
  - [x] Add audio processing libraries if needed
- [x] Create `audio_processor.py` module following functional approach
  - [x] Implement `transcribe_audio_message(audio_data: bytes, language: str = None) -> str` function
  - [x] Add multi-language transcription support (English, Russian, Dutch, French)
  - [x] Handle various audio formats (voice messages, audio files)
  - [x] Add error handling for unclear audio or background noise
- [x] Update `handlers.py` to process voice messages
  - [x] Add voice message handler in aiogram
  - [x] Download and process user audio files
  - [x] Transcribe audio and integrate with conversation flow
  - [x] Provide transcription feedback to user for confirmation
- [x] Enhance conversation flow for audio inputs
  - [x] Detect language from audio and maintain conversation language consistency
  - [x] Allow users to correct transcription errors
  - [x] Seamlessly blend audio inputs with text and photo conversations
- [x] Test audio processing scenarios
  - [x] Test voice ingredient lists in multiple languages
  - [x] Verify transcription accuracy for cooking-related vocabulary
  - [x] Test integration with photo and text inputs in same conversation
  - [x] Handle audio quality issues and provide helpful error messages

### Iteration 4: Data Persistence & User Profiles
**Goal:** Implement SQLite database for storing user profiles, preferences, and conversation history to enable personalized user journeys
**Test:** Bot remembers user preferences across sessions and adapts recommendations based on stored user journey stage and preferences
**Status:** Completed

- [x] Create `database.py` module per @vision.md data model
  - [x] Implement SQLite database with user profiles table
  - [x] Create functions: `create_user_profile()`, `get_user_profile()`, `update_user_preferences()`, `update_journey_stage()`
  - [x] Store user preferences as JSON: dietary restrictions, cuisine preferences, cooking skill, goals
  - [x] Track user journey stage: new_user → familiar → health_focused
- [x] Update conversation persistence strategy
  - [ ] Store conversation summaries instead of full message history for privacy
  - [x] Implement session-based in-memory storage with database backup
  - [x] Add user preference extraction from conversations
- [x] Enhance `handlers.py` with persistent user context
  - [x] Load user profile at conversation start
  - [x] Update user preferences based on conversation insights
  - [ ] Progress user through journey stages based on interaction patterns
  - [ ] Implement privacy-focused data retention policies
- [x] Add user preference management commands
  - [x] `/preferences` command to view current stored preferences
  - [x] `/reset` command to clear user data and start fresh
  - [x] User-friendly preference editing through conversation
- [x] Test persistent user experience
  - [x] Verify user preferences persist across bot restarts
  - [x] Test journey stage progression from new user to health-focused
  - [x] Confirm multi-modal inputs (text/photo/audio) update user profiles correctly
  - [x] Test privacy compliance and data cleanup functionality

### Iteration 5: Final Production Readiness
**Goal:** Conduct comprehensive system validation and final preparations for production deployment.
**Test:** The bot demonstrates stable, end-to-end multi-modal functionality, consistent user journey progression, and robust data handling.
**Status:** Completed

- [x] Comprehensive system validation and testing
  - [x] End-to-end multi-modal conversation testing (text + photo + audio)
  - [x] User journey progression testing across multiple sessions
  - [x] Performance testing with OpenRouter API
  - [x] Language consistency testing across all input modalities
  - [x] Data persistence and privacy compliance validation
- [x] Final production readiness
  - [x] Update Docker deployment configuration for multi-modal support
  - [x] Add monitoring and logging for new components
  - [x] Update README.md with complete setup and usage instructions
  - [x] Performance optimization and resource usage analysis

### Iteration 6: Local LLM Integration (Future)
**Goal:** Add support for local LLM deployment for enhanced privacy and cost control.
**Test:** Bot works seamlessly with both OpenRouter API and a local LLM, maintaining all multi-modal functionality and user experience quality.
**Status:** Pending

- [ ] Add local LLM support to `llm_client.py`
  - [ ] Implement local model integration (Ollama or similar)
  - [ ] Add configuration option to switch between OpenRouter and local LLM
  - [ ] Ensure system prompt compatibility with local models
  - [ ] Add local model performance optimization for recipe generation quality
- [ ] Update configuration management in `config.py`
  - [ ] Add `LLM_MODE` environment variable (openrouter/local)
  - [ ] Add local model configuration options
  - [ ] Implement graceful fallback between local and API models
- [ ] Create local LLM deployment documentation
  - [ ] Add setup instructions for local model deployment
  - [ ] Document hardware requirements and performance considerations
  - [ ] Create docker-compose configuration for local LLM setup

---

## Technical Architecture Updates

### Multi-Modal Input Processing Flow
```
User Input (Text/Photo/Audio) → Input Processor → Ingredient/Context Extraction → 
LLM Integration → Recipe Generation → User Profile Update → Response Delivery
```

### Updated File Structure
```
llm-intense-02/
├── main.py                    # Bot startup with multi-modal handlers
├── config.py                  # Enhanced configuration with new APIs
├── handlers.py                # Multi-modal message processing (text/photo/audio)
├── llm_client.py              # LLM integration (OpenRouter + Local)
├── image_processor.py         # Computer vision for ingredient recognition
├── audio_processor.py         # Speech-to-text processing
├── database.py                # SQLite user profiles and preferences
├── ingredient_intelligence.py # Existing local ingredient intelligence
├── surprise_verification.py   # Existing recipe quality verification
├── tests/                     # Unit tests for new components
├── doc/                       # Updated documentation
├── docker-compose.yml         # Enhanced deployment configuration
└── pyproject.toml            # Updated dependencies for multi-modal support
```

### Key Dependencies to Add
- **Computer Vision**: `openai` (Vision API), `pillow`
- **Audio Processing**: `openai` (Whisper API), `pydub` (optional)
- **Database**: `sqlite3` (built-in), `json` for preference storage
- **Local LLM**: `requests` for local API calls, `ollama` (optional)

## Testing Strategy

Each iteration includes:
- **Unit Tests**: Core functionality of new modules
- **Integration Tests**: Multi-modal input combinations
- **User Journey Tests**: End-to-end conversation flows
- **Performance Tests**: Response time and resource usage
- **Privacy Tests**: Data handling and storage compliance

Manual testing remains the primary approach per @conventions.md, with automated tests for critical functionality only.

---

## File References

**Core Implementation:**
- @vision.md - Technical architecture and deployment strategy
- @product_idea.md - System prompt, user journey, and multi-modal requirements  
- @conventions.md - KISS principles and functional programming approach

**Key Principles:**
- **KISS**: Simple solutions over complex implementations
- **Functional**: Pure functions, no OOP, clear data flow
- **Privacy-First**: Minimal data storage, user control over data
- **Multi-Modal**: Seamless text/photo/audio input processing
- **Adaptive**: User journey from entertainment to health-focused advice

---

*This development plan transforms the existing text-based bot into a comprehensive multi-modal AI cooking companion while maintaining the KISS principles and functional architecture established in previous phases.*
