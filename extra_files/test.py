from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    ## not set it none mean its mandatory
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    ## to set it none mean it's not mandatory
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {
    # 1: {
    #     "name": "Milk",
    #     "price": 3.99,
    #     "brand": "Olper"
    # }
}


@app.get("/get-item/{item_id}")
async def get_item(item_id: int = Path(None, description="The Id of the item you like to view")):
    return inventory[item_id]


@app.get("/get_all_items")
async def get_all_items():
    return inventory


##http://127.0.0.1:8000/get-by-name?name="Behari kabab Pizza"

@app.get("/get-by-name")
## "*, name: Optional[str] = None, test: int" is called query parameters
async def get_item(name: str = Query(None, title="Name", description="Name of item.")):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item name not found")


@app.post("/create_item/{item_id}")
async def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item Id already exists"}

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item Id does not exists"}

    if item.name is not None:
        inventory[item_id].name = item.name

    if item.price is not None:
        inventory[item_id].price = item.price

    if item.brand is not None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete_item")
def delete_item(item_id: int = Query(..., description="The Id of the item to delete", gt=0)):
    if item_id not in inventory:
        return {"Error": "Item does not exist"}
    del inventory[item_id]
    return {"Success": "Item deleted!"}

