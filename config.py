# config.py
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = 'API TOKEN HERE'
YANDEX_MAPS_API_KEY = 'API TOKEN HERE'
DATABASE_NAME = 'bot.db'
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))

# Поддерживаемые языки
SUPPORTED_LANGUAGES = ['ru', 'en']
DEFAULT_LANGUAGE = 'ru'
