from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import scheduler
from database import get_db
from models import Product
from schemas import ProductResponse
from utils import create_or_update_product

app = FastAPI()

origins = [
    "http://localhost:8000",
    "https://your-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/products/{nm_id}", response_model=ProductResponse)
async def read_product(nm_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.nm_id == nm_id).first()

    if product is None:
        product = await create_or_update_product(nm_id, db)

    return product
