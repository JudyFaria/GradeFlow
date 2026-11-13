from fastapi import APIRouter, Depends
from fastapi.testclient import TestClient

from app.dependencias import (
    Dependencias,
    montar_dependencias,
    obter_dependencias,
)
from app.main import criar_app


def test_montar_dependencias_roda_sem_rede_nem_banco():
    assert isinstance(montar_dependencias(), Dependencias)


def test_rotas_recebem_o_conteiner_entregue_a_criar_app():
    conteiner = Dependencias()
    roteador = APIRouter()

    @roteador.get("/conteiner")
    def conteiner_recebido(
            recebido: Dependencias = Depends(obter_dependencias)):
        return {"mesmo": recebido is conteiner}

    aplicacao = criar_app(conteiner)
    aplicacao.include_router(roteador)

    assert TestClient(aplicacao).get("/conteiner").json() == {"mesmo": True}


def test_conteiner_fica_em_app_state():
    conteiner = Dependencias()

    assert criar_app(conteiner).state.dependencias is conteiner
