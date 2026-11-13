"""Tradução de erros em respostas HTTP. Só app/ conhece status HTTP."""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.erros import ErroDeDominio, ErroNaoEncontrado

MENSAGEM_ERRO_INTERNO = "Erro interno. Tente novamente em instantes."

registro = logging.getLogger(__name__)


def _resposta(status: int, mensagem: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"detail": mensagem})


def registrar_tratadores_de_erro(aplicacao: FastAPI) -> None:
    @aplicacao.exception_handler(ErroNaoEncontrado)
    async def tratar_nao_encontrado(_: Request, erro: ErroNaoEncontrado):
        return _resposta(404, str(erro))

    @aplicacao.exception_handler(ErroDeDominio)
    async def tratar_erro_de_dominio(_: Request, erro: ErroDeDominio):
        return _resposta(400, str(erro))

    @aplicacao.exception_handler(Exception)
    async def tratar_erro_inesperado(_: Request, erro: Exception):
        registro.error("Erro inesperado", exc_info=erro)
        return _resposta(500, MENSAGEM_ERRO_INTERNO)
