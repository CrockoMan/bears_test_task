from pydantic import BaseModel


class QuantityByWh(BaseModel):
    wh: int
    quantity: int

class QuantityBySize(BaseModel):
    size: str
    quantity_by_wh: list[QuantityByWh]

class ProductResponse(BaseModel):
    nm_id: int
    current_price: int
    sum_quantity: int
    quantity_by_sizes: list[QuantityBySize]

    class Config:
        from_attributes = True
