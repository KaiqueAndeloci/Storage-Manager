from fastapi import APIRouter, Response
from DB.CRUD.index import db
import uuid
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from time import time
from enum import Enum
from Routes.Users.index import verify_permission


router = APIRouter(
    prefix="/storages",
    tags=["storages"]
)

class Storages_Interface(BaseModel):
    name: str
    description: str
    state: int
    items_count: int
    maximum_size: str
    minimum_size: str
    export_storage_id: str
    import_storage_id: str
    notify_id: int

def create_storage(storage: Storages_Interface):
    storage_id = db.Create_item("Storages", 
                               "Name, Description, State, Items_count, Maximum_Size, Minimum_Size, Export_Storage_id, Import_Storage_id, Notify_id", 
                               [storage.name, storage.description, storage.state, storage.items_count, storage.maximum_size,
                                storage.minimum_size, storage.export_storage_id, storage.import_storage_id, storage.notify_id])

    return storage_id

@router.post("/")
async def post_storage(token: str, storage: Storages_Interface):
    permission = verify_permission(token, 'CREATE', 'Storages')

    if permission == False:
        return Response(content={"message": "Unauthorized"}, status_code=401)

    storages = db.Read("Storages",
                       "ID, Name",
                       f" WHERE Name = {storage.name}")

    if len(storages) > 0:
        return Response(content={"message": "This storage name is already in use"}, status_code=400)

    id_storage = create_storage(storage)

    if len(id_storage) == 0:
        return Response(content={"message": "Bad request"}, status_code=400)

    return Response(content={"id_storage": id_storage}, status_code=200)

@router.get("/")
async def get_storage(token: str, name: str = None, state: str = None, items_count: int = None):
    permission = verify_permission(token, 'READ', 'Storages')

    if permission == False:
        return Response(content={"message": "Unauthorized"}, status_code=401)

    storages = []

    if name != None:
        storages = db.Read("Storages", 
                        "ID, Name, Description, State, Items_count, Maximum_Size, Minimum_Size, Export_Storage_id, Import_Storage_id, Notify_id",
                        f" WHERE Name = {name}")
    elif state != None:
        storages = db.Read("Storages", 
                        "ID, Name, Description, State, Items_count, Maximum_Size, Minimum_Size, Export_Storage_id, Import_Storage_id, Notify_id",
                        f" WHERE State = {state}")
    elif items_count != None:
        storages = db.Read("Storages", 
                        "ID, Name, Description, State, Items_count, Maximum_Size, Minimum_Size, Export_Storage_id, Import_Storage_id, Notify_id",
                        f" WHERE Items_count = {items_count}")
    else:
        return Response(content={"message": "Bad request"}, status_code=400)

    return Response(content={"id_storage": storages}, status_code=200)

@router.patch("/")
async def patch_storage():
    pass

@router.put("/")
async def put_storage():
    pass

@router.delete("/")
async def delete_storage():
    pass