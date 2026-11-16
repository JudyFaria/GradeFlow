"""CA10: o código de produção não grava em disco (a Vercel é somente
leitura)."""
import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAMADAS = ("app", "domain", "use_cases", "infra")

METODOS_DE_ESCRITA = frozenset({
    "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename",
    "replace", "rmdir", "mkstemp", "NamedTemporaryFile",
    "TemporaryDirectory", "mkdtemp",
})


def gravacoes_em(codigo: str) -> list[str]:
    encontradas = []
    for no in ast.walk(ast.parse(codigo)):
        if not isinstance(no, ast.Call):
            continue
        nome = (no.func.attr if isinstance(no.func, ast.Attribute)
                else getattr(no.func, "id", ""))
        if nome in METODOS_DE_ESCRITA:
            encontradas.append(nome)
        elif nome == "open" and _abre_para_escrita(no):
            encontradas.append("open(escrita)")
    return encontradas


def _abre_para_escrita(chamada: ast.Call) -> bool:
    modos = [a for a in chamada.args[1:2]]
    modos += [k.value for k in chamada.keywords if k.arg == "mode"]
    return any(isinstance(m, ast.Constant) and isinstance(m.value, str)
               and set(m.value) & set("wax+") for m in modos)


def test_producao_nao_grava_em_disco():
    violacoes = []
    for camada in CAMADAS:
        for arquivo in sorted((RAIZ / camada).rglob("*.py")):
            codigo = arquivo.read_text(encoding="utf-8")
            for gravacao in gravacoes_em(codigo):
                violacoes.append(f"{arquivo.relative_to(RAIZ)}: {gravacao}")

    assert violacoes == []


def test_detecta_gravacoes():
    assert gravacoes_em("open('a', 'w')") == ["open(escrita)"]
    assert gravacoes_em("Path('a').write_text('x')") == ["write_text"]
    assert gravacoes_em("open('a')") == []
    assert gravacoes_em("open('a', 'r')") == []
