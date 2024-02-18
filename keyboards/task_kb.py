
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

task_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Добавить задачу'),
        KeyboardButton(
            text='Посмотреть задачи')
    ],
    [
        KeyboardButton(
            text='В главное меню')
    ]
], resize_keyboard=True, one_time_keyboard=False)
def complate_task(id_task):
    kb = InlineKeyboardBuilder()
    print(id_task)
    kb.button(text='Выполнено', callback_data=f'btn_done_{id_task}')
    kb.adjust(1)
    return kb.as_markup()
