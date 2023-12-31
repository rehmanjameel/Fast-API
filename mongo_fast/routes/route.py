from fastapi import APIRouter
from mongo_fast.model.todos import Todo
from mongo_fast.config.db_mongo import collection_name
from mongo_fast.schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()


# Get Request Method
@router.get("/get_todo")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos


# POST Request Method
@router.post("/add_todo")
async def post_todo(todo: Todo):
    collection_name.insert_one(dict(todo))


# UPDATE Request Method
@router.put("/update_todo/{id}")
async def update_todo(id: str, todo: Todo):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})


# DELETE Request Method
@router.delete("/delete_todo/{id}")
async def delete_todo(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
