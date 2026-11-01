from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
from decimal import Decimal

import pytest


def test_produto_armazena_dados_da_api(produto_base):
    assert produto_base.item_id == "123"
    assert produto_base.nome == "Produto Teste"
    assert produto_base.preco == Decimal("100.0")
    assert produto_base.preco_min == Decimal("90.0")
    assert produto_base.preco_max == Decimal("120.0")
    assert produto_base.nota == Decimal("4.5")
    assert produto_base.vendas == 250
    assert produto_base.link_produto == "https://exemplo.com/produto"
    assert produto_base.imagem_url == "https://exemplo.com/imagem.jpg"
    assert produto_base.categorias_id == ("100", "200")
    assert produto_base.loja_id == "456"
    assert produto_base.loja_nome == "Loja Teste"
    assert produto_base.loja_tipo == "oficial"


def test_oferta_armazena_dados_comerciais(oferta_base, produto_base):
    assert oferta_base.produto == produto_base
    assert oferta_base.desconto_percentual == Decimal("35.0")
    assert oferta_base.link_oferta == "https://exemplo.com/oferta"
    assert oferta_base.comissao == Decimal("10.0")
    assert oferta_base.taxa_comissao == Decimal("10.0")
    assert oferta_base.inicio_vigencia == datetime(2026, 9, 1, tzinfo=timezone.utc)
    assert oferta_base.fim_vigencia == datetime(
        2026, 9, 30, 23, 59, 59, tzinfo=timezone.utc
    )


def test_produto_eh_imutavel(produto_base):
    with pytest.raises(FrozenInstanceError):
        produto_base.preco = Decimal("1")


def test_produto_converte_categorias_em_tupla(produto_base):
    produto = replace(produto_base, categorias_id=["1", "2"])

    assert produto.categorias_id == ("1", "2")


@pytest.mark.parametrize("campo", ["preco", "preco_min", "preco_max", "nota"])
def test_produto_rejeita_float_em_campo_decimal(produto_base, campo):
    with pytest.raises(TypeError):
        replace(produto_base, **{campo: 4.5})


@pytest.mark.parametrize(
    "alteracao",
    [
        {"preco": Decimal("-1")},
        {"preco_min": Decimal("130"), "preco_max": Decimal("120")},
        {"nota": Decimal("5.01")},
        {"nota": Decimal("-0.1")},
        {"nota": Decimal("NaN")},
        {"vendas": -1},
        {"item_id": " "},
        {"nome": ""},
    ],
)
def test_produto_rejeita_valores_invalidos(produto_base, alteracao):
    with pytest.raises(ValueError):
        replace(produto_base, **alteracao)


def test_produto_rejeita_vendas_nao_inteira(produto_base):
    with pytest.raises(TypeError):
        replace(produto_base, vendas=250.0)


def test_produto_rejeita_categorias_como_texto(produto_base):
    with pytest.raises(TypeError):
        replace(produto_base, categorias_id="100")


@pytest.mark.parametrize("campo", ["desconto_percentual", "comissao", "taxa_comissao"])
def test_oferta_rejeita_float_em_campo_decimal(oferta_base, campo):
    with pytest.raises(TypeError):
        replace(oferta_base, **{campo: 10.0})


@pytest.mark.parametrize(
    "alteracao",
    [
        {"desconto_percentual": Decimal("100.01")},
        {"desconto_percentual": Decimal("-1")},
        {"comissao": Decimal("-1")},
        {"taxa_comissao": Decimal("-1")},
        {"link_oferta": ""},
    ],
)
def test_oferta_rejeita_valores_invalidos(oferta_base, alteracao):
    with pytest.raises(ValueError):
        replace(oferta_base, **alteracao)


def test_oferta_rejeita_datas_sem_timezone(oferta_base):
    with pytest.raises(ValueError):
        replace(oferta_base, inicio_vigencia=datetime(2026, 9, 1))


def test_oferta_rejeita_data_como_texto(oferta_base):
    with pytest.raises(TypeError):
        replace(oferta_base, fim_vigencia="2026-09-30T23:59:59Z")


def test_oferta_rejeita_inicio_igual_ou_posterior_ao_fim(oferta_base):
    with pytest.raises(ValueError):
        replace(oferta_base, inicio_vigencia=oferta_base.fim_vigencia)


def test_oferta_rejeita_produto_invalido(oferta_base):
    with pytest.raises(TypeError):
        replace(oferta_base, produto="123")
