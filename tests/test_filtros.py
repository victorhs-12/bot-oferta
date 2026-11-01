from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from src.processor import filtros


@pytest.mark.parametrize(
    ("nota", "vendas", "esperado"),
    [
        (Decimal("4.5"), 250, True),
        (Decimal("4.49"), 250, False),
        (Decimal("4.5"), 249, False),
    ],
)
def test_qualidade_eh_valida(
    produto_base,
    config_filtros,
    nota,
    vendas,
    esperado,
):
    produto = replace(produto_base, nota=nota, vendas=vendas)

    assert filtros.qualidade_eh_valida(produto, config_filtros) is esperado


@pytest.mark.parametrize(
    ("preco", "esperado"),
    [
        (Decimal("60.00"), True),
        (Decimal("2500.00"), True),
        (Decimal("59.99"), False),
        (Decimal("2500.01"), False),
    ],
)
def test_preco_eh_valido(produto_base, config_filtros, preco, esperado):
    produto = replace(produto_base, preco=preco)

    assert filtros.preco_eh_valido(produto, config_filtros) is esperado


@pytest.mark.parametrize(
    ("desconto", "esperado"),
    [
        (Decimal("35.0"), True),
        (Decimal("34.99"), False),
    ],
)
def test_desconto_eh_valido(oferta_base, config_filtros, desconto, esperado):
    oferta = replace(oferta_base, desconto_percentual=desconto)

    assert filtros.desconto_eh_valido(oferta, config_filtros) is esperado


def test_oferta_eh_valida_quando_atende_todas_as_regras(
    oferta_base,
    config_filtros,
    config_categorias,
    agora,
):
    assert filtros.oferta_eh_valida(
        oferta_base,
        config_filtros,
        config_categorias,
        agora,
    ) is True


@pytest.mark.parametrize(
    ("alteracao_produto", "desconto"),
    [
        ({"preco": Decimal("2500.01")}, Decimal("35.0")),
        ({"nota": Decimal("4.49")}, Decimal("35.0")),
        ({"vendas": 249}, Decimal("35.0")),
        ({}, Decimal("34.99")),
    ],
)
def test_oferta_eh_invalida_quando_uma_regra_falha(
    produto_base,
    oferta_base,
    config_filtros,
    config_categorias,
    agora,
    alteracao_produto,
    desconto,
):
    produto = replace(produto_base, **alteracao_produto)
    oferta = replace(
        oferta_base,
        produto=produto,
        desconto_percentual=desconto,
    )

    assert filtros.oferta_eh_valida(
        oferta,
        config_filtros,
        config_categorias,
        agora,
    ) is False


def test_oferta_eh_invalida_fora_da_vigencia(
    oferta_base,
    config_filtros,
    config_categorias,
):
    depois_do_fim = oferta_base.fim_vigencia + timedelta(seconds=1)

    assert filtros.oferta_eh_valida(
        oferta_base,
        config_filtros,
        config_categorias,
        depois_do_fim,
    ) is False


def test_oferta_eh_invalida_fora_das_categorias(
    produto_base,
    oferta_base,
    config_filtros,
    config_categorias,
    agora,
):
    produto = replace(produto_base, categorias_id=("999",))
    oferta = replace(oferta_base, produto=produto)

    assert filtros.oferta_eh_valida(
        oferta,
        config_filtros,
        config_categorias,
        agora,
    ) is False


# vigência: inicio_vigencia <= agora < fim_vigencia
def test_vigencia_inclui_inicio_e_exclui_fim(oferta_base):
    assert filtros.vigencia_eh_valida(oferta_base, oferta_base.inicio_vigencia) is True
    assert filtros.vigencia_eh_valida(oferta_base, oferta_base.fim_vigencia) is False
    assert filtros.vigencia_eh_valida(
        oferta_base,
        oferta_base.inicio_vigencia - timedelta(seconds=1),
    ) is False


def test_vigencia_rejeita_relogio_sem_timezone(oferta_base):
    with pytest.raises(ValueError):
        filtros.vigencia_eh_valida(oferta_base, datetime(2026, 9, 15))


def test_vigencia_compara_fusos_diferentes(oferta_base):
    # fim = 2026-09-30 23:59:59Z = 20:59:59-03:00; um segundo antes ainda vale
    brasilia = timezone(timedelta(hours=-3))
    quase_fim = datetime(2026, 9, 30, 20, 59, 58, tzinfo=brasilia)

    assert filtros.vigencia_eh_valida(oferta_base, quase_fim) is True


# categorias
def test_categoria_aceita_produto_com_id_configurado(produto_base, config_categorias):
    assert filtros.categoria_eh_valida(produto_base, config_categorias) is True


def test_categoria_compara_ids_numericos_do_config_como_texto(
    produto_base,
    config_categorias,
):
    produto = replace(produto_base, categorias_id=("200",))

    assert filtros.categoria_eh_valida(produto, config_categorias) is True


def test_categoria_rejeita_id_nao_configurado(produto_base, config_categorias):
    produto = replace(produto_base, categorias_id=("999",))

    assert filtros.categoria_eh_valida(produto, config_categorias) is False


def test_categoria_rejeita_quando_ids_api_vazio(produto_base):
    config_vazio = [{"nome": "Cozinha", "ids_api": []}]

    assert filtros.categoria_eh_valida(produto_base, config_vazio) is False


def test_categoria_rejeita_produto_sem_categorias(produto_base, config_categorias):
    produto = replace(produto_base, categorias_id=())

    assert filtros.categoria_eh_valida(produto, config_categorias) is False
