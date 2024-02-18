from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Ежедневник'),
        KeyboardButton(
            text='Журнал'
        )
    ],
    [
        KeyboardButton(
            text='Мероприятия'
        ),
        KeyboardButton(
            text='Расписание'
        ),
    ],
    [
        KeyboardButton(
            text='Курсы'
        ),
    ],

], resize_keyboard=True, one_time_keyboard=True)
