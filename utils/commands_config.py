from aiogram import Bot
from aiogram.types import BotCommand

async def set_default_commands(bot: Bot):
    default_commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="help", description="Показать доступные команды"),
        BotCommand(command="quiz", description="Начать опрос"),
        BotCommand(command="about", description="Информация о боте")
    ]
    await bot.set_my_commands(default_commands)