from src.utils.config_loader import carregar_config


def test_carregar_config_retorna_secoes_principais():
    config = carregar_config()

    assert isinstance(config, dict)
    assert {
        "shopee",
        "filtros",
        "whatsapp",
        "agendamento",
    }.issubset(config)


def test_carregar_config_converte_valores_para_decimal():
    from decimal import Decimal

    config = carregar_config()
    preco = config["filtros"]["preco"]
    nota_minima = config["filtros"]["qualidade"]["nota_minima"]

    assert preco["min"] == Decimal("60.00")
    assert preco["max"] == Decimal("2500.00")
    assert isinstance(preco["desconto_minimo_percentual"], Decimal)
    assert isinstance(nota_minima, Decimal)
    assert nota_minima == Decimal("4.5")
