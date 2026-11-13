# GradeFlow

Aplicação web para o aluno da PUC-Rio planejar os períodos que ainda faltam
cursar e se matricular em turmas. O aluno monta o planejamento em um grafo de
disciplinas que respeita pré e co-requisitos; a coordenação define a oferta de
turmas.

O GradeFlow é pensado como um módulo do SAU (sistema acadêmico da
universidade). A integração com o SAU é simulada: o "Falta Cursar", as grades
curriculares e as matrículas "vêm do SAU", mas não há comunicação real com ele.


## Atores e casos de uso

| Ator | Casos de uso |
|------|--------------|
| **Aluno** | UC01 Cadastro e seleção de curso · UC02 Importar "Falta Cursar" · UC03 Planejar períodos e matricular-se (grafo, catálogo, planejamentos salvos, matrícula) |
| **Coordenação** | UC04 Controlar oferta de turmas |

## Principais funcionalidades

- **Grafo de disciplinas**: colunas por período ("Período atual", +1, +2…),
  arrastar e soltar com mouse, touchpad e toque. A movimentação só é aceita se
  respeitar pré e co-requisitos e o limite de 30 créditos por período.
- **Códigos curriculares**: disciplinas normais, optativas (escolher uma de um
  conjunto) e eletivas (buscar em qualquer curso até completar os créditos),
  com limites de contabilização de eletivas.
- **Importação do Falta Cursar** a partir de arquivo `.xlsx`. Sem importação,
  vale a grade sugerida mais atual do curso.
- **Catálogo e turmas**: consulta da oferta, com micro-horário.
- **Matrícula**: exige vaga, ausência de choque de horário e requisitos
  atendidos; só é registrada ao clicar em "Confirmar matrícula".
- **Planejamentos salvos**: cada aluno salva e restaura os próprios
  planejamentos.
- **Oferta de turmas** (coordenação): cadastro de turmas, horários e vagas, com
  demanda agregada por turma e disciplina.

## Tecnologias

| Área | Tecnologia |
|------|------------|
| Linguagem | Python |
| API web | FastAPI |
| Frontend | HTML, CSS e JavaScript puros, sem framework nem etapa de build |
| Banco de dados | PostgreSQL, hospedado no Neon (modelo relacional com 20 tabelas, Apêndice B do SRS) |
| Testes | pytest, com repositórios falsos em memória nos testes de casos de uso |
| Estilo | PEP-8, verificado com flake8 |
| Hospedagem | Vercel |
| Importação | Arquivos `.xlsx` (Falta Cursar) |
| Metodologia | Spec-Driven Development (SDD) |

## Arquitetura

O projeto segue Clean Architecture: as dependências apontam sempre para dentro,
e o domínio não conhece FastAPI, PostgreSQL nem nenhuma outra camada externa.

```
frontend/ (HTML, CSS, JS)  ──HTTP──→  app/ (FastAPI, rotas)
app/                       ──→  use_cases/  ──→  domain/
infra/ (PostgreSQL)        ──→  interfaces de use_cases/  ──→  domain/
```

| Camada | Responsabilidade |
|--------|------------------|
| `domain/` | Entidades, objetos de valor e regras de negócio puras: pré e co-requisitos, limite de créditos, vagas, choque de horário, limites de eletivas |
| `use_cases/` | Um caso de uso por ação de negócio. Define as interfaces dos repositórios e as recebe por injeção de dependência |
| `infra/` | Repositórios concretos (PostgreSQL) e integrações externas, como a leitura de `.xlsx` |
| `app/` | Adaptador HTTP: converte requisições em chamadas aos casos de uso e erros de domínio em respostas HTTP, sem regra de negócio |
| `frontend/` | Telas do aluno e da coordenação. Consome a API e só exibe o resultado das verificações, que acontecem no domínio |

As dependências são montadas na inicialização da aplicação. Os princípios
completos (Clean Code, SOLID, testes) estão em
[`spec/constitution.md`](spec/constitution.md).

## Estrutura do projeto

```
GradeFlow/
├── app/                    # Rotas FastAPI (adaptador HTTP)
├── use_cases/              # Casos de uso e interfaces de repositório
├── domain/                 # Entidades e regras de negócio
├── infra/                  # Repositórios PostgreSQL e integrações
├── frontend/               # HTML, CSS e JS puros (telas, grafo, arrastar e soltar)
├── tests/                  # Testes pytest
├── docs/
│   └── GradeFlow_SRS.pdf   # Requisitos (RF-nn, RNF-nn, RN-nn), telas e modelo de dados
├── spec/                   # Spec-Driven Development
│   ├── README.md           # Fluxo do SDD
│   ├── constitution.md     # Princípios inegociáveis do projeto
│   ├── templates/          # Modelos de spec.md, plan.md e tasks.md
│   └── features/           # Uma pasta por feature (001-nome, 002-nome…)
├── .claude/skills/         # Skill criar-feature-sdd
├── AGENTS.md               # Instruções para agentes de IA
├── TO-DO.md                # Decisões tomadas e tarefas do porte do protótipo
└── README.md
```


## Como contribuir

1. **Especificar**: crie `spec/features/NNN-nome/spec.md` a partir do template,
   com a história de usuário e os critérios de aceitação. Cite os IDs dos
   requisitos do SRS.
2. **Planejar**: escreva `plan.md` com entidades, casos de uso, repositórios e
   rotas, seguindo a constituição.
3. **Quebrar em tarefas**: escreva `tasks.md`, com os testes primeiro.
4. **Implementar e validar**: cada critério de aceitação precisa de um teste
   `pytest` passando.

No Claude Code, a skill `criar-feature-sdd` gera os três artefatos de uma
feature a partir de um pedido.

Cite o ID do requisito (RF-nn, RNF-nn, RN-nn) nas specs, nos testes e nas
mensagens de commit.

## Origem

Reaproveita o protótipo
[grafo_disciplinas](https://github.com/JudyFaria/grafo_disciplinas), que já
implementa a visualização do grafo e a verificação de pré e co-requisitos.
