import asyncio
import os

from aiogram_dialog import setup_dialogs
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Dispatcher, Bot
from aiogram.types import ChatMemberUpdated, ChatMember
from config import TOKEN_ID




import logging

from handlers.sample.start import start_router

logger = logging.getLogger(__name__)


async def on_user_joined(event: ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.status == ChatMember.Status.MEMBER:
        await bot.send_message(event.chat.id, "Добро пожаловать! Введите /start или /help для начала.")



async def start():

    bot = Bot(token=TOKEN_ID, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()


    # db = DataBase()
    # await db.create_db()

    dp.include_router(start_router)


    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(filename='logs/logs.log', level=logging.ERROR)
    asyncio.run(start())

