from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


"""
изменения в menu не сразу появляются
"""
async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запустить бота '
        ),
        BotCommand(
            command='sample2',
            description='Пример с callback'
        ),

    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())