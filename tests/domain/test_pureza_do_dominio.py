import ast
from pathlib import Path

PASTA_DOMINIO = Path(__file__).resolve().parents[2] / "domain"

MODULOS_PROIBIDOS = frozenset({
    "use_cases", "infra", "app",
    "fastapi", "starlette", "pydantic",
    "psycopg", "psycopg2", "asyncpg", "sqlalchemy",
})


def imports_proibidos(codigo: str,
                      proibidos: frozenset = MODULOS_PROIBIDOS) -> list[str]:
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
                        if n.split(".")[0] in proibidos]
    return encontrados


LEITURAS_DO_RELOGIO = frozenset({"now", "today", "utcnow"})


def leituras_do_relogio(codigo: str) -> list[str]:
    """Devolve as chamadas que leem a data/hora do sistema (R8)."""
    encontradas = []
    for no in ast.walk(ast.parse(codigo)):
        if not (isinstance(no, ast.Call)
                and isinstance(no.func, ast.Attribute)):
            continue
        funcao = no.func
        e_time_time = (funcao.attr == "time"
                       and isinstance(funcao.value, ast.Name)
                       and funcao.value.id == "time")
        if funcao.attr in LEITURAS_DO_RELOGIO or e_time_time:
            encontradas.append(ast.unparse(funcao))
    return encontradas


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


def test_dominio_nao_le_o_relogio_do_sistema():
    violacoes = []
    for arquivo in sorted(PASTA_DOMINIO.rglob("*.py")):
        codigo = arquivo.read_text(encoding="utf-8")
        for chamada in leituras_do_relogio(codigo):
            violacoes.append(
                f"{arquivo.relative_to(PASTA_DOMINIO.parent)} "
                f"chama '{chamada}' (a data entra por injeção)")

    assert violacoes == []


def test_detecta_leitura_do_relogio_do_sistema():
    assert leituras_do_relogio("date.today()") == ["date.today"]
    assert leituras_do_relogio("datetime.now()") == ["datetime.now"]
    assert leituras_do_relogio("time.time()") == ["time.time"]


def test_nao_confunde_metodo_comum_com_leitura_do_relogio():
    assert leituras_do_relogio("relogio.hoje()") == []
