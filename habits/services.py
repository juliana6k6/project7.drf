from config import settings
import requests


def send_telegram_message(tg_id, message):
    params = {
        'text': message,
        'chat_id': tg_id,
    }
    try:
        response = requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage', params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
