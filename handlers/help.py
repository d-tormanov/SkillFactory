from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.logger_config import logger

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("help"))
async def help_command(message: Message):
    """Справка по командам."""
    logger.info(f"Команда /help вызвана пользователем {message.from_user.id}")
    await message.answer(
        "/start - Начать работу\n"
        "/help - Справка по командам\n"
        "/quiz - Начать викторину\n"
        "/about - О боте"
    )