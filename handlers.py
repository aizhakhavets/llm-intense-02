from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm_client import generate_response

router = Router()

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
    """Handle any user message with LLM response"""
    user_message = message.text
    
    # Generate LLM response
    llm_response = generate_response(user_message)
    
    await message.answer(llm_response)
