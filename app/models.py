from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    category = Column(String, nullable=False)

    price = Column(Float, nullable=False)

    description = Column(String)

    stock = Column(Integer, default=0)

class CartItem(Base):

    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, default=1)

    product = relationship("Product")
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    status = Column(String, default="Processing")

    total_amount = Column(Float, nullable=False)
