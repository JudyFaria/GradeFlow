# Spec: Esqueleto das camadas `use_cases/`, `infra/` e `app/`

- **ID**: 002
- **Status**: Implementada
- **Data**: 2026-11-13

Requisitos: RNF-16, RNF-17 (SRS); AGENTS.md (Arquitetura, Privacidade).
TO-DO: seção 1, item "Criar `domain/`, `use_cases/`, `infra/`, `app/` conforme a constituição, com a montagem das dependências na inicialização." (`domain/` já foi feito na feature 001; esta feature cobre `use_cases/`, `infra/`, `app/` e a montagem das dependências).

## História de usuário

**Como** pessoa que desenvolve o GradeFlow,
**quero** as camadas `use_cases/`, `infra/` e `app/` prontas como esqueleto, com a aplicação web iniciando e as dependências montadas num único ponto de inicialização, e com o erro de domínio traduzido para uma resposta de erro padronizada,
**para que** cada funcionalidade seguinte entre pela mesma estrutura (rota → caso de uso → domínio, com repositórios injetados) e as regras de negócio continuem testáveis sem interface e sem banco (RNF-16, RNF-17).

Não há ator final (Aluno ou Coordenação) nem tela nesta feature; o único contato externo é uma rota de verificação de saúde.

## Critérios de aceitação

- [x] CA1: Dado o repositório, quando se listam as pastas de código, então `domain/`, `use_cases/`, `infra/` e `app/` existem como pacotes, com as subpastas `use_cases/portas/`, `infra/repositories/` e `app/routes/`.
- [x] CA2: Dada a aplicação, quando ela é iniciada, então as dependências concretas são montadas num único ponto da inicialização e entregues às rotas; nenhum caso de uso nem rota cria repositório ou conexão por conta própria.
- [x] CA3: Dada a aplicação em execução, quando se consulta a rota de saúde sem estar logado, então a resposta indica que o serviço está no ar.
- [x] CA4: Dado um caso de uso que levanta um erro de domínio, quando a rota que o chama é acionada, então a resposta é 400, com a mensagem do erro de domínio em português no formato padrão de erro da API (`detail`).
- [x] CA5 (exceção): Dado um caso de uso que levanta o erro de "não encontrado" (inclusive dado de outro aluno), quando a rota é acionada, então a resposta é 404 e não revela se o dado existe para outra pessoa (nunca 403).
- [x] CA6 (exceção): Dado um erro inesperado (que não é erro de domínio), quando a rota é acionada, então a resposta é 500 com mensagem genérica, sem detalhe interno (stack trace, SQL, caminho de arquivo).
- [x] CA7: Dado qualquer módulo de `use_cases/`, quando se examinam seus imports, então ele não depende de `app/`, `infra/`, FastAPI nem de biblioteca de banco.
- [x] CA8: Dado qualquer módulo de `infra/`, quando se examinam seus imports, então ele não depende de `app/`.
- [x] CA9 (exceção): Dado que um módulo de `use_cases/` ou `infra/` passe a importar uma camada proibida, quando os testes rodam, então o teste de pureza falha indicando o módulo e o import.
- [x] CA10: Dado um caso de uso de teste com repositório falso em memória injetado, quando ele é executado, então funciona sem banco e sem FastAPI.
- [x] CA11: Dado o projeto, quando se roda `pytest` e `flake8`, então ambos passam sem erros.

## Regras de negócio

- R1: Dependências apontam para dentro: `app/` → `use_cases/` → `domain/`; `infra/` implementa as portas definidas em `use_cases/portas/` (constituição, seção 1).
- R2: Casos de uso levantam erros de domínio, nunca `HTTPException`; o mapeamento para HTTP fica só em `app/` (AGENTS.md).
- R3: Dado de outro aluno responde 404, não 403 (AGENTS.md, Privacidade).
- R4: Um caso de uso por ação; recebe os repositórios por injeção, sem criar conexões (constituição, seções 1 e 3).
- R5: Mensagens de erro ao usuário em português do Brasil, explicando a causa (RNF-13); detalhes internos nunca vazam (constituição, seção 1).
- R6: Nenhum dado de negócio (grades, disciplinas, oferta) entra no código desta feature (RNF-17).
- R7: Repositórios falsos em memória vivem em `tests/`, não em código de produção (constituição, seção 4).

## Fora do escopo

- PostgreSQL, `DATABASE_URL`, migrações, seed e repositórios concretos de banco (item seguinte do TO-DO: "Configurar FastAPI, PostgreSQL, migrações...").
- `StaticFiles` e `frontend/`; porta `Relogio`; deploy na Vercel.
- Autenticação, autorização por perfil e proteção "tudo exige login" (RF-09, RNF-07, RNF-09): feature própria; só a rota de saúde existe e é pública.
- Entidades e casos de uso de negócio reais (TO-DO seções 3 em diante).
- Seção "Comandos" do `AGENTS.md` (item próprio do TO-DO).

## Dúvidas em aberto

- Nenhuma.

## Decisões

- D1 (resolvida, pelo usuário): `ErroNaoEncontrado(ErroDeDominio)` entra nesta feature, em `domain/erros.py`, porque o mapeamento para 404 é transversal.
- D2 (resolvida, pelo usuário): `ErroDeDominio` genérico responde 400.
- D3 (resolvida, pelo usuário): formato padrão de erro do FastAPI, `{"detail": "<mensagem>"}`.
- D4 (resolvida, pelo usuário): `fastapi`, `uvicorn` e `httpx` entram no `requirements.txt`.
- D5 (resolvida, pelo usuário): fronteira desta feature = esqueleto mínimo com FastAPI; PostgreSQL, migrações e `StaticFiles` ficam para o item seguinte do TO-DO.
