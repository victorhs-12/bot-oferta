import yaml
from decimal import Decimal
from pathlib import Path

def _para_decimal(valor) -> Decimal:
    # str() evita o ruído binário do float (ex.: Decimal(4.5) vs Decimal("4.5"))
    return Decimal(str(valor))


def carregar_config():

    #colocando o caminho do arquivo config.yaml
    diretorio_atual = Path(__file__).resolve().parent
    raiz_projeto = diretorio_atual.parent.parent
    caminho_config = raiz_projeto / 'config' / 'config.yaml'

    # vai abrir o arquivo config.yaml e carregar as configurações
    with open(caminho_config, 'r', encoding='utf-8') as arquivo:
        config = yaml.safe_load(arquivo)

    # dinheiro, desconto e nota sempre Decimal, nunca float
    preco = config["filtros"]["preco"]
    for chave in ("min", "max", "desconto_minimo_percentual"):
        preco[chave] = _para_decimal(preco[chave])
    qualidade = config["filtros"]["qualidade"]
    qualidade["nota_minima"] = _para_decimal(qualidade["nota_minima"])

    return config
