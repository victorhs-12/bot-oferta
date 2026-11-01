import pytest
from datetime import datetime, timezone
from decimal import Decimal
from src.processor.modelos import Oferta, Produto


@pytest.fixture
def produto_base():
    """Produto válido nos limites mínimos definidos para qualidade."""
    return Produto(
        item_id="123",
        nome="Produto Teste",
        preco=Decimal("100.0"),
        preco_min=Decimal("90.0"),
        preco_max=Decimal("120.0"),
        nota=Decimal("4.5"),
        vendas=250,
        link_produto="https://exemplo.com/produto",
        imagem_url="https://exemplo.com/imagem.jpg",
        categorias_id=("100", "200"),
        loja_id="456",
        loja_nome="Loja Teste",
        loja_tipo="oficial",
    )


@pytest.fixture
def oferta_base(produto_base):
    """Oferta válida no limite mínimo de desconto configurado."""
    return Oferta(
        produto=produto_base,
        desconto_percentual=Decimal("35.0"),
        link_oferta="https://exemplo.com/oferta",
        comissao=Decimal("10.0"),
        taxa_comissao=Decimal("10.0"),
        inicio_vigencia=datetime(2026, 9, 1, tzinfo=timezone.utc),
        fim_vigencia=datetime(2026, 9, 30, 23, 59, 59, tzinfo=timezone.utc),
    )


@pytest.fixture
def config_filtros():
    """Recorte do config.yaml utilizado pelas regras de filtragem."""
    return {
        "filtros": {
            "preco": {
                "min": Decimal("60.00"),
                "max": Decimal("2500.00"),
                "desconto_minimo_percentual": Decimal("35.0"),
            },
            "qualidade": {
                "nota_minima": Decimal("4.5"),
                "vendas_minimas": 250,
            },
        }
    }


@pytest.fixture
def config_categorias():
    """Recorte de shopee.categorias do config.yaml."""
    return [
        {"nome": "Cozinha", "ids_api": ["100", "101"]},
        {"nome": "Eletrônicos", "ids_api": [200]},
    ]


@pytest.fixture
def agora():
    """Relógio fixo, dentro da vigência de oferta_base."""
    return datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)
