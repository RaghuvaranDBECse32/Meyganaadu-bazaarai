from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, models, schemas
from .db import Base, SessionLocal, engine
from .demand_model import demand_forecast

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if payload is None or 'sub' not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    email = payload['sub']
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user


@app.get("/")
def home():
    return {"message": "Meyganaadu BazaarAI API Running"}


@app.post("/auth/signup", response_model=schemas.Token)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/auth/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/forecast")
def forecast(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    data = demand_forecast()
    slice_data = data[skip: skip + limit]
    return {"forecast": slice_data, "total": len(data), "skip": skip, "limit": limit}


def map_marketplace(item):
    import random
    amazon = round(item['price'] * (0.95 + random.random() * 0.15), 2)
    flipkart = round(item['price'] * (0.94 + random.random() * 0.16), 2)
    best = 'Amazon' if amazon < flipkart else 'Flipkart' if flipkart < amazon else 'Tie'
    return {
        **item,
        'amazon': amazon,
        'flipkart': flipkart,
        'best': best,
    }


@app.get("/compare/product")
def product_comparison(query: str, skip: int = 0, limit: int = 50, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.name.ilike(f'%{query}%')).offset(skip).limit(limit).all()
    return {"items": [schemas.Product.from_orm(p) for p in products], "total": len(products)}


@app.get("/marketplace/amazon")
def get_amazon_products(skip: int = 0, limit: int = 20, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.amazon_price.isnot(None)).offset(skip).limit(limit).all()
    return {"products": [schemas.Product.from_orm(p) for p in products], "total": len(products)}

@app.get("/marketplace/flipkart")
def get_flipkart_products(skip: int = 0, limit: int = 20, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.flipkart_price.isnot(None)).offset(skip).limit(limit).all()
    return {"products": [schemas.Product.from_orm(p) for p in products], "total": len(products)}

@app.get("/food/hotels")
def get_food_items(skip: int = 0, limit: int = 20, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    food_items = db.query(models.FoodItem).offset(skip).limit(limit).all()
    return {"food_items": [schemas.FoodItem.from_orm(f) for f in food_items], "total": len(food_items)}

@app.get("/analytics/demand-trends")
def get_demand_trends(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Simple analytics: count by forecast category
    trends = db.query(models.Product.forecast, db.func.count(models.Product.id)).group_by(models.Product.forecast).all()
    return {"trends": [{"forecast": f, "count": c} for f, c in trends]}

@app.get("/analytics/price-comparison")
def get_price_comparison(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Average prices by category
    comparisons = db.query(
        models.Product.category,
        db.func.avg(models.Product.price).label('avg_price'),
        db.func.avg(models.Product.amazon_price).label('avg_amazon'),
        db.func.avg(models.Product.flipkart_price).label('avg_flipkart')
    ).group_by(models.Product.category).all()
    return {"comparisons": [
        {
            "category": cat,
            "avg_price": round(avg_price, 2),
            "avg_amazon": round(avg_amazon, 2) if avg_amazon else None,
            "avg_flipkart": round(avg_flipkart, 2) if avg_flipkart else None
        } for cat, avg_price, avg_amazon, avg_flipkart in comparisons
    ]}

@app.get("/compare/food")
def food_comparison(query: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    food_items = db.query(models.FoodItem).filter(
        models.FoodItem.hotel.ilike(f'%{query}%') | models.FoodItem.dish.ilike(f'%{query}%')
    ).limit(10).all()
    return {"query": query, "results": [schemas.FoodItem.from_orm(f) for f in food_items]}

