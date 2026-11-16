"""Prova a injeção do relógio: a data atual vem da porta `Relogio` (CA10)."""
from datetime import date

from use_cases.portas.relogio import Relogio


class RelogioFalso:
    def __init__(self, data: date):
        self._data = data

    def hoje(self) -> date:
        return self._data


class SemestreAtual:
    """Caso de uso de teste: rótulo `AA.S` do semestre de hoje."""

    def __init__(self, relogio: Relogio):
        self._relogio = relogio

    def executar(self) -> str:
        hoje = self._relogio.hoje()
        periodo = 1 if hoje.month <= 6 else 2
        return f"{hoje.year % 100}.{periodo}"


def test_data_fixa_no_primeiro_semestre():
    assert SemestreAtual(RelogioFalso(date(2027, 3, 10))).executar() == "27.1"


def test_data_fixa_no_segundo_semestre():
    assert SemestreAtual(RelogioFalso(date(2027, 8, 1))).executar() == "27.2"
