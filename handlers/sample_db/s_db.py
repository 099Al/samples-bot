from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.models import T_A
from database.requests.req_a import ReqA
import logging

from handlers.sample_db.filter_s_db import Sample_DB_Filter
from handlers.sample_db.kb_s_db import kb_sample_db
from handlers.sample_db.state_s_db import Sample_DB_State

logger = logging.getLogger(__name__)

router_s_db = Router()


@router_s_db.message(Command(commands='s_db'))
async def step_db_1(message: Message, bot: Bot, state: FSMContext):
    try:
        await message.bot.send_message(message.from_user.id, "Выберете номер", reply_markup=await kb_sample_db(18, 3))
        await state.set_state(Sample_DB_State.state1)
    except Exception as e:
       logging.error(f"Error in step_db_1: {e}")

@router_s_db.callback_query(Sample_DB_State.state1)       #сюда попадаем только в определенном состояннии
async def step_db_2(callback: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        data = Sample_DB_Filter.unpack(callback.data)
        id = int(data.id)

        req_a = ReqA()
        res: T_A = await req_a.get_a(id)

        #res_d = await req_a.get_desc(id)
        if res:
            await callback.message.answer(f"Data from db: {res.id} {res.name} {res.r_desc.desc}")
        else:
            await callback.message.answer(f"Data not found")
    except Exception as e:
       logging.error(f"Error in step_db_1: {e}")

