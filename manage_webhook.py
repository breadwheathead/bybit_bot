import requests
from config import BOT_URL, WEBHOOK_URL


def set_webhook():
    url = f'{BOT_URL}setWebhook?url={WEBHOOK_URL}'
    r = requests.post(url)
    print(r.json())


def delete_webhook():
    url = f'{BOT_URL}deleteWebhook'
    r = requests.post(url)
    print(r.json())


if __name__ == '__main__':
    set_webhook()
    # delete_webhook()
