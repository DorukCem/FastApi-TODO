from fastapi import FastAPI
from . import models
from .database import engine
from .routers import todo, users, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(todo.router)
app.include_router(users.router)


@app.get("/")
def index():
   return {"message" : "welcome"}


# TODO: Repsonse models