from datetime import datetime

from src.processor.modelos import Produto, Oferta


def qualidade_eh_valida(produto: Produto, config_filtros):
    nota_minima = config_filtros["filtros"]["qualidade"]["nota_minima"]
    vendas_minimas = config_filtros["filtros"]["qualidade"]["vendas_minimas"]

    return (
        produto.nota >= nota_minima
        and produto.vendas >= vendas_minimas
    )

def preco_eh_valido(produto: Produto, config_filtros):
    preco_min = config_filtros["filtros"]["preco"]["min"]
    preco_max = config_filtros["filtros"]["preco"]["max"]

    return (produto.preco >= preco_min) and (produto.preco <= preco_max)


def desconto_eh_valido(oferta: Oferta, config_filtros) -> bool:
    desconto_minimo_percentual = (
        config_filtros["filtros"]["preco"]["desconto_minimo_percentual"]
        )

    return oferta.desconto_percentual >= desconto_minimo_percentual

def vigencia_eh_valida(oferta: Oferta, agora: datetime) -> bool:
    if agora.tzinfo is None:
        raise ValueError("agora deve ter timezone")

    return (
        oferta.inicio_vigencia 
        <= agora 
        < oferta.fim_vigencia
    )

def categoria_eh_valida(produto: Produto, config_categorias: list[dict]) -> bool:
    """Produto pertence a ao menos uma categoria declarada em config.yaml."""
    ids_configurados = {
        str(id_api)
        for categoria in config_categorias
        for id_api in categoria["ids_api"]
    }

    return not ids_configurados.isdisjoint(produto.categorias_id)


def oferta_eh_valida(
    oferta: Oferta,
    config_filtros,
    config_categorias: list[dict],
    agora: datetime,
) -> bool:
    produto = oferta.produto
    return (
        categoria_eh_valida(produto, config_categorias)
        and preco_eh_valido(produto, config_filtros)
        and qualidade_eh_valida(produto, config_filtros)
        and desconto_eh_valido(oferta, config_filtros)
        and vigencia_eh_valida(oferta, agora)
    )
    