from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm_client import generate_response
from config import MAX_CONTEXT_MESSAGES

router = Router()

# In-memory conversation storage per chat_id
conversations: dict[int, list[dict]] = {}

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

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🌟✨ Welcome, culinary adventurer! I'm your funny recipe wizard who creates "
        "impossible-but-delicious combinations!\n\n"
        "Tell me - what ingredients do you have available? Or what's been on your mind "
        "ingredient-wise? I'll help you create something surprisingly tasty! 🥘"
    )

@router.message()
async def message_handler(message: Message):
    """Handle user message with conversation memory"""
    chat_id = message.chat.id
    user_message = message.text
    
    # Add user message to conversation
    add_to_conversation(chat_id, "user", user_message)
    
    # Get full conversation history
    chat_history = get_conversation_history(chat_id)
    
    # Generate LLM response with full context
    llm_response = generate_response(chat_history)
    
    # Add assistant response to conversation
    add_to_conversation(chat_id, "assistant", llm_response)
    
    await message.answer(llm_response)
