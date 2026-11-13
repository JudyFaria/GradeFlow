from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.dependencias import Dependencias
from app.main import criar_app
from domain.erros import ErroDeDominio, ErroNaoEncontrado

roteador = APIRouter()


@roteador.get("/erro-de-dominio")
def erro_de_dominio():
    raise ErroDeDominio("Passaria de 30 créditos nesse período (32)")


@roteador.get("/nao-encontrado")
def nao_encontrado():
    raise ErroNaoEncontrado("Planejamento não encontrado")


@roteador.get("/inesperado")
def inesperado():
    raise RuntimeError("SELECT * FROM aluno /srv/segredo.py")


def cliente_com_rotas_de_erro() -> TestClient:
    aplicacao = criar_app(Dependencias())
    aplicacao.include_router(roteador)
    return TestClient(aplicacao, raise_server_exceptions=False)


def test_erro_de_dominio_vira_400_com_a_mensagem_em_detail():
    resposta = cliente_com_rotas_de_erro().get("/erro-de-dominio")

    assert resposta.status_code == 400
    assert resposta.json() == {
        "detail": "Passaria de 30 créditos nesse período (32)"}


def test_nao_encontrado_vira_404_e_nunca_403():
    resposta = cliente_com_rotas_de_erro().get("/nao-encontrado")

    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Planejamento não encontrado"}


def test_erro_inesperado_vira_500_generico_sem_vazar_detalhes():
    resposta = cliente_com_rotas_de_erro().get("/inesperado")

    assert resposta.status_code == 500
    assert "SELECT" not in resposta.text
    assert "segredo" not in resposta.text
    assert resposta.json() == {
        "detail": "Erro interno. Tente novamente em instantes."}
