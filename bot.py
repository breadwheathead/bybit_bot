import logging
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pybit import inverse_perpetual
from config.reader import load_config

logging.basicConfig(level=logging.INFO)

session = inverse_perpetual.HTTP(endpoint='https://api.bybit.com')

config = load_config('config/bot.ini')
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Hi')

# print(session.latest_information_for_symbol(symbol='SOLUSDT'))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
