from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from py7zr.callbacks import Callback

from handlers.sample2.filter_sample2 import Sample2Filter
from handlers.sample2.kb_sample2 import kb_sample2, kb_sample2_1_button
from handlers.sample2.state_sample2 import Sample2State

import logging
logger = logging.getLogger(__name__)

router_sample2 = Router()


@router_sample2.message(Command(commands='sample2'))
async def step_1(message: Message, bot: Bot, state: FSMContext):
    try:
        await state.set_state(Sample2State.state1)                 #переход в состояние
        await state.update_data({"value_1": "Текст_1"})
        await message.bot.send_message(message.from_user.id, "Введите текст")
    except Exception as e:
       logging.error(f"Error in step_1: {e}")

@router_sample2.message(Sample2State.state1)       #сюда попадаем только в определенном состояннии
async def step_2(message: Message, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        t1 = data.get("value_1")        #берем данные из словаря
        await state.set_state(Sample2State.state2)   # состояние 2

        l_buttons = [{"id": 1, "name": "Button_1"}, {"id": 2, "name": "Button_2"}, {"id": 3, "name": "Button_3"}]

        await message.bot.send_message(message.from_user.id, f"Message: {message.text} \nData value: {t1}", reply_markup=await kb_sample2(l_buttons, action='choose_button'))
    except Exception as e:
       logging.error(f"Error in step_2: {e}")

#@router_sample2.callback_query(Sample2State.state2)    #Варинт через состояние
#@router_sample2.callback_query(Sample2Filter.filter(F.action=='choose_button'),Sample2State.state2) # Варинт через фильтр и состояние
@router_sample2.callback_query(Sample2Filter.filter(F.action=='choose_button'))  #Нажимать на кнопку можно несколько раз, т.к. не зависит от состояния
async def step_3(callback: CallbackQuery, callback_data: Sample2Filter, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        t1 = data.get("value_1")        #берем данные из словаря
        filter_data = Sample2Filter.unpack(callback.data)


        await state.set_state(Sample2State.state3)   # состояние 3
        await callback.bot.send_message(
            callback.from_user.id,
            f"Data from callback: {filter_data.id} \nData value: {t1}\nData from callback_data: {str(callback_data.id)}",         #Вариант передачи данных
            reply_markup=await kb_sample2_1_button()
        )
    except Exception as e:
       logging.error(f"Error in step_3: {e}")


#Перехват сообщения или callback в любом состоянии
@router_sample2.callback_query(Sample2State.state3)    #сюда попадаем только в определенном состояннии
@router_sample2.callback_query(Sample2Filter.filter(F.action=='simple_button'),Sample2State.state3) # Варинт через фильтр и состояние
async def step_4(event: [CallbackQuery, Message], bot: Bot, state: FSMContext):
    try:

        if isinstance(event, CallbackQuery):
            await event.bot.send_message(event.from_user.id, "Вы нажали кнопку")
        elif isinstance(event, Message):
            await event.bot.send_message(event.from_user.id, event.text)
    except Exception as e:
       logging.error(f"Error in step_4: {e}")