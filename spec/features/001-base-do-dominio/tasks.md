# Tarefas: Base do domain/

Referências: `spec.md` e `plan.md` desta pasta.
Marque `[x]` ao concluir. Escreva os testes antes da implementação.
Só iniciar após a spec ser aprovada.

## Preparação

- [x] T1: Confirmar o pacote `domain/` (CA1) e instalar `pytest` e `flake8` a partir do `requirements.txt` existente

## Domain

- [x] T2: Escrever testes de `ErroDeDominio` em `tests/domain/test_erros.py` (CA2, CA3)
- [x] T3: Implementar `ErroDeDominio` em `domain/erros.py`
- [x] T4: Escrever o teste de pureza em `tests/domain/test_pureza_do_dominio.py`, incluindo o caso que detecta import proibido (CA4, CA5)

## Use cases / Infra / Web

- Nada nesta feature.

## Validação

- [x] T5: `pytest` passando (CA6)
- [x] T6: `flake8` sem erros (CA6)
- [x] T7: Critérios de aceitação da `spec.md` conferidos (CA1–CA6)
