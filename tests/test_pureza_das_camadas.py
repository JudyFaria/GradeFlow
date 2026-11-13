from pathlib import Path

from tests.domain.test_pureza_do_dominio import (
    MODULOS_PROIBIDOS,
    imports_proibidos,
)

RAIZ = Path(__file__).resolve().parents[1]

PROIBIDOS_EM_INFRA = frozenset({"app"})


def violacoes_da_camada(camada: str, proibidos: frozenset) -> list[str]:
    violacoes = []
    for arquivo in sorted((RAIZ / camada).rglob("*.py")):
        codigo = arquivo.read_text(encoding="utf-8")
        for modulo in imports_proibidos(codigo, proibidos):
            violacoes.append(
                f"{arquivo.relative_to(RAIZ)} importa '{modulo}' "
                f"(proibido em {camada}/)")
    return violacoes


def test_use_cases_nao_importam_camadas_externas_nem_frameworks():
    proibidos = MODULOS_PROIBIDOS - {"use_cases"}

    assert violacoes_da_camada("use_cases", proibidos) == []


def test_infra_nao_importa_app():
    assert violacoes_da_camada("infra", PROIBIDOS_EM_INFRA) == []


def test_detecta_use_case_importando_fastapi():
    assert imports_proibidos("from fastapi import HTTPException",
                             MODULOS_PROIBIDOS) == ["fastapi"]


def test_detecta_infra_importando_app():
    codigo = "from app.main import app"

    assert imports_proibidos(codigo, PROIBIDOS_EM_INFRA) == ["app.main"]
