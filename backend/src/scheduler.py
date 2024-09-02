import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import HTTPException

from src.constants import UPDATE_PERIOD
from src.database import SessionLocal
from src.models import Product
from src.utils import create_or_update_product

log = logging.getLogger(__name__)


async def update_product_data():
    db = SessionLocal()
    log.info('Updating product data started at: %s', datetime.now())
    products = db.query(Product).all()

    for product in products:
        try:
            await create_or_update_product(product.nm_id, db, update=True)
        except HTTPException:
            log.error('Error updating product: %s', product.nm_id)

    db.close()
    log.info('Updating product data finished at: %s', datetime.now())


scheduler = AsyncIOScheduler()
scheduler.add_job(update_product_data, 'interval', minutes=UPDATE_PERIOD)
scheduler.start()
