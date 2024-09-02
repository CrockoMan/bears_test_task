import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
URL_BACKEND = os.getenv('URL_BACKEND')

TIMEOUT = 2

NEED_NM_ID = 'Введите nm_id товара, чтобы получить информацию.'
NEED_CORRECT_NM_ID = 'Пожалуйста, введите корректный nm_id (число).'
RESPONSE_ERROR = 'Ошибка получения данных. Попробуйте позже.'
NEED_BOT_TOKEN = 'BOT_TOKEN должен быть передан.'
NOT_FOUND_ERROR = 'Товар не найден'