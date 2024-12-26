import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import start, quiz, help, about
from utils.commands_config import set_default_commands
from utils.logger_config import logger


# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация хендлеров
start.register_handlers(dp)
quiz.register_handlers(dp)
help.register_handlers(dp)
about.register_handlers(dp)


async def main():
    logger.info("Бот запущен!")
    await set_default_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())