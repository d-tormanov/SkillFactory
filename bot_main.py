import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from recipes_handler import register_handlers
from token_data import BOT_TOKEN
from commands_config import set_default_commands

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот рецептов. Используйте /category_search_random <число рецептов>, чтобы найти рецепты.")

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "/start - Начать работу\n"
        "/help - Показать доступные команды\n"
        "/category_search_random <число рецептов> - Найти случайные рецепты по категории\n"
        "/about - Информация о боте"
    )

@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer("Я бот, который поможет найти рецепты для различных блюд. Используйте команды для поиска рецептов!")

register_handlers(router)

dp.include_router(router)

async def main():
    await set_default_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
