import datetime
import os
import re
from utils.database import Database
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.scheduler_kb import scheduler_keyboard
from state.scheduler import DateSchedulerState


async def get_scheduler_kb(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Вы вошли в расписание', reply_markup=scheduler_keyboard)

async def get_scheduler_on_date(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Введите интересующую вас дату\n'
                                                 f'Введите дату в формате DD.MM.YY\n'
                                                 f'пример: 20.02.24')
    await state.set_state(DateSchedulerState.date)

async def get_scheduler_date(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^\d{2}\.\d{2}\.\d{2}$', message.text)):
        await state.update_data(date=message.text)
        user_date = await state.get_data()
        date = (user_date.get('date'))
        db = Database(os.getenv('DATABASE_NAME'))
        tasks = db.scheduler_date('tasks', 'date', date)
        events = db.scheduler_date('events', 'date_event', date)
        if tasks:
            await bot.send_message(message.from_user.id, f'Задачи на {date}')
            for task in tasks:
                await bot.send_message(message.from_user.id, f'{task[2]}')
        else:
            await message.answer(f'Задачи на {date} нет')
        if events:
            await bot.send_message(message.from_user.id, f'Мероприятия на {date}')
            for event in events:
                await bot.send_message(message.from_user.id, f'Описание: {event[4]}\n'
                                                             f'Время проведения: {event[3]}\n'
                                                             f'Место проведения: {event[1]}\n')
        else:
            await bot.send_message(message.from_user.id, 'Мероприятий на {date} нет')
        await state.clear()
    else:
        await message.answer(f'Проверьте введённую вами дату\n'
                             f'Пример: 24.03.25')

async def get_scheduler_today(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Расписание на сегодня:')
    current_date = datetime.datetime.now().date()
    date = current_date.strftime("%d.%m.%y")
    db = Database(os.getenv('DATABASE_NAME'))
    tasks = db.scheduler_date('tasks', 'date', date)
    events = db.scheduler_date('events', 'date_event', date)
    if tasks:
        await bot.send_message(message.from_user.id, f'Задачи:')
        for task in tasks:
            await bot.send_message(message.from_user.id, f'{task[2]}')
    else:
        await bot.send_message(message.from_user.id,f'Задач сегодня нет')
    if events:
        await bot.send_message(message.from_user.id, f'Мероприятия:')
        for event in events:
            await bot.send_message(message.from_user.id, f'Описание: {event[4]}\n'
                                                         f'Время проведения: {event[3]}\n'
                                                         f'Место проведения: {event[1]}\n')
    else:
        await bot.send_message(message.from_user.id, f'Мероприятий сегодня нет')


async def get_scheduler_tomorrow(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Рассписание на завтра')
    current_date = datetime.datetime.now().date()
    next = current_date + datetime.timedelta(days=1)
    date = next.strftime("%d.%m.%y")
    db = Database(os.getenv('DATABASE_NAME'))
    tasks = db.scheduler_date('tasks', 'date', date)
    events = db.scheduler_date('events', 'date_event', date)
    if tasks:
        await bot.send_message(message.from_user.id, f'Задачи:')
        for task in tasks:
            await bot.send_message(message.from_user.id, f'{task[2]}')
    else:
        await message.answer(f'Задач на завтра нет')
    if events:
        await bot.send_message(message.from_user.id, f'Мероприятия:')
        for event in events:
            await bot.send_message(message.from_user.id, f'Описание: {event[4]}\n'
                                                         f'Время проведения: {event[3]}\n'
                                                         f'Место проведения: {event[1]}\n')
    else:
        await bot.send_message(message.from_user.id, f'Мероприятий на завтра нет')

