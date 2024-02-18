from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime


def date_kb():
    kb = InlineKeyboardBuilder()
    current_date = datetime.date.today()
    for i in range(30):
        current_date += datetime.timedelta(days=1)
        kb.button(text=f"{current_date.strftime('%d.%m')}", callback_data=f"{current_date.strftime('%d.%m.%y')}")
    kb.adjust(5)
    return kb.as_markup()

def time_kb():
    kb = InlineKeyboardBuilder()
    for x in range(0, 24, 1):
        kb.button(text=f"{x}:00",callback_data=f"{x}:00")
    kb.adjust(3)
    return kb.as_markup()

