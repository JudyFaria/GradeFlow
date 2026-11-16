import re
from pathlib import Path

PASTA = Path(__file__).resolve().parents[1] / "frontend"

PADROES_PROIBIDOS = {
    "script inline": re.compile(r"<script(?![^>]*\bsrc=)[^>]*>", re.I),
    "bloco <style>": re.compile(r"<style\b", re.I),
    "atributo style": re.compile(r"\sstyle\s*=", re.I),
    "manipulador on*": re.compile(r"\son[a-z]+\s*=", re.I),
    "innerHTML": re.compile(r"innerHTML|outerHTML|insertAdjacentHTML"),
}


def violacoes(texto: str) -> list[str]:
    return [nome for nome, padrao in PADROES_PROIBIDOS.items()
            if padrao.search(texto)]


def test_frontend_nao_tem_script_estilo_inline_nem_innerhtml():
    encontrados = []
    for arquivo in sorted(PASTA.rglob("*")):
        if arquivo.suffix in {".html", ".css", ".js"}:
            for nome in violacoes(arquivo.read_text(encoding="utf-8")):
                encontrados.append(f"{arquivo.relative_to(PASTA)}: {nome}")

    assert encontrados == []


def test_detecta_cada_tipo_de_violacao():
    assert violacoes("<script>x()</script>") == ["script inline"]
    assert violacoes("<style>a{}</style>") == ["bloco <style>"]
    assert violacoes('<p style="color:red">') == ["atributo style"]
    assert violacoes('<a onclick="x()">') == ["manipulador on*"]
    assert violacoes("el.innerHTML = x") == ["innerHTML"]
    assert violacoes('<script src="js/a.js"></script>') == []
