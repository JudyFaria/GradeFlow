"""Prova a convenção: caso de uso recebe o repositório por injeção.

O caso de uso e o repositório falso existem só neste teste (R7).
"""
from typing import Protocol

from domain.erros import ErroNaoEncontrado


class RepositorioDeNomes(Protocol):
    def buscar(self, identificador: int) -> str | None: ...


class RepositorioDeNomesEmMemoria:
    def __init__(self, nomes: dict[int, str]):
        self._nomes = nomes

    def buscar(self, identificador: int) -> str | None:
        return self._nomes.get(identificador)


class ConsultarNome:
    def __init__(self, repositorio: RepositorioDeNomes):
        self._repositorio = repositorio

    def executar(self, identificador: int) -> str:
        nome = self._repositorio.buscar(identificador)
        if nome is None:
            raise ErroNaoEncontrado("Registro não encontrado")
        return nome


def test_caso_de_uso_usa_o_repositorio_em_memoria_injetado():
    caso_de_uso = ConsultarNome(RepositorioDeNomesEmMemoria({1: "Ana"}))

    assert caso_de_uso.executar(1) == "Ana"


def test_caso_de_uso_levanta_erro_de_dominio_quando_nao_encontra():
    caso_de_uso = ConsultarNome(RepositorioDeNomesEmMemoria({}))

    try:
        caso_de_uso.executar(1)
    except ErroNaoEncontrado as erro:
        assert str(erro) == "Registro não encontrado"
    else:
        raise AssertionError("esperava ErroNaoEncontrado")
