from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from Rotes.Authentication import index as authentication
from DB.CRUD.index import SQLite
import sys, os

args = sys.argv

print("Todos os argumentos:", args)

if len(sys.argv) > 1:
    # print(f"Primeiro argumento: {sys.argv[1]}")
    if sys.argv[1] == "create_user":
        username = "" # input("")
        password = "" # input("")

db = SQLite('layout.json')
db.Init_main()
app = FastAPI()
app.include_router(authentication.router)


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("./Templates/home.html", "r", encoding="utf-8") as f:
        html_texto = f.read()

    return html_texto
