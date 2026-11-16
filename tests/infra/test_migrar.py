"""Testes do executor de migrações.

Usam um PostgreSQL real só se TEST_DATABASE_URL existir (D2); sem ele, os
testes de banco são ignorados e o resto roda com conexão simulada.
"""
import os

import pytest

from infra import migrar
from infra.erros import ErroDeMigracao

URL_DE_TESTE = os.environ.get("TEST_DATABASE_URL")
precisa_de_banco = pytest.mark.skipif(
    not URL_DE_TESTE, reason="TEST_DATABASE_URL não definida")


def test_lista_as_migracoes_em_ordem_de_nome(tmp_path):
    for nome in ("0002_b.sql", "0001_a.sql", "leia-me.txt"):
        (tmp_path / nome).write_text("select 1;")

    assert [m.name for m in migrar.listar_migracoes(tmp_path)] == [
        "0001_a.sql", "0002_b.sql"]


def test_pasta_de_migracoes_do_projeto_nao_cria_tabela_de_negocio():
    for arquivo in migrar.listar_migracoes(migrar.PASTA_MIGRACOES):
        assert "create table" not in arquivo.read_text().lower()


class ConexaoSimulada:
    """Registra o que o executor faz, sem banco."""

    def __init__(self, aplicadas=(), falha_em=None):
        self.aplicadas = list(aplicadas)
        self.falha_em = falha_em
        self.executadas = []
        self.commits = 0
        self.rollbacks = 0

    def execute(self, sql, params=None):
        if self.falha_em and self.falha_em in sql:
            raise RuntimeError("erro de sql")
        self.executadas.append((sql, params))
        return self

    def fetchall(self):
        return [(nome,) for nome in self.aplicadas]

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


def _migracoes(tmp_path, **conteudos):
    for nome, sql in conteudos.items():
        (tmp_path / f"{nome}.sql").write_text(sql)
    return tmp_path


def test_aplica_pendentes_em_ordem_e_registra(tmp_path):
    pasta = _migracoes(tmp_path, m0001="-- um", m0002="-- dois")
    conexao = ConexaoSimulada()

    aplicadas = migrar.aplicar_pendentes(conexao, pasta)

    assert aplicadas == ["m0001.sql", "m0002.sql"]
    registros = [p for _, p in conexao.executadas if p]
    assert registros == [("m0001.sql",), ("m0002.sql",)]


def test_nao_reaplica_migracao_ja_registrada(tmp_path):
    pasta = _migracoes(tmp_path, m0001="-- um", m0002="-- dois")
    conexao = ConexaoSimulada(aplicadas=["m0001.sql"])

    assert migrar.aplicar_pendentes(conexao, pasta) == ["m0002.sql"]


def test_falha_desfaz_para_e_informa_o_nome(tmp_path):
    pasta = _migracoes(tmp_path, m0001="-- ok", m0002="quebra", m0003="-- x")
    conexao = ConexaoSimulada(falha_em="quebra")

    with pytest.raises(ErroDeMigracao) as erro:
        migrar.aplicar_pendentes(conexao, pasta)

    assert "m0002.sql" in str(erro.value)
    assert conexao.rollbacks == 1
    registrados = [p[0] for _, p in conexao.executadas if p]
    assert registrados == ["m0001.sql"]


@precisa_de_banco
def test_banco_real_e_idempotente(tmp_path):
    import psycopg
    pasta = _migracoes(tmp_path, m0001="select 1;")
    with psycopg.connect(URL_DE_TESTE) as conexao:
        conexao.execute("drop table if exists migracoes_aplicadas")
        assert migrar.aplicar_pendentes(conexao, pasta) == ["m0001.sql"]
        assert migrar.aplicar_pendentes(conexao, pasta) == []
        conexao.execute("drop table migracoes_aplicadas")


@precisa_de_banco
def test_banco_real_desfaz_migracao_que_falha(tmp_path):
    import psycopg
    pasta = _migracoes(
        tmp_path,
        m0001="create table teste_migracao (id int); select * from nada;")
    with psycopg.connect(URL_DE_TESTE) as conexao:
        conexao.execute("drop table if exists migracoes_aplicadas")
        with pytest.raises(ErroDeMigracao):
            migrar.aplicar_pendentes(conexao, pasta)
        existe = conexao.execute(
            "select to_regclass('teste_migracao')").fetchone()[0]
        assert existe is None
        conexao.execute("drop table if exists migracoes_aplicadas")
