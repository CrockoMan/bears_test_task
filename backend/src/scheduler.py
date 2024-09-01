import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import HTTPException

from src.constants import UPDATE_PERIOD
from src.database import SessionLocal
from src.models import Product
from utils import create_or_update_product

log = logging.getLogger(__name__)


async def update_product_data():
    db = SessionLocal()
    log.info('Updating product data started at: %s', datetime.now())
    # print(f'Updating product data started at {datetime.now()}')
    products = db.query(Product).all()

    for product in products:
        try:
            # Обновляем каждый продукт, передавая его nm_id и флаг обновления
            await create_or_update_product(product.nm_id, db, update=True)
        except HTTPException as e:
            # Обработка ошибок, если продукт не найден в API
            log.error('Error updating product: %s', product.nm_id)
            # print(f'Error updating product {product.nm_id}: {e.detail}')

    db.close()
    log.info('Updating product data finished at: %s', datetime.now())
    # print(f'Updating product data finished at {datetime.now()}')


# scheduler = BackgroundScheduler()
scheduler = AsyncIOScheduler()
# scheduler.add_job(update_product_data, 'interval', seconds=30)
scheduler.add_job(update_product_data, 'interval', minutes=UPDATE_PERIOD)
# scheduler.add_job(update_product_data, 'interval', minutes=5)
scheduler.start()
