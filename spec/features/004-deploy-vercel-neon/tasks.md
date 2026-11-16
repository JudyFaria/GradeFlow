# Tarefas: Deploy na Vercel com banco no Neon

Referências: `spec.md` e `plan.md` desta pasta.
Marque `[x]` ao concluir. Escreva os testes antes da implementação.
Só iniciar após a spec ser aprovada (dúvidas já resolvidas).
Legenda: **[Claude]** feito no repositório; **[Você]** feito nos painéis/contas.

## Código e configuração

- [x] T1 [Claude]: Escrever `tests/test_segredos_fora_do_repositorio.py` (CA6)
- [x] T2 [Claude]: Escrever `tests/test_configuracao_de_deploy.py` (CA1, CA9)
- [x] T3 [Claude]: Garantir `.env*` e `.vercel/` no `.gitignore` e criar `.vercelignore` (D5); criar `vercel.json` só se a detecção automática não bastar (D1)
- [x] T4 [Claude]: Conferir que nada grava em disco em execução (CA10)
- [x] T5 [Claude]: Acrescentar ao `AGENTS.md` ("Comandos") a verificação do deploy e a migração em produção (CA11)

## Contas e painéis

- [ ] T6 [Você]: Importar o repositório na Vercel (produção = `main`)
- [ ] T7 [Você]: Adicionar o Neon pela integração do Marketplace e conferir `DATABASE_URL` no painel
- [ ] T8 [Você]: Rodar `python -m infra.migrar` com a `DATABASE_URL` do Neon (CA5, CA8)

## Verificação

- [ ] T9 [Você + Claude]: Deploy de preview a partir de uma branch, com push pedido por você (R4, D4); conferir `/`, `/saude`, 404, CSP e HTTPS (CA2 a CA4)
- [ ] T10 [Claude]: Se `/` não servir (CA9), mover os estáticos para `public/` e ajustar `app/main.py` e a CSP
- [ ] T11 [Você]: Push na `main` e conferir o deploy de produção (CA1)
- [ ] T12: Marcar os itens da seção 1.1 do `TO-DO.md`

## Validação

- [ ] T13: `pytest` passando (CA12)
- [ ] T14: `flake8` sem erros (CA12)
- [ ] T15: Critérios de aceitação conferidos e status da spec atualizado
