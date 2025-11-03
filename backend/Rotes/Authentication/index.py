from fastapi import APIRouter
from DB.CRUD.index import SQLite
import uuid
from passlib.context import CryptContext
from fastapi import Response
from pydantic import BaseModel
from datetime import datetime, timedelta
from time import time


class TokenRefresh(BaseModel):
    access: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def verify_permission():
    if "User_ADMIN":
        return True
    if "User_cashier" and "information_type == User_cashier_information":
        return True
    if "User_cashier" and ("information_type == User_cashier_information" or "information_type == User_logistic_information"):
        return True
    return False

db = SQLite('layout.json')

router = APIRouter(
    prefix="/authentication",
    tags=["authentication"]
)

@router.post("/token")
async def post_token(user: str, pw: str):
    access = None
    refresh = None

    users = db.Read("Users", "ID, ID_access_token, ID_refresh_Token, Username, pw", f" WHERE 'Username' = {user}")

    if len(users) > 0:
        for user in users:
            if pwd_context.verify_password(pw, user['pw']) == True:
                # buscar na lista de tokens os tokens access e refresh válidos                
                today = int(time()) #datetime.fromtimestamp(time()).strftime("%d/%m/%Y %H:%M:%S")

                access_list = db.Read("Authentications", "*", f" WHERE 'ID' = {user['ID_access_token']}")

                for token in access_list:
                    if int(token['Date expirate']) > today:
                        access = token['Token']
                        break

                refresh_list = db.Read("Authentications", "*", f" WHERE 'ID' = {user['ID_refresh_Token']}")

                for token in refresh_list:
                    if int(token['Date expirate']) > today:
                        refresh = token['Token']
                        break

                if access == None:
                    access = str(uuid.uuid4())
                    data_futura = datetime.now() + timedelta(days=30)
                    expirate = int(data_futura.timestamp())
                    db.Create_item("Authentications", "Token, Date_creation, Date expirate, ID_user", f"{access}, {today}, {expirate}, {user['ID']}")
                    db.Update("Users", 
                              f"{user['Name']}, {user['Date_creation']}, {access}, {user['ID_refresh_Token']}, {user['ID_permission_group']}, {
                                  user['User_type']}, {user['Username']}, {user['pw']}", 
                              f" WHERE 'ID' = {user['ID']}")

                if refresh == None:
                    refresh = str(uuid.uuid4())
                    data_futura = datetime.now() + timedelta(days=30)
                    expirate = int(data_futura.timestamp())
                    db.Create_item("Authentications", "Token, Date_creation, Date expirate, ID_user", f"{refresh}, {today}, {expirate}, {user['ID']}")
                    db.Update("Users", 
                              f"{user['Name']}, {user['Date_creation']}, {user['ID_access_token']}, {refresh}, {user['ID_permission_group']}, {
                                  user['User_type']}, {user['Username']}, {user['pw']}", 
                              f" WHERE 'ID' = {user['ID']}")

                break

        if access != None and refresh != None:
            return {
                "access": access,
                "refresh": refresh
            }
            
    return Response(content={"message": "Bad credencials"}, status_code=401)

@router.post("/token/refresh")
async def post_refresh(access: TokenRefresh):
    return { "access": f"your access {access.access}" }

@router.post("/token/verify")
async def post_verify():
    return {
        "detail": "Token is invalid",
        "code": "token_not_valid"
    }