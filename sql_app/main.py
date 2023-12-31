from fastapi import FastAPI, HTTPException, status, Depends
from typing import Optional,List
from sqlalchemy.orm import Session

from . import schemas, models, hashing
from .database import engine, SessionLocal
from .schemas import Item


app = FastAPI()

models.Base.metadata.create_all(engine)


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

# TODO unique entries
@app.post("/create-todo", response_model = schemas.ShowItem,  status_code=status.HTTP_201_CREATED, tags = ['todos'])
def create_todo(request: schemas.Item, db: Session = Depends(get_db)):
   new_todo = models.Item(name = request.name, is_done = request.is_done, user_id = 1)
   db.add(new_todo)
   db.commit()
   db.refresh(new_todo)
   return new_todo

# TODO maybe sort?
@app.get("/get-todos", response_model = List[schemas.ShowItem], tags = ['todos'])
def get_todos(sort: Optional[bool] = None, db: Session = Depends(get_db)):
   """ Returns a list of all items in our TODO list """
   return db.query(models.Item).all()

@app.post("/toggle-todo/{todo}", tags = ['todos'])
def toggle_todo(todo_name : str, db: Session = Depends(get_db)):
   """ Toggles the status of the given todo """
   todo = db.query(models.Item).filter(models.Item.name == todo_name).first()
   if not todo: 
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
   
   todo.is_done = not todo.is_done
   db.commit()
   return {"message" : f"Updated {todo_name} as {todo.is_done}"}

@app.put("/update-todo/{id}", tags = ['todos'])
def update_todo(id : int, request : Item, db: Session = Depends(get_db)):
   todo = db.query(models.Item).filter(models.Item.id == id)
   if not todo.first(): 
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
   
   todo.update(request.model_dump())
   db.commit()
   return {"message" : "updated"}

@app.delete("/remove-todo/{todo}", status_code=status.HTTP_204_NO_CONTENT, tags = ['todos'])
def remove_todo(todo_name : str, db: Session = Depends(get_db)):
   """ Deletes the given todo """
   todo = db.query(models.Item).filter(models.Item.name == todo_name).delete(synchronize_session=False)
   db.commit()

   return {"message": "deleted"}

@app.post("/create-user", response_model = schemas.ShowUser, tags = ['users'])
def create_user(request : schemas.User, db: Session = Depends(get_db)):
   hashed_password = hashing.Hash.encrypt(request.password)
   new_user = models.User(name = request.name, email = request.email, password = hashed_password)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user

@app.get("/get-users", response_model = List[schemas.ShowUser], tags = ['users'])
def get_users(db: Session = Depends(get_db)):
   return db.query(models.Item).all()
