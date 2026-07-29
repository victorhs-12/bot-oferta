from src.processor.modelos import Produto, Oferta


def test_produto(produto_base):
    assert produto_base.id == "123"
    assert produto_base.nome == "Produto Teste"
    assert produto_base.preco == 100.0
    assert produto_base.preco_original == 150.0
    assert produto_base.nota == 4.5
    assert produto_base.numero_avaliacoes == 10
    assert produto_base.marca == "Marca Teste"
    assert produto_base.link == "http://exemplo.com/produto"
    assert produto_base.imagem_url == "http://exemplo.com/imagem.jpg"


def test_oferta(produto_base):
    oferta = Oferta(produto=produto_base, desconto_percentual=33.33)
    assert oferta.produto == produto_base
    assert oferta.desconto_percentual == 33.33