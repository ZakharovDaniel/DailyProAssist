import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.database import Database


def curses_kb():
    db = Database(os.getenv('DATABASE_NAME'))
    courses = db.db_select_column('courses')
    kb = InlineKeyboardBuilder()
    for course in courses:
        kb.button(text=f'{course[1]}', callback_data=f'{course[0]}')
    kb.adjust(1)
    return kb.as_markup()


def lesson_kb(course_id):
    db = Database(os.getenv('DATABASE_NAME'))
    lessons = db.db_select_column_lesson(course_id)
    kb = InlineKeyboardBuilder()
    for lesson in lessons:
        kb.button(text=f'{lesson[2]}', callback_data=f'{lesson[0]}')
    kb.adjust(1)
    return kb.as_markup()


def lesson_kb(course_id):
    db = Database(os.getenv('DATABASE_NAME'))
    lessons = db.db_select_column_lesson(course_id)
    kb = InlineKeyboardBuilder()
    for lesson in lessons:
        kb.button(text=f'{lesson[1]}', callback_data=f'{lesson[0]}')
    kb.adjust(1)
    return kb.as_markup()


def paragraph_kb(lesson_id):
    db = Database(os.getenv('DATABASE_NAME'))
    paragraphs = db.db_select_column_paragraphs(lesson_id)
    kb = InlineKeyboardBuilder()
    for paragraph in paragraphs:
        kb.button(text=f'{paragraph[1]}', callback_data=f'{paragraph[0]}')
    kb.adjust(1)
    return kb.as_markup()


# def paragrpaph_text(paragraph_id):
#     db = Database(os.getenv('DATABASE_NAME'))
#     paragraphs = db.db_select_column_paragraphs_text(paragraph_id)
#     print(paragraphs)
#     kb = InlineKeyboardBuilder()
#     kb.button(text=f'Назад', callback_data='back_')
#     kb.button(text=f'В главное меню', callback_data='mainmenu_')
#     kb.adjust(1)
#     return kb.as_markup()
