from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Item(BaseModel):
   name: str = Field(..., min_length=3, max_length=30)
   is_done: Optional[bool] = False

   @field_validator('name')
   @classmethod
   def name_must_contain_letters(cls, v):
      if not any(char.isalpha() for char in v):
         raise ValueError('Name must contain at least one letter')
      return v

# This allows me to custmoize my responses
class ShowItem(Item):
   class Config():
      orm_mode = True

class User(BaseModel):
   name : str
   email: str
   password : str