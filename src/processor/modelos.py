from dataclasses import dataclass

# isso vai ser o modelo para representar o produto e a oferta, para eu usar na filtragem
@dataclass
class Produto:
    id: str
    nome: str
    preco: float
    preco_original: float
    nota: float
    numero_avaliacoes: int
    marca: str 
    link: str
    imagem_url: str

@dataclass
class Oferta():
    produto: Produto
    desconto_percentual: float

