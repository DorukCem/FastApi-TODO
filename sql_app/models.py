from .database import Base
from sqlalchemy import Boolean, Column, Integer, String

class Item(Base):
   __tablename__ = "items"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(30), index=True)
   is_done = Column(Boolean, default=False)