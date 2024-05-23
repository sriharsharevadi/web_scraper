# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_title = Column(String, index=True)
    product_price = Column(String)
    path_to_image = Column(String)


class Product(BaseModel):
    product_title: str
    product_price: str
    path_to_image: str
    image_url: str
