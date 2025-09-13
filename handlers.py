from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm_client import generate_contextual_response, generate_recipe_with_local_ingredients, generate_recipe_variations
from config import MAX_CONTEXT_MESSAGES
from ingredient_intelligence import select_surprise_ingredients, get_cultural_context, has_local_ingredients
from surprise_verification import verify_recipe_surprise, enhance_recipe, get_regeneration_hints
import re
import logging

router = Router()

# In-memory conversation storage per chat_id
conversations: dict[int, list[dict]] = {}

# Conversation state management
conversation_states = {
    "waiting_for_ingredients": "discovering_location",
    "discovering_location": "asking_mood", 
    "asking_mood": "checking_skill_level",
    "checking_skill_level": "ready_for_recipe",
    "ready_for_recipe": "recipe_generated",
    "recipe_generated": "post_recipe_reaction",
    "post_recipe_reaction": "post_recipe_followup",
    "post_recipe_followup": "post_recipe_followup"  # Loop in followup state
}

# Track user state and profile per chat_id
user_states: dict[int, str] = {}
user_profiles: dict[int, dict] = {}

def add_to_conversation(chat_id: int, role: str, content: str):
    """Add message with automatic trimming for token efficiency"""
    if chat_id not in conversations:
        conversations[chat_id] = []
    
    conversations[chat_id].append({"role": role, "content": content})
    
    # Keep last 12 messages (more generous with 10k tokens)
    if len(conversations[chat_id]) > 12:
        conversations[chat_id] = conversations[chat_id][-12:]

def get_conversation_history(chat_id: int) -> list[dict]:
    """Get recent conversation history (token-aware)"""
    history = conversations.get(chat_id, [])
    # Keep last 8 messages for better token efficiency in requests
    return history[-8:] if len(history) > 8 else history

def extract_user_info(user_message: str, current_state: str) -> dict:
    """Extract relevant user information from current message"""
    info = {}
    message_lower = user_message.lower()
    user_message_clean = user_message.strip()
    
    if current_state == "waiting_for_ingredients":
        # Extract ingredients - only if message seems to contain ingredients
        if len(user_message_clean) > 2 and not user_message_clean.lower() in ['hi', 'hello', 'hey', 'start', 'ok', 'yes', 'no']:
            info['ingredients'] = user_message_clean
        
    elif current_state == "discovering_location":
        # Extract location/country information
        location_patterns = [
            r"from ([\w\s]+)",
            r"in ([\w\s]+)", 
            r"i'm from ([\w\s]+)",
            r"live in ([\w\s]+)",
            r"based in ([\w\s]+)",
            r"i am in ([\w\s]+)"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, message_lower)
            if match:
                location = match.group(1).strip()
                # Validate location - should be more than just articles/pronouns
                if len(location) > 2 and location not in ['the', 'my', 'a', 'an', 'of']:
                    info['location'] = location
                break
        
        # If no pattern match, assume entire message is location if it looks valid
        if 'location' not in info and len(user_message_clean) > 2 and len(user_message_clean) < 50:
            # Filter out common non-location responses
            if user_message_clean.lower() not in ['hi', 'hello', 'hey', 'ok', 'yes', 'no', 'sure', 'thanks', 'thank you']:
                info['location'] = user_message_clean
            
    elif current_state == "asking_mood":
        # Only accept mood if it's not a generic response
        if len(user_message_clean) > 1 and user_message_clean.lower() not in ['hi', 'hello', 'hey', 'ok', 'yes', 'no']:
            info['mood'] = user_message_clean
        
    elif current_state == "checking_skill_level":
        # Only accept skill level if it seems reasonable
        if len(user_message_clean) > 1 and user_message_clean.lower() not in ['hi', 'hello', 'hey', 'ok', 'yes', 'no']:
            info['skill_level'] = user_message_clean
        
    return info

def get_conversation_context_summary(conversation_history: list[dict], user_profile: dict) -> str:
    """Generate context summary of what user has shared so far for better LLM understanding"""
    context_parts = []
    
    # Add what we know about the user
    if user_profile.get('ingredients'):
        context_parts.append(f"User has ingredients: {user_profile['ingredients']}")
    if user_profile.get('location'):
        context_parts.append(f"User is from: {user_profile['location']}")
    if user_profile.get('mood'):
        context_parts.append(f"User's cooking mood: {user_profile['mood']}")
    if user_profile.get('skill_level'):
        context_parts.append(f"User's skill level: {user_profile['skill_level']}")
    
    # Add recent conversation highlights (last 2 user messages if meaningful)
    recent_user_messages = [msg['content'] for msg in conversation_history[-4:] if msg['role'] == 'user']
    if recent_user_messages:
        context_parts.append(f"Recent user messages: {'; '.join(recent_user_messages[-2:])}")
    
    return "; ".join(context_parts) if context_parts else "New conversation starting"

def should_ask_for_missing_info(user_profile: dict) -> str:
    """Determine what critical information is still needed, if any"""
    if not user_profile.get('ingredients'):
        return 'ingredients'
    elif not user_profile.get('location'):
        return 'location'
    elif not user_profile.get('mood'):
        return 'mood'  
    elif not user_profile.get('skill_level'):
        return 'skill_level'
    return None

def is_information_sufficient(user_profile: dict, current_state: str) -> bool:
    """Check if we have sufficient information for current state to proceed"""
    if current_state == "waiting_for_ingredients":
        return bool(user_profile.get('ingredients'))
    elif current_state == "discovering_location":
        return bool(user_profile.get('location'))
    elif current_state == "asking_mood":
        return bool(user_profile.get('mood'))
    elif current_state == "checking_skill_level":
        return bool(user_profile.get('skill_level'))
    return True  # For other states, assume we can proceed

def should_generate_recipe(chat_id: int) -> bool:
    """Check if we have enough information to generate a surprising recipe"""
    profile = user_profiles.get(chat_id, {})
    current_state = user_states.get(chat_id, "waiting_for_ingredients")
    
    # Need at least ingredients and have gone through the flow
    required_info = ['ingredients']
    has_required = all(profile.get(key) for key in required_info)
    
    return has_required and current_state == "ready_for_recipe"

def detect_user_language(user_message: str) -> str:
    """Detect user language from message content (simple approach)"""
    message_lower = user_message.lower().strip()
    
    # Simple keyword-based detection for common languages
    language_indicators = {
        "russian": ["привет", "спасибо", "пожалуйста", "как", "что", "где", "когда", "почему"],
        "spanish": ["hola", "gracias", "por favor", "cómo", "qué", "dónde", "cuándo", "por qué"],
        "french": ["bonjour", "merci", "s'il vous plaît", "comment", "quoi", "où", "quand", "pourquoi"],
        "german": ["hallo", "danke", "bitte", "wie", "was", "wo", "wann", "warum"],
        "dutch": ["hallo", "dank je", "alsjeblieft", "hoe", "wat", "waar", "wanneer", "waarom"],
        "italian": ["ciao", "grazie", "prego", "come", "cosa", "dove", "quando", "perché"],
        "portuguese": ["olá", "obrigado", "por favor", "como", "que", "onde", "quando", "por que"]
    }
    
    # Check for language indicators
    for language, keywords in language_indicators.items():
        if any(keyword in message_lower for keyword in keywords):
            return language
    
    # Default to English if no clear indicators
    return "english"

def update_user_language(chat_id: int, user_message: str):
    """Update user's detected language in profile"""
    if chat_id not in user_profiles:
        user_profiles[chat_id] = {}
    
    # Only update if we don't have language yet or if message has clear indicators
    current_language = user_profiles[chat_id].get('language', 'english')
    detected_language = detect_user_language(user_message)
    
    if detected_language != current_language:
        user_profiles[chat_id]['language'] = detected_language
        logging.info(f"LANGUAGE_DETECTED chat_id={chat_id} language={detected_language}")

def is_variation_request(user_message: str, user_language: str = "english") -> bool:
    """Detect variation requests in multiple languages"""
    message_lower = user_message.lower().strip()
    
    # Multilingual variation keywords
    variation_keywords_by_language = {
        "english": ["variation", "variations", "different", "another", "more ideas", "twist", "twists", "other version", "alternative", "change it"],
        "russian": ["вариант", "варианты", "другой", "еще", "больше идей", "поворот", "изменить", "альтернатива"],
        "spanish": ["variación", "variaciones", "diferente", "otro", "más ideas", "giro", "cambiar", "alternativa"],
        "french": ["variation", "variations", "différent", "autre", "plus d'idées", "tournure", "changer", "alternative"],
        "german": ["variante", "varianten", "anders", "andere", "mehr ideen", "wendung", "ändern", "alternative"],
        "dutch": ["variatie", "variaties", "anders", "andere", "meer ideeën", "wending", "veranderen", "alternatief"],
        "italian": ["variazione", "variazioni", "diverso", "altro", "più idee", "svolta", "cambiare", "alternativa"],
        "portuguese": ["variação", "variações", "diferente", "outro", "mais ideias", "virada", "mudar", "alternativa"]
    }
    
    keywords = variation_keywords_by_language.get(user_language, variation_keywords_by_language["english"])
    return any(keyword in message_lower for keyword in keywords)

def has_recent_recipe(conversation_history: list[dict]) -> bool:
    """Check if there was a recent recipe in conversation"""
    # Look for recipe indicators in last few assistant messages
    recent_assistant_msgs = [msg['content'] for msg in conversation_history[-6:] 
                            if msg['role'] == 'assistant']
    
    recipe_indicators = ["**Ingredients:**", "**Steps:**", "**Result:**", "# "]
    
    return any(indicator in msg for msg in recent_assistant_msgs 
               for indicator in recipe_indicators)

def detect_conversation_ending(user_message: str, conversation_history: list[dict]) -> bool:
    """Detect if conversation is ending or going poorly"""
    message_lower = user_message.lower().strip()
    
    # Short/dismissive responses
    ending_indicators = [
        "ok", "thanks", "bye", "goodbye", "stop", "enough", "no more",
        "that's it", "done", "finished", "nothing else"
    ]
    
    # Very short messages
    if len(message_lower) <= 3 and message_lower in ending_indicators:
        return True
    
    # Check for conversation stagnation (repeated similar responses)
    if len(conversation_history) >= 4:
        recent_user_messages = [msg['content'].lower() 
                               for msg in conversation_history[-4:] 
                               if msg['role'] == 'user']
        if len(set(recent_user_messages)) <= 2:  # User repeating same responses
            return True
    
    return False

def generate_recovery_prompt(user_profile: dict) -> str:
    """Generate prompt to re-engage user with new questions"""
    missing_info = []
    
    if not user_profile.get('location'):
        missing_info.append("your location for local surprises")
    if not user_profile.get('mood'):
        missing_info.append("what cooking mood you're in")
    if not user_profile.get('skill_level'):
        missing_info.append("your cooking confidence level")
    
    if missing_info:
        return f"Let me ask about {missing_info[0]} to create something amazing for you!"
    else:
        return "What other ingredients are hiding in your kitchen? Or shall we explore a completely different cuisine?"

@router.message(Command("start"))
async def start_handler(message: Message):
    """Initialize conversation with multilingual welcome"""
    chat_id = message.chat.id
    
    # Reset conversation state
    user_states[chat_id] = "waiting_for_ingredients"
    user_profiles[chat_id] = {}
    
    welcome_message = (
        "🌟✨ Welcome, culinary adventurer! I'm your funny recipe wizard who creates "
        "impossible-but-delicious combinations rooted in ancient fusion traditions!\n\n"
        "Let's start our culinary detective work... What ingredients are currently "
        "lurking in your fridge or pantry? Tell me what you have available! 🥘🔍\n\n"
        "💬 I can speak your language - just write to me in any language!"
    )
    
    await message.answer(welcome_message)

@router.message()
async def message_handler(message: Message):
    """Handle user message with multilingual support, variation detection, and recovery logic"""
    chat_id = message.chat.id
    user_message = message.text
    
    # LANGUAGE DETECTION & UPDATE
    update_user_language(chat_id, user_message)
    
    # Get current state and profile
    current_state = user_states.get(chat_id, "waiting_for_ingredients")
    user_profile = user_profiles.get(chat_id, {})
    conversation_history = get_conversation_history(chat_id)
    user_language = user_profile.get('language', 'english')
    
    # Extract and store user information
    user_info = extract_user_info(user_message, current_state)
    if chat_id not in user_profiles:
        user_profiles[chat_id] = {}
    user_profiles[chat_id].update(user_info)
    
    # Add to conversation history
    add_to_conversation(chat_id, "user", user_message)
    
    # CHECK FOR VARIATION REQUEST (multilingual)
    if is_variation_request(user_message, user_language) and has_recent_recipe(conversation_history):
        logging.info(f"VARIATION_REQUEST chat_id={chat_id} language={user_language}")
        response = await generate_recipe_variations(chat_id, user_profiles[chat_id])
        user_states[chat_id] = "post_recipe_followup"
    
    # RECOVERY LOGIC - Check if conversation is ending
    elif detect_conversation_ending(user_message, conversation_history):
        recovery_prompt = generate_recovery_prompt(user_profiles[chat_id])
        response = f"Wait! Before we wrap up... 🤔✨ {recovery_prompt}"
        user_states[chat_id] = "discovering_location"
    
    # RECIPE GENERATION (simplified without complex verification for now)
    elif should_generate_recipe(chat_id):
        response = await generate_recipe_with_local_ingredients(
            chat_id, user_profiles[chat_id]
        )
        user_states[chat_id] = "recipe_generated"
    
    # NORMAL CONVERSATION
    else:
        response = await generate_contextual_response(
            chat_id, user_profile, conversation_history, current_state
        )
        
        # Smart state transitions
        missing_info = should_ask_for_missing_info(user_profile)
        if missing_info is None and current_state not in ["post_recipe_reaction", "post_recipe_followup"]:
            user_states[chat_id] = "ready_for_recipe"
        elif current_state in ["post_recipe_reaction", "post_recipe_followup"]:
            user_states[chat_id] = "post_recipe_followup"
    
    # Add response and send
    add_to_conversation(chat_id, "assistant", response)
    await message.answer(response)
