#teste de conexão com o BD
import pytest
from src.database.conexao import cria_conexao
from pymongo.errors import PyMongoError

@pytest.mark.integration
def test_mongodb():
    client = cria_conexao()

    try:
        resposta = client.admin.command("ping")
        print("Conexão com MongoDB criada com sucesso")
    except PyMongoError as erro:
        pytest.fail(f"Não foi possível realizar a conexão: {erro}")
    finally:
        client.close()

        assert resposta["ok"] == 1