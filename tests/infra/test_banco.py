import pytest

import infra.banco as banco
from infra.erros import ErroDeConfiguracao, ErroDeInfraestrutura

URL_COM_SEGREDO = "postgresql://usuario:senha-secreta@servidor-x:5432/db"


def test_sem_database_url_falha_em_portugues(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ErroDeConfiguracao) as erro:
        banco.abrir_conexao()

    assert "DATABASE_URL" in str(erro.value)


def test_abre_a_conexao_com_a_url_da_variavel_de_ambiente(monkeypatch):
    recebidas = []
    monkeypatch.setenv("DATABASE_URL", URL_COM_SEGREDO)
    monkeypatch.setattr(banco.psycopg, "connect",
                        lambda url, **_: recebidas.append(url) or "conexao")

    assert banco.abrir_conexao() == "conexao"
    assert recebidas == [URL_COM_SEGREDO]


def test_falha_de_conexao_nao_expoe_credenciais(monkeypatch):
    def conectar_falhando(url, **_):
        raise banco.psycopg.OperationalError(f"falhou em {url}")

    monkeypatch.setenv("DATABASE_URL", URL_COM_SEGREDO)
    monkeypatch.setattr(banco.psycopg, "connect", conectar_falhando)

    with pytest.raises(ErroDeInfraestrutura) as erro:
        banco.abrir_conexao()

    mensagem = str(erro.value)
    assert "senha-secreta" not in mensagem
    assert "servidor-x" not in mensagem
    assert erro.value.__cause__ is None
