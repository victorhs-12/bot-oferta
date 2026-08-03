from src.processor.modelos import Produto

# logica da filtragem. simplesmente as regras de negócio que definem se um produto é válido ou não, de acordo com a configuração de filtros.
def calcular_desconto_percentual(produto: Produto) -> float:
    if produto.preco_original == 0:
        return 0
    return (produto.preco_original - produto.preco) / produto.preco_original * 100

def marca_eh_valida(produto: Produto, config_filtros):
    marca = produto.marca
    marcas_permitidas = config_filtros["marcas"]["permitidas"]
    marcas_premium = config_filtros["marcas"]["premium"]
    permitir_excecoes_marcaPremium = config_filtros["filtros"]["preco"]["permitir_excecoes_marcaPremium"]

    return (marca in marcas_permitidas) or (permitir_excecoes_marcaPremium and marca in marcas_premium)

def marca_eh_premium(produto: Produto, config_filtros) -> bool:
    return produto.marca in config_filtros["marcas"]["premium"]

def confianca_eh_valida(produto: Produto, config_filtros):
    nota_minima = config_filtros["filtros"]["confianca"]["nota_minima"]
    avaliacoes_minimas = config_filtros["filtros"]["confianca"]["avaliacoes_minimas"]

    return (produto.nota >= nota_minima) and (produto.numero_avaliacoes >= avaliacoes_minimas)

def preco_eh_valido(produto: Produto, config_filtros):
    preco_min = config_filtros["filtros"]["preco"]["min"]
    preco_max = config_filtros["filtros"]["preco"]["max"]

    return (produto.preco >= preco_min) and (produto.preco <= preco_max)




def desconto_eh_valido(produto: Produto, config_filtros) -> bool:
    desconto_minimo_percentual = config_filtros["filtros"]["preco"]["desconto_minimo_percentual"]
    desconto_percentual = calcular_desconto_percentual(produto)
    
    return desconto_percentual >= desconto_minimo_percentual

def produto_eh_valido(produto: Produto, config_filtros) -> bool:
    # marca e confiança são obrigatórios
    if not marca_eh_valida(produto, config_filtros):
        return False
    if not confianca_eh_valida(produto, config_filtros):
        return False

    # Se a marca for premium e o desconto for válido, ignora a faixa de preço definida
    if marca_eh_premium(produto, config_filtros) and desconto_eh_valido(produto, config_filtros):
        return True

    # caso contrário, o produto precisa atender aos critérios de preço e desconto
    return preco_eh_valido(produto, config_filtros) and desconto_eh_valido(produto, config_filtros)