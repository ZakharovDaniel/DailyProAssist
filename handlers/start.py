from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from keyboards.main_kb import main_keyboard
from utils.database import Database
import os


async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_telegram_id(message.from_user.id)
    if users:
        await bot.send_message(message.from_user.id, f'Плодотворного дня, {users[2]}!', reply_markup=main_keyboard)
    else:
        await bot.send_message(message.from_user.id, f'Добро пожаловать в профессионального помощника.\n\n'
            f'Прежде, чем начать - зарегистрируйтесь\n\n', reply_markup=register_keyboard)
