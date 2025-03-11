import logging

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import Select, Group, Button, Back, Cancel
from aiogram_dialog.widgets.text import Format, Const

from database.requests.req_a import ReqA

dialog3_router = Router()

sample_l_items = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}, {"id": 3, "name": "C"}, {"id": 4, "name": "D"},
                       {"id": 5, "name": "E"}, {"id": 6, "name": "F"}, {"id": 7, "name": "G"}, {"id": 8, "name": "H"},
                       {"id": 9, "name": "I"}, {"id": 10, "name": "J"}, {"id": 11, "name": "K"}, {"id": 12, "name": "L"},
                       {"id": 13, "name": "M"}]



sample_l_elements = [{"id":1, "val": [100,200,300]}, {"id":2, "val": [400,500,600]}, {"id":3, "val": [700,800,900]}, {"id":4, "val": [1000,1100,1200]}
              ,{"id":5, "val": [1300,1400,1500]}, {"id":6, "val": [1600,1700,1800]}, {"id":7, "val": [1900,2000,2100]}, {"id":8, "val": [2200,2300,2400]}]

def _get_elem_by_id(id) -> list[int]:
    for elem in sample_l_elements:
        if elem["id"] == id:
            return elem["val"]


#-------------Диалог---------------------------

class DialogState_A(StatesGroup):
    categories = State()
    elements = State()

class DialogState_B(StatesGroup):
    window1 = State()


@dialog3_router.message(Command('dialog3'))
async def d3_start_dialog_a(event, bot: Bot, state: FSMContext, dialog_manager: DialogManager):
    try:
        #l_items = sample_l_items
        req = ReqA()
        l_items = await req.get_all()

        await dialog_manager.start(DialogState_A.categories, data={"l_categories": l_items}, mode=StartMode.RESET_STACK)
    except Exception as e:
       logging.error(f"Error in d3_start_dialog: {e}")

#async def getter_pass_start_data_to_dialog(dialog_manager: DialogManager, data, **kwargs):



async def click_category(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["elements"] = _get_elem_by_id(int(item_id))
    await dialog_manager.next()

window_a_1 = Window(
        Const("Выберите категорию"),
            Group(
            Select(
                Format("{item.name}"),    # Format("{item[name]}")  - для словарей
                id="category",
                # item_id_getter=lambda item: item["id"],              # для словарей
                item_id_getter=lambda x: x.id,
                #items=lambda data: data["l_categories"],   # либо
                items='l_categories',
                on_click=click_category,
                ),
                width=int(len(sample_l_items)/3)     # из data получить данные здесь нельзя
            ),

    state=DialogState_A.categories
    )

async def getter_window_2(dialog_manager: DialogManager, **kwargs):
    return {"elements": dialog_manager.dialog_data.get("elements", [])}


async def click_element(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["chosen_element"] = item_id
    await callback.answer(f"Selected element: {item_id}")


#on_click ожидает функцию с определеными аргументами
async def open_dialod_b(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    chosen_element = dialog_manager.dialog_data.get("chosen_element")
    await dialog_manager.start(DialogState_B.window1, data={"chosen_element": chosen_element})


window_a_2 = Window(
        Const("Выберите элемент"),
            Group(
            Select(
                Format("{item}"),     # Format("{item[name]}")  - для словарей
                id="element",
                # item_id_getter=lambda item: item["id"],              # для словарей
                item_id_getter=lambda x: x,
                items=lambda data: data["elements"],   # либо
                on_click=click_element
                #items='data[elements]'
                ),
                width=2     # из data получить данные здесь нельзя
            ),
        Button(Const("Open Dialog B"), id="next", on_click=open_dialod_b),
        Back(text=Const("Back")),
    getter=getter_window_2,
    state=DialogState_A.elements
    )


async def getter_pass_start_data_to_dialog(dialog_manager: DialogManager, **kwargs):
    start_data = dialog_manager.current_context().start_data
    l_categories = start_data.get("l_categories", [])
    return {"l_categories": l_categories}

dialog_a = Dialog(
    window_a_1,
    window_a_2,
    getter=getter_pass_start_data_to_dialog
)



async def getter_window_b(dialog_manager: DialogManager, **kwargs):
    chosen_element = dialog_manager.start_data.get("chosen_element", 0)
    return {"chosen_element": chosen_element}

async def close_dialog_b(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.done()

async def open_dialod_a(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    #await dialog_manager.start(DialogState_A.categories)  #так не работает. Можно переходить только назад

dialog_b = Dialog(
    Window(
        Format("Dialog B"),
        Format("Chosen element: {chosen_element}"),
        Button(Const("Close v1"), id="next", on_click=close_dialog_b),
        Cancel(text=Const("Close")),
        Button(Const("window_a_1"), id="w_a_1", on_click=open_dialod_a),

        getter=getter_window_b,
        state=DialogState_B.window1
    )
)