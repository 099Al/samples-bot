from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Const, Format


router_dialog_tst_1 = Router()



class MySG(StatesGroup):
    window1 = State()
    window2 = State()


@router_dialog_tst_1.message(Command("dialog2"))
async def start(message: Message, dialog_manager: DialogManager):
    # Important: always set `mode=StartMode.RESET_STACK` you don't want to stack dialogs
    print(1, dialog_manager, datetime.now())
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)



async def window1_get_data(**kwargs):
    return {
        "something": "data from Window1 getter",
    }


async def window2_get_data(**kwargs):
    return {
        "something": "data from Window2 getter",
    }


async def dialog_get_data(**kwargs):
    return {
        "name": "Dialog Data",
    }


async def button1_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    """ Add data to `dialog_data` and switch to the next window of current dialog """
    manager.dialog_data['user_input'] = 'some data from user, stored in `dialog_data`'
    print(1, manager, datetime.now())
    await manager.next()


dialog_2 = Dialog(

    Window(
        Format("Window 1, {name}"),
        Format("W1: {something}"),
        Button(Const("Next window"), id="button1", on_click=button1_clicked),  #добавляется data в dialog_data
        state=MySG.window1,
        getter=window1_get_data,  # here we specify data getter for window1
    ),

    Window(
        Format("Window2, {name}"),
        Format("W2: {something}"),
        Format("User input: {dialog_data[user_input]}"),       # здесь эта data используется
        Back(text=Const("Back")),
        state=MySG.window2,
        getter=window2_get_data,  # here we specify data getter for window2
    ),

    getter=dialog_get_data  # here we specify data getter for dialog
)