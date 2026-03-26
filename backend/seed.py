from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Product, FoodItem
from demand_model import demand_forecast
import random

def seed_database():
    db = SessionLocal()
    try:
        # Seed products from CSV
        forecast_data = demand_forecast()
        for item in forecast_data:
            amazon = round(item['price'] * (0.95 + random.random() * 0.15), 2)
            flipkart = round(item['price'] * (0.94 + random.random() * 0.16), 2)
            best = 'Amazon' if amazon < flipkart else 'Flipkart' if flipkart < amazon else 'Tie'

            # Determine category based on product name
            name_lower = item['product'].lower()
            if any(word in name_lower for word in ['mobile', 'laptop', 'tv', 'phone']):
                category = 'electronics'
            elif any(word in name_lower for word in ['rice', 'wheat', 'sugar', 'tea', 'coffee']):
                category = 'grocery'
            elif any(word in name_lower for word in ['shirt', 'pant', 'dress', 'shoe']):
                category = 'fashion'
            else:
                category = 'other'

            product = Product(
                name=item['product'],
                category=category,
                sales=item['sales'],
                price=item['price'],
                forecast=item['forecast'],
                amazon_price=amazon,
                flipkart_price=flipkart,
                best_store=best
            )
            db.add(product)

        # Seed food items
        food_samples = [
            ("Dominos", "Margherita Pizza", 250, 260, 4.2),
            ("Pizza Hut", "Chicken Pizza", 320, 330, 4.1),
            ("McDonald's", "Big Mac", 180, 185, 4.0),
            ("Burger King", "Whopper", 190, 195, 3.9),
            ("KFC", "Chicken Bucket", 350, 355, 4.3),
            ("Subway", "Chicken Sub", 220, 225, 4.0),
            ("Starbucks", "Latte", 150, 155, 4.1),
            ("CCD", "Cappuccino", 140, 145, 3.8),
            ("Biryani House", "Chicken Biryani", 180, 185, 4.4),
            ("Paradise", "Mutton Biryani", 220, 225, 4.5),
            ("Saravana Bhavan", "Dosa", 120, 125, 4.2),
            ("Murugan Idli", "Idli Sambar", 80, 85, 4.0),
            ("A2B", "Pongal", 100, 105, 4.1),
            ("Sangeetha", "Poori Masala", 90, 95, 3.9),
            ("Anjappar", "Chettinad Chicken", 280, 285, 4.3),
        ]

        for hotel, dish, swiggy, zomato, rating in food_samples:
            rec = 'Swiggy' if swiggy < zomato else 'Zomato' if zomato < swiggy else 'Tie'
            food_item = FoodItem(
                hotel=hotel,
                dish=dish,
                swiggy_price=swiggy,
                zomato_price=zomato,
                rating=rating,
                recommendation=rec
            )
            db.add(food_item)

        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    from models import Base
    Base.metadata.create_all(bind=engine)
    seed_database()
