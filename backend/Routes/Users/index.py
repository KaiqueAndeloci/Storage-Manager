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
from typing import Annotated

security = HTTPBearer()

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def verify_token(credentials: str | None):
    token = credentials
    users = None

    if token != None and token != "":
        token_list = None
        today = int(time.time())
        token_list = db.Read("Authentications", 
                "ID, Token, Date_creation, Date_expirate, ID_user", 
                f" WHERE Date_expirate > {today} AND Token = '{token}'")

        if token_list != None:
            if len(token_list) > 0:
                users = db.Read("Users", "ID, Name, Date_creation, ID_access_token, ID_refresh_Token, User_type, Username", 
                                f" WHERE ID_access_token = {token_list[0][0]}")

    return users

def verify_permission(token: str, action_type: str, name_permission: str):
    autorized = False
    tokens = db.Read("Authentications", "ID, Token, Date_expirate, ID_user", f" WHERE Token = '{token}'")
    if tokens == None:
        tokens = []


    if len(tokens) > 0:
        today = int(time.time())

        for token in tokens:
            if int(token[2]) > today:
                groups = db.Read("Meta_Group_Users", "ID, ID_user, ID_group",
                                f" WHERE ID_user = {token[3]}")
                if groups == None:
                    groups = []

                for group in groups:
                    permissions = db.Read("Meta_permissions", 
                                        "ID, ID_permission, ID_group, Permission_type, Permission_name, ID_user_created_by", 
                                        f" WHERE ID_group = {group[2]} AND Permission_type = '{action_type}' AND Permission_name = '{name_permission}'")

                    if permissions == None:
                        permissions = []

                    if len(permissions) > 0:
                        autorized = True

                        break

                break

    return autorized

def create_user(Username: str, pw: str, user_object: Union[AdminUser, CashierUser, LogisticUser] = Field(discriminator="UserType")):
    Date_creation = int(time.time())
    access = f"{str(uuid.uuid4())}"
    refresh = f"{str(uuid.uuid4())}"
    today = int(time.time())
    data_futura = datetime.now() + timedelta(days=30)
    expirate = int(data_futura.timestamp())

    ID_access = db.Create_item("Authentications", "Token, Date_creation, 'Date_expirate', ID_user", 
                               [access, today, expirate, 0])

    ID_refresh = db.Create_item("Authentications", "Token, Date_creation, 'Date_expirate', ID_user", 
                                [refresh, today, expirate, 0])

    id_user = db.Create_item('Users', "Name, Date_creation, ID_access_token, ID_refresh_Token, User_type, Username, pw",
                             [user_object.Name, Date_creation, ID_access, ID_refresh, user_object.UserType, Username, pw])

    if id_user != None:
        db.Update("Authentications", ["Token", "Date_creation", 'Date_expirate', "ID_user"], 
                  [access, today, expirate, id_user], f"WHERE ID = {ID_access}")

        db.Update("Authentications",  ["Token", "Date_creation", 'Date_expirate', "ID_user"], 
                  [refresh, today, expirate, id_user], f"WHERE ID = {ID_refresh}")

        if user_object.UserType == "ADMIN":
            id_user = db.Create_item('User_ADMIN', 
                            "id_user, Name, Date_creation, email",
                            [id_user, user_object.Name, Date_creation, user_object.Email])
        elif user_object.UserType == "cashier":
            id_user = db.Create_item('User_cashier', 
                            "id_user, Name, Date_creation, email, Phone_number, DDD_number, Work_position, Leader_email",
                            [id_user, user_object.Name, Date_creation, user_object.Email, user_object.PhoneNumber, 
                             user_object.DDDNumber, user_object.WorkPosition, user_object.LeaderEmail])
        elif user_object.UserType == "logistic":
            id_user = db.Create_item('User_logistic', 
                            "id_user, Name, Date_creation, email, Phone_number, DDD_number, Work_position, Leader_email",
                            [id_user, user_object.Name, Date_creation, user_object.Email, user_object.PhoneNumber, 
                             user_object.DDDNumber, user_object.WorkPosition, user_object.LeaderEmail])

    return id_user

def find_user_type(user_objct: list, user_type: User_Types) -> None | list:
    user_return = None

    if user_type == "ADMIN":
        user_return = db.Read("User_ADMIN", 
                        "ID, id_user, Name, Date_creation, email", 
                        f" WHERE id_user = {user_objct[0]}")
    if user_type == "cashier":
        user_return = db.Read("User_cashier", 
                        "ID, id_user, Name, Date_creation, email, Phone_number, DDD_number, Work_position, Leader_email", 
                        f" WHERE id_user = {user_objct[0]}")
    if user_type == "logistic":
        user_return = db.Read("User_logistic", 
                        "ID, id_user, Name, Date_creation, email, Phone_number, DDD_number, Work_position, Leader_email", 
                        f" WHERE id_user = {user_objct[0]}")
    return user_return

@router.post("", response_model=int | None)
async def post_user(user: PostUser, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users_found = verify_token(credentials.credentials)
        if users_found == None:
            users_found = []

        if len(users_found) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'CREATE', 'Users')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        found = db.Read('Users', 'ID, Username', f" WHERE Username = '{user.User.Username}'")

        if found == None:
            found = []

        User_created = None

        if len(found) == 0:
            password = authentication.hash_password(user.User.PW)

            User_created = create_user(user.User.Username, password, user.User)
            password = None

        if User_created != None:
            return JSONResponse(content={"User_created": User_created}, status_code=200)

        return JSONResponse(content={"message": "Bad request"}, status_code=500)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.get("", response_model=ResponseGetUsers | None)
async def get_user(filter_query: Annotated[GetUsers, Query()], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'READ', 'Users')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        users = []

        filter1 = []
        filter2 = f"ORDER BY {filter_query.OrderBy} ASC LIMIT {filter_query.Limit} OFFSET {filter_query.Offset}"
        filter3 = ""

        if filter_query.UserType != None:
            filter1.append(f"User_type = '{filter_query.UserType[0:]}'")

        if filter_query.Name != None:
            filter1.append(f"Name = '{filter_query.Name}'")

        if filter_query.DateCreation != None:
            filter1.append(f"Date_creation = '{filter_query.DateCreation}'")

        if len(filter1) > 0:
            filter3 = f" WHERE "

            for index, filter in enumerate(filter1):
                if index > 0:
                    filter3 += f" And "

                filter3 += f"{filter}"

        users = db.Read("Users", 
                            "Name, Date_creation, User_type", 
                            f"{filter3} {filter2}")
        total = db.Read("Users", "COUNT(*)", f"{filter3}")

        if users == None:
            users = []
            response = {
                "Users": users,
                "Total": 0,
                "Limit": int(filter_query.Limit),
                "Offset": int(filter_query.Offset),
            }
            return JSONResponse(content=response, status_code=200)

        if len(users) > 0:
            users_copy = users
            users = []
            for item in users_copy:
                users.append({
                    "Name": item[0],
                    "DateCreation": item[1],
                    "UserType": item[2]
                })

        if total == None:
            total = 0
        else:
            total = total[0][0]

        response = {
            "Users": users,
            "Total": int(total),
            "Limit": int(filter_query.Limit),
            "Offset": int(filter_query.Offset),
        }

        return JSONResponse(content=response, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.patch("/")
async def patch_user():
    return {
        "message": "ok"
    }

@router.put("/")
async def put_user():
    return {
        "message": "ok"
    }

@router.delete("/")
async def delete_user():
    return {
        "message": "ok"
    }

@router.get("/me", response_model=ResponseMe,  response_model_exclude=["ID", "username"])
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)

        if users != None:
            if len(users) > 0:
                access, refresh = authentication.get_tokens(users[0])

                specific_user = find_user_type(users[0], users[0][5])
                formated = str(datetime.fromtimestamp(float(users[0][2])).strftime("%d/%m/%Y"))

                return JSONResponse(content=
                    {
                        "Name": users[0][1],
                        "DateCreation": formated,
                        "access": access,
                        "refresh": refresh,
                        "UserType": users[0][5],
                        "email": specific_user[0][4]
                    }, 
                    status_code=200)

        return JSONResponse(content={"message": "Bad request"}, status_code=500)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)
