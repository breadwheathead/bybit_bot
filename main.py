import requests
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from flask import Flask, request, jsonify
from flask_sslify import SSLify
from pybit import inverse_perpetual, InvalidRequestError
from config import TOKEN

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)


def get_response_from_bybit(symbol):
    url = 'https://breadwheathead.pythonanywhere.com/'
    session = inverse_perpetual.HTTP(endpoint=url)


def get_updates():
    url = URL + 'getUpdates?offset=-1'
    r = requests.get(url)
    return r.json()


def send_message(chat_id, text='проверка'):
    url = URL + 'sendMessage'
    answer = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=answer)
    return r.json()


def main():
    response = get_updates()
    chat_id = response['result'][0]['message']['chat']['id']
    send_message(chat_id)


if __name__ == '__main__':
    main()
