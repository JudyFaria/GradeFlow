# Plano técnico: Esqueleto das camadas `use_cases/`, `infra/` e `app/`

Referência: `spec.md` desta pasta. Todas as dúvidas da spec foram resolvidas.

## Domain (`domain/`)

| Entidade | Atributos | Regras/validações |
|----------|-----------|-------------------|
| `ErroNaoEncontrado` (`domain/erros.py`, D1) | mensagem | Deriva de `ErroDeDominio`; usado quando o recurso não existe **ou** pertence a outro aluno (R3) |

Nenhuma entidade de negócio é criada.

## Use cases (`use_cases/`)

Nenhum caso de uso de negócio nesta feature. `use_cases/portas/` fica pronto para receber as interfaces de repositório (uma por necessidade, pequenas, SOLID-I), cada uma como `typing.Protocol` ou `abc.ABC` em módulo próprio.

| Use case | Entrada | Saída | Erros possíveis |
|----------|---------|-------|-----------------|
| (nenhum em produção; casos de uso de teste em `tests/`) | | | |

Interfaces de repositório necessárias: nenhuma em produção. Convenção registrada: portas em `use_cases/portas/`, classes de caso de uso com dependências no `__init__` e um único método público `executar`.

## Infra (`infra/`)

- Tabelas/colunas no PostgreSQL: nenhuma (fora do escopo).
- Implementação: nenhuma. `infra/repositories/` permanece como destino dos repositórios concretos; a montagem (abaixo) é o único lugar que os instanciará.
- Repositórios falsos em memória: `tests/` (R7).

## Interface web (`app/`)

Estrutura:

- `app/main.py`: `criar_app(dependencias) -> FastAPI` (fábrica, facilita teste) e `app = criar_app(montar_dependencias())` para o servidor ASGI. Registra os routers com `include_router` e os handlers de erro.
- `app/dependencias.py`: **ponto de montagem (composition root)**. `montar_dependencias()` instancia os repositórios concretos de `infra/` e os casos de uso, e devolve um contêiner simples (dataclass). Nesta feature o contêiner é vazio de repositórios; as features seguintes acrescentam campos. As rotas obtêm o que precisam via `Depends` que lê o contêiner de `app.state`; nenhuma rota importa `infra/`.
- `app/erros_http.py`: converte erros em resposta `{"detail": "<mensagem>"}` (formato padrão do FastAPI): `ErroNaoEncontrado` → 404; `ErroDeDominio` → 400; `Exception` → 500 com mensagem genérica em português (e registro do erro em log, sem expor ao cliente).
- `app/routes/saude.py`: rota pública de saúde.

| Método | Rota | Use case chamado | Resposta |
|--------|------|------------------|----------|
| GET | `/saude` | nenhum (sem regra de negócio) | 200 `{"status": "ok"}`; pública (sem login), perfil: nenhum |

Autorização por perfil (Aluno/Coordenação) fica para a feature de autenticação; nenhuma rota de negócio é criada aqui.

Dependências novas (D4, autorizadas): `fastapi`, `uvicorn` (servir), `httpx` (exigido pelo `TestClient`).

## Princípios SOLID aplicados

- S: cada módulo de `app/` tem uma responsabilidade (montar, traduzir erros, rota).
- O: novas rotas e dependências entram por `include_router` e novos campos no contêiner, sem alterar o que existe.
- L: qualquer repositório que cumpra a porta (falso em memória ou PostgreSQL) substitui o outro.
- I: portas pequenas, uma por necessidade do caso de uso.
- D: casos de uso recebem repositórios por parâmetro; só `app/dependencias.py` conhece `infra/`.

## Estratégia de testes

- `tests/app/test_saude.py`: rota de saúde pública (CA3).
- `tests/app/test_erros_http.py`: rotas de teste registradas só no teste, cada uma levantando `ErroDeDominio`, `ErroNaoEncontrado` e `RuntimeError`; verifica 400, 404 e 500 genérico sem vazamento (CA4, CA5, CA6).
- `tests/app/test_montagem.py`: `criar_app` recebe o contêiner e o expõe às rotas; `montar_dependencias()` roda sem rede nem banco (CA2).
- `tests/use_cases/test_exemplo_de_injecao.py`: caso de uso de teste com repositório falso em memória, sem FastAPI e sem banco (CA10).
- `tests/test_pureza_das_camadas.py` (generaliza o teste da feature 001, que continua valendo): `use_cases/` não importa `app`, `infra`, `fastapi`, `starlette`, `pydantic`, drivers de banco; `infra/` não importa `app`; inclui caso que prova a detecção de import proibido (CA7, CA8, CA9).
- Desempenho (RNF-01 a RNF-04): não se aplica.
