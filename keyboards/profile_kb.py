from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import datetime


def profile_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Актуальные мероприятия')
    kb.button(text='Мои мероприятия')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placehilder='Выберете действие')


def add_event(event_id, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Записаться', callback_data=f'add_event_{event_id}_{user_id}')
    kb.adjust(1)
    return kb.as_markup()


def delete_event(event_id, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Отказаться', callback_data=f'delete_event_{event_id}_{user_id}')
    kb.adjust(1)
    return kb.as_markup()
