---
name: criar-feature-sdd
description: "Use when the user asks to start a new feature, create SDD artifacts, or turn a product request into a specification, technical plan, and implementation tasks for this project. Também quando pedir em português: nova feature, criar spec, especificar uma funcionalidade, escrever spec/plano/tarefas de um item do TO-DO."
---

# Criar Feature com SDD

Crie os artefatos de uma feature seguindo o fluxo Spec-Driven Development
deste repositório. Esta skill prepara a feature; ela não implementa código.

## Fontes de verdade

Antes de criar os arquivos, consulte:

- `spec/README.md` para o fluxo e a estrutura do SDD.
- `spec/constitution.md` para as regras obrigatórias de arquitetura, código e
  testes.
- `spec/templates/spec-template.md`, `spec/templates/plan-template.md` e
  `spec/templates/tasks-template.md` para os formatos dos artefatos.
- As features existentes em `spec/features/` para evitar IDs repetidos e
  manter consistência com o projeto.
- `docs/GradeFlow_SRS.pdf` para os requisitos (RF-nn, RNF-nn, RN-nn), os casos
  de uso (UC01–UC04) e o modelo de dados (Apêndice B). Leia só as seções
  ligadas à feature.
- `TO-DO.md`, seção 0 (decisões tomadas), que prevalece sobre o SRS onde
  divergirem, e o item do TO-DO que a feature cobre.
- `DOCUMENTO_PONTE.md` só na seção `§n` citada pelo item do TO-DO ou necessária
  para o comportamento exato do protótipo. Não leia o arquivo inteiro: liste os
  títulos com `grep -n "^#" DOCUMENTO_PONTE.md` e leia só o trecho da seção.

Prevalência: `AGENTS.md`, `spec/constitution.md` e as decisões do `TO-DO.md`
vencem o SRS e o documento ponte.

## Fluxo

1. Entenda o objetivo, os usuários envolvidos (Aluno ou Coordenação), o
   benefício esperado e os critérios de aceitação. Identifique os RF, RNF, RN e
   o caso de uso do SRS e o item do `TO-DO.md` que a feature cobre. Faça
   perguntas objetivas quando faltarem decisões necessárias; não invente regras
   de negócio.
2. Determine o próximo ID sequencial de três dígitos com base nas pastas de
   `spec/features/` (se estiver vazia, comece em `001`). Use o formato
   `NNN-nome-curto-em-kebab-case`.
3. Crie `spec/features/NNN-nome/` com `spec.md`, `plan.md` e `tasks.md`, usando
   os templates do projeto como estrutura.
4. Escreva a spec em linguagem de produto, sem decisões de tecnologia nos
   critérios de aceitação.
   - Logo abaixo do cabeçalho, registre os requisitos cobertos (ex.:
     `Requisitos: RF-20, RN-04, RNF-15`) e o item do `TO-DO.md` correspondente.
   - Nas regras de negócio, cite o ID do SRS quando a regra vier dele (ex.:
     `RN-04 (SRS): ...`) e use o prefixo `R1`, `R2`... para regras locais da
     feature, para não confundir com os `RN-nn` do SRS. Se uma decisão do
     `TO-DO.md` alterar a regra do SRS, escreva a versão decidida e indique a
     origem.
   - Inclua critérios de aceitação para os fluxos de exceção do caso de uso
     (RNF-16), não só para o fluxo principal.
   - Registre itens fora de escopo e dúvidas em aberto.
   - Inicie o status como `Rascunho`; só marque `Aprovada` quando o usuário
     confirmar explicitamente.
5. Elabore o plano técnico a partir da spec e respeite a constituição.
   - Regras de negócio em `domain/` e `use_cases/`, detalhes de HTTP em
     `app/`, persistência e integrações em `infra/`, dependências apontando
     para dentro.
   - Use cases levantam erros de domínio; o mapeamento para HTTP fica em
     `app/`. Dado de outro aluno responde 404, não 403. Indique o perfil
     (Aluno ou Coordenação) autorizado em cada rota.
   - Tabelas e colunas partem do modelo do SRS (Apêndice B) com os ajustes da
     seção "Modelo de dados" do `AGENTS.md`; não crie tabelas fora dele sem
     registrar a dúvida.
   - Quando a feature tiver tela, acrescente ao plano uma seção
     "Interface (`frontend/`)" com as telas afetadas (seção 3.1 do SRS), as
     chamadas à API e os textos exibidos. HTML, CSS e JS puros, texto do
     usuário só via `textContent`, sem script ou estilo inline, e nenhuma regra
     de negócio só no frontend.
   - Cite os limites de desempenho (RNF-01 a RNF-04) quando se aplicarem.
6. Divida o trabalho em tarefas pequenas e ordenadas, escrevendo testes antes
   da implementação. Inclua tarefas de `frontend/` quando o plano tiver tela,
   pelo menos um teste por fluxo de exceção, validação dos critérios de
   aceitação, `pytest` e `flake8`.
7. Confira que os três documentos concordam entre si e com as decisões do
   `TO-DO.md`, que nenhuma decisão pendente foi apresentada como certa e que
   não há código de aplicação sendo implementado como parte desta skill.

## Resposta

Ao terminar, informe o ID e os caminhos dos artefatos criados, os requisitos
do SRS cobertos, resuma as principais decisões e liste as dúvidas ainda
abertas. Se não foi possível definir algum ponto sem inventar comportamento,
deixe-o registrado na spec e explique isso ao usuário.
