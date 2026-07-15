from fastapi import APIRouter, Response, Depends, Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials
from DB.CRUD.index import db
import uuid
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
import time
from enum import Enum
from Routes.Authentication import index as authentication
from Interfaces.index import *
from fastapi.security import HTTPBearer
from Routes.Users.index import verify_permission, verify_token
from typing import Annotated


security = HTTPBearer()

router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)

# criar rotas para grupos
# especialmente Meta_Group_Users

def add_user_on_group(ID_user: int, ID_group: int, ID_user_added_by: int) -> None | int:
    groups = db.Read("Permissions_Group", "ID, Group_name", 
                     f" WHERE ID = {ID_group}")

    if groups == None:
        return None

    if len(groups) > 0:
        users = db.Read("Users", "ID, Name", f" WHERE ID = {ID_user}")

        if users == None:
            return None

        if len(users) > 0:
            id_response = db.Create_item("Meta_Group_Users", 
                                         "ID_user, ID_group, ID_user_added_by", 
                                         [ID_user, ID_group, ID_user_added_by])

            return id_response

    return None

# find in Meta_Group_Users
def find_user_in_group(ID_user: int):
    groups = db.Read("Meta_Group_Users", "ID, ID_user, ID_group, ID_user_created_by", 
                     f" WHERE ID_user = {ID_user}")
    return groups


# edit group
@router.post("", response_model=int | None)
async def post_group(group: Groups_Types, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'CREATE', 'Permissions_Group')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        id_group = db.Create_item("Permissions_Group", 
                               "Group_name, Group_description, ID_user_created_by", 
                               [group.GroupName, group.GroupDescription, users[0][0]])

        if id_group != None:
            return JSONResponse(content={"id_group": id_group}, status_code=200)

        return JSONResponse(content={"message": "Bad request"}, status_code=500)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.get("", response_model=ResponseGetGroup | None)
async def get_group(filter_query: Annotated[GetGroup, Query()], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'READ', 'Permissions_Group')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        groups = []

        filter1 = []
        filter2 = f"ORDER BY {filter_query.order_by} ASC LIMIT {filter_query.limit} OFFSET {filter_query.offset}"
        filter3 = ""

        if filter_query.id_group != None:
            filter1.append(f"ID = {filter_query.id_group}")

        if filter_query.GroupName != None:
            filter1.append(f"Group_name = '{filter_query.GroupName}'")

        if len(filter1) > 0:
            filter3 = f" WHERE "

            for index, filter in enumerate(filter1):
                if index > 0:
                    filter3 += f" And "

                filter3 += f"{filter}"

        groups = db.Read("Permissions_Group", 
                            "ID, Group_name, Group_description, ID_user_created_by", 
                            f"{filter3} {filter2}")

        if groups == None:
            groups = []
            return JSONResponse(content={"products": groups}, status_code=200)

        if len(groups) > 0:
            groups_copy = groups
            for index, item in enumerate(groups_copy):
                groups[index] = {
                    "ID": item[0],
                    "GroupName": item[1],
                    "GroupDescription": item[2],
                    "IDUserCreatedBy": item[3],
                }

        return JSONResponse(content={"groups": groups}, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.patch("/{id_group}", response_model=int | None)
async def patch_group(id_group: int, group: Groups_Types, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'CREATE', 'Permissions_Group')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        id_group = db.Update("Permissions_Group", 
                               "Group_name, Group_description, ID_user_created_by", 
                               [group.GroupName, group.GroupDescription, users[0][0]], 
                               F" WHERE ID = {id_group}")

        if id_group != None:
            return JSONResponse(content={"id_group": id_group}, status_code=200)

        return JSONResponse(content={"message": "Bad request"}, status_code=500)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.delete("/{id_group}", response_model=bool)
async def delete_group(id_group: int, group: Groups_Types, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'CREATE', 'Permissions_Group')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        is_deleted = db.Delete("Permissions_Group", 
                               F" WHERE ID = {id_group}")

        return JSONResponse(content={"is_deleted": is_deleted}, status_code=200)

    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

# add users on group
@router.post("/users", response_model=list[int] | None)
async def post_group_users(group: list[UsersInGroup], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        id_users_added = []
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'CREATE', 'Meta_Group_Users')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
        
        for index, item_group in enumerate(group):
            for item_user in group[index].users:
                id_users_added.append(db.Create_item("Meta_Group_Users", 
                                    "ID_user, ID_group, ID_user_added_by", 
                                    [item_user.ID, item_group.ID, users[0][0]]))

        return JSONResponse(content={"id-users-added": id_users_added}, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

# remove users on group
@router.delete("/users", response_model=list[bool] | None)
async def delete_group_users(groups: list[int], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        id_users_removed = []
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'DELETE', 'Meta_Group_Users')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
        
        for item in groups:
            id_users_removed.append(db.Delete("Meta_Group_Users", f" WHERE ID = {item}"))

        return JSONResponse(content={"id-users-removed": id_users_removed}, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

# edit the users on group
@router.patch("/users")
async def delete_group_users():
    return JSONResponse(content={"message": "Bad request"}, status_code=500)

# create permissions to the group
@router.post("/permissions")
async def post_group_permissions():
    return JSONResponse(content={"message": "Bad request"}, status_code=500)

# edit permissions to the group
@router.patch("/permissions")
async def patch_group_permissions():
    return JSONResponse(content={"message": "Bad request"}, status_code=500)

# get permissions on the group
@router.get("/permissions")
async def get_group_permissions():
    return JSONResponse(content={"message": "Bad request"}, status_code=500)

# remove permissions on group
@router.delete("/permissions")
async def delete_group_permissions():
    return JSONResponse(content={"message": "Bad request"}, status_code=500)