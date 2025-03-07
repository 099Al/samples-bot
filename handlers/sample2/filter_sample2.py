from aiogram.filters.callback_data import CallbackData


class Sample2Filter(CallbackData, prefix="example_2"):
    action: str   # заполнять надо все параметры
    id: int


class Sample2Button1Filter(CallbackData, prefix="example_2_button"):
    action: str