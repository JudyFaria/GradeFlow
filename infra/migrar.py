"""Executor de migrações: `python -m infra.migrar`.

Aplica, em ordem de nome, os arquivos `infra/migracoes/*.sql` ainda não
registrados em `migracoes_aplicadas`. Cada migração roda em transação
própria. Roda por comando explícito, nunca na subida da aplicação.
"""
import sys
from pathlib import Path

from infra.banco import abrir_conexao
from infra.erros import (
    ErroDeConfiguracao,
    ErroDeInfraestrutura,
    ErroDeMigracao,
)

PASTA_MIGRACOES = Path(__file__).resolve().parent / "migracoes"

CRIAR_TABELA_DE_CONTROLE = (
    "create table if not exists migracoes_aplicadas ("
    "nome text primary key, "
    "aplicada_em timestamptz not null default now())")
LISTAR_APLICADAS = "select nome from migracoes_aplicadas"
REGISTRAR = "insert into migracoes_aplicadas (nome) values (%s)"


def listar_migracoes(pasta: Path) -> list[Path]:
    return sorted(pasta.glob("*.sql"), key=lambda arquivo: arquivo.name)


def aplicar_pendentes(conexao, pasta: Path = PASTA_MIGRACOES) -> list[str]:
    """Aplica as migrações pendentes e devolve os nomes aplicados."""
    conexao.execute(CRIAR_TABELA_DE_CONTROLE)
    conexao.commit()
    ja_aplicadas = {linha[0]
                    for linha in conexao.execute(LISTAR_APLICADAS).fetchall()}
    aplicadas = []
    for arquivo in listar_migracoes(pasta):
        if arquivo.name in ja_aplicadas:
            continue
        try:
            conexao.execute(arquivo.read_text(encoding="utf-8"))
            conexao.execute(REGISTRAR, (arquivo.name,))
            conexao.commit()
        except Exception as erro:
            conexao.rollback()
            raise ErroDeMigracao(
                f"A migração {arquivo.name} falhou e foi desfeita: "
                f"{type(erro).__name__}. As seguintes não foram aplicadas."
            ) from erro
        aplicadas.append(arquivo.name)
    return aplicadas


def main() -> int:
    try:
        with abrir_conexao() as conexao:
            aplicadas = aplicar_pendentes(conexao)
    except (ErroDeConfiguracao, ErroDeInfraestrutura, ErroDeMigracao) as erro:
        print(erro, file=sys.stderr)
        return 1
    if aplicadas:
        print("Migrações aplicadas: " + ", ".join(aplicadas))
    else:
        print("Nenhuma migração pendente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
