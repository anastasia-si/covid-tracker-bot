from .config import BOT_TOKEN, CHAT_ID
import requests

def bot_send(bot_message):
    params = {
        "chat_id": CHAT_ID,
        "text": bot_message,
        "parse_mode": "HTML",
    }

    response = requests.get(
        "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN),
        params=params
    ).json()

    return response