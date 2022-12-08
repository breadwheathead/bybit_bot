import logging
import requests
from flask import Flask, request, jsonify
from flask_sslify import SSLify
from pybit import inverse_perpetual, InvalidRequestError
from config import TOKEN, WEBHOOK_URL

'''string_url = 'https://api.telegram.org/bot5605337710:AAGQ2jtf2oImgzZ3ajxoYhODUwpIOy-yee8/setWebhook?url=
https://9205-176-215-100-51.eu.ngrok.io'''

logging.basicConfig(
    filename='pybit.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

bot = Flask(__name__)
# sslify = SSLify(bot)

URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)


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
    url = URL + 'sendMessage'
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


def set_webhook():
    tunnel = 'https://183e-176-215-100-51.eu.ngrok.io'
    url = f'{URL}setWebhook?url={tunnel}'
    r = requests.post(url)
    print(r.json())


def delete_webhook():
    url = f'{URL}deleteWebhook'
    r = requests.post(url)
    print(r.json())


if __name__ == '__main__':
    # set_webhook()
    # delete_webhook()
    bot.run()
