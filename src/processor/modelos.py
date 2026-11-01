from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


def _exige_decimal(entidade: str, **campos: Decimal) -> None:
    for nome, valor in campos.items():
        if not isinstance(valor, Decimal):
            raise TypeError(
                f"{entidade}.{nome} deve ser Decimal, recebeu {type(valor).__name__}"
            )
        if not valor.is_finite():
            raise ValueError(f"{entidade}.{nome} deve ser finito")


def _exige_texto(entidade: str, **campos: str) -> None:
    for nome, valor in campos.items():
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{entidade}.{nome} não pode ser vazio")


# modelos que representam o produto e a oferta; só validam invariantes, sem regra de negócio
@dataclass(frozen=True)
class Produto:
    item_id: str
    nome: str
    preco: Decimal
    preco_min: Decimal
    preco_max: Decimal
    nota: Decimal
    vendas: int
    link_produto: str
    imagem_url: str
    categorias_id: tuple[str, ...]
    loja_id: str
    loja_nome: str
    loja_tipo: str

    def __post_init__(self):
        _exige_texto(
            "Produto",
            item_id=self.item_id,
            nome=self.nome,
            link_produto=self.link_produto,
            loja_id=self.loja_id,
        )
        _exige_decimal(
            "Produto",
            preco=self.preco,
            preco_min=self.preco_min,
            preco_max=self.preco_max,
            nota=self.nota,
        )
        if self.preco < 0 or self.preco_min < 0:
            raise ValueError("Produto: preços não podem ser negativos")
        if self.preco_min > self.preco_max:
            raise ValueError("Produto.preco_min não pode ser maior que preco_max")
        if not Decimal("0") <= self.nota <= Decimal("5"):
            raise ValueError("Produto.nota deve estar entre 0 e 5")
        if isinstance(self.vendas, bool) or not isinstance(self.vendas, int):
            raise TypeError("Produto.vendas deve ser int")
        if self.vendas < 0:
            raise ValueError("Produto.vendas não pode ser negativo")
        if isinstance(self.categorias_id, (str, bytes)) or not all(
            isinstance(c, str) for c in self.categorias_id
        ):
            raise TypeError("Produto.categorias_id deve ser sequência de str")
        # normaliza para tupla: mantém o modelo imutável de fato
        object.__setattr__(self, "categorias_id", tuple(self.categorias_id))


@dataclass(frozen=True)
class Oferta:
    produto: Produto
    desconto_percentual: Decimal
    link_oferta: str
    comissao: Decimal
    taxa_comissao: Decimal
    inicio_vigencia: datetime
    fim_vigencia: datetime

    def __post_init__(self):
        if not isinstance(self.produto, Produto):
            raise TypeError("Oferta.produto deve ser Produto")
        _exige_texto("Oferta", link_oferta=self.link_oferta)
        _exige_decimal(
            "Oferta",
            desconto_percentual=self.desconto_percentual,
            comissao=self.comissao,
            taxa_comissao=self.taxa_comissao,
        )
        if not Decimal("0") <= self.desconto_percentual <= Decimal("100"):
            raise ValueError("Oferta.desconto_percentual deve estar entre 0 e 100")
        if self.comissao < 0 or self.taxa_comissao < 0:
            raise ValueError("Oferta: comissão não pode ser negativa")
        for nome in ("inicio_vigencia", "fim_vigencia"):
            valor = getattr(self, nome)
            if not isinstance(valor, datetime):
                raise TypeError(f"Oferta.{nome} deve ser datetime")
            if valor.tzinfo is None or valor.utcoffset() is None:
                raise ValueError(f"Oferta.{nome} deve ter timezone")
        if self.inicio_vigencia >= self.fim_vigencia:
            raise ValueError("Oferta.inicio_vigencia deve ser anterior a fim_vigencia")
