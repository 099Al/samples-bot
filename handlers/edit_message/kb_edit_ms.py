from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.edit_message.filter_edit_ms import FilterEditMsg
from handlers.edit_message.state_edit_ms import SampleEditMsg
from handlers.sample2.filter_sample2 import Sample2Filter, Sample2Button1Filter


async def kb_menu_1():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text="Open Menu 2",
            callback_data=FilterEditMsg(action="open_m2").pack()
        ),
        InlineKeyboardButton(
            text="Edit Menu 2",
            callback_data=FilterEditMsg(action="edit_m2").pack()
        )
    )
    kb.adjust(1)
    return kb.as_markup()



async def kb_menu_2():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text="Edit Message in Menu 1",
            callback_data=FilterEditMsg(action="edit_msg_m1").pack()
        ),
        InlineKeyboardButton(
            text="Delete Inline in Menu 1",
            callback_data=FilterEditMsg(action="del_inline_m1").pack()
        ),

        InlineKeyboardButton(
            text="Close Menu 2",
            callback_data=FilterEditMsg(action="del_inline_m2").pack()
        ),

        InlineKeyboardButton(
            text="Open Menu 1",
            callback_data=FilterEditMsg(action="open_m1").pack()
        )
    )
    kb.adjust(1)
    return kb.as_markup()

