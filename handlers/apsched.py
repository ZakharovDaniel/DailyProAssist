import datetime
import os
from aiogram import Bot
from utils.database import Database


async def get_scheduler_today(bot: Bot, chat_id):
    await bot.send_message(chat_id, f'Расписание на сегодня:')
    current_date = datetime.datetime.now().date()
    date = current_date.strftime("%d.%m.%y")
    db = Database(os.getenv('DATABASE_NAME'))
    tasks = db.scheduler_date('tasks', 'date', date)
    events = db.scheduler_date('events', 'date_event', date)
    if tasks:
        count = 0
        await bot.send_message(chat_id, f'Задачи:')
        for task in tasks:
            count += 1
            await bot.send_message(chat_id, f'{count}.{task[2]}')
    else:
        await bot.send_message(chat_id, f'Задач на сегодня нет')
    if events:
        await bot.send_message(chat_id, f'Мероприятия:')
        for event in events:
            await bot.send_message(chat_id, f'Описание: {event[4]}\n'
                                            f'Время проведения: {event[3]}\n'
                                            f'Место проведения: {event[1]}\n')
    else:
        await bot.send_message(chat_id, f'Мероприятий на сегодня нет')


async def get_scheduler_tomorrow(bot: Bot, chat_id):
    await bot.send_message(chat_id, f'Рассписание на завтра')
    current_date = datetime.datetime.now().date()
    next = current_date + datetime.timedelta(days=1)
    date = next.strftime("%d.%m.%y")
    db = Database(os.getenv('DATABASE_NAME'))
    tasks = db.scheduler_date('tasks', 'date', date)
    events = db.scheduler_date('events', 'date_event', date)
    await bot.send_message(chat_id, f'Расписание на {date}')
    if tasks:
        await bot.send_message(chat_id, f'Задачи:')
        for task in tasks:
            i = 0
            await bot.send_message(chat_id, f'{i+1}. {task[2]}')
    else:
        await bot.send_message(chat_id, f'Задач на завтра нет')
    if events:
        await bot.send_message(chat_id, f'Мероприятия:')
        for event in events:
            await bot.send_message(chat_id, f'Описание: {event[4]}\n'
                                            f'Время проведения: {event[3]}\n'
                                            f'Место проведения: {event[1]}\n')
    else:
        await bot.send_message(chat_id, f'Мероприятий на завтра нет')
