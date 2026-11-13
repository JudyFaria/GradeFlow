import ast
from pathlib import Path

PASTA_DOMINIO = Path(__file__).resolve().parents[2] / "domain"

MODULOS_PROIBIDOS = frozenset({
    "use_cases", "infra", "app",
    "fastapi", "starlette", "pydantic",
    "psycopg", "psycopg2", "asyncpg", "sqlalchemy",
})


def imports_proibidos(codigo: str) -> list[str]:
    """Devolve os módulos proibidos importados por um trecho de código."""
    encontrados = []
    for no in ast.walk(ast.parse(codigo)):
        if isinstance(no, ast.Import):
            nomes = [alias.name for alias in no.names]
        elif isinstance(no, ast.ImportFrom) and no.level == 0:
            nomes = [no.module or ""]
        else:
            continue
        encontrados += [n for n in nomes
                        if n.split(".")[0] in MODULOS_PROIBIDOS]
    return encontrados


def test_modulos_do_dominio_nao_importam_camadas_externas():
    violacoes = []
    for arquivo in sorted(PASTA_DOMINIO.rglob("*.py")):
        codigo = arquivo.read_text(encoding="utf-8")
        for modulo in imports_proibidos(codigo):
            violacoes.append(
                f"{arquivo.relative_to(PASTA_DOMINIO.parent)} "
                f"importa '{modulo}' (proibido em domain/)")

    assert violacoes == []


def test_detecta_import_simples_de_camada_externa():
    assert imports_proibidos("import fastapi") == ["fastapi"]


def test_detecta_import_from_de_camada_externa():
    codigo = "from infra.repositories import algo"

    assert imports_proibidos(codigo) == ["infra.repositories"]


def test_aceita_imports_da_biblioteca_padrao_e_do_proprio_dominio():
    codigo = "import dataclasses\nfrom domain.erros import ErroDeDominio"

    assert imports_proibidos(codigo) == []
