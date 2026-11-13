from fastapi import APIRouter

roteador = APIRouter()


@roteador.get("/saude")
def saude():
    return {"status": "ok"}
