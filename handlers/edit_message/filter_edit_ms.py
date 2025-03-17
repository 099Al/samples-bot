from aiogram.filters.callback_data import CallbackData


class FilterEditMsg(CallbackData, prefix="menu"):
    action: str
