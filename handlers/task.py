import os

from utils.database import Database
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.task import TaskState
from keyboards.task_kb import task_keyboard
import re


async def get_task_kb(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Вы вошли в ежедневник', reply_markup=task_keyboard)


async def add_task(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'На какую дату добавить задачу?\n'
                                                 f'Введите дату в формате DD.MM.YY\n'
                                                 f'пример: 20.02.24')
    await state.set_state(TaskState.datetask)


async def add_date(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^\d{2}\.\d{2}\.\d{2}$', message.text)):
        await bot.send_message(message.from_user.id, f'Добавьте описание задачи')
        await state.update_data(adddate=message.text)
        await state.set_state(TaskState.taskdescription)
    else:
        await message.answer(f'Проверьте введённую вами дату\n'
                             f'Пример: 24.03.25')
        await state.set_state(TaskState.datetask)


async def add_description(message: Message, state: FSMContext):
    pattern = r"[A-Za-zА-Яа-яёЁ0-9]"
    if re.findall(pattern, message.text):
        await state.update_data(adddescription=message.text)
        reg_data = await state.get_data()
        description = reg_data.get('adddescription')
        date_ex = reg_data.get('adddate')
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_task(message.from_user.id, description, date_ex)
        await message.answer(f'Задача создана')
        await state.clear()
    else:
        await message.answer(f'Бот не понимает введённое вами сообщение\n'
                             f'Введите повторно')
        await state.set_state(TaskState.taskdescription)


async def get_task(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    tasks = db.db_select_column('tasks')
    if tasks:
        for task in tasks:
            if task[4] == 0:
                msg = f'{task[2]}'
                await bot.send_message(message.from_user.id, msg)
    else:
        await bot.send_message(message.from_user.id, 'Нет задач')


# async def update_task(call: CallbackQuery):
#     db = Database(os.getenv('DATABASE_NAME'))
#     print(call.data)
#     await call.message.delete()
