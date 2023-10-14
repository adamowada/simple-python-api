from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # This would typically be hashed in a real-world scenario
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship('Order', back_populates='user')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    order_details = relationship('OrderDetails', back_populates='product')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='orders')
    order_details = relationship('OrderDetails', back_populates='order')


class OrderDetails(Base):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    sub_total = Column(Float, nullable=False)

    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details')
