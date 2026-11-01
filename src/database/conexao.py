import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

#indicando a raiz do projeto (C:\robo_oferta)
raiz_projeto = Path(__file__).resolve().parents[2]

# carregando o arquivo .env
load_dotenv(raiz_projeto / ".env")


# funções para a conexão do BD
def cria_conexao() -> MongoClient:
    # indicando a connection string do BD
    uri = os.getenv("MONGODB_URI")

    if not uri or not uri.strip():
        raise RuntimeError(
            "A variável de ambiente MONGODB_URI não está definida ou está vazia."
            )

    try:
        return MongoClient(
            uri, serverSelectionTimeoutMS=5000
            )
    except ConfigurationError as erro:
        raise RuntimeError(
            "A variável de ambiente MONGODB_URI não é válida ou está malformada."
        ) from erro

def obter_banco(client: MongoClient):
    nome_banco = os.environ.get("MONGODB_DATABASE")

    if not nome_banco or not nome_banco.strip():
        raise RuntimeError(
            "A variável de ambiente MONGODB_DATABASE não está definida ou está vazia."
        )
    return client.get_database(nome_banco)

    



    