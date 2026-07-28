import yaml
from pathlib import Path

def carregar_config():

    #colocando o caminho do arquivo config.yaml
    diretorio_atual = Path(__file__).resolve().parent
    raiz_projeto = diretorio_atual.parent.parent
    caminho_config = raiz_projeto / 'config' / 'config.yaml'
   
    # vai abrir o arquivo config.yaml e carregar as configurações
    with open(caminho_config, 'r', encoding='utf-8') as arquivo:
        config = yaml.safe_load(arquivo)
    return config

    print(caminho_config)