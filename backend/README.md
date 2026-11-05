# Backend — Storage Manager

API do Storage Manager, desenvolvida com FastAPI e Python. Os dados são armazenados em um banco SQLite.

## Arquitetura

- `main.py`: cria a aplicação FastAPI, inicializa o banco e registra os endpoints.
- `Routes/`: endpoints organizados por domínio, como autenticação, usuários, produtos, grupos e permissões.
- `Interfaces/`: modelos de dados usados pela API.
- `DB/CRUD/`: acesso e operações no banco SQLite.
- `layout.json`: configuração do esquema inicial do banco.
- `Templates/`: página HTML simples servida pela rota raiz.

Na inicialização, o backend prepara o banco em `DB/db.sqlite3` a partir do esquema definido em `layout.json`.

## Requisitos

- Python 3.12 ou superior.
- `pip`.

## Instalação e execução

No PowerShell, a partir da raiz do repositório:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

O modo de desenvolvimento ficará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000). A documentação interativa da API pode ser acessada em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Para criar o usuário administrador inicial durante a inicialização, defina `create_root=True` no arquivo `.env` antes de iniciar o servidor. O processo solicitará os dados do usuário no terminal.
