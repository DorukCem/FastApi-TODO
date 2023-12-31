from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
   __tablename__ = "items"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(30), index=True)
   is_done = Column(Boolean, default=False)
   user_id = Column(Integer, ForeignKey('users.id'))

   creator = relationship("User", back_populates="items")


class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String)
   email = Column(String)
   password = Column(String)

   items = relationship("Item", back_populates="creator")