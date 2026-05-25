from fastapi import APIRouter, Response, Depends
from DB.CRUD.index import db
import uuid
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from time import time
from enum import Enum
from Routes.Users.index import verify_permission, verify_token
from Interfaces.index import *
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse

security = HTTPBearer()

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# class Products_Types(BaseModel):
#     Name: str
#     Details: str
#     ID_image: int
#     ID_storage: int
#     value: str
#     Token_product: str
#     Category: str
#     State: str

def create_product(product: Products_Types):
    id_product = db.Create_item("Products", 
                               "Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                               [product.Name, product.Details, product.ID_image, product.ID_storage,
                                product.value, product.Token_product, product.Category, product.State])

    return id_product

def find_product():
    pass

@router.post("/")
async def post_product(product: PostProduct):
    permission = verify_permission(product.token, 'CREATE', 'Products')

    if permission == False:
        return Response(content={"message": "Unauthorized"}, status_code=401)

    id_storage = db.Read("Storages", 
                    "ID, Name", 
                    f" WHERE ID = {product.product.ID_storage}")

    if len(id_storage) == 0:
        return Response(content={"message": "This storage does not exist"}, status_code=400)

    id_product = create_product(product.product)

    if len(id_product) == 0:
        return Response(content={"message": "Bad request"}, status_code=400)

    return Response(content={"id_product": id_product}, status_code=200)

@router.get("/", response_model=GetProduct,  response_model_exclude=["ID", "username"])
async def get_product(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        product: GetProduct = {"token": "", "id_product": None, "name": None, "token_product": None, "category": None, "state": None}
        permission = verify_permission(credentials.credentials, 'READ', 'Products')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        users = verify_token(credentials.credentials)

        if users == None or len(users) > 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=500)

        products = []

        if product.id_product != None:
            products = db.Read("Products", 
                            "ID, Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                            f" WHERE ID = {product.id_product}")
        elif product.name != None:
            products = db.Read("Products", 
                            "ID, Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                            f" WHERE Name = {product.name}")
        elif product.token_product != None:
            products = db.Read("Products", 
                            "ID, Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                            f" WHERE Token_product = {product.token_product}")
        elif product.category != None:
            products = db.Read("Products", 
                            "ID, Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                            f" WHERE Category = {product.category}")
        elif product.state != None:
            products = db.Read("Products", 
                            "ID, Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                            f" WHERE State = {product.state}")
        else:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        if len(product) > 0:
            return JSONResponse(content={"products": products}, status_code=200)

        return JSONResponse(content={"message": "Bad request"}, status_code=500)

    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.patch("/")
async def patch_product():
    return {
        "message": "ok"
    }

@router.put("/")
async def put_product():
    return {
        "message": "ok"
    }