import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pybit import inverse_perpetual, InvalidRequestError

from config import TOKEN


logging.basicConfig(
    filename='pybit.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger('bot')


session = inverse_perpetual.HTTP(endpoint='https://api.bybit.com')

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.answer('Введите код криптовалюты, например SOL, BTC, ETH.')


@dp.message_handler(content_types='text')
async def get_course(message: types.Message):
    symbol = message.text.strip().upper()
    try:
        _result = session.latest_information_for_symbol(symbol=f'{symbol}USDT')
        result = _result['result'][0]['ask_price']
        await message.answer(f'Текущий курс {symbol}: {result}$')
    except InvalidRequestError:
        logger.error(f'Код {symbol} не найден!')
        await message.reply(f'Код {symbol} не найден!')


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def interception(message: types.Message):
    await message.reply('Принимается только текст!')
    await message.delete()


if __name__ == '__main__':
    executor.start(dp, skip_updates=True)
