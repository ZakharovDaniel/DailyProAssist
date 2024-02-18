import os
import re
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.event_kb import event_keyboard
from state.event import EventState
from utils.database import Database


async def get_event_kb(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, 'Вы вошли в Мероприятия', reply_markup=event_keyboard)


async def create_event(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Где будет мероприятие?')
    await state.set_state(EventState.place)


async def select_place(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id,f'Когда будет мероприятие\n'
                                                f'Введите дату в формате DD.MM.YY\n'
                                                f'пример: 20.02.24')
    await state.update_data(place=message.text)
    await state.set_state(EventState.date)


async def select_date(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^\d{2}\.\d{2}\.\d{2}$', message.text)):
        await bot.send_message(message.from_user.id,f'В какое время будет проходить мероприятие\n'
                               f'Введите время в формате HH:MM')
        await state.update_data(date=message.text)
        await state.set_state(EventState.time)
    else:
        await message.answer(f'Проверьте введённую вами дату\n'
                             f'Пример: 24.03.25')


async def select_time(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^(([0,1][0-9])|(2[0-3])):[0-5][0-9]$', message.text)):
        await bot.send_message(message.from_user.id,f'Добавьте описание мероприятию')
        await state.update_data(time=message.text)
        await state.set_state(EventState.desciption)
    else:
        await message.answer(f'Проверьте введённое вами время\n'
                             f'Пример: 23:03')

async def select_description_event(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(description=message.text)
    await bot.send_message(message.from_user.id, f'Мероприятие добавлено')
    create_date = await state.get_data()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_event(create_date['place'], create_date['date'], create_date['time'], create_date['description'])
    await state.clear()


async def get_event(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    events = db.db_select_column('events')
    if events:
        for event in events:
            await bot.send_message(message.from_user.id, f'Мероприятие состоится: {event[2]} в {event[3]} \n'
                                                         f'Место проведения:\n{event[1]}\n'
                                                         f'Описание: \n{event[4]}\n')
    else:
        await bot.send_message(message.from_user.id, 'Мероприятий нет')