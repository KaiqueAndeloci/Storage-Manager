from fastapi import APIRouter, Response
from DB.CRUD.index import db
from pydantic import BaseModel
from datetime import datetime, timedelta
import time
import bcrypt, uuid
from Interfaces.index import *
from fastapi.responses import JSONResponse, RedirectResponse

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/authentication",
    tags=["authentication"]
)

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5


# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
#     "baz": {
#         "name": "Baz",
#         "description": "There goes my baz",
#         "price": 50.2,
#         "tax": 10.5,
#     },
# }

# @router.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include=["name", "description"],
# )
# async def read_item_name(item_id: str):
#     return items[item_id]

# @router.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
# async def read_item_public_data(item_id: str):
#     return items[item_id]

# @app.get("/portal")
# async def get_portal(teleport: bool = False) -> Response:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return JSONResponse(content={"message": "Here's your interdimensional portal."})

def hash_password(password: str) -> bytes:
    # return pwd_context.hash(password.encode())

    salt = bcrypt.gensalt(14)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # return pwd_context.verify(plain_password, hashed_password)
    return bcrypt.checkpw(plain_password.encode(), hashed_password)

def verify_permission():
    if "User_ADMIN":
        return True

    if "User_cashier" and "information_type == User_cashier_information":
        return True

    if "User_cashier" and ("information_type == User_cashier_information" or "information_type == User_logistic_information"):
        return True

    return False

def get_tokens(user_obj) -> tuple[str | None, str | None]:
    access = None
    refresh = None

    # buscar na lista de tokens os tokens access e refresh válidos                
    today = int(time.time()) #datetime.fromtimestamp(time()).strftime("%d/%m/%Y %H:%M:%S")

    access_list = db.Read("Authentications", "ID, Token, Date_creation, Date_expirate, ID_user", 
                    f" WHERE ID = {user_obj[3]}")

    for token in access_list:
        if int(token[3]) > today:
            access = token[1]
            break

    refresh_list = db.Read("Authentications", "ID, Token, Date_creation, Date_expirate, ID_user", 
                            f" WHERE ID = {user_obj[4]}")

    for token in refresh_list:
        if int(token[3]) > today:
            refresh = token[1]
            break

    return (access, refresh)

def create_tokens(user_obj, access: None | str, refresh: None | str) -> tuple[str, str]:
    # buscar na lista de tokens os tokens access e refresh válidos                
    today = int(time.time()) #datetime.fromtimestamp(time()).strftime("%d/%m/%Y %H:%M:%S")
    returned_access = access
    returned_refresh = refresh

    if returned_access == None:
        returned_access = str(uuid.uuid4())
        data_futura = datetime.now() + timedelta(days=30)
        expirate = int(data_futura.timestamp())
        id_access = db.Create_item("Authentications", "Token, Date_creation, Date_expirate, ID_user", 
                                [returned_access, today, expirate, user_obj[0]])
        db.Update("Users", ["Name", "Date_creation", "ID_access_token", "ID_refresh_Token", "Username", "pw"], 
                [user_obj[1], user_obj[2], id_access, user_obj[4], user_obj[5], user_obj[6]], f" WHERE ID = {user_obj[0]}")

    if returned_refresh == None:
        returned_refresh = str(uuid.uuid4())
        data_futura = datetime.now() + timedelta(days=30)
        expirate = int(data_futura.timestamp())
        id_refresh = db.Create_item("Authentications", "Token, Date_creation, Date_expirate, ID_user", 
                                    [returned_refresh, today, expirate, user_obj[0]])
        db.Update("Users", ["Name", "Date_creation", "ID_refresh_Token", "Username", "pw"], 
                    [user_obj[1], user_obj[2], id_refresh, user_obj[5], user_obj[6]], f" WHERE ID = {user_obj[0]}")

    return (returned_access, returned_refresh)

@router.post("/token", response_model=ResponseToken)
async def post_token(user: User) -> Response:
    access = None
    refresh = None

    try:
        users = db.Read("Users", "ID, Name, Date_creation, ID_access_token, ID_refresh_Token, Username, pw", 
                        f" WHERE Username = '{user.username}'")

        if users != None:
            if len(users) > 0:
                for user_obj in users:
                    if verify_password(user.pw, user_obj[6]) == True:
                        access, refresh = get_tokens(user_obj)

                        access, refresh = create_tokens(user_obj, access, refresh)
                        break

                if access != None and refresh != None:
                    return {
                        "access": access,
                        "refresh": refresh
                    }

    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)

    return JSONResponse(content={"message": "Bad credencials"}, status_code=401)


@router.post("/token/refresh")
async def post_refresh(refresh: TokenRefresh):
    access = None
    refresh_authentication = db.Read("Authentications", "ID, Token, Date_creation, Date_expirate, ID_user", f" WHERE Token = '{refresh.token}'")
    today = int(time.time())

    for refresh_auth in refresh_authentication:
        if int(refresh_auth[3]) > today:
            users = db.Read("Users", "ID, Name, Date_creation, ID_access_token, ID_refresh_Token, Username, pw", f" WHERE ID = {refresh_auth['ID_user']}")

            for user in users:
                access_authentication = db.Read("Authentications", "ID, Token, Date_creation, 'Date_expirate', ID_user", 
                                                f" WHERE 'ID' = {user[3]}")

                for access_auth in access_authentication:
                    if int(access_auth[3]) > today:
                        access = access_auth[1]

                        break

                if access == None:
                    access = str(uuid.uuid4())
                    data_futura = datetime.now() + timedelta(days=30)
                    expirate = int(data_futura.timestamp())
                    id_access = db.Create_item("Authentications", "Token, Date_creation, 'Date_expirate', ID_user", 
                                   [access, today, expirate, user[0]])
                    db.Update('Users', ["Name", "Date_creation", "ID_access_token", "ID_refresh_Token", "Username", "pw"], 
                              [user[1], user[2], id_access, user[4], user[5], user[6]], f" WHERE 'ID' = {user[0]}")
                break

            break

    if access != None:
        return { "access": access }

    return Response(content={"message": "Bad credencials"}, status_code=401)

@router.post("/token/verify")
async def post_verify(token: TokenRefresh):
    authentication = db.Read("Authentications", "ID, Token, Date_creation, 'Date_expirate', ID_user", 
                             f" WHERE 'Token' = {token.token}")
    today = int(time.time())

    for auth in authentication:
        if int(auth['Date expirate']) > today:
            return {
                'Date expirate': auth['Date expirate']
            }

    return Response(content={"message": "Token is invalid"}, status_code=401)