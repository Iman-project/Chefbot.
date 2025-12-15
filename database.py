# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///chefbot.db"  # or your DB
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Restaurant table
class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    token = Column(String, unique=True)  # NEW: unique token for each restaurant
    whatsapp_number = Column(String, unique=True, nullable=True)  # optional
    menus = relationship("Menu", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")

# Customer table
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String, unique=True)
    orders = relationship("Order", back_populates="customer")

# Menu table
class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    item_name = Column(String)
    price = Column(Float)
    menu_day = Column(String, nullable=True)  # Monday, Tuesday...
    menu_date = Column(Date, nullable=True)
    restaurant = relationship("Restaurant", back_populates="menus")

# Order table
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_ref = Column(String, unique=True)
    items = Column(JSON)
    total_amount = Column(Float)
    status = Column(String)
    timestamp = Column(Date, default=None)
    restaurant = relationship("Restaurant", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")

def create_all():
    Base.metadata.create_all(bind=engine)
