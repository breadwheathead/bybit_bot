import logging
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pybit import inverse_perpetual

logging.basicConfig(level=logging.INFO)

session = inverse_perpetual.HTTP(endpoint='https://api.bybit.com')

print(session.latest_information_for_symbol(symbol='SOLUSDT'))


if __name__ == '__main__':
    pass
