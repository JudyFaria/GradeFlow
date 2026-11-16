"""CA1 e CA9: a configuração de deploy é válida e não corta o que a
aplicação precisa."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

PASTAS_DA_APLICACAO = ("app", "domain", "use_cases", "infra", "frontend")
PASTAS_FORA_DO_DEPLOY = ("docs", "spec", "tests")


def entradas_do_vercelignore() -> list[str]:
    linhas = (RAIZ / ".vercelignore").read_text().splitlines()
    return [linha.strip().strip("/") for linha in linhas
            if linha.strip() and not linha.startswith("#")]


def test_vercelignore_nao_exclui_o_que_a_aplicacao_precisa():
    entradas = entradas_do_vercelignore()

    for pasta in PASTAS_DA_APLICACAO:
        assert pasta not in entradas
        assert not any(e.startswith(f"{pasta}/") for e in entradas)


def test_vercelignore_exclui_o_que_nao_vai_para_producao():
    entradas = entradas_do_vercelignore()

    for pasta in PASTAS_FORA_DO_DEPLOY:
        assert pasta in entradas
    assert "DOCUMENTO_PONTE.md" in entradas


def test_vercel_json_quando_existe_e_json_valido_sem_segredos():
    arquivo = RAIZ / "vercel.json"
    if not arquivo.exists():
        return
    texto = arquivo.read_text(encoding="utf-8")

    json.loads(texto)
    assert "postgres" not in texto.lower()
    assert "DATABASE_URL" not in texto


def test_ponto_de_entrada_exporta_o_app_asgi():
    from app.main import app

    assert callable(app)


def test_frontend_existe_para_ser_servido():
    assert (RAIZ / "frontend" / "index.html").is_file()
