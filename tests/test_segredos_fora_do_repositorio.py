"""CA6: nenhuma credencial de banco nos arquivos versionados nem no git."""
import re
import subprocess
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]

URL_COM_SENHA = re.compile(r"postgres(?:ql)?://[^\s:/@]+:([^\s@]+)@")
# Senhas de mentira usadas só em testes ("abc123" já consta no histórico).
SENHAS_FICTICIAS = frozenset({"senha-secreta", "abc123"})


def credenciais_em(texto: str) -> list[str]:
    return [m.group(0) for m in URL_COM_SENHA.finditer(texto)
            if m.group(1) not in SENHAS_FICTICIAS]


def git(*argumentos: str) -> str:
    resultado = subprocess.run(
        ["git", *argumentos], cwd=RAIZ, capture_output=True,
        text=True, encoding="utf-8", errors="replace")
    if resultado.returncode != 0:
        pytest.skip("git indisponível ou fora de um repositório")
    return resultado.stdout


def test_detecta_url_de_conexao_com_senha():
    # Montada em partes para o próprio teste não parecer um vazamento.
    url = "postgresql://u:" + "x9Kq72" + "@host/db"

    assert credenciais_em(url)


def test_ignora_url_sem_senha_e_senha_ficticia():
    assert credenciais_em("postgresql://host/db") == []
    assert credenciais_em("postgresql://u:senha-secreta@h/db") == []


def test_arquivos_versionados_nao_tem_url_de_conexao_com_senha():
    violacoes = []
    for nome in git("ls-files").splitlines():
        arquivo = RAIZ / nome
        if not arquivo.is_file() or arquivo.suffix == ".pdf":
            continue
        texto = arquivo.read_text(encoding="utf-8", errors="ignore")
        if credenciais_em(texto):
            violacoes.append(nome)

    assert violacoes == []


def test_historico_do_git_nao_tem_url_de_conexao_com_senha():
    assert credenciais_em(git("log", "--all", "-p")) == []


def test_nenhum_arquivo_env_esta_versionado():
    versionados = [nome for nome in git("ls-files").splitlines()
                   if Path(nome).name.startswith(".env")]

    assert versionados == []


def test_gitignore_cobre_env_e_pasta_da_vercel():
    linhas = (RAIZ / ".gitignore").read_text().splitlines()

    assert ".env*" in linhas
    assert ".vercel/" in linhas
