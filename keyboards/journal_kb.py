from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

journal_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Добавить запись'),
        KeyboardButton(
            text='Посмотреть записи')
    ],
    [
        KeyboardButton(
            text='В главное меню')
    ]
], resize_keyboard=True, one_time_keyboard=True)
