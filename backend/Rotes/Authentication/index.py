from fastapi import APIRouter
from DB.CRUD.index import SQLite
import uuid
from passlib.context import CryptContext
from fastapi import Response


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
    access = str(uuid.uuid4())
    refresh = str(uuid.uuid4())

    users = db.Read("Users", "ID, ID_access_token, ID_refresh_Token, Username, pw", f" WHERE 'Username' = {user}")

    if len(users) > 0:
        id_access = 0
        id_refresh = 0
        for line in users:
            if pwd_context.verify(pw, line['pw']) == True:
                # buscar na lista de tokens os tokens access e refresh válidos
                access = db.Read("Authentications", "*", f" WHERE 'ID' = {line['ID_access_token']}")
                break
    else:
        return Response(content={"message": "Bad credencials"}, status_code=401)

    return {
        "access": access,
        "refresh": refresh
    }

@router.post("/token/refresh")
async def post_refresh():
    return { "access": "string" }

@router.post("/token/verify")
async def post_verify():
    return {
        "detail": "Token is invalid",
        "code": "token_not_valid"
    }