from aiogram import Bot
from aiogram.types import Message

from keyboards.main_kb import main_keyboard


async def back_kb(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, 'Что ещё сделаем?', reply_markup=main_keyboard)
