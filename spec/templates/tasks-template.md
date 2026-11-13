# Tarefas: [Nome da feature]

Referências: `spec.md` e `plan.md` desta pasta.
Marque `[x]` ao concluir. Escreva os testes antes da implementação.

## Domain

- [ ] T1: Escrever testes da entidade em `tests/domain/`
- [ ] T2: Implementar a entidade em `domain/`

## Use cases

- [ ] T3: Definir a interface do repositório
- [ ] T4: Escrever testes do use case em `tests/use_cases/` (repositório em memória)
- [ ] T5: Implementar o use case em `use_cases/`

## Infra

- [ ] T6: Implementar o repositório PostgreSQL em `infra/repositories/`

## Web

- [ ] T7: Criar a rota em `app/routes/` e registrar o router em `app/main.py` (`include_router`)

## Validação

- [ ] T8: `pytest` passando
- [ ] T9: `flake8` sem erros
- [ ] T10: Critérios de aceitação da `spec.md` conferidos