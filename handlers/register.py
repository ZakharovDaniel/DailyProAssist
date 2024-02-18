from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import os
from utils.database import Database
import re
from keyboards.main_kb import main_keyboard


# начало регистрации
async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_telegram_id(message.from_user.id)
    if users:
        await bot.send_message(message.from_user.id, f'Вы уже зарегистрированы', reply_markup=main_keyboard)
    else:
        await bot.send_message(message.from_user.id,
                               f'Процесс регистарции запущен. \n Как к вам обращатся? Введите ваше имя:')
        await state.set_state(RegisterState.registerName)


# регистрация имени пользователя
async def register_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id,
                           f'Введите номер телефона, для поддрежания связи с вами.\n'
                           f'Формат ввода телефона +7xxxxxxxxxx или 8хххххххххх')
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.registerPhone)


async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', message.text)):
        await state.update_data(regphone=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get('regname')
        reg_phone = reg_data.get('regphone')
        msg = f'Добро пожаловать {reg_name}'
        await message.answer(msg, reply_markup=main_keyboard)
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_user(message.from_user.id, reg_name, reg_phone, message.chat.id)
        await state.clear()

    else:
        await message.answer(f'Проверьте введённый вами номер телефона\n'
                             f'Возможно вы допустили ошибку')
