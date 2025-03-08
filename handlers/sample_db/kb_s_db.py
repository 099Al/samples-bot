from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.sample_db.filter_s_db import Sample_DB_Filter


async def kb_sample_db(ln, k_buttons):
    kb = InlineKeyboardBuilder()
    for i in range(ln):

        kb.add(
            InlineKeyboardButton(
                text=f"id: {str(i)}",
                callback_data=Sample_DB_Filter(id=i).pack()
            )
        )


    #настройка кнопок в строке
    k = k_buttons   # кнопки в строке
    a = ln // k
    b = ln % k
    c = (k,) * a + (b, 1) * b + (2, 1)
    kb.adjust(*c)

    # kb.adjust(2)  # 2 кнопки в строке

    return kb.as_markup()


