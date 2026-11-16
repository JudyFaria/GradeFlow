"""Ponto de montagem das dependências (composition root).

É o único módulo que instancia repositórios concretos de infra/ e os
entrega aos casos de uso. As rotas só recebem o contêiner pronto.
"""
from dataclasses import dataclass

from fastapi import Request

from infra.relogio_sistema import RelogioSistema
from use_cases.portas.relogio import Relogio


@dataclass(frozen=True)
class Dependencias:
    """Contêiner com repositórios e casos de uso montados.

    Cada feature acrescenta aqui os seus campos. A conexão com o banco
    não é aberta aqui: quem precisa dela a abre sob demanda.
    """

    relogio: Relogio


def montar_dependencias() -> Dependencias:
    return Dependencias(relogio=RelogioSistema())


def obter_dependencias(request: Request) -> Dependencias:
    return request.app.state.dependencias
