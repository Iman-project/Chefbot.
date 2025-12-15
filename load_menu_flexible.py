# load_menu_flexible.py
import os
import pandas as pd
from dateutil import parser as date_parser
from database import SessionLocal, Restaurant, Menu, create_all

COLUMN_MAP = {
    'item_name': ['item_name', 'name', 'dish', 'item'],
    'price': ['price', 'cost', 'amount'],
    'menu_date': ['menu_date', 'date'],
    'menu_day': ['menu_day', 'day', 'weekday']
}

def find_column(cols, candidates):
    for c in candidates:
        for col in cols:
            if col.lower() == c.lower():
                return col
    return None

def read_file(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext in (".xls", ".xlsx"):
        return pd.read_excel(path)
    if ext == ".json":
        return pd.read_json(path)
    raise ValueError("Unsupported file type: use csv, xlsx, or json")

def normalize_rows(df):
    cols = list(df.columns)
    item_col = find_column(cols, COLUMN_MAP['item_name'])
    price_col = find_column(cols, COLUMN_MAP['price'])
    date_col = find_column(cols, COLUMN_MAP['menu_date'])
    day_col = find_column(cols, COLUMN_MAP['menu_day'])
    if not item_col or not price_col:
        raise ValueError("File must include item and price columns.")
    rows = []
    for _, r in df.iterrows():
        item = r[item_col]
        price = r[price_col]
        menu_date = r[date_col] if date_col and pd.notna(r[date_col]) else None
        menu_day = r[day_col] if day_col and pd.notna(r[day_col]) else None
        if isinstance(menu_date, str):
            try:
                menu_date = date_parser.parse(menu_date).date()
            except Exception:
                menu_date = None
        if isinstance(price, str):
            price = int(price.replace("₦","").replace(",","").strip())
        rows.append({"item_name": str(item).strip(), "price": int(price), "menu_date": menu_date, "menu_day": (menu_day.strip().title() if menu_day else None)})
    return rows

def load_menu(file_path, restaurant_name):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    df = read_file(file_path)
    rows = normalize_rows(df)
    create_all()
    session = SessionLocal()
    restaurant = session.query(Restaurant).filter_by(name=restaurant_name).first()
    if not restaurant:
        restaurant = Restaurant(name=restaurant_name)
        session.add(restaurant)
        session.commit()
    count = 0
    for r in rows:
        m = Menu(restaurant_id=restaurant.id, menu_date=r["menu_date"], menu_day=r["menu_day"], item_name=r["item_name"], price=r["price"])
        session.add(m); count += 1
    session.commit(); session.close()
    return count

if __name__ == "__main__":
    print("Usage: call load_menu('file.csv','Restaurant Name')")
