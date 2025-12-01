from sqlalchemy import Column, Integer, String, Float, Date
from database import Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class StockDaily(Base):
    __tablename__ = 'stocks_daily'

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255))
    is_active = Column(Integer, default=1)




