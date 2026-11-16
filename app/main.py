from collections.abc import Sequence
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.dependencias import Dependencias, montar_dependencias
from app.erros_http import registrar_tratadores_de_erro
from app.routes import saude

PASTA_FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
POLITICA_DE_SEGURANCA_DE_CONTEUDO = "default-src 'self'"


def criar_app(dependencias: Dependencias,
              roteadores_extras: Sequence[APIRouter] = ()) -> FastAPI:
    """Monta a aplicação. `roteadores_extras` entram antes do front."""
    aplicacao = FastAPI(title="GradeFlow")
    aplicacao.state.dependencias = dependencias
    registrar_tratadores_de_erro(aplicacao)
    aplicacao.include_router(saude.roteador)
    for roteador in roteadores_extras:
        aplicacao.include_router(roteador)

    @aplicacao.middleware("http")
    async def acrescentar_csp(requisicao: Request, proximo):
        resposta = await proximo(requisicao)
        resposta.headers["Content-Security-Policy"] = (
            POLITICA_DE_SEGURANCA_DE_CONTEUDO)
        return resposta

    # Por último: o front em "/" não pode encobrir as rotas da API.
    aplicacao.mount("/", StaticFiles(directory=PASTA_FRONTEND, html=True),
                    name="frontend")
    return aplicacao


app = criar_app(montar_dependencias())
