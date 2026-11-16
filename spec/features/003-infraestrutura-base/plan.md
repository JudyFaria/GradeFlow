# Plano técnico: Infraestrutura base

Referência: `spec.md` desta pasta. Todas as dúvidas da spec foram resolvidas; "(D#)" indica a decisão correspondente.

## Domain (`domain/`)

Nenhuma entidade nova. Regra: nenhum módulo de `domain/` lê o relógio do sistema; datas entram por parâmetro (R8). O teste de pureza do domínio passa a vetar `datetime.now`, `datetime.today`, `date.today` e `time.time` (CA10).

## Use cases (`use_cases/`)

Nenhum caso de uso de negócio.

Portas novas em `use_cases/portas/` (pequenas, SOLID-I):

- `Relogio` (`relogio.py`): `hoje() -> date`.

Sobre o banco: não há porta genérica "de banco". Cada feature define a sua porta de repositório; `infra/` recebe a conexão.

## Infra (`infra/`)

- `infra/relogio_sistema.py`: `RelogioSistema` implementa `Relogio` com a data do sistema (CA11).
- `infra/banco.py`: `abrir_conexao(url=None)` lê `DATABASE_URL` (R2); sem a variável, levanta `ErroDeConfiguracao` com mensagem em português (CA2); falha de conexão vira `ErroDeInfraestrutura` sem credenciais (CA3). Conexão por requisição (D3). Driver `psycopg` (D2).
- `infra/migrar.py` (`python -m infra.migrar`): cria a tabela `migracoes_aplicadas(nome, aplicada_em)` se faltar, lista `infra/migracoes/*.sql` em ordem, aplica cada pendente em transação própria e registra; falha desfaz a migração, interrompe e informa o nome (CA4–CA6, R3). (D1)
- `infra/migracoes/`: pasta com `0001_base.sql` apenas se preciso para provar o mecanismo; **sem tabelas de negócio** (CA4). A decisão de manter uma migração vazia ou usar só a de controle fica para a implementação, sem criar tabela fora do SRS (Apêndice B).
- Erros novos `ErroDeConfiguracao` e `ErroDeInfraestrutura` ficam em `infra/erros.py`; não pertencem ao domínio. O mapeamento para 500 genérico já existe em `app/erros_http.py` (feature 002).
- Nada grava em disco em execução (R4).

## Interface web (`app/`)

- `app/dependencias.py`: `Dependencias` ganha o campo `relogio: Relogio`; `montar_dependencias()` instancia `RelogioSistema`. O banco **não** é aberto na montagem (CA2); rotas futuras recebem uma conexão por `Depends` que chama `infra.banco` por meio do contêiner, nunca importando `infra/` diretamente.
- `app/main.py`: após `include_router`, monta `StaticFiles(directory="frontend", html=True)` em `/`, **depois** dos routers para não encobrir a API (CA7). Middleware simples acrescenta a todas as respostas o cabeçalho `Content-Security-Policy: default-src 'self'` (D4) (CA8). 404 de estático no formato `{"detail": ...}` (CA9).
- Segurança de caminho: `StaticFiles` impede saída do diretório; a pasta é resolvida a partir do arquivo, não do diretório de trabalho, para funcionar na Vercel.

| Método | Rota | Use case chamado | Resposta |
|--------|------|------------------|----------|
| GET | `/` | nenhum | `frontend/index.html`; pública, perfil: nenhum |
| GET | `/saude` | nenhum | já existe (feature 002) |

## Interface (`frontend/`)

Tela afetada: nenhuma das 11 do SRS; apenas página inicial mínima.

- `frontend/index.html`, `frontend/css/estilo.css`, `frontend/js/principal.js`: sem script nem estilo inline (R6).
- Chamada à API: `GET /saude`; mostra "GradeFlow" e o estado do serviço. Texto do usuário/da API só via `textContent`.
- Textos exibidos (pt-BR): título "GradeFlow"; "Serviço no ar" / "Serviço indisponível no momento. Tente novamente em instantes."
- Nenhuma regra de negócio no front (R7).

## Princípios SOLID aplicados

- S: relógio, conexão, migração e estáticos em módulos separados.
- O: novas migrações são novos arquivos; novos campos entram no contêiner sem alterar o existente.
- L: `RelogioSistema` e o relógio falso dos testes substituem-se pela porta.
- I: `Relogio` tem um único método.
- D: o domínio e os casos de uso dependem da porta `Relogio`; só `app/dependencias.py` conhece `RelogioSistema`.

## Estratégia de testes

- `tests/domain/test_pureza_do_dominio.py`: estende o detector para chamadas ao relógio do sistema (CA10).
- `tests/use_cases/test_relogio_injetado.py`: caso de uso de teste com `RelogioFalso`, data fixa (CA10).
- `tests/infra/test_relogio_sistema.py`: `hoje()` igual à data do sistema (CA11).
- `tests/infra/test_banco.py`: sem `DATABASE_URL` → `ErroDeConfiguracao` em português; URL inválida → erro sem credenciais (CA1–CA3), sem rede (driver simulado).
- `tests/infra/test_migrar.py`: lógica do executor com conexão simulada ou, se `TEST_DATABASE_URL` existir, banco real: aplica em ordem, idempotente, falha desfaz tudo e para (CA4–CA6). Ignorado sem banco de teste (D2).
- `tests/app/test_front_estatico.py`: `/` serve HTML; `/saude` continua JSON; caminho inexistente 404 com `detail`; CSP presente e sem `unsafe-inline` (CA7–CA9).
- `tests/test_frontend_sem_inline.py`: varre `frontend/` e falha em `<script>` sem `src`, atributo `style=`, `<style>`, `on*=` e `innerHTML` (CA8).
- `tests/app/test_montagem.py`: continua provando que montar não abre banco (CA2, CA13).
- `tests/test_pureza_das_camadas.py`: `infra/` continua sem importar `app/`; `use_cases/` sem driver de banco, incluindo `psycopg`.
- Desempenho (RNF-01 a RNF-04): não se aplica.
