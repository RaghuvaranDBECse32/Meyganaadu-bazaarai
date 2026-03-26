from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ProductComparison(BaseModel):
    product: str
    sales: int
    price: float
    forecast: str
    amazon: float
    flipkart: float
    best: str

class FoodComparison(BaseModel):
    hotel: str
    dish: str
    swiggy: float
    zomato: float
    rating: float
    recommendation: str

class ProductBase(BaseModel):
    name: str
    category: str
    sales: int
    price: float
    forecast: str
    amazon_price: Optional[float] = None
    flipkart_price: Optional[float] = None
    best_store: Optional[str] = None

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FoodItemBase(BaseModel):
    hotel: str
    dish: str
    swiggy_price: float
    zomato_price: float
    rating: float
    recommendation: str

class FoodItem(FoodItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

