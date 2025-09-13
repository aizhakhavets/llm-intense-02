from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm_client import generate_response
from config import MAX_CONTEXT_MESSAGES
import logging

router = Router()

# In-memory conversation storage per chat_id
conversations: dict[int, list[dict]] = {}
interaction_counters: dict[int, int] = {}

def add_to_conversation(chat_id: int, role: str, content: str):
    """Add message to conversation history, keeping it to MAX_CONTEXT_MESSAGES"""
    if chat_id not in conversations:
        conversations[chat_id] = []
    
    conversations[chat_id].append({"role": role, "content": content})
    
    # Trim conversation to MAX_CONTEXT_MESSAGES
    if len(conversations[chat_id]) > MAX_CONTEXT_MESSAGES:
        conversations[chat_id] = conversations[chat_id][-MAX_CONTEXT_MESSAGES:]

def get_conversation_history(chat_id: int) -> list[dict]:
    """Returns the last MAX_CONTEXT_MESSAGES from the conversation"""
    return conversations.get(chat_id, [])

@router.message(Command("start"))
async def start_handler(message: Message):
    """Initialize conversation and clear any previous history."""
    chat_id = message.chat.id
    conversations[chat_id] = []  # Clear history
    interaction_counters[chat_id] = 0 # Reset counter
    
    welcome_message = (
        "🌟✨ Welcome, culinary adventurer! I'm your funny recipe wizard who creates "
        "impossible-but-delicious combinations rooted in ancient fusion traditions!\n\n"
        "Let's start our culinary detective work... What ingredients are currently "
        "lurking in your fridge or pantry? Tell me what you have available! 🥘🔍"
    )
    
    add_to_conversation(chat_id, "assistant", welcome_message)
    await message.answer(welcome_message)

@router.message()
async def message_handler(message: Message):
    """Handle all user messages by passing them to the LLM."""
    chat_id = message.chat.id
    user_message = message.text
    
    # Increment interaction counter
    interaction_counters[chat_id] = interaction_counters.get(chat_id, 0) + 1

    # Check if the interaction limit is reached
    if interaction_counters[chat_id] >= 30:
        # Reset for a new cycle
        interaction_counters[chat_id] = 0
        conversations[chat_id] = []

        retuning_message = (
            "🕰️✨ Wow, time flies when you're cooking with ideas! We've had quite a long chat. "
            "To keep my suggestions fresh and exciting, let's retune our culinary senses. \n\n"
            "What new ingredients or cravings have sparked your imagination recently? "
            "Tell me what you're working with now!"
        )
        add_to_conversation(chat_id, "assistant", retuning_message)
        await message.answer(retuning_message)
        return

    # Add user message to conversation
    add_to_conversation(chat_id, "user", user_message)
    
    # Get conversation history
    conversation_history = get_conversation_history(chat_id)
    
    # Generate response from LLM
    response = await generate_response(chat_id, conversation_history)
    
    # Add bot response to conversation and send to user
    add_to_conversation(chat_id, "assistant", response)
    await message.answer(response)
