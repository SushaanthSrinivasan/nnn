from fastapi import APIRouter
from backend.models.item import Item
from backend.schemas.item import ItemSchema

router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    return item

@router.get("/items/")
def read_items():
    return [{"name": "Item 1", "price": 10.99}, {"name": "Item 2", "price": 5.99}]

@router.get("/items/{item_id}")
def read_item(item_id: int):
    return {"name": f"Item {item_id}", "price": 9.99}