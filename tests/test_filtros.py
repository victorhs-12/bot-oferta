import src.processor.filtros as filtros
import pytest

from src.processor.modelos import Produto

#teste de cálculo de desconto (teste unitário também, mas está separado dos outros testes unitários, para entender melho)
def test_calcular_desconto_percentual(config_filtros):
    produto = Produto(id = "1", nome = "Xiaomi Redmi Note 10", preco = 2000.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    desconto = filtros.calcular_desconto_percentual(produto)
    assert desconto == pytest.approx(20.0, rel=1e-3)


#testes unitários


# marca válida
def test_marca_eh_valida(config_filtros):
    produto = Produto(id = "5", nome = "Samsung Galaxy S21", preco = 2000.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 300, marca = "Samsung", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.marca_eh_valida(produto, config_filtros) == True

# marca premium
def test_marca_eh_premium(config_filtros):
    produto = Produto(id = "6", nome = "IPhone 13", preco = 2700.0, preco_original = 4500.0, nota = 4.5, numero_avaliacoes = 260, marca = "Apple", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.marca_eh_premium(produto, config_filtros) == True

# confianca válida ou inválida, dependendo da configuração de filtros
def test_confianca_eh_valida(config_filtros):

    #confiança inválida, pois o número de avaliações é menor que o mínimo definido na configuração
    produto = Produto(id = "7", nome = "Xiaomi Redmi Note 10", preco = 2000.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.confianca_eh_valida(produto, config_filtros) == False

    #confiança válida, pois o número de avaliações é maior que o mínimo definido na configuração
    produto = Produto(id = "8", nome = "Xiaomi Redmi Note 10", preco = 2000.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 260, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.confianca_eh_valida(produto, config_filtros) == True

    #confiança válida, pois o número de avaliações é igual ao mínimo definido na configuração
    produto = Produto(id = "9", nome = "Xiaomi Redmi Note 10", preco = 2000.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 250, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.confianca_eh_valida(produto, config_filtros) == True


def test_preco_eh_valido(config_filtros):
    # preço válido, pois o preço do produto está dentro da faixa definida na configuração
    produto = Produto(id = "8", nome = "Xiaomi Redmi Note 10", preco = 2500.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.preco_eh_valido(produto, config_filtros) == True

    # preço inválido, pois o preço do produto está fora da faixa definida na configuração
    produto = Produto(id = "9", nome = "Xiaomi Redmi Note 10", preco = 3000.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.preco_eh_valido(produto, config_filtros) == False

    # preço válido, pois o preço do produto está dentro da faixa definida na configuração
    produto = Produto(id = "10", nome = "Fone de Ouvido", preco = 60.0, preco_original = 100.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.preco_eh_valido(produto, config_filtros) == True

    # preço inválido, pois o preço do produto está fora da faixa definida na configuração
    produto = Produto(id = "10", nome = "Fone de Ouvido", preco = 40.0, preco_original = 100.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.preco_eh_valido(produto, config_filtros) == False

    



def test_desconto_eh_valido(config_filtros):
    # desconto válido, pois o desconto do produto está dentro da faixa definida na configuração
    produto = Produto(id = "9", nome = "Xiaomi Redmi Note 10", preco = 1500.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.desconto_eh_valido(produto, config_filtros) == True

    # desconto válido, pois o desconto do produto está dentro da faixa definida na configuração
    produto = Produto(id = "10", nome = "Fone de Ouvido", preco = 130.0, preco_original = 200.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.desconto_eh_valido(produto, config_filtros) == True

    # desconto inválido, pois o desconto do produto está fora da faixa definida na configuração
    produto = Produto(id = "11", nome = "Fone de Ouvido", preco = 150.0, preco_original = 200.0, nota = 4.5, numero_avaliacoes = 100, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.desconto_eh_valido(produto, config_filtros) == False

# teste de  produto válido, considerando todas as regras de negócio 
def test_produto_eh_valido(config_filtros):
    produto = Produto(id = "10", nome = "Xiaomi Redmi Note 10", preco = 1600.0, preco_original = 2500.0, nota = 4.5, numero_avaliacoes = 300, marca = "Xiaomi", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.produto_eh_valido(produto, config_filtros) == True

    #teste de marca inválida, colocando de propósito uma marca que não está na lista de marcas permitidas e na premium
    produto = Produto(id = "2", nome = "RedMagic 10s Pro", preco = 3000.0, preco_original = 3500.0, nota = 4.5, numero_avaliacoes = 250, marca = "RedMagic", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.produto_eh_valido(produto, config_filtros) == False

    #teste de produto premium fora da faixa de preço, mas com desconto válido
    produto = Produto(id = "3", nome = "IPhone 13", preco = 2700.0, preco_original = 4500.0, nota = 4.5, numero_avaliacoes = 260, marca = "Apple", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.produto_eh_valido(produto, config_filtros) == True

    #teste de produto premium fora da faixa de preço, mas com desconto válido, porém com nota abaixo do mínimo definido na configuração
    produto = Produto(id = "4", nome = "IPhone 13 Pro Max", preco = 3500.0, preco_original = 6500.0, nota = 3.5, numero_avaliacoes = 260, marca = "Apple", link = "http://exemplo.com/produto", imagem_url = "http://exemplo.com/imagem.jpg")
    assert filtros.produto_eh_valido(produto, config_filtros) == False
    