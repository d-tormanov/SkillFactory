from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.logger_config import logger

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("start"))
async def start_command(message: Message):
    """Приветственное сообщение."""
    logger.info(f"Команда /start вызвана пользователем {message.from_user.id}")
    await message.answer(
        "Привет! Добро пожаловать в викторину Московского зоопарка!\n"
        "Мы поможем вам узнать ваше тотемное животное и расскажем о программе опеки.\n"
        "Нажмите /quiz, чтобы начать!"
    )
