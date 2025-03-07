from aiogram import Dispatcher




# Регистрация списка роутеров
def admin_routers(dp: Dispatcher):
    dp.include_router(admin_router)