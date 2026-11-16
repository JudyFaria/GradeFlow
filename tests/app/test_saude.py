from fastapi.testclient import TestClient

from app.dependencias import montar_dependencias
from app.main import criar_app


def test_saude_responde_ok_sem_login():
    cliente = TestClient(criar_app(montar_dependencias()))

    resposta = cliente.get("/saude")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}
