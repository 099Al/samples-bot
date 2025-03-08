from aiogram.filters.callback_data import CallbackData


class Sample_DB_Filter(CallbackData, prefix="s_db"):
    id: int

