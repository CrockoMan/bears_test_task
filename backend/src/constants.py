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

DATABASE_URL = 'sqlite:///./products.db'
if not os.getenv('DEBUG', True):
    DATABASE_URL = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}'
    )


TIMEOUT = 2
