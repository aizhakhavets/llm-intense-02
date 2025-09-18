import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from config import TELEGRAM_BOT_TOKEN
from handlers import router
from database import init_db

def setup_logging():
    """Setup logging with rotating file handler and console output for Docker"""
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                "logs/recipe_bot.log", 
                maxBytes=10*1024*1024,  # 10MB
                backupCount=3
            ),
            logging.StreamHandler()  # Console for Docker logs
        ]
    )

async def main():
    setup_logging()
    logging.info("Starting Funny Recipe Bot...")
    
    init_db()
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
