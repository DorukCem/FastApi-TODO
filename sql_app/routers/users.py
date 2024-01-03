from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, hashing

from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/create-user", response_model = schemas.ShowUser, tags = ['users'])
def create_user(request : schemas.User, db: Session = Depends(database.get_db)):
   hashed_password = hashing.Hash.encrypt(request.password)
   new_user = models.User(name = request.name, email = request.email, password = hashed_password)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user

@router.get("/get-users", response_model = List[schemas.ShowUser], tags = ['users'])
def get_users(db: Session = Depends(database.get_db)):
   return db.query(models.Item).all()