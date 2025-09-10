from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("🌟 Welcome! I'm your funny recipe bot! Send me ingredients and I'll create something amazing!")
