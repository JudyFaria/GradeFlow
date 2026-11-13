# Plano técnico: Base do domain/

Referência: `spec.md` desta pasta. Todas as dúvidas da spec foram resolvidas.

## Domain (`domain/`)

| Entidade | Atributos | Regras/validações |
|----------|-----------|-------------------|
| `ErroDeDominio` (`domain/erros.py`) | mensagem | Raiz de todas as exceções de domínio; deriva de `Exception`; sem imports externos |

Nenhuma entidade de negócio é criada aqui.

## Use cases (`use_cases/`)

Nenhum nesta feature.

Interfaces de repositório necessárias: nenhuma.

## Infra (`infra/`)

- Tabelas/colunas no PostgreSQL: nenhuma.
- Implementação: nenhuma.

## Interface web (`app/routes/`)

Nenhuma rota. O mapeamento de `ErroDeDominio` para HTTP entra com a feature de `app/`.

## Princípios SOLID aplicados

- S: `domain/erros.py` só define erros.
- O: erros específicos futuros estendem `ErroDeDominio` sem alterá-lo.
- D: o domínio não depende de camadas externas (verificado por teste).

## Estratégia de testes

- `tests/domain/test_erros.py`: `ErroDeDominio` carrega a mensagem e é `Exception` (CA2, CA3).
- `tests/domain/test_pureza_do_dominio.py` percorre os módulos de `domain/` com `ast` e falha se algum importar `use_cases`, `infra`, `app`, `fastapi` ou driver de banco; um teste auxiliar prova que um import proibido é detectado (CA4, CA5).
- Desempenho (RNF-01 a RNF-04): não se aplica.
