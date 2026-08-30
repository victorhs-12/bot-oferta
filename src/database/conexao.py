import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

#indicando a raiz do projeto (C:\robo_oferta)
raiz_projeto = Path(__file__).resolve().parents[2]

# carregando o arquivo .env
load_dotenv(raiz_projeto / ".env")
# indicando a connection string do BD
uri = os.getenv("MONGODB_URI")

# funções para a conexão do BD
def cria_conexao() -> MongoClient:
    return MongoClient(uri, serverSelectionTimeoutMS=5000)


def obter_banco():
    client = cria_conexao()
    nome_banco = os.environ.get("MONGODB_DATABASE")

    return client[nome_banco]



    