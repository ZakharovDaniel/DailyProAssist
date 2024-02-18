from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

event_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Добавить мероприятие'),
        KeyboardButton(
            text='Посмотреть мероприятия')
    ],
    [
        KeyboardButton(
            text='В главное меню')
    ]
], resize_keyboard=True, one_time_keyboard=True)