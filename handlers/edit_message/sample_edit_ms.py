from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from py7zr.callbacks import Callback

from handlers.edit_message.filter_edit_ms import FilterEditMsg
from handlers.edit_message.kb_edit_ms import kb_menu_1, kb_menu_2
from handlers.edit_message.state_edit_ms import SampleEditMsg
from handlers.sample2.filter_sample2 import Sample2Filter
from handlers.sample2.kb_sample2 import kb_sample2, kb_sample2_1_button
from handlers.sample2.state_sample2 import Sample2State

import logging
logger = logging.getLogger(__name__)

router_edit_msg = Router()


@router_edit_msg.message(Command(commands='test_edit'))
async def open_menu_1(message: Message, bot: Bot, state: FSMContext):
    try:
        await message.bot.send_message(message.from_user.id, "Menu1. Сообщение A", reply_markup=await kb_menu_1())
        await state.set_state(SampleEditMsg.menu_1)
    except Exception as e:
       logging.error(f"Error in open_menu_1: {e}")

@router_edit_msg.callback_query(SampleEditMsg.menu_1, FilterEditMsg.filter(F.action=='open_m2'))       #сюда попадаем только в определенном состояннии
async def open_menu_2(callback: CallbackQuery,  bot: Bot, state: FSMContext):
    try:
        await callback.bot.send_message(callback.from_user.id, "Menu2. Сообщение B", reply_markup=await kb_menu_2())
        await state.set_state(SampleEditMsg.menu_2)
        await state.update_data({"message_id_open_menu_2": callback.message.message_id})
    except Exception as e:
       logging.error(f"Error in open_menu_2: {e}")


@router_edit_msg.callback_query(SampleEditMsg.menu_2, FilterEditMsg.filter(F.action=='edit_msg_m1'))       #сюда попадаем только в определенном состояннии
async def menu_2_edit_m_1_msg(callback: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        prev_message_id = data.get("message_id_open_menu_2")
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=prev_message_id,
            text="Menu1. Сообщение A 2",
            reply_markup=await kb_menu_1()
        )
    except Exception as e:
       logging.error(f"Error in menu_2_edit_m_1_msg: {e}")

@router_edit_msg.callback_query(SampleEditMsg.menu_2, FilterEditMsg.filter(F.action=='del_inline_m1'))       #сюда попадаем только в определенном состояннии
async def menu_2_edit_m_1_inline(callback: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        prev_message_id = data.get("message_id_open_menu_2")
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=prev_message_id,
            text="Menu1. Сообщение A 3",
        )

    except Exception as e:
       logging.error(f"Error in menu_2_edit_m_1_inline: {e}")