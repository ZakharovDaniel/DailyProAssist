from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

scheduler_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Посмотреть по дате'),
        KeyboardButton(
            text='Расписание сегодня')
    ],[
        KeyboardButton(
            text='Расписание завтра'),
        KeyboardButton(
        text='В главное меню')

    ]
], resize_keyboard=True, one_time_keyboard=True)
