from fastapi import FastAPI, HTTPException, status, Depends
from typing import Optional
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, SessionLocal
from .schemas import Item

app = FastAPI()

# TODO: SQL


def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

todos : dict[str , Item] = {}

@app.get("/")
def index():
   return {"message" : "welcome"}

@app.post("/test_db")
def create(request: schemas.Item, db: Session = Depends(get_db)):
   new_todo = models.Item(name = request.name, is_done = request.is_done)
   db.add(new_todo)
   db.commit()
   db.refresh(new_todo)
   return new_todo

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