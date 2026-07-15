from fastapi import APIRouter, Response, Depends, Query
from DB.CRUD.index import db
import uuid
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from time import time
from enum import Enum
from Routes.Users.index import verify_permission, verify_token
from Interfaces.index import *
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from typing import Annotated



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

@router.post("", response_model=int | None,  response_model_exclude=["ID", "username"])
async def post_product(product: Products_Types, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'CREATE', 'Products')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        id_product = db.Create_item("Products", 
                               "Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                               [product.Name, product.Details, product.ID_image, product.ID_storage,
                                product.value, product.Token_product, product.Category, product.State])

        if id_product != None:
            return JSONResponse(content={"id_product": id_product}, status_code=200)

        return JSONResponse(content={"message": "Bad request"}, status_code=500)

    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.get("", response_model=ResponseGetProduct | None)
async def get_product(filter_query: Annotated[GetProduct, Query()], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'READ', 'Products')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        products = []
        if filter_query.category == None:
            filter_query.category = []

        filter1 = []
        filter2 = f"ORDER BY {filter_query.order_by} ASC LIMIT {filter_query.limit} OFFSET {filter_query.offset}"
        filter3 = ""

        if filter_query.id_product != None:
            filter1.append(f"ID = {filter_query.id_product}")

        if filter_query.name != None:
            filter1.append(f"Name = '{filter_query.name}'")

        if filter_query.token_product != None:
            filter1.append(f"Token_product = '{filter_query.token_product}'")

        if len(filter_query.category) > 0:
            for category in filter_query.category:

                filter1.append(f"Category = '{category}'")

        if filter_query.state != None:
            filter1.append(f"State = '{filter_query.state}'")

        if len(filter1) > 0:
            filter3 = f" WHERE "

            for index, filter in enumerate(filter1):
                if index > 0:
                    filter3 += f" And "

                filter3 += f"{filter}"

        products = db.Read("Products", 
                            "ID, Name, Details, ID_image, ID_storage, value, Token_product, Category, State", 
                            f"{filter3} {filter2}")

        if products == None:
            products = []
            return JSONResponse(content={"products": products}, status_code=200)

        if len(products) > 0:
            products_copy = products
            products = []
            for item in products_copy:
                products.append({
                    "ID": item[0],
                    "Name": item[1],
                    "Details": item[2],
                    "ID_image": item[3],
                    "ID_storage": item[4],
                    "value": item[5],
                    "Token_product": item[6],
                    "Category": item[7],
                    "State": item[8]
                })

        return JSONResponse(content={"products": products}, status_code=200)

    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.patch("")
async def patch_product():
    return {
        "message": "ok"
    }

@router.put("")
async def put_product():
    return {
        "message": "ok"
    }