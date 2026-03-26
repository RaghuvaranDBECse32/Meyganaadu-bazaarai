from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    sales = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    forecast = Column(String, nullable=False)
    amazon_price = Column(Float, nullable=True)
    flipkart_price = Column(Float, nullable=True)
    best_store = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True, index=True)
    hotel = Column(String, index=True, nullable=False)
    dish = Column(String, nullable=False)
    swiggy_price = Column(Float, nullable=False)
    zomato_price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    recommendation = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

