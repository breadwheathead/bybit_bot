import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from pybit import inverse_perpetual, InvalidRequestError

from config import TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT


logging.basicConfig(
    filename='pybit.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)
# logger = logging.getLogger('bot')


session = inverse_perpetual.HTTP(endpoint='https://api.bybit.com')

bot = Bot(TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


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
        logging.error(f'Код {symbol} не найден!')
        await message.reply(f'Код {symbol} не найден!')


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def interception(message: types.Message):
    await message.reply('Принимается только текст!')
    await message.delete()


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down...')
    # insert code here to run it before shutdown
    await bot.delete_webhook()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
