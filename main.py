import asyncio
import os

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Dispatcher, Bot
from aiogram.types import ChatMemberUpdated, ChatMember
from config import TOKEN_ID




import logging

from handlers.common import routers_list
from handlers.sample.start import start_router
from handlers.sample_db.s_db import router_s_db

logger = logging.getLogger(__name__)


async def on_user_joined(event: ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.status == ChatMember.Status.MEMBER:
        await bot.send_message(event.chat.id, "Добро пожаловать! Введите /start или /help для начала.")



async def start():

    bot = Bot(token=TOKEN_ID, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # storage = MemoryStorage()
    # dp = Dispatcher(storage=storage)

    dp = Dispatcher()

    # db = DataBase()
    # await db.create_db()

    dp.include_router(start_router)
    routers_list(dp)           # Регистрация списка роутеров  вынесена в отдельный модуль

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(filename='logs/logs.log', level=logging.ERROR)
    asyncio.run(start())

