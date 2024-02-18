import random
from aiogram import Bot
from utils.quotes import quotes, entrys

async def get_quote(bot: Bot, chat_id):
    if quotes and entrys:
        quote = random.choice(quotes)
        entry = random.choice(entrys)
        await bot.send_message(chat_id, f'{entry}'
                                        f'{quote}')
