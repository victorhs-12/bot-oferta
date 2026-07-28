from src.utils.config_loader import carregar_config

def test_config_estrutura():
    config = carregar_config()

    assert 'shopee' in config

    categorias = config['shopee']['categorias']
    assert isinstance(categorias, list)
    assert len(categorias) == 2 #vai verificar se tem as categorias principais: Cozinha e Eletrônicos
    

    for cat in categorias:
        assert 'nome' in cat
        assert 'id_shopee' in cat
        assert 'subcategorias' in cat
        assert isinstance(cat['subcategorias'], list)
        assert len(cat['subcategorias']) > 0
        assert 'subcategorias' is not None


