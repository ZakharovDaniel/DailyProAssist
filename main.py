import datetime
from aiogram import Dispatcher, Bot, F
import asyncio
import os
import logging
from dotenv import load_dotenv
from handlers import apsched
from utils.commands import set_commands
from handlers.start import get_start
from state.register import RegisterState
from handlers.register import start_register, register_name, register_phone
from aiogram.filters import Command
from state.event import EventState
from state.task import TaskState
from handlers.task import get_task_kb, add_task, add_description, get_task, add_date
from handlers.journal import add_note, note_descriprion, get_journal, get_journal_kb
from handlers.back import back_kb
from handlers.scheduler import get_scheduler_kb, get_scheduler_date, get_scheduler_on_date, get_scheduler_today, \
    get_scheduler_tomorrow
from state.journal import JournalState
from handlers.event import create_event, select_place, select_date, select_time, select_description_event, get_event, \
    get_event_kb
from handlers.courses import get_course_kb, get_lesson_kb, get_paragraph_kb, get_paragraph_text
from state.courses import CoursesState
from state.scheduler import DateSchedulerState
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tzlocal import get_localzone
from handlers import motivation

load_dotenv()
token = os.getenv('TOKEN')
bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()

dp.message.register(get_start, Command(commands='start'))

# регистрация пользователя
dp.message.register(start_register, F.text == 'Зарегистрироваться')
dp.message.register(register_name, RegisterState.registerName)
dp.message.register(register_phone, RegisterState.registerPhone)
# Кнопка возврата в главное меню
dp.message.register(back_kb, F.text == 'В главное меню')
# Журнал
dp.message.register(get_journal_kb, F.text == 'Журнал')
dp.message.register(get_journal, F.text == 'Посмотреть записи')
dp.message.register(add_note, F.text == 'Добавить запись')
dp.message.register(note_descriprion, JournalState.notedescriprion)
# Ежедневник
dp.message.register(get_task_kb, F.text == 'Ежедневник')
dp.message.register(add_task, F.text == 'Добавить задачу')
dp.message.register(add_date, TaskState.datetask)
dp.message.register(add_description, TaskState.taskdescription)
dp.message.register(get_task, F.text == 'Посмотреть задачи')
# Расписание
dp.message.register(get_scheduler_kb, F.text == 'Расписание')
dp.message.register(get_scheduler_on_date, F.text == 'Посмотреть по дате')
dp.message.register(get_scheduler_date, DateSchedulerState.date)
dp.message.register(get_scheduler_today, F.text == 'Расписание сегодня')
dp.message.register(get_scheduler_tomorrow, F.text == 'Расписание завтра')

# Мероприятия
dp.message.register(get_event_kb, F.text == 'Мероприятия')
dp.message.register(create_event, F.text == 'Добавить мероприятие')
dp.message.register(select_place, EventState.place)
dp.message.register(select_date, EventState.date)
dp.message.register(select_time, EventState.time)
dp.message.register(select_description_event, EventState.desciption)
dp.message.register(get_event, F.text == 'Посмотреть мероприятия')
# Курсы
dp.message.register(get_course_kb, F.text == 'Курсы')
dp.callback_query.register(get_lesson_kb, CoursesState.course)
dp.callback_query.register(get_paragraph_kb, CoursesState.lesson)
dp.callback_query.register(get_paragraph_text, CoursesState.paragraph)
scheduler = AsyncIOScheduler(timezone=get_localzone())

chat_id = os.getenv('USER_ID')


async def start():
    logging.basicConfig(level=logging.DEBUG)

    scheduler.add_job(apsched.get_scheduler_today, trigger='cron', hour=datetime.datetime.now().hour,
                      minute=datetime.datetime.now().minute + 1,
                      kwargs={'bot': bot, 'chat_id': chat_id})
    scheduler.add_job(apsched.get_scheduler_tomorrow, trigger='cron', hour=datetime.datetime.now().hour,
                      minute=datetime.datetime.now().minute + 2,
                      kwargs={'bot': bot, 'chat_id': chat_id})
    scheduler.add_job(motivation.get_quote, trigger='interval', minutes=1,
                      kwargs={'bot': bot, 'chat_id': chat_id})

    scheduler.start()
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
