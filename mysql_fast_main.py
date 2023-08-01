from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from fast_mysql import models
from fast_mysql.mysql_database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# this class is for out data validation i.e (when request come in we will validate the data
# and then return the correct response)
class PostBase(BaseModel):
    title: str
    content: str
    user_id: int


class UserBase(BaseModel):
    username: str


# method to get db
# where we can create db for our session local
def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        # closing db means we don't want to keep open the db connection for too long
        db.close()


db_dependency = Annotated[Session, Depends(get_db())]


