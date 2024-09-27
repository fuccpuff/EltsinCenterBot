# config.py
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
YANDEX_MAPS_API_KEY = os.getenv('YANDEX_MAPS_API_KEY')
DATABASE_NAME = 'bot.db'
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))

# Поддерживаемые языки
SUPPORTED_LANGUAGES = ['ru', 'en']
DEFAULT_LANGUAGE = 'ru'