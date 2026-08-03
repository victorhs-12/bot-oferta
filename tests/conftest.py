import pytest
from src.processor.modelos import Produto

# criei um fixture para testes, para que eu não escreva toda a hora o mesmo objeto Produto
@pytest.fixture
def produto_base():
    return Produto(
        id="123",
        nome="Produto Teste",
        preco=100.0,
        preco_original=150.0,
        nota=4.5,
        numero_avaliacoes=10,
        marca="Marca Teste",
        link="http://exemplo.com/produto",
        imagem_url="http://exemplo.com/imagem.jpg"
    )

@pytest.fixture
def config_filtros():
    return {
        "filtros":{
            "preco": {"min": 60, "max": 2500, "permitir_excecoes_marcaPremium": True, "desconto_minimo_percentual": 35},
            "confianca": {"nota_minima": 4.5, "avaliacoes_minimas": 250}
        },
        "marcas": {
            "permitidas": ["Xiaomi", "Samsung"],
            "premium": ["Apple", "AOC"]
        }
    }
    