from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base, engine


class QuantityByWh(Base):
    __tablename__ = 'quantity_by_wh'

    id = Column(Integer, primary_key=True, index=True)
    wh = Column(Integer)
    quantity = Column(Integer)
    size_id = Column(Integer, ForeignKey('quantity_by_size.id'))

    size_relation = relationship(
        'QuantityBySize',
        back_populates='quantity_by_wh'
    )


class QuantityBySize(Base):
    __tablename__ = 'quantity_by_size'

    id = Column(Integer, primary_key=True, index=True)
    size = Column(String)
    product_id = Column(Integer, ForeignKey('products.nm_id'))
    quantity_by_wh = relationship(
        'QuantityByWh',
        back_populates='size_relation'
    )
    product = relationship(
        'Product',
        back_populates='quantity_by_sizes'
    )


class Product(Base):
    __tablename__ = 'products'

    nm_id = Column(Integer, primary_key=True, index=True)
    current_price = Column(Integer)
    sum_quantity = Column(Integer)
    quantity_by_sizes = relationship(
        'QuantityBySize',
        back_populates='product'
    )


Base.metadata.create_all(bind=engine)
