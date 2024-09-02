import logging
from datetime import datetime

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import src.scheduler
from src.database import get_db
from src.models import Product
from src.schemas import ProductResponse
from src.utils import create_or_update_product

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

log = logging.getLogger(__name__)

log.info('Application started at: %s', datetime.now())


origins = [
    "http://localhost:8000",
    "0.0.0.0:8000",
    'http://194.26.226.134/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/products/{nm_id}", response_model=ProductResponse)
async def read_product(nm_id: int, db: Session = Depends(get_db)):
    log.info('Get info product id: %s', nm_id)
    product = db.query(Product).filter(Product.nm_id == nm_id).first()

    if product is None:
        product = await create_or_update_product(nm_id, db)

    return product
