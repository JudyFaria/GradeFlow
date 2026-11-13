from fastapi import FastAPI

from app.dependencias import Dependencias, montar_dependencias
from app.erros_http import registrar_tratadores_de_erro
from app.routes import saude


def criar_app(dependencias: Dependencias) -> FastAPI:
    aplicacao = FastAPI(title="GradeFlow")
    aplicacao.state.dependencias = dependencias
    registrar_tratadores_de_erro(aplicacao)
    aplicacao.include_router(saude.roteador)
    return aplicacao


app = criar_app(montar_dependencias())
