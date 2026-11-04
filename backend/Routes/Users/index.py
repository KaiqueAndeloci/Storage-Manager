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
        created = None
        db.Update("Authentications", ["Token", "Date_creation", 'Date_expirate', "ID_user"], 
                  [access, today, expirate, id_user], f"WHERE ID = {ID_access}")

        db.Update("Authentications",  ["Token", "Date_creation", 'Date_expirate', "ID_user"], 
                  [refresh, today, expirate, id_user], f"WHERE ID = {ID_refresh}")

        if user_object.UserType == "ADMIN":
            created = db.Create_item('User_ADMIN', 
                            "id_user, Name, Date_creation, email",
                            [id_user, user_object.Name, Date_creation, user_object.Email])
        elif user_object.UserType == "cashier":
            created = db.Create_item('User_cashier', 
                            "id_user, Name, Date_creation, email, Phone_number, DDD_number, Work_position, Leader_email",
                            [id_user, user_object.Name, Date_creation, user_object.Email, user_object.PhoneNumber, 
                             user_object.DDDNumber, user_object.WorkPosition, user_object.LeaderEmail])
        elif user_object.UserType == "logistic":
            created = db.Create_item('User_logistic', 
                            "id_user, Name, Date_creation, email, Phone_number, DDD_number, Work_position, Leader_email",
                            [id_user, user_object.Name, Date_creation, user_object.Email, user_object.PhoneNumber, 
                             user_object.DDDNumber, user_object.WorkPosition, user_object.LeaderEmail])

        if created == None:
            return None

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
                            "Name, Date_creation, User_type, ID", 
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
                    "ID": item[3],
                    "Name": item[0],
                    "DateCreation": str(datetime.fromtimestamp(float(item[1])).strftime("%d/%m/%Y")),
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

@router.get("/{user_id}/details", response_model=ResponseGetUser | None)
async def get_user(user_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'READ', 'Users')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        found = db.Read('Users', 'ID, Name, Date_creation, Username, User_type', f" WHERE ID = {user_id}")

        if found == None:
            return JSONResponse(content={"message": "Bad request"}, status_code=500)
        elif len(found) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=500)

        response = {
            "ID": found[0][0],
            "Name": found[0][1],
            "DateCreation": str(datetime.fromtimestamp(float(found[0][2])).strftime("%d/%m/%Y")),
            "UserType": found[0][4]
            }

        if found[0][4] == "ADMIN":
            found_ADMIN = db.Read('User_ADMIN', 'email', f" WHERE id_user = {found[0][0]}")
            response["Email"] = found_ADMIN[0][0]

        if found[0][4] == "cashier":
            found_cashier = db.Read('User_cashier', 'email, Phone_number, DDD_number, Work_position, Leader_email', f" WHERE id_user = {found[0][0]}")
            response["Email"] = found_cashier[0][0]
            response["PhoneNumber"] = found_cashier[0][1]
            response["DDDNumber"] = found_cashier[0][2]
            response["WorkPosition"] = found_cashier[0][3]
            response["LeaderEmail"] = found_cashier[0][4]

        if found[0][4] == "logistic":
            found_logistic = db.Read('User_logistic', 'email, Phone_number, DDD_number, Work_position, Leader_email', f" WHERE id_user = {found[0][0]}")
            response["Email"] = found_logistic[0][0]
            response["PhoneNumber"] = found_logistic[0][1]
            response["DDDNumber"] = found_logistic[0][2]
            response["WorkPosition"] = found_logistic[0][3]
            response["LeaderEmail"] = found_logistic[0][4]

        return JSONResponse(content=response, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

# get gropus of one user
@router.get("/{user_id}/groups")
async def get_group_permissions(user_id: Annotated[int, Field(gt=0)], filter_query: Annotated[GetMetaGroupUsers, Query()], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        response = []
        return JSONResponse(content=response, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

# get permissions for each group for one user
@router.get("/{user_id}/groups/permissions")
async def get_group_permissions(user_id: Annotated[int, Field(gt=0)], filter_query: Annotated[GetMetaGroupUsers, Query()], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'READ', 'Permissions_Group')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        users_group = db.Read("Meta_Group_Users", 
                            "ID, ID_user, ID_group, ID_user_added_by", 
                            f" WHERE ID_user = {user_id}")

        filter1 = []
        filter2 = f"ORDER BY {filter_query.OrderBy} ASC LIMIT {filter_query.Limit} OFFSET {filter_query.Offset}"
        filter3 = ""

        filter1.append(f"ID_user = {user_id}")

        if len(filter1) > 0:
            filter3 = f" WHERE "

            for index, filter in enumerate(filter1):
                if index > 0:
                    filter3 += f" And "

                filter3 += f"{filter}"
        permissions_response = []
        total = 0
        if users_group != None:
            if len(users_group) > 0:
                for index_group, group in enumerate(users_group):
                    group_permissions = db.Read("Meta_permissions", 
                                "ID, ID_permission, ID_group, Permission_type, Permission_name, ID_user_created_by", 
                                f" WHERE ID_group = {group[2]} {filter2}")

                    if group_permissions != None:
                        if len(group_permissions) > 0:
                            permissions_array = []
                            for permission_item in group_permissions:
                                permissions_array.append({
                                    "ID": permission_item[0], 
                                    "ID_permission": permission_item[1],
                                    "ID_group": permission_item[2],
                                    "Permission_type": permission_item[3],
                                    "Permission_name": permission_item[4],
                                    "ID_user_created_by": permission_item[5]
                                })
                            total = total + len(group_permissions)
                            permissions_response.append({
                                "IDGroup": group[2],
                                "Permissions": permissions_array
                            })


        response = {
            "GroupsDetails": permissions_response,
            "Total": total,
            "Limit": int(filter_query.Limit),
            "Offset": int(filter_query.Offset),
        }
        return JSONResponse(content=response, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

@router.patch("/{user_id}", response_model=int | None)
async def patch_user(user_id: int, user: PatchUser, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'UPDATE', 'Users')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        found = db.Read('Users', 'ID, Username, User_type', f" WHERE ID = {user_id}")

        if found == None:
            return JSONResponse(content={"message": "Bad request"}, status_code=500)
        elif len(found) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=500)

        user_id_returned = None
        user_updated = False
        today = int(time.time())

        if user.ResetPassword == True:
            access = f"{str(uuid.uuid4())}"
            refresh = f"{str(uuid.uuid4())}"
            data_futura = datetime.now() + timedelta(days=30)
            expirate = int(data_futura.timestamp())

            ID_access = db.Create_item("Authentications", "Token, Date_creation, 'Date_expirate', ID_user", 
                                    [access, today, expirate, user_id])

            ID_refresh = db.Create_item("Authentications", "Token, Date_creation, 'Date_expirate', ID_user", 
                                        [refresh, today, expirate, user_id])

            user_updated = db.Update("Users", 
                                 ["Name", "ID_access_token", "ID_refresh_Token", "User_type", "Username", "pw"], 
                                 [user.User.Name, ID_access, ID_refresh, user.User.UserType, user.User.Username, authentication.hash_password(f"{str(uuid.uuid4())}")],
                                 f" WHERE ID = {user_id}"
                                 )
        else:
            user_updated = db.Update("Users", 
                                 ["Name", "User_type", "Username"], 
                                 [user.User.Name, user.User.UserType, user.User.Username],
                                 f" WHERE ID = {user_id}"
                                 )

        if user_updated == True:
            user_id_returned = user_id
        else:
            return JSONResponse(content={"message": "Bad request"}, status_code=500)

        user_updated = False

        if found[0][2] != user.User.UserType:
            user_deleted = False
            # delete the old user and create the new user
            if found[0][2] == "ADMIN":
                user_deleted = db.Delete("User_ADMIN", f" WHERE id_user = {user_id}")
            elif found[0][2] == "cashier":
                user_deleted = db.Delete("User_cashier", f" WHERE id_user = {user_id}")
            elif found[0][2] == "logistic":
                user_deleted = db.Delete("User_logistic", f" WHERE id_user = {user_id}")

            if user_deleted == False:
                return JSONResponse(content={"message": "Bad request"}, status_code=500)
            user_created = None
            if user.User.UserType == "ADMIN":
                user_created = db.Create_item(
                    "User_ADMIN", 
                    "id_user, Name, Date_creation, email", 
                    [user_id, user.User.Name, today, user.User.Email]
                )
            elif user.User.UserType == "cashier":
                user_created = db.Create_item(
                    "User_cashier", 
                    "id_user, Name, Date_creation, email", 
                    [user_id, user.User.Name, user.User.Email, user.User.PhoneNumber, user.User.DDDNumber,
                      user.User.WorkPosition, user.User.LeaderEmail, today]
                )
            elif user.User.UserType == "logistic":
                user_created = db.Create_item(
                    "User_logistic", 
                    "id_user, Name, email, Phone_number, DDD_number, Work_position, Leader_email, Date_creation", 
                    [user_id, user.User.Name, user.User.Email, user.User.PhoneNumber, user.User.DDDNumber,
                      user.User.WorkPosition, user.User.LeaderEmail, today]
                )
            if user_created != None:
                user_updated = True
        else:
            # update the same user
            if user.User.UserType == "ADMIN":
                user_updated = db.Update("User_ADMIN", 
                                    ["Name", "email"], 
                                    [user.User.Name, user.User.Email],
                                    f" WHERE id_user = {user_id}"
                                    )
            elif user.User.UserType == "cashier":
                user_updated = db.Update("User_cashier", 
                                    ["Name", "email", "Phone_number", "DDD_number", "Work_position", "Leader_email"], 
                                    [user.User.Name, user.User.Email, user.User.PhoneNumber, user.User.DDDNumber,
                                      user.User.WorkPosition, user.User.LeaderEmail],
                                    f" WHERE id_user = {user_id}"
                                    )
            elif user.User.UserType == "logistic":
                user_updated = db.Update("User_logistic", 
                                    ["Name", "email", "Phone_number", "DDD_number", "Work_position", "Leader_email"], 
                                    [user.User.Name, user.User.Email, user.User.PhoneNumber, user.User.DDDNumber,
                                      user.User.WorkPosition, user.User.LeaderEmail],
                                    f" WHERE id_user = {user_id}"
                                    )
            
        if user_updated == False:
            return JSONResponse(content={"message": "Bad request"}, status_code=500)

        return JSONResponse(content={"User_updated": user_id_returned}, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

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

