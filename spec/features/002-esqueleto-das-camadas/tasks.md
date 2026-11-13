# Tarefas: Esqueleto das camadas `use_cases/`, `infra/` e `app/`

Referências: `spec.md` e `plan.md` desta pasta.
Marque `[x]` ao concluir. Escreva os testes antes da implementação.
Só iniciar após a spec ser aprovada (dúvidas já resolvidas).

## Preparação

- [x] T1: Confirmar os pacotes e subpastas existentes (CA1) e, adicionar (D4) `fastapi`, `uvicorn` e `httpx` ao `requirements.txt` e instalar

## Domain

- [x] T2: Escrever teste de `ErroNaoEncontrado` em `tests/domain/test_erros.py` (deriva de `ErroDeDominio`, preserva a mensagem) (CA5)
- [x] T3: Implementar `ErroNaoEncontrado` em `domain/erros.py`

## Pureza das camadas

- [x] T4: Escrever `tests/test_pureza_das_camadas.py` para `use_cases/` e `infra/`, incluindo o caso que detecta import proibido (CA7, CA8, CA9); reaproveitar o detector da feature 001 sem duplicar

## Use cases

- [x] T5: Escrever o teste com caso de uso e repositório falso em memória em `tests/use_cases/` (CA10)
- [x] T6: Registrar a convenção de portas e casos de uso (docstring em `use_cases/portas/__init__.py`, sem código de negócio)

## Web (`app/`)

- [x] T7: Escrever `tests/app/test_saude.py` (CA3)
- [x] T8: Escrever `tests/app/test_erros_http.py` para 400, 404 e 500 genérico (CA4, CA5, CA6)
- [x] T9: Escrever `tests/app/test_montagem.py` (CA2)
- [x] T10: Implementar `app/erros_http.py`
- [x] T11: Implementar `app/dependencias.py` (contêiner e `montar_dependencias()`)
- [x] T12: Implementar `app/routes/saude.py`
- [x] T13: Implementar `app/main.py` (`criar_app`, `include_router`, handlers, `app`)

## Infra

- Nada nesta feature (repositórios PostgreSQL vêm no item seguinte do TO-DO).

## Validação

- [x] T14: `pytest` passando (CA11)
- [x] T15: `flake8` sem erros (CA11)
- [x] T16: Iniciar a aplicação localmente e consultar `/saude` (CA2, CA3)
- [x] T17: Critérios de aceitação da `spec.md` conferidos (CA1–CA11) e status da spec atualizado
