from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.logger_config import logger

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("about"))
async def about_command(message: Message):
    """Информация о боте."""
    logger.info(f"Команда /about вызвана пользователем {message.from_user.id}")
    await message.answer(
        "Я бот Московского зоопарка, который поможет вам найти ваше тотемное животное и узнать, как вы можете поддержать наших обитателей."
    )