# uvicorn main:app --reload
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = FastAPI()

# TODO: SQL

class Item(BaseModel):
   name: str = Field(..., min_length=3, max_length=30)
   is_done: Optional[bool] = False

   @field_validator('name')
   @classmethod
   def name_must_contain_letters(cls, v):
      if not any(char.isalpha() for char in v):
         raise ValueError('Name must contain at least one letter')
      return v

todos : dict[str , Item] = {}

@app.get("/")
def index():
   return {"message" : "welcome"}

@app.get("/get-todos")

def get_todos(sort: Optional[bool] = None):
   """ Returns a list of all items in our TODO list """
   return sorted(todos) if sort else todos

@app.post("/add-todo")
def add_todo(todo : Item):
   """ Adds the given item to our list """
   if todo.name in todos:
      raise HTTPException( status_code= status.HTTP_400_BAD_REQUEST, detail=f"Error: Todo '{todo.name}' already exists" )
   todos[todo.name] = todo
   return {"message" : f"Added todo: {todo.name}"}

@app.post("/toggle-todo/{todo}")
def toggle_todo(todo_name : str):
   """ Toggles the status of the given todo """
   if todo_name not in todos: 
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
   todos[todo_name].is_done = not todos[todo_name].is_done
   return {f"{todo_name}" : f"{todos[todo_name].is_done}"}

@app.delete("/remove-todo/{todo}")
def remove_todo(todo_name : str):
   """ Deletes the given todo """
   if todo_name in todos:
      del todos[todo_name]
      return {"message" : f"Removed {todo_name}"}
   raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")