from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from Rotes.Authentication import index as authentication
from DB.CRUD.index import SQLite
from pathlib import Path
import sys, os, getpass
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from time import time
from datetime import datetime


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CREATE_ROOT = os.getenv("create_root")

db = SQLite('layout.json')
db.Init_main()
app = FastAPI()
app.include_router(authentication.router)

if CREATE_ROOT == 'True':
    username = input("Username: ")
    found = db.Read('Users', 'ID, Username', f" WHERE 'Username' = {username}")
    if found == None:
        name = input("Name: ")
        password = getpass.getpass("Senha: ")
        Date_creation = int(time()) #datetime.fromtimestamp(time()).strftime("%d/%m/%Y %H:%M:%S")
        ID_Access = db.Create_item('')
        db.Create_item('Users', "Name, Date_creation, ID_access_token, ID_refresh_Token, ID_permission_group, User_type, Username, pw",
                         f"{name}, {Date_creation}, ID_access_token, ID_refresh_Token, ID_permission_group, ADMIN, {username}, {authentication.hash_password(password)}")
        password = ""
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
