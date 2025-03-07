from aiogram import Dispatcher

from handlers.sample2.sample2 import router_sample2


# Регистрация списка роутеров
def routers_list(dp: Dispatcher):
    dp.include_router(router_sample2)