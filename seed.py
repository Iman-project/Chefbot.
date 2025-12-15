# seed.py
import os
from datetime import date, timedelta
from db import SessionLocal, create_all, Restaurant, Menu

def seed():
    create_all()
    session = SessionLocal()

    # Create two demo restaurants
    r1 = Restaurant(name="Mama's Kitchen", phone_number_id=None)
    r2 = Restaurant(name="Grill House", phone_number_id=None)
    session.add_all([r1, r2])
    session.commit()

    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Mama's menu today
    menus = [
        Menu(restaurant_id=r1.id, menu_date=today, item_name="Jollof Rice", price=1500),
        Menu(restaurant_id=r1.id, menu_date=today, item_name="Grilled Chicken", price=2500),
        # tomorrow
        Menu(restaurant_id=r1.id, menu_date=tomorrow, item_name="Fried Rice", price=1600)
    ]

    # Grill House menu today
    menus += [
        Menu(restaurant_id=r2.id, menu_date=today, item_name="Beef Burger", price=1200),
        Menu(restaurant_id=r2.id, menu_date=today, item_name="Fries", price=500)
    ]

    session.add_all(menus)
    session.commit()
    session.close()
    print("Seeded demo restaurants and menus.")

if __name__ == "__main__":
    seed()
