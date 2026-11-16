import os

import psycopg

from infra.erros import ErroDeConfiguracao, ErroDeInfraestrutura

VARIAVEL_DA_URL = "DATABASE_URL"


def abrir_conexao(url: str | None = None) -> psycopg.Connection:
    """Abre uma conexão com o PostgreSQL a partir de `DATABASE_URL`."""
    url = url or os.environ.get(VARIAVEL_DA_URL)
    if not url:
        raise ErroDeConfiguracao(
            f"A variável de ambiente {VARIAVEL_DA_URL} não está definida. "
            "Defina-a com a URL de conexão do PostgreSQL.")
    try:
        return psycopg.connect(url)
    except psycopg.Error:
        # `from None`: a causa original pode conter usuário, senha e host.
        raise ErroDeInfraestrutura(
            "Não foi possível conectar ao banco de dados. "
            "Verifique a URL e se o banco está acessível.") from None
