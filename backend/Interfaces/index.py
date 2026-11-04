from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Literal, Union

class ErrorMessage(BaseModel):
    message: str

class ResponseToken(BaseModel):
    access: str
    refresh: str

class TokenRefresh(BaseModel):
    token: str

class User_Types(str, Enum):
    ADMIN = "ADMIN"
    cashier = "cashier"
    logistic = "logistic"

class ResponseUser(BaseModel):
    ID: int
    Name: str
    DateCreation: str
    UserType: User_Types

class ResponseMe(BaseModel):
    Name: int
    DateCreation: str
    access: str
    refresh: str
    UserType: User_Types
    email: str

class User(BaseModel):
    username: str
    pw: str

class ModelResponseUser(BaseModel):
    Name: str = Field(min_length=1, max_length=100)
    DateCreation: None | str = Field(min_length=1, max_length=150)
    UserType: User_Types

class ModelResponseMe(ModelResponseUser):
    access: str
    refresh: str

class BaseUser(ModelResponseUser):
    Username: str = Field(min_length=1, max_length=100)
    PW: str = Field(min_length=10, max_length=100)
    Email: EmailStr = Field(min_length=1, max_length=100)

class AdminUser(BaseUser):
    UserType: Literal["ADMIN"]
    IDUser: int = Field(ge=1, le=10000000000000000000000000000000000)

class CashierUser(BaseUser):
    UserType: Literal["cashier"]
    IDUser: int = Field(ge=1, le=10000000000000000000000000000000000)
    PhoneNumber: int = Field(ge=1, le=10000000000000000000000000000000000)
    DDDNumber: int = Field(ge=1, le=10000000000000000000000000000000000)
    WorkPosition: str = Field(min_length=1, max_length=100)
    LeaderEmail: EmailStr = Field(min_length=1, max_length=100)

class LogisticUser(BaseUser):
    UserType: Literal["logistic"]
    IDUser: int = Field(ge=1, le=10000000000000000000000000000000000)
    PhoneNumber: int = Field(ge=1, le=10000000000000000000000000000000000)
    DDDNumber: int = Field(ge=1, le=10000000000000000000000000000000000)
    WorkPosition: str = Field(min_length=1, max_length=100)
    LeaderEmail: EmailStr = Field(min_length=1, max_length=100)

class PostUser(BaseModel):
    User: Union[AdminUser, CashierUser, LogisticUser] = Field(discriminator="UserType")

class PatchUser(PostUser):
    ResetPassword: bool

class GetUsers(ModelResponseUser):
    Limit: int = Field(gt=0, le=100)
    Offset: int = Field(ge=0)
    OrderBy: Literal["ID", "Name", "DateCreation", "UserType"] = "ID"
    Name: str | None = Field(default=None, min_length=1, max_length=100)
    DateCreation: str | None = Field(default=None, min_length=1, max_length=150)
    UserType: None | User_Types = None

class ResponseGetUsers(BaseModel):
    Users: list[ModelResponseUser]
    Total: int
    Limit: int = Field(gt=0, le=100)
    Offset: int = Field(ge=0)

class ResponseGetUser(BaseModel):
    User: Union[AdminUser, CashierUser, LogisticUser] = Field(discriminator="UserType")

class Groups_Types(BaseModel):
    GroupName: str = Field(min_length=1, max_length=100)
    GroupDescription: str = Field(min_length=1, max_length=150)

class Group(BaseModel):
    ID: int
    GroupName: str
    GroupDescription: str
    IDUserCreatedBy: str

class Permission(BaseModel):
    ID: int
    PermissionName: str
    PermissionType: str
    PermissionDetails: str
    IDUserCreatedBy: str

class ResponseGetGroup(BaseModel):
    groups: list[Group]

class UsersInGroup(Group):
    users: list[ResponseUser]

class PostUsersInGroup(BaseModel):
    groups: list[UsersInGroup]

class ResponseGetPermission(BaseModel):
    Permissions: list[Permission]

class GetPermission(BaseModel):
    Limit: int = Field(gt=0, le=100)
    Offset: int = Field(ge=0)
    OrderBy: Literal["ID", "GroupName", "IDUserCreatedBy"] = "ID"
    idPermission: None | int = Field(None, ge=1)
    PermissionType: str | None = Field(default=None, min_length=1, max_length=100)
    PermissionName: str | None = Field(default=None, min_length=1, max_length=100)

class GetGroup(BaseModel):
    Limit: int = Field(gt=0, le=100)
    Offset: int = Field(ge=0)
    OrderBy: Literal["ID", "GroupName", "IDUserCreatedBy"] = "ID"
    idGroup: None | int = Field(None, ge=1)
    GroupName: str | None = Field(default=None, min_length=1, max_length=100)

class GetMetaGroupUsers(BaseModel):
    Limit: int = Field(gt=0, le=100)
    Offset: int = Field(ge=0)
    OrderBy: Literal["ID", "GroupName", "IDUserCreatedBy"] = "ID"

class Products_Types(BaseModel):
    Name: str = Field(min_length=1, max_length=100)
    Details: str = Field(min_length=1, max_length=150)
    ID_image: int = Field(gt=0)
    ID_storage: int = Field(gt=0)
    value: int = Field(ge=0)
    Token_product: str = Field(min_length=1, max_length=150)
    Category: str = Field(min_length=1, max_length=100)
    State: str = Field(min_length=1, max_length=100)

class PostProduct(BaseModel):
    token: str
    product: Products_Types

class GetProduct(BaseModel):
    limit: int = Field(gt=0, le=100)
    offset: int = Field(ge=0)
    order_by: Literal["ID", "Name", "Category", "State"] = "ID"
    category: None | list[str] = []
    id_product: None | int = Field(None, ge=1)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    state: str | None = Field(default=None, min_length=1, max_length=100)
    token_product: str | None = Field(default=None, min_length=1, max_length=150)

class ResponseGetProduct(BaseModel):
    products: list[Product]

class Product(BaseModel):
    ID: int
    Name: str
    Details: str
    ID_image: int
    ID_storage: int
    value: int
    Token_product: str
    Category: str
    State: str

class ProductResponse(BaseModel):
    products: list[Product]