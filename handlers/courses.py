import os

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards.courses_kb import curses_kb, lesson_kb, paragraph_kb
from state.courses import CoursesState
from utils.database import Database


async def get_course_kb(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Курсы по профессиональному развитию', reply_markup=curses_kb())
    await state.set_state(CoursesState.course)

async def get_lesson_kb(call: CallbackQuery, state: FSMContext):
    print(call.data)
    course_id = call.data.split('_')[0]
    await call.message.edit_reply_markup(reply_markup=lesson_kb(course_id))
    await state.set_state(CoursesState.lesson)

async def get_paragraph_kb(call: CallbackQuery, state: FSMContext):
    lesson_id = call.data.split('_')[0]
    await call.message.edit_reply_markup(reply_markup=paragraph_kb(lesson_id))
    await state.set_state(CoursesState.paragraph)

async def get_paragraph_text(call: CallbackQuery, state: FSMContext):
    paragraph_id = call.data.split('_')[0]
    db = Database(os.getenv('DATABASE_NAME'))
    paragraphs = db.db_select_column_paragraphs_text(paragraph_id)
    msg = (f'{paragraphs[0][2]}\n\n'
           f'{paragraphs[0][3]}')
    await call.message.answer(msg)
    await state.clear()