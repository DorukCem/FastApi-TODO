from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models

from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
   tags= ['todo']
) 

# TODO maybe sort?
@router.get("/get-todos" )
def get_todos(sort: Optional[bool] = None, db: Session = Depends(database.get_db)):
   """ Returns a list of all items in our TODO list """
   return db.query(models.Item).all()

# TODO unique entries
@router.post("/create-todo", status_code=status.HTTP_201_CREATED)
def create_todo(request: schemas.Item, db: Session = Depends(database.get_db)):
   new_todo = models.Item(name = request.name, is_done = request.is_done, user_id = 1)
   db.add(new_todo)
   db.commit()
   db.refresh(new_todo)
   return new_todo

@router.post("/toggle-todo/{todo}")
def toggle_todo(todo_name : str, db: Session = Depends(database.get_db)):
   """ Toggles the status of the given todo """
   todo = db.query(models.Item).filter(models.Item.name == todo_name).first()
   if not todo: 
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
   
   todo.is_done = not todo.is_done
   db.commit()
   return {"message" : f"Updated {todo_name} as {todo.is_done}"}

@router.put("/update-todo/{id}", )
def update_todo(id : int, request : schemas.Item, db: Session = Depends(database.get_db)):
   todo = db.query(models.Item).filter(models.Item.id == id)
   if not todo.first(): 
      raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
   
   todo.update(request.model_dump())
   db.commit()
   return {"message" : "updated"}

@router.delete("/remove-todo/{todo}", status_code=status.HTTP_204_NO_CONTENT )
def remove_todo(todo_name : str, db: Session = Depends(database.get_db)):
   """ Deletes the given todo """
   todo = db.query(models.Item).filter(models.Item.name == todo_name).delete(synchronize_session=False)
   db.commit()

   return {"message": "deleted"}