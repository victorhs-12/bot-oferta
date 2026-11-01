from src.utils.config_loader import carregar_config


def test_categorias_possuem_estrutura_esperada():
    config = carregar_config()
    categorias = config["shopee"]["categorias"]

    assert isinstance(categorias, list)
    assert len(categorias) == 2

    for categoria in categorias:
        assert isinstance(categoria["nome"], str)
        assert categoria["nome"].strip()
        assert isinstance(categoria["ids_api"], list)


def test_filtros_possuem_valores_validos():
    config = carregar_config()
    preco = config["filtros"]["preco"]
    qualidade = config["filtros"]["qualidade"]

    assert 0 <= preco["min"] <= preco["max"]
    assert 0 <= preco["desconto_minimo_percentual"] <= 100
    assert 0 <= qualidade["nota_minima"] <= 5
    assert qualidade["vendas_minimas"] >= 0


def test_categorias_nao_repetem_nome_nem_id():
    categorias = carregar_config()["shopee"]["categorias"]
    nomes = [c["nome"] for c in categorias]
    ids = [str(i) for c in categorias for i in c["ids_api"]]

    assert len(nomes) == len(set(nomes))
    assert len(ids) == len(set(ids))


def test_ids_api_sao_texto_ou_inteiro():
    categorias = carregar_config()["shopee"]["categorias"]

    for categoria in categorias:
        assert all(isinstance(i, (str, int)) for i in categoria["ids_api"])
