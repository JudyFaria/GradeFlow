# Tarefas: Infraestrutura base

Referências: `spec.md` e `plan.md` desta pasta.
Marque `[x]` ao concluir. Escreva os testes antes da implementação.
Só iniciar após a spec ser aprovada (dúvidas já resolvidas).

## Preparação

- [x] T1: Adicionar `psycopg` (D2, autorizado) ao `requirements.txt` e instalar

## Relógio (domain + use_cases + infra)

- [x] T2: Estender `tests/domain/test_pureza_do_dominio.py` para vetar leitura do relógio do sistema (CA10)
- [x] T3: Escrever `tests/use_cases/test_relogio_injetado.py` com `RelogioFalso` (CA10)
- [x] T4: Definir a porta `Relogio` em `use_cases/portas/relogio.py`
- [x] T5: Escrever `tests/infra/test_relogio_sistema.py` (CA11)
- [x] T6: Implementar `infra/relogio_sistema.py`

## Banco e migrações (infra)

- [x] T7: Escrever `tests/infra/test_banco.py` (CA1, CA2, CA3)
- [x] T8: Implementar `infra/erros.py` e `infra/banco.py`
- [x] T9: Escrever `tests/infra/test_migrar.py` (CA4, CA5, CA6)
- [x] T10: Implementar `infra/migrar.py` e a pasta `infra/migracoes/`

## Montagem e front estático (app + frontend)

- [x] T11: Atualizar `tests/app/test_montagem.py`: contêiner expõe `relogio` e montar não abre banco (CA2, CA13)
- [x] T12: Acrescentar `relogio` a `Dependencias` e a `montar_dependencias()` em `app/dependencias.py`
- [x] T13: Escrever `tests/app/test_front_estatico.py` (CA7, CA8, CA9) e `tests/test_frontend_sem_inline.py` (CA8)
- [x] T14: Criar `frontend/index.html`, `frontend/css/estilo.css` e `frontend/js/principal.js` (sem inline, `textContent`)
- [x] T15: Montar `StaticFiles` e o middleware de CSP em `app/main.py`, depois dos routers

## Documentação

- [x] T16: Preencher a seção "Comandos" do `AGENTS.md` (rodar com `uvicorn`, `pytest`, `flake8`, migrar; "popular o banco" como pendente até a seção 2 do TO-DO) (CA12)
- [x] T17: Marcar os itens correspondentes da seção 1 do `TO-DO.md`

## Validação

- [x] T18: `pytest` passando (CA13)
- [x] T19: `flake8` sem erros (CA13)
- [x] T20: Subir a aplicação, abrir `/` e `/saude`; rodar o comando de migração contra um PostgreSQL local, se houver (CA1, CA4, CA7)
- [x] T21: Critérios de aceitação da `spec.md` conferidos (CA1–CA13) e status da spec atualizado
