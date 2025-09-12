from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm_client import generate_contextual_response, generate_recipe_with_local_ingredients
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
    """Add message to conversation history and auto-trim if needed"""
    if chat_id not in conversations:
        conversations[chat_id] = []
    
    # Add new message
    conversations[chat_id].append({"role": role, "content": content})
    
    # Auto-trim if exceeded limit (keep last MAX_CONTEXT_MESSAGES)
    if len(conversations[chat_id]) > MAX_CONTEXT_MESSAGES:
        conversations[chat_id] = conversations[chat_id][-MAX_CONTEXT_MESSAGES:]

def get_conversation_history(chat_id: int) -> list[dict]:
    """Get conversation history for chat_id"""
    return conversations.get(chat_id, [])

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

@router.message(Command("start"))
async def start_handler(message: Message):
    """Initialize conversation with welcome message and first question"""
    chat_id = message.chat.id
    
    # Reset conversation state for new session
    user_states[chat_id] = "waiting_for_ingredients"
    user_profiles[chat_id] = {}
    
    welcome_message = (
        "🌟✨ Welcome, culinary adventurer! I'm your funny recipe wizard who creates "
        "impossible-but-delicious combinations rooted in ancient fusion traditions!\n\n"
        "Let's start our culinary detective work... What ingredients are currently "
        "lurking in your fridge or pantry? Tell me what you have available! 🥘🔍"
    )
    
    await message.answer(welcome_message)

@router.message()
async def message_handler(message: Message):
    """Handle user message with LLM-powered contextual conversation flow"""
    chat_id = message.chat.id
    user_message = message.text
    
    # Get current conversation state (default to waiting for ingredients)
    current_state = user_states.get(chat_id, "waiting_for_ingredients")
    
    # Extract and store user information based on current state
    user_info = extract_user_info(user_message, current_state)
    if chat_id not in user_profiles:
        user_profiles[chat_id] = {}
    user_profiles[chat_id].update(user_info)
    
    # Add user message to conversation history
    add_to_conversation(chat_id, "user", user_message)
    
    # Check if ready for recipe generation
    if should_generate_recipe(chat_id):
        # Generate and verify recipe with regeneration loop (max 3 attempts)
        max_attempts = 3
        attempt = 1
        final_recipe = None
        verification_result = None
        
        while attempt <= max_attempts:
            logging.info(f"RECIPE_ATTEMPT chat_id={chat_id} attempt={attempt}/{max_attempts}")
            
            # Generate recipe with local ingredient intelligence
            # Use regeneration hints for attempts after the first one
            hints = None
            if attempt > 1 and verification_result:
                # Get hints from previous verification result
                hints = get_regeneration_hints(verification_result, attempt)
            
            current_recipe = await generate_recipe_with_local_ingredients(chat_id, user_profiles[chat_id], hints)
            
            # Verify recipe for surprise factor and humor
            logging.info(f"VERIFY_START chat_id={chat_id} attempt={attempt} - checking surprise factor and humor")
            verification_result = await verify_recipe_surprise(current_recipe, user_profiles[chat_id])
            
            # Check if recipe meets surprise criteria
            surprise_threshold = 0.5  # Minimum surprise score required
            meets_surprise_criteria = (
                verification_result["surprise_score"] >= surprise_threshold and 
                verification_result["has_humor"]
            )
            
            if meets_surprise_criteria:
                # Recipe passed verification - use it
                logging.info(f"RECIPE_VERIFIED chat_id={chat_id} attempt={attempt} surprise_score={verification_result['surprise_score']} has_humor={verification_result['has_humor']}")
                final_recipe = current_recipe
                break
            else:
                # Recipe failed verification
                logging.info(f"RECIPE_FAILED_VERIFICATION chat_id={chat_id} attempt={attempt} surprise_score={verification_result['surprise_score']} has_humor={verification_result['has_humor']}")
                
                if attempt == max_attempts:
                    # Last attempt - enhance the recipe instead of regenerating
                    logging.info(f"MAX_ATTEMPTS_REACHED chat_id={chat_id} - enhancing recipe")
                    final_recipe = await enhance_recipe(current_recipe, verification_result)
                else:
                    # Try regenerating with more emphasis on surprise
                    logging.info(f"REGENERATING_RECIPE chat_id={chat_id} attempt={attempt} - trying again")
                    attempt += 1
                    continue
            
            attempt += 1
        
        response = final_recipe if final_recipe else "Sorry, I'm having trouble creating a surprising enough recipe. Please try again! 😅✨"
        user_states[chat_id] = "recipe_generated"
    else:
        # Generate contextual response using conversation-aware approach
        conversation_history = get_conversation_history(chat_id)
        user_profile = user_profiles.get(chat_id, {})
        
        # Create context summary for better LLM understanding
        context_summary = get_conversation_context_summary(conversation_history, user_profile)
        missing_info = should_ask_for_missing_info(user_profile)
        
        # Add context summary to the conversation for LLM
        enhanced_conversation_history = conversation_history.copy()
        if context_summary != "New conversation starting":
            enhanced_conversation_history.append({
                "role": "system", 
                "content": f"CONVERSATION CONTEXT: {context_summary}"
            })
        
        # Add guidance about missing information if needed
        if missing_info:
            enhanced_conversation_history.append({
                "role": "system",
                "content": f"MISSING INFO: Still need to learn about user's {missing_info}. Work this into the conversation naturally."
            })
        
        response = await generate_contextual_response(
            chat_id,
            user_profile,
            enhanced_conversation_history,
            current_state
        )
        
        # Smart state transitions based on information completeness rather than rigid rules
        if missing_info is None and current_state not in ["post_recipe_reaction", "post_recipe_followup"]:
            # We have all info needed - transition toward recipe generation
            user_states[chat_id] = "ready_for_recipe"
            logging.info(f"SMART_TRANSITION chat_id={chat_id} -> ready_for_recipe (all info collected)")
        elif current_state in ["post_recipe_reaction", "post_recipe_followup"]:
            # Stay in post-recipe conversation mode
            user_states[chat_id] = "post_recipe_followup"
        elif user_info:
            # User provided some new information, keep conversing
            logging.info(f"CONTEXT_CONTINUE chat_id={chat_id} state={current_state} - new info: {list(user_info.keys())}")
        else:
            # No new info extracted, stay in current state
            logging.info(f"CONTEXT_STAY chat_id={chat_id} state={current_state} - no new information")
    
    # Add assistant response to conversation history
    add_to_conversation(chat_id, "assistant", response)
    
    await message.answer(response)
