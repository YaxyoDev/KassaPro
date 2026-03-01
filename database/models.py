from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(Enum('active', 'inactive'), default='active')
    joined_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}', status='{self.status}')>"


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    barcode = Column(String(50), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    status = Column(Enum('active', 'inactive'), default='active')
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})>"


class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    sale_owner = Column(String(50), nullable=False)
    saled_items = Column(String(1000), nullable=False)
    total_sum = Column(Float, nullable=False)
    paid_sum = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    payment = Column(Enum('cash', 'card', 'click'), nullable=False)
    saled_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Sale(id={self.id}, sale_owner='{self.sale_owner}', total_sum={self.total_sum}, payment='{self.payment}')>"