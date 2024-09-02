import os

from dotenv import load_dotenv

load_dotenv()


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
UPDATE_PERIOD = int(os.getenv('UPDATE_PERIOD', '5'))
HTTP_PREFIX = os.getenv('HTTP_PREFIX')
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    default='127.0.0.1:8000,localhost:8000,http://194.26.226.134/'
).split(',')

DATABASE_URL = 'sqlite:///./products.db'
if not os.getenv('DEBUG', True):
    DATABASE_URL = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}'
    )


TIMEOUT = 2
