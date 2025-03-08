from aiogram import Dispatcher

from handlers.sample2.sample2 import router_sample2
from handlers.sample_db.s_db import router_s_db


# Регистрация списка роутеров
def routers_list(dp: Dispatcher):
    dp.include_router(router_sample2)
    dp.include_router(router_s_db)