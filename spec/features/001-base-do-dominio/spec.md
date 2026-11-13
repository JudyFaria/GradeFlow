# Spec: Base do domain/

- **ID**: 001
- **Status**: Implementada
- **Data**: 2026-11-13

Requisitos: RNF-16, RNF-17 (SRS).
TO-DO: seção 1, item "Criar `domain/` conforme a constituição, com a montagem das dependências na inicialização." (só a parte de `domain/`; ver "Fora do escopo").

## História de usuário

**Como** pessoa que desenvolve o GradeFlow,
**quero** a camada `domain/` pronta com a base de erros de domínio e uma garantia automática de que ela não depende de nenhuma outra camada,
**para que** as regras de negócio (pré e co-requisitos, créditos, vagas, choque de horário, limites de eletivas) possam ser escritas e testadas isoladas da interface e do banco (RNF-16, RNF-17).

Não há ator final (Aluno ou Coordenação) nem tela nesta feature.

## Critérios de aceitação

- [x] CA1: Dado o repositório, quando se listam as pastas de código, então `domain/` existe como pacote.
- [x] CA2: Dado a camada `domain/`, quando uma regra de negócio é violada, então existe um tipo de erro de domínio base do qual todos os erros de domínio futuros derivam.
- [x] CA3: Dado um erro de domínio criado com uma mensagem, quando a mensagem é lida, então ela é a mesma informada, sem detalhes de HTTP ou de banco.
- [x] CA4: Dado qualquer módulo de `domain/`, quando se examinam seus imports, então ele não depende de `use_cases/`, `infra/`, `app/`, FastAPI nem de biblioteca de banco.
- [x] CA5 (exceção): Dado que um módulo de `domain/` passe a importar uma camada externa, quando os testes rodam, então o teste de pureza falha indicando o módulo e o import proibido.
- [x] CA6: Dado o projeto, quando se roda `pytest` e `flake8`, então ambos passam sem erros.

## Regras de negócio

- R1: `domain/` contém só entidades, objetos de valor e regras puras; não importa FastAPI, PostgreSQL nem outra camada (constituição, seção 1; AGENTS.md).
- R2: Erros de regra de negócio são erros de domínio; o mapeamento para HTTP fica em `app/` e nunca em `domain/` (AGENTS.md).
- R3: O domínio não lê relógio, variável de ambiente nem arquivo; o que for externo entra por parâmetro (RNF-16; a porta `Relogio` é item próprio do TO-DO).
- R4: Grades, disciplinas e oferta ficam no banco, nunca no código (RNF-17); esta feature não cria nenhuma delas.

## Fora do escopo

- Montagem das dependências na inicialização: pertence a `app/`, não a `domain/` (constituição, seção 1); fica para a feature de `app/`/`use_cases/`/`infra/`.
- Entidades e regras reais (`Semestre`, `Disciplina`, `Plano`…): TO-DO seções 3 e 4.
- Porta `Relogio`, FastAPI, PostgreSQL, migrações, `StaticFiles`, `frontend/`.
- Erros de domínio específicos (ex.: movimento bloqueado): entram com as regras que os usam.

## Dúvidas em aberto

- Nenhuma.

## Decisões

- D1 (resolvida): os erros de domínio ficam num módulo único, `domain/erros.py`.
- D2 (resolvida): a verificação de pureza de `domain/` (CA4/CA5) é um teste automatizado em `tests/domain/`.
- D3 (resolvida): o `requirements.txt` (`pytest`, `flake8`) já foi criado manualmente pelo usuário; esta feature não o cria.
