# Plano técnico: Deploy na Vercel com banco no Neon

Referência: `spec.md` desta pasta. Todas as dúvidas da spec foram resolvidas (D1 a D5).

## Domain / Use cases

Nenhuma mudança.

## Infra (`infra/`)

Nenhuma mudança de código esperada: `infra/banco.py` e `infra/migrar.py` (feature 003) já leem `DATABASE_URL`. O Neon exige SSL; a URL do Neon traz `sslmode=require`, que o `psycopg` respeita. Sem tabelas novas.

## Configuração de deploy

- Ponto de entrada: o `app` de `app/main.py` (variável ASGI `app`), que a Vercel detecta para FastAPI. Confirmar no primeiro deploy.
- `requirements.txt` já traz `fastapi`, `uvicorn` e `psycopg[binary]` (wheel binária, sem compilação na Vercel). `pytest`, `flake8` e `httpx` só servem ao desenvolvimento e ficam fora do pacote implantado se a Vercel permitir separar; senão, ficam e o custo é só de tamanho. A separação de arquivos de requisitos só entra se necessária e sem nova dependência.
- `vercel.json` (se preciso): roteamento para a função e `includeFiles` para `frontend/` (D1). Sem segredos.
- `.vercelignore` (D5).
- `.gitignore`: garantir `.env*` e `.vercel/` ignorados (CA6).

## Interface web (`app/`)

Sem rotas novas. A verificação pós-deploy usa `/`, `/saude` e um caminho inexistente. Se `StaticFiles` não servir na Vercel (CA9, D1), os estáticos vão para `public/` e `app/main.py` deixa de montar o `StaticFiles` em produção, mantendo as rotas da API e a CSP (a CSP passa para a configuração de cabeçalhos da Vercel nesse caso).

## Passos operacionais (fora do código, feitos pelo usuário)

1. Importar o repositório na Vercel (projeto novo, ligado ao GitHub, produção = `main`).
2. Adicionar o Neon pela integração do Marketplace; a integração injeta `DATABASE_URL` no projeto.
3. Conferir no painel que `DATABASE_URL` existe em Production (e Preview, se desejado). Nenhum segredo é colado no repositório nem na conversa.
4. Rodar `python -m infra.migrar` localmente com a `DATABASE_URL` do Neon (D2).
5. Verificar o deploy (preview e depois produção): `/`, `/saude`, 404, CSP e HTTPS.

## Princípios SOLID aplicados

- Nenhum código de negócio muda. A dependência de `DATABASE_URL` fica isolada em `infra/banco.py` (D), sem a Vercel vazar para as camadas internas.

## Estratégia de testes

- `tests/test_segredos_fora_do_repositorio.py`: varre os arquivos versionados atrás de URLs de conexão com senha (`postgres(ql)://usuario:senha@`) e de `.env` rastreado (CA6). `.gitignore` contém `.env*` e `.vercel/`.
- `tests/test_configuracao_de_deploy.py`: `vercel.json` (se existir) é JSON válido, sem segredos; `.vercelignore` não exclui `app/`, `domain/`, `use_cases/`, `infra/` nem `frontend/` (CA1, CA9).
- Testes existentes continuam cobrindo `/`, `/saude`, 404, CSP (feature 003) e a ausência de `DATABASE_URL` (CA7).
- Verificação manual pós-deploy (CA1 a CA5, CA9, CA10): roteiro curto no `AGENTS.md`, seção "Comandos"; a leitura do sistema de arquivos somente leitura é conferida pela ausência de gravações no código (`grep` por `open(..., "w")` fora de `tests/`).
- Desempenho (RNF-01 a RNF-04): não se aplica.
