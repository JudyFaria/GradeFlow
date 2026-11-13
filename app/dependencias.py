"""Ponto de montagem das dependências (composition root).

É o único módulo que instancia repositórios concretos de infra/ e os
entrega aos casos de uso. As rotas só recebem o contêiner pronto.
"""
from dataclasses import dataclass

from fastapi import Request


@dataclass(frozen=True)
class Dependencias:
    """Contêiner com repositórios e casos de uso montados.

    Cada feature acrescenta aqui os seus campos.
    """


def montar_dependencias() -> Dependencias:
    return Dependencias()


def obter_dependencias(request: Request) -> Dependencias:
    return request.app.state.dependencias
