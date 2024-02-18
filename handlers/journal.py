import datetime
from utils.database import Database
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.journal import JournalState
import os
import re
from keyboards.journal_kb import journal_keyboard


async def get_journal_kb(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, 'Вы вошли в журнал', reply_markup=journal_keyboard)


async def add_note(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Какую мысль хотите записать?')
    await state.set_state(JournalState.notedescriprion)


async def note_descriprion(message: Message, state: FSMContext):
    pattern = r"[A-Za-zА-Яа-яёЁ0-9]"
    if not (re.findall(pattern, message.text)):
        await message.answer(f'Бот не понимает введённое вами сообщение\n'
                             f'Введите повторно')
        await state.set_state(JournalState.notedescriprion)
    else:
        await state.update_data(notedescriprion=message.text)
        await message.answer(f'Запись создана')
        reg_data = await state.get_data()
        description = reg_data.get('notedescriprion')
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_note(message.from_user.id, description, datetime.date.today())
        await state.clear()


async def get_journal(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = message.from_user.id
    notes = db.db_select_column('journal')
    if notes:
        await bot.send_message(message.from_user.id, 'Ваши записи:')
        for note in notes:
            await bot.send_message(message.from_user.id, f'{note[3]}\n'
                                                         f'{note[2]}\n')
    else:
        await bot.send_message(message.from_user.id, 'Записей нет')
