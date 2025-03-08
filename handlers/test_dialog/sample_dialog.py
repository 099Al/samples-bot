from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

tst_dialog_router = Router()

class MySG(StatesGroup):
    main = State()


async def next_element(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    index = dialog_manager.dialog_data.get("index", 0) + 1
    dialog_manager.dialog_data["index"] = index  #Передаем параметр при нажатии кнопки
    await dialog_manager.show()

async def prev_element(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    index = dialog_manager.dialog_data.get("index", 0) - 1
    dialog_manager.dialog_data["index"] = index  #Передаем параметр при нажатии кнопки
    await dialog_manager.show()

async def get_data(dialog_manager: DialogManager, **kwargs):
    index = dialog_manager.dialog_data.get("index", 0)  # читаем значение, переданного из dialog_data

    ln_dict = 3


    data = [
        {"has_prev": index > 0, "has_next": index < ln_dict - 1, "x": 1,
         "image": MediaAttachment(ContentType.PHOTO, path="media/img_1.png"),
         "p_1": 1},
        {"has_prev": index > 0, "has_next": index < ln_dict - 1, "x": 2,
         "image": MediaAttachment(ContentType.PHOTO, path="media/img_2.png"),
         "p_1": 2},
        {"has_prev": index > 0, "has_next": index < ln_dict - 1, "x": 3,
         "image": MediaAttachment(ContentType.PHOTO, file_id=MediaId(
             "AgACAgIAAxkBAAI0h2fEUPCaVa2D_BLBPgPGdcOyDrPjAALI8zEbdz4gSv6nPSscMPu4AQADAgADbQADNgQ")),
             "p_1": 3,
         "las_element": True},
    ]

    return data[index]       # вернуть надо только один словарь

tst_dialog = Dialog(
    Window(
DynamicMedia("image"),
        Const("Hello, unknown person"),  # just a constant text
        Format("x={x}"),
        Button(Const("Useless button"), id="nothing"),  # button Текст должен быть в Const
        Button(Const("🛒 Add to Cart"), id="add_to_cart"),
        Row(
                    Button(Const("⬅️ Previous"), id="prev", on_click=prev_element, when="has_prev"),         #when - прописываются условия для появления кнопки
                    Button(Format("{p_1}/3"), id="page_number"),
                    Button(Const("➡️ Next"), id="next", on_click=next_element, when="has_next"),
                    Button(Const("  "), id="no_next", when="las_element"),
                ),
        state=MySG.main,  # state is used to identify window between dialogs
        getter=get_data
))


@tst_dialog_router.message(Command("dialog"))
async def start(message: Message, dialog_manager: DialogManager):
    # Important: always set `mode=StartMode.RESET_STACK` you don't want to stack dialogs
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)     # Вызов диалога