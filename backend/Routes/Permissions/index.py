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
from Routes.Users.index import verify_permission, verify_token

security = HTTPBearer()

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"]
)

#get all permissions
@router.get("", response_model=ResponseGetPermission | None)
async def get_permissions(filter_query: Annotated[GetPermission, Query()], credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        users = verify_token(credentials.credentials)
        if users == None:
            users = []

        if len(users) == 0:
            return JSONResponse(content={"message": "Bad request"}, status_code=400)

        permission = verify_permission(credentials.credentials, 'READ', 'Permissions')

        if permission == False:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        groups = []

        filter1 = []
        filter2 = f"ORDER BY {filter_query.OrderBy} ASC LIMIT {filter_query.Limit} OFFSET {filter_query.Offset}"
        filter3 = ""

        if filter_query.idPermission != None:
            filter1.append(f"ID = {filter_query.idPermission}")

        if filter_query.PermissionName != None:
            filter1.append(f"Permission_name = '{filter_query.PermissionName}'")

        if filter_query.PermissionType != None:
            filter1.append(f"Permission_type = '{filter_query.PermissionType}'")

        if len(filter1) > 0:
            filter3 = f" WHERE "

            for index, filter in enumerate(filter1):
                if index > 0:
                    filter3 += f" And "

                filter3 += f"{filter}"

        permissions = db.Read("Permissions", 
                            "ID, Permission_name, Permission_type, Details, ID_user_created_by", 
                            f"{filter3} {filter2}")

        if permissions == None:
            permissions = []

        response = []

        for index, item in enumerate(permissions):
            response.append({
                "ID": item[0],
                "Permission_name": item[1],
                "Permission_type": item[2],
                "Details": item[3],
                "ID_user_created_by": item[4],
            })

        return JSONResponse(content={"permissions": response}, status_code=200)
    except Exception as error:
        print(error)
        return JSONResponse(content={"message": "Bad request"}, status_code=500)