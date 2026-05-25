from Routes.Authentication import index as authentication
from Routes.Users import index as users
from Routes.Products import index as products
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
from Routes.Users.index import User_ADMIN



load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CREATE_ROOT = os.getenv("create_root")

db.Init_main()
app = FastAPI()
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(products.router)



if CREATE_ROOT == 'True':
    username = input("\nUsername: ")
    found = db.Read('Users', 'ID, Username', f" WHERE Username = '{username}'")

    if found == None or len(found) == 0:
        name = input("\nName: ")
        email = input("\nEmail: ")
        # password = authentication.hash_password("kaique123") 
        password = authentication.hash_password(getpass.getpass("\nSenha: "))
        today = int(time())
        Date_creation = int(time())
        access = f"{str(uuid.uuid4())}"
        refresh = f"{str(uuid.uuid4())}"
        data_futura = datetime.now() + timedelta(days=30)
        expirate = int(data_futura.timestamp())
        user = User_ADMIN(Name=name, email=email)
        users.create_user("ADMIN", username, password, user)
        print("User created!")
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
