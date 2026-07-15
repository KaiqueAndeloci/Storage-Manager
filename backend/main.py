from Routes.Authentication import index as authentication
from Routes.Users import index as users
from Routes.Products import index as products
from Routes.Groups import index as groups
from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from DB.CRUD.index import db
from pathlib import Path
import sys, os, getpass, uuid
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from time import time
from datetime import datetime, timedelta
from Interfaces.index import PostUser, AdminUser
import uvicorn


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CREATE_ROOT = os.getenv("create_root")
DEBUG = os.getenv("debug")

db.Init_main()
app = FastAPI()
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(groups.router)



if CREATE_ROOT == 'True':
    username = input("\nUsername: ")
    found = db.Read('Users', 'ID, Username', f" WHERE Username = '{username}'")

    if found == None:
        found = []

    if len(found) == 0:
        name = input("\nName: ")
        email = input("\nEmail: ")
        password = authentication.hash_password(getpass.getpass("\nSenha: "))
        user = AdminUser(Name=name, UserType='ADMIN', Email=email, Username=username, PW=password, IDUser=0)
        ID_user = users.create_user(username, password, PostUser(User=user))
        print("User created!")
        groups.add_user_on_group(ID_user, 1, 0)
        password = None
    else:
        print("This user root already exist")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # libera todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # libera todos os headers
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("./Templates/home.html", "r", encoding="utf-8") as f:
        html_texto = f.read()

    return html_texto

# debug mode:
if DEBUG == 'True':
    uvicorn.run(app, host="0.0.0.0", port=8000)
