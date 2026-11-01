#teste de conexão com o BD
import pytest
from src.database.conexao import cria_conexao, obter_banco
from pymongo.errors import PyMongoError
import os




@pytest.mark.integration
def test_mongodb_connection():
    client = cria_conexao()

    try:
        resposta = client.admin.command("ping")
    except PyMongoError as erro:
        pytest.fail(f"Não foi possível realizar a conexão: {erro}")
    finally:
        client.close()

    assert resposta["ok"] == 1

@pytest.mark.integration
def test_mongodb_validacao():
    client = cria_conexao()
  

    try:
        banco = obter_banco(client)
        client.admin.command("ping")
        nome_banco_esperado = os.getenv("MONGODB_DATABASE")

        assert nome_banco_esperado is not None
        assert nome_banco_esperado.strip()
        assert banco.name == nome_banco_esperado.strip()
        banco.list_collection_names()
    except PyMongoError as erro:
        pytest.fail(f"Não foi possível validar o banco de dados: {erro}")
    finally:
        client.close()
