from pydantic import BaseModel
from enum import Enum

class ErrorMessage(BaseModel):
    message: str

class ResponseToken(BaseModel):
    access: str
    refresh: str

class TokenRefresh(BaseModel):
    token: str

class ResponseUser(BaseModel):
    ID: int
    Name: str
    Date_creation: int
    access: str
    refresh: str
    User_type: str
    username: str

class User(BaseModel):
    username: str
    pw: str

class User_Types(str, Enum):
    ADMIN = "ADMIN"
    cashier = "cashier"
    logistic = "logistic"

class PostUser(BaseModel):
    token: str
    name: str
    user_type: User_Types
    username: str
    pw: str

class User_cashier(BaseModel):
    Name: str
    email: str
    Phone_number: int
    DDD_number: int
    Work_position: str
    Leader_email: str

class User_logistic(BaseModel):
    Name: str

class User_ADMIN(BaseModel):
    Name: str
    email: str

class GetUser(BaseModel):
    token: str
    user_id: int = None
    name: str = None
    username: str = None

class Products_Types(BaseModel):
    Name: str
    Details: str
    ID_image: int
    ID_storage: int
    value: str
    Token_product: str
    Category: str
    State: str

class PostProduct(BaseModel):
    token: str
    product: Products_Types

class GetProduct(BaseModel):
    token: str
    id_product: int = None
    name: str = None
    token_product: str = None
    category: str = None
    state: str = None