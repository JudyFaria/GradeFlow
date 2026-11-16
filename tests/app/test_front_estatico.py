from fastapi.testclient import TestClient

from app.dependencias import montar_dependencias
from app.main import criar_app


def cliente() -> TestClient:
    return TestClient(criar_app(montar_dependencias()))


def test_raiz_serve_a_pagina_inicial_do_front():
    resposta = cliente().get("/")

    assert resposta.status_code == 200
    assert "text/html" in resposta.headers["content-type"]
    assert "GradeFlow" in resposta.text


def test_api_continua_respondendo_com_o_front_montado():
    resposta = cliente().get("/saude")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_serve_css_e_js_externos():
    assert cliente().get("/css/estilo.css").status_code == 200
    assert cliente().get("/js/principal.js").status_code == 200


def test_csp_estrita_no_front_e_na_api():
    for caminho in ("/", "/saude"):
        csp = cliente().get(caminho).headers["content-security-policy"]

        assert csp == "default-src 'self'"
        assert "unsafe-inline" not in csp


def test_caminho_inexistente_responde_404_no_formato_da_api():
    resposta = cliente().get("/nao-existe.html")

    assert resposta.status_code == 404
    assert set(resposta.json()) == {"detail"}
    assert "frontend" not in resposta.json()["detail"]
