from datetime import datetime

from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional, Union
from pydantic import BaseModel
from fastapi import Depends

app = FastAPI()


class Person:
    def __init__(self, name: str):
        self.name = name


def get_person_name(one_person: Person):
    return one_person.name


class Item(BaseModel):
    # name: str
    # price: float
    # is_offer: Union[bool, None] = None
    id: int
    name = "john doe"
    signup_ts: datetime | None = None
    friends: list[int] = []


external_data = {
    "id": "23",
    "signup_ts": "2023-01-31 12:22",
    "friends": [1, "2", b"3"],
}

user = Item(**external_data)
print(user)
print(user.name)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def say_hello(item_id: int, q: Union[str, None] = None, ):
    return {"item_d": {item_id}, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}
