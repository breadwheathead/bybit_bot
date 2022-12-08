import logging
import requests
from flask import Flask, request, jsonify
from flask_sslify import SSLify
from pybit import inverse_perpetual, InvalidRequestError
from config import BOT_URL


logging.basicConfig(
    filename='pybit.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

bot = Flask(__name__)
sslify = SSLify(bot)


def create_session():
    return inverse_perpetual.HTTP(endpoint='https://api.bybit.com')


def send_rate(chat_id: str, message: str):
    symbol = message.strip()
    try:
        session = create_session()
        _result = session.latest_information_for_symbol(symbol=symbol.upper() + 'USDT')
        result = _result['result'][0]['ask_price']
        send_message(chat_id, f'Текущий курс {symbol.upper()}: {result}$')
    except InvalidRequestError:
        logging.error(f'Код {symbol} не найден!')
        send_message(chat_id, f'Код {symbol} не найден!')


def send_message(chat_id: str, text: str):
    url = BOT_URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


@bot.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        try:
            message = r['message']['text']
            send_rate(chat_id, message)
        except KeyError:
            message = 'Принимается только текст!'
            send_message(chat_id, message)
        return jsonify(r)
    return


if __name__ == '__main__':
    bot.run()
