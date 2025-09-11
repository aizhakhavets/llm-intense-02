from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm_client import generate_response, generate_recipe_with_local_ingredients
from config import MAX_CONTEXT_MESSAGES
from ingredient_intelligence import select_surprise_ingredients, get_cultural_context, has_local_ingredients
import re

router = Router()

# In-memory conversation storage per chat_id
conversations: dict[int, list[dict]] = {}

# Conversation state management
conversation_states = {
    "waiting_for_ingredients": "discovering_location",
    "discovering_location": "asking_mood", 
    "asking_mood": "checking_skill_level",
    "checking_skill_level": "ready_for_recipe",
    "ready_for_recipe": "recipe_generated"
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
    
    if current_state == "waiting_for_ingredients":
        # Extract ingredients - simple approach
        info['ingredients'] = user_message.strip()
        
    elif current_state == "discovering_location":
        # Extract location/country information
        # Look for country names, "from", "in", etc.
        location_patterns = [
            r"from ([\w\s]+)",
            r"in ([\w\s]+)", 
            r"i'm ([\w\s]+)",
            r"live in ([\w\s]+)",
            r"based in ([\w\s]+)"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, message_lower)
            if match:
                info['location'] = match.group(1).strip()
                break
        
        # If no pattern match, assume entire message is location
        if 'location' not in info and len(user_message.strip()) < 30:
            info['location'] = user_message.strip()
            
    elif current_state == "asking_mood":
        info['mood'] = user_message.strip()
        
    elif current_state == "checking_skill_level":
        info['skill_level'] = user_message.strip()
        
    return info

def get_next_question(chat_id: int, current_state: str, user_message: str = "") -> str:
    """Generate next question based on conversation state with personality"""
    
    if current_state == "waiting_for_ingredients":
        return (
            "Fantastic ingredients! 🍽️✨ Now, here's where the magic happens... "
            "Mind sharing where you're from? (This helps me surprise you with the most "
            "unexpected local flavor combinations!) 🌍🎭"
        )
    
    elif current_state == "discovering_location":
        profile = user_profiles.get(chat_id, {})
        location = profile.get('location', '')
        
        if location and has_local_ingredients(location):
            context = get_cultural_context(location)
            return (
                f"Ah, {location}! 🌟 *rubs hands together mischievously* "
                f"I'm already plotting something inspired by {context}... "
                f"\n\nWhat's your cooking mood today? Feeling adventurous and ready to "
                f"shock your taste buds? Or more in a comfort-food-with-a-twist mood? 🎭🍳"
            )
        else:
            return (
                "Interesting! 🤔 I love a good culinary mystery... "
                "What's your cooking mood today? Feeling adventurous and ready to "
                "experiment, or more in a comfort-food zone? 🎭🍳"
            )
            
    elif current_state == "asking_mood":
        return (
            "Perfect vibe! 😄✨ One last thing before I work my culinary magic... "
            "Are you more of a kitchen ninja (confident with complex techniques) or "
            "a cautious experimenter (prefer simpler, foolproof methods)? 👨‍🍳🥷"
        )
        
    elif current_state == "checking_skill_level":
        return (
            "Excellent! 🎉 Now I have everything I need to create something "
            "absolutely surprising for you! Give me a moment to channel some "
            "culinary chaos... 🧙‍♂️✨"
        )
        
    return "Tell me more! 😊"

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
    """Handle user message with step-by-step conversation flow"""
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
        # Generate recipe with local ingredient intelligence
        response = await generate_recipe_with_local_ingredients(chat_id, user_profiles[chat_id])
        user_states[chat_id] = "recipe_generated"
    else:
        # Generate next question in the conversation flow
        response = get_next_question(chat_id, current_state, user_message)
        
        # Move to next state
        next_state = conversation_states.get(current_state, current_state)
        user_states[chat_id] = next_state
    
    # Add assistant response to conversation history
    add_to_conversation(chat_id, "assistant", response)
    
    await message.answer(response)
