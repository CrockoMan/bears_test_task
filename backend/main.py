from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from src.database import get_db
from src.models import Product
from src.schemas import ProductResponse
from src.utils import create_or_update_product

app = FastAPI()

origins = [
    "http://localhost:8000",
    "0.0.0.0:8000",
    'https://bird-sacred-humbly.ngrok-free.app'
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
    product = db.query(Product).filter(Product.nm_id == nm_id).first()

    if product is None:
        product = await create_or_update_product(nm_id, db)

    return product
