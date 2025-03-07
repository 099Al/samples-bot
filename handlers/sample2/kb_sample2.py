from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.sample2.filter_sample2 import Sample2Filter, Sample2Button1Filter


async def kb_sample2(l_buttons, action):
    kb = InlineKeyboardBuilder()
    for button in l_buttons:

        text = button['name']

        kb.add(
            InlineKeyboardButton(
                text=text,
                callback_data=Sample2Filter(
                    action=action, id=button['id']
                ).pack()
            )
        )


    #настройка кнопок в строке
    ln = len(l_buttons)
    k = 2   #  2 кнопки в строке
    a = ln // k
    b = ln % k
    c = (k,) * a + (b, 1) * b + (2, 1)
    kb.adjust(*c)

    # kb.adjust(2)  # 2 кнопки в строке

    return kb.as_markup()




async def kb_sample2_1_button():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text="Simple Button",
            callback_data=Sample2Button1Filter(
                action='simple_button'
            ).pack()
        )
    )

    return kb.as_markup()

