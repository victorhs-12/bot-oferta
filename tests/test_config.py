from src.utils.config_loader import carregar_config



def test_config():
    config = carregar_config()

    # vai retornar se a estrutura do arquivo config.yaml está correta
    assert 'shopee' in config
    assert isinstance(config['shopee']['categorias'], list)
    assert len(config['shopee']['categorias']) > 0 