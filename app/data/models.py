#models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

tm = pytz.timezone('Asia/Jakarta')

Base = declarative_base()

class User(Base):
    # Dev Table
    __tablename__ = 'userstest'
    # Prod Table
    # __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False)
    userprofile_link = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now(tm))
    updated_at = Column(DateTime, default=datetime.now(tm), onupdate=datetime.now(tm))
    # this data is nullable
    age = Column(Integer, nullable=True)
    gender = Column(String(21), nullable=True)
    address = Column(String(100), nullable=True)
    