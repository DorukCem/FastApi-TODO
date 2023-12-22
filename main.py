# uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
   name: str
   is_done: bool | None = False

todos : dict[str , Item] = {}

@app.get("/")
def index():
   return {"message" : "welcome"}

@app.get("/get-todos")
def get_todos():
   return todos

@app.post("/add-todo")
def add_todo(todo : Item):
   if todo.name in todos:
      return {f"Error: {todo} already in todos list"}
   todos[todo.name] = todo
   return {"message" : f"Added todo: {todo.name}"}

@app.post("/toggle-todo/{todo}")
def toggle_todo(todo_name : str):
   if todo_name not in todos: 
      return {f"Error: {todo_name} not in todos list"}
   todos[todo_name].is_done = not todos[todo_name].is_done
   return {f"{todo_name}" : f"{todos[todo_name].is_done}"}

@app.delete("/remove-todo/{todo}")
def remove_todo(todo_name : str):
   if todo_name in todos:
      del todos[todo_name]
      return {"message" : f"Removed {todo_name}"}
   return {"message" : f"{todo_name} was not in todos"}