
import datetime

from enum import auto
from operator import index
from xmlrpc.client import DateTime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Recipse(Base):
  __tablename__ = "recipses"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  making_time = Column(String, index=True)
  serves = Column(String, index=True)
  ingredients = Column(String, index=True)
  cost = Column(Integer, index=True)
  created_at = Column(DateTime, index=True, default=datetime.datetime.now())
  updated_at = Column(DateTime, index=True, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

