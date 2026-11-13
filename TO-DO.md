# TO-DO — Portar o protótipo para o GradeFlow

Tarefas para trazer ao GradeFlow o que existe no protótipo `grafo_disciplinas` (Flutter/Firebase), conforme o `DOCUMENTO_PONTE.md`.
As referências `§n` apontam para seções do documento ponte; `RF/RNF/RN` apontam para o `docs/GradeFlow_SRS.pdf`.

Legenda: **[P]** comportamento herdado a preservar · **[C]** quirk do protótipo a corrigir · **[N]** novo, não existia no protótipo. As decisões tomadas estão na seção 0.

---

## 0. Decisões

### 0.1 Tomadas

- **Stack:** FastAPI + PostgreSQL, com as camadas da `spec/constitution.md`: `domain/` ← `use_cases/` ← `infra/` e `app/`. As camadas sugeridas no §9.1 do documento ponte (`application/`, `infrastructure/`, `interfaces/`) **não** valem.
- **Limite de créditos:** no máximo 30 por período. Bloqueia só quando o total **passa** de 30 (`> 30`, como no protótipo, §5.7).
- **Horários:** são duas funcionalidades diferentes, e as duas entram:
  - **Micro-horário** (SRS 4.4): grade semanal das turmas ofertadas pela coordenação, usada para escolher turmas antes da matrícula.
  - **Agenda** (protótipo, §6.2): mostra o horário, a aula e a sala das disciplinas em que o aluno **está matriculado**.
- **Pré-requisitos alternativos:** criar tabela nova de grupos de pré-requisito, seguindo o protótipo (grupos "OU" de itens "E").
- **Funcionalidades do protótipo que o SRS não cita** (Concluídas, Sem período fixo, reset para a grade oficial, ajuda, "+ Período", login por apelido, recuperação de senha): **implementar**, seguindo o protótipo, mas dentro do escopo do SRS.
- **Regra geral:** onde o protótipo e o SRS tratam da mesma coisa, seguir o protótipo e ajustar ao que o SRS exige explicitamente. Disso decorre:
  - **Rótulo das colunas:** o SRS exige "Período atual", "+1", "+2"… (RF-15); o protótipo mostra `AA.S`. Mostrar os dois (ex.: `+1 · 27.1`).
  - **Nome:** usar "Planejamentos salvos" (SRS, tela 10) no lugar de "Momentos"; o comportamento é o do protótipo.
  - **Cascata (§7.7) e optativas (§7.8):** o SRS não aceita estado que viole pré/co-requisitos (RNF-15) nem período acima do limite (RN-06). Se o resultado da cascata ou da escolha de optativa violar algo, a ação é recusada com o motivo.
  - **Destaque no grafo:** cor laranja e co-requisito em linha tracejada com legenda, como pede o RF-23.

- **Sala:** cadastrada pela coordenação junto com a oferta da turma (campo novo `sala` em `TURMA_HORARIO`, um por dia e horário).
- **Agenda:** de segunda a sexta, sem sábado.
- **Migração de usuários do Firebase:** necessária (seção 13).
- **Posicionamento após importar o Falta Cursar:** o menor período pendente da planilha vai para o período atual, e os demais seguem a partir dele (`semestre = hoje + (p − p_min)`). No protótipo, o período 1 ia para o atual (`hoje + (p − 1)`, §7.4).
- **Pré-requisitos que não são disciplina** ("118 créditos", "PORTUGUÊS (nivel 3)"): só exibir, sem bloquear.
- **Excluir planejamento salvo:** com confirmação.
- **Front-end:** HTML, CSS e JavaScript puros, servidos pelo próprio FastAPI (`StaticFiles`).
- **Hospedagem:** Vercel, com deploy automático a cada push na `main`. Banco PostgreSQL no Neon (integração do Marketplace da Vercel), conectado por `DATABASE_URL`.
- **SRS:** é a base do projeto e não será alterado. As decisões acima prevalecem onde divergirem dele.

- **Vários grupos de pré-requisito já cumpridos (§5.4c):** manter o comportamento do protótipo. Sem escolha explícita e com mais de um grupo cumprido, vale o primeiro grupo válido da lista.
- **Scraper (§3.4):** não será portado agora. O banco é populado só com os JSONs já gerados pelo protótipo.
- **Senhas na migração (§11.3):** opção B. Importar o hash do Firebase e convertê-lo para argon2/bcrypt no primeiro login. O protótipo tem cerca de 10 usuários.

---

## 1. Infraestrutura do projeto

- [ ] Criar `domain/`, `use_cases/`, `infra/`, `app/` conforme a constituição, com a montagem das dependências na inicialização.
- [ ] Configurar FastAPI, PostgreSQL, migrações de schema, `pytest` e `flake8`.
- [ ] Servir o front (HTML, CSS e JS puros) pelo FastAPI com `StaticFiles`.
- [ ] Criar a porta `Relogio` (`hoje()`) e injetá-la no domínio; o protótipo chama `DateTime.now()` em três pontos (§9.1) **[N]**.
- [ ] Preencher a seção "Comandos" do `AGENTS.md` (rodar, testar, migrar, popular o banco).

### 1.1 Deploy

- [ ] Criar o projeto na Vercel ligado ao repositório, com deploy automático na `main`.
- [ ] Criar o banco no Neon pela integração do Marketplace da Vercel e ler a conexão de `DATABASE_URL`.
- [ ] Conferir que o FastAPI com `StaticFiles` serve o front na Vercel; se não servir, mover os arquivos estáticos para o formato que a Vercel serve direto.
- [ ] Rodar as migrações de schema e o seed no Neon fora do ciclo de requisição (o sistema de arquivos da Vercel é somente leitura).
- [ ] Configurar as variáveis de ambiente de produção (`DATABASE_URL` e o segredo de sessão/token) só no painel da Vercel, nunca no repositório.

## 2. Catálogo de disciplinas e carga de dados (§3)

### 2.1 Modelo
- [ ] `Disciplina`: código `^[A-Z]{3}\d{4}$`, nome, créditos anuláveis, grupos de pré-requisito, co-requisitos, opções de slot **[P]**.
- [ ] Reconciliar as tabelas do §10 com o modelo relacional do SRS (Apêndice B): `DISCIPLINA`, `PERIODO`/`CODIGO`, `CONJUNTO_OPTATIVAS` e `OPTATIVA_DISCIPLINA` (slots e opções), `CONJUNTO_ELETIVAS` e `ELETIVA_DISCIPLINA`.

### 2.2 Tabela nova de pré-requisitos (seguindo o protótipo)
- [ ] `GRUPO_PREREQUISITO(id PK, id_disciplina FK, ordem)`: cada grupo é uma alternativa (OU) **[N]**.
- [ ] `GRUPO_PREREQUISITO_ITEM(id_grupo FK, ordem, tipo ∈ {disciplina, creditos_minimos, nivel, texto}, id_disciplina NULL FK, texto NULL)`: os itens do grupo são exigidos juntos (E) **[N]**.
- [ ] Co-requisitos em tabela própria, deduplicados e simétricos.
- [ ] `id` do grupo estável, usado na escolha do aluno (corrige §7.6) **[C]**.

### 2.3 Carga
- [ ] Seed a partir de `assets/dados_materias.json` e `assets/periodos_curriculo_atual_cc.json` (211 disciplinas, 49 na grade de CC) **[P]**.
- [ ] Tratar a qualidade dos dados (§3.3):
  - [ ] Deduplicar co-requisitos (ex.: `INF1039` lista `INF1403` duas vezes).
  - [ ] Gravar os 19 itens de texto livre com o `tipo` correspondente, sem descartá-los. Esses itens são só exibidos ao aluno, nunca bloqueiam movimento.
  - [ ] Registrar os 64 códigos de pré-requisito que não existem no catálogo.
  - [ ] Manter os nomes como vierem, sem normalizar caixa ou acento.
  - [ ] Aceitar `creditos = null` (contam como 0).
- Scrapers `grade_cc.py` e `pre_requisitos.py` (§3.4): fora do escopo por enquanto; a carga usa só os JSONs acima.
- [ ] Suportar mais de um curso e versões de currículo, carregando a grade mais atual no cadastro (RN-01, RN-02) **[N]**.

## 3. Domínio: objeto de valor `Semestre` (§4.1)

- [ ] `Semestre(ano, periodo∈{1,2})`, ordenável por `ano*2 + periodo` **[P]**.
- [ ] `de_data`: jan–jun = 1, jul–dez = 2 **[P]**.
- [ ] `avancar(n)` (com `n <= 0` devolvendo o mesmo semestre) e rótulo `AA.S` **[P]**.
- [ ] Rótulo relativo ao semestre atual ("Período atual", "+1", "+2"…) (RF-15) **[N]**.

## 4. Domínio: agregado `Plano` (§4.2, §5)

- [ ] Construção e filtro "fora do currículo" (§5.1) **[P]**, usando o período personalizado quando houver (§7.3) **[C]**.
- [ ] Cálculo das "opções-apenas" (§5.1) **[P]**.
- [ ] Inicialização padrão sem planilha: período p da grade → semestre `hoje + (p-1)`, sem concluídas (§5.2) **[P]**.
- [ ] Inicialização após importar: o menor período pendente vai para o período atual (`hoje + (p − p_min)`); concluídas e "sem período fixo" fora das colunas (§7.4) **[C]**.
- [ ] Restauração validada contra o catálogo, reportando códigos e escolhas inválidos (§5.3, §7.2, §7.11) **[C]**.
- [ ] Status de cada disciplina persistido (`planejada | concluida | sem_periodo`), para "Sem período fixo" não sumir ao recarregar (§7.1) **[C]**.
- [ ] **Grupos de pré-requisito** (§5.4) **[P]**:
  - [ ] Grupo válido = não vazio e com todos os itens no plano.
  - [ ] Grupo ativo: fallback sem grupo válido; um grupo; vários sem escolha (o mais satisfeito; empate fica com o 1º); escolha explícita.
  - [ ] Mais de um grupo satisfeito sem escolha explícita: usar o primeiro grupo válido (índice 0), como no protótipo **[P]**.
  - [ ] Itens que não são disciplina aparecem no card/diálogo, mas não entram na validação.
- [ ] **Slots de optativa** (§5.5) **[P]**: `resolver_codigo_efetivo`, `aplicar_escolha` (o card mantém o código do slot e usa nome, requisitos e créditos da opção), escolher, trocar e desfazer.
  - [ ] Limpar a escolha de grupo ao desfazer a optativa (§7.6) **[C]**.
  - [ ] Recusar a escolha se o período passar de 30 créditos ou violar requisitos (§7.8) **[C]**.
- [ ] **Eletivas** (RF-25, RF-26, RN-15) **[N]**: buscar disciplinas de qualquer curso até completar os créditos do código; contar no máximo 12 créditos de eletiva livre e 16 de eletiva de orientação.
- [ ] **Dependências derivadas** (§5.6) **[P]**, calculadas sob demanda sem cache defasado (§7.10) **[C]**; co-requisitos simétricos e resolvidos para o slot (§7.9) **[C]**.
- [ ] **Bloqueio de movimento** (`motivo_bloqueio`, §5.7) **[P]**:
  - [ ] Pré-requisito em semestre estritamente anterior; concluído ou sem posição não bloqueia.
  - [ ] `LIMITE_CREDITOS_POR_PERIODO = 30`, bloqueando quando o total passa de 30.
  - [ ] Mensagens `Precisa vir depois de {código}` e `Passaria de 30 créditos nesse período ({n})`, acrescentando o período do pré-requisito (RF-20).
  - [ ] Ordem determinística (ordem do catálogo e do grupo, §7.12).
- [ ] **Mover / concluir / retirar** (§5.8) **[P]**; "Sem período fixo" só aceita quem não tem período definido.
- [ ] **Cascata BFS** (§5.9) **[P]**: dependentes só avançam; co-requisitos se alinham no mesmo semestre; devolve os códigos alterados.
  - [ ] Validar o estado final da cascata; se algum período passar de 30 créditos ou algum requisito for violado, recusar o movimento inteiro com o motivo (§7.7, RNF-15) **[C]**.
  - [ ] Detectar ciclo e avisar, em vez de truncar em silêncio nos 500 passos (§7.20) **[C]**.
- [ ] **Reencaixe** após escolher optativa ou grupo (§5.10) **[P]**.
- [ ] **Colunas** (§5.11) **[P]**: faixa contígua do menor ao maior semestre usado; semestre atual sempre visível; adicionar o próximo; remover só coluna vazia, extra e numa ponta (flag `removivel`, §7.5) **[C]**.
- [ ] **Visões derivadas** (§5.12) **[P]**: por coluna (ordem do catálogo), créditos por coluna, concluídas (ordenadas por código), sem período, arestas pré e co, vizinhos do foco.

## 5. Importação do "Falta Cursar" (§6.1; RF-10 a RF-14)

- [ ] Leitor `.xlsx` como porta + implementação em `infra/` (openpyxl): só a 1ª planilha, pular 2 linhas, período na coluna A (1º número da célula), código na coluna C **[P]**.
- [ ] Extrair a matrícula da célula A1 (`Matr[ií]cula:\s*(\d+)`) e gravar no aluno **[P]**.
- [ ] Período > 10 → "sem período fixo"; o que está na grade oficial e não está na planilha vira concluído **[P]**.
- [ ] Mensagens: "Nenhuma matéria foi encontrada nessa planilha." e "Erro ao importar a planilha: {erro}" **[P]**.
- [ ] Arquivo inválido não altera nada; aceitar só `.xlsx`, sem limite de tamanho, sem executar conteúdo (RF-11, RNF-11) **[N]**.
- [ ] Pedir confirmação antes de substituir o plano; opcionalmente salvar um planejamento automático "antes da importação" (§7.16) **[C]**.
- [ ] Processar em até 5 s (RNF-04).

## 6. Planejamentos salvos (antigos "Momentos") (§6 UC15–UC18; RF-34 a RF-39)

- [ ] Salvar o plano atual com nome, a partir do grafo, do catálogo e da revisão da matrícula; nome vazio ou cancelar = nada acontece; janela com o resumo (períodos e disciplinas) (RF-34, RF-35) **[P]**.
- [ ] Feedback `Planejamento "{nome}" salvo!` / `Erro ao salvar: {erro}`; em falha, manter o plano na sessão (RF-38) **[P]**.
- [ ] Listar por data decrescente, com data `dd/mm/aaaa HH:mm` e número de períodos (RF-36) **[P]**.
- [ ] Pré-visualizar em modo somente leitura com o mesmo motor de domínio **[P]**.
- [ ] "Restaurar como atual" com o texto de confirmação do UC17; copiar só os campos do plano e preservar a matrícula (§7.15) **[C]**.
- [ ] Renomear (RF-37) **[N]**.
- [ ] Excluir, com confirmação **[P]**.
- [ ] Cada planejamento visível só ao dono (RN-12) **[N]**.

## 7. Reset para a grade oficial (§6 UC14)

- [ ] Ação "Resetar para grade oficial" no menu, com a confirmação "Resetar para o padrão da universidade?" / "Isso descarta a planilha importada e qualquer alteração manual, voltando pra grade oficial da PUC do zero, como um usuário novo." **[P]**.
- [ ] Reconstruir o plano como a grade sugerida mais atual do curso (mesma base do RF-06/RF-14) e salvar **[P]**.

## 8. Contas e autenticação (§6 UC01–UC05; RF-01 a RF-09)

- [ ] Cadastro com e-mail, senha (mínimo 6), usuário (apelido) e curso, com busca de curso e aviso de carga da grade (RF-01 a RF-06) **[P]**.
- [ ] `UNIQUE` em `lower(apelido)` dentro da transação do cadastro (§7.18) **[C]**.
- [ ] Login por e-mail ou apelido, resolvido no servidor sem expor o e-mail (§7.19, RF-09) **[C]**.
- [ ] Mensagem única para "usuário não existe" e "senha errada" (Apêndice A.1) **[C]**.
- [ ] Recuperação e redefinição de senha, com resposta sempre igual (UC03) **[P]**.
- [ ] Senha com hash e salt (argon2 ou bcrypt), nunca em log (RNF-08).
- [ ] Sair **[P]**.
- [ ] Trocar de curso só quando o curso realmente muda, com confirmação, sem apagar o plano em silêncio (§7.14) **[C]**.
- [ ] Vincular curso adicional e alternar pelo seletor da barra superior, com um plano por curso (RF-07, RF-08) **[N]**.
- [ ] Perfil de coordenação com acesso só ao controle de oferta (RF-48, RNF-09) **[N]**.

## 9. API (§9)

- [ ] O domínio vive no servidor; o front envia **ações**, não o estado inteiro (§7.17) **[C]**.
- [ ] Rotas em `app/`, convertendo erros de domínio em HTTP só nessa camada.
- [ ] Auth, `/me`, `/cursos` (§9.2).
- [ ] `GET /plano` e ações: mover, concluir, retirar, colunas, optativas, eletivas, grupo de pré-requisito, importar, reset.
- [ ] `GET /plano/disciplinas/{codigo}/destinos` (motivo por coluna, buscado uma vez no início do arrasto) **[N]**.
- [ ] Planejamentos salvos: listar, criar, ver (somente leitura), restaurar, renomear, excluir.
- [ ] Agenda: `GET /agenda/{ano}/{periodo}` (ver seção 12).
- [ ] Contrato `PlanoView` (§9.3) com `colunas` (incluindo rótulo relativo), `concluidas`, `sem_periodo`, `disciplinas`, `arestas` (pré e co), `alterados`, `removivel`, `grupo_ativo_id`.
- [ ] Erro `422 {"codigo":"MOVIMENTO_BLOQUEADO","motivo":...}`.
- [ ] Autorização: aluno só acessa os próprios dados (RNF-09).

## 10. Front-end: grafo de planejamento (§8; RF-15 a RF-25)

- [ ] Barra superior com seletor de curso + menu lateral do SRS (Planejamento, Importar Falta Cursar, Catálogo e turmas, Matrícula, Planejamentos salvos), acrescido de Agenda, Resetar para grade oficial, Como usar e Sair.
- [ ] Colunas com cabeçalho (rótulo relativo + `AA.S` + `N créditos`), período atual sinalizado, cores da paleta de 9 tons por índice (§8.3, §8.8) **[P]**.
- [ ] Geometria: coluna 200 px, gap 48, cabeçalho 44, card 56, gap 12; zoom 0,4–2,5 (§8.3) **[P]**.
- [ ] Card: código + nome com reticências e créditos; ícone de setas (optativa, RF-24), planeta com lupa (eletiva, RF-25) e `alt_route` (vários grupos de pré-requisito) **[P]**.
- [ ] Prioridade de cor: inválido → destacado → foco → slot sem escolha → cor da coluna (§8.4) **[P]**.
- [ ] Hover tem prioridade sobre seleção; clique alterna seleção; foco destaca em laranja o card e os relacionados e esmaece o resto (§8.5, RF-23) **[P]**.
- [ ] Setas em `<svg>` sobreposto (`pointer-events: none`), Bézier cúbica, ponta de 6 px; pré-requisito contínuo, co-requisito tracejado, legenda visível (§8.6, RF-23) **[P]**.
- [ ] Arrastar com Pointer Events: long-press de 200 ms, fantasma de 196 px, original a 35 % de opacidade; mouse, touch e caneta (§8.7, RF-17) **[P]**.
- [ ] Durante o arrasto: coluna vermelha + etiqueta com o motivo, drop recusado; sem motivo, cor da paleta a 15 % (§8.5, RF-20) **[P]**.
- [ ] Após soltar: destacar os alterados por 2 s (§8.5) **[P]**.
- [ ] Seções recolhíveis "Concluídas (N)" (começa fechada) e "Sem período fixo (N)" (começa aberta); cabeçalho é alvo de drop mesmo recolhido; "Nenhuma matéria aqui" (§8.5) **[P]**.
- [ ] Botão "+ Período" e "×" só em coluna removível (§8.5) **[P]**.
- [ ] Diálogos de optativa ("Escolher matéria — {nome}", "Remover escolha", "(sem ementa)"), de eletiva (busca) e de grupo ("Pré-requisito usado — {nome}", itens `A + B`) (Apêndice A.2) **[P]**.
- [ ] Modo somente leitura (pré-visualização de planejamento salvo) **[P]**.
- [ ] Tela "Como usar" com os 7 passos (Apêndice A.3), conferindo o texto em `tela_ajuda.dart` e acrescentando catálogo, matrícula e agenda **[P]**.
- [ ] Interface em pt-BR, datas `dd/mm/aaaa`, layout adaptável a telas menores (RNF-19).
- [ ] Movimentação em ≤ 1 s (p95) e grafo carregado em ≤ 3 s (RNF-01, RNF-02).

## 11. Front-end: login e cadastro (§8.10)

- [ ] Uma tela com dois modos ("Entrar" / "Criar conta"), formulário com largura máxima de 360 px **[P]**.
- [ ] Campos: "E-mail ou usuário" e "Senha" no login; "E-mail", "Senha", "Usuário" e "Curso" (com busca) no cadastro **[P]**.
- [ ] Link "Esqueci minha senha"; validações "Obrigatório", "E-mail inválido", "Mínimo 6 caracteres", "Escolha um apelido" **[P]**.

## 12. Agenda (horários do protótipo) (§6.2, §8.9)

Mostra o horário, a aula e a sala das disciplinas em que o aluno **está matriculado**. Diferente do micro-horário (SRS 4.4), que serve para escolher turmas.

- [ ] Montar os blocos a partir das matrículas registradas (`ALUNO_TURMA` → `TURMA` → `TURMA_HORARIO`), não de digitação livre **[N]**.
- [ ] Campo novo `sala` em `TURMA_HORARIO`, preenchido pela coordenação no cadastro e na edição da turma (tela 11, ao lado de dias e horários) **[N]**.
- [ ] Grade de segunda a sexta × blocos (`7h-9h` … `19h-21h`, 150 × 72 px, cabeçalho 36 px, coluna de horas 64 px), título `Horário — {AA.S}` (§8.9) **[P]**.
- [ ] Célula com fundo da cor da disciplina, código, nome e sala; cor por hash estável do código (§7.13) **[C]**.
- [ ] Mostrar qualquer semestre com matrícula, não só o atual (§7.13) **[C]**.
- [ ] Turma com horários diferentes em dias diferentes (vários registros em `TURMA_HORARIO`) (§7.13) **[C]**.
- [ ] Sem matrícula no semestre: mensagem equivalente a "Nenhuma matéria no período atual pra montar horário." **[P]**.
- [ ] Atualizar a agenda ao registrar ou cancelar matrícula (RF-45, RF-47) **[N]**.

## 13. Migração Firestore → PostgreSQL (§11)

Os usuários do protótipo precisam ser migrados.

- [ ] `tools/migracao_firestore/`: `exportar.py`, `transformar.py`, `carregar.py`, `verificar.py`.
- [ ] Regras de §11.2: concluída vence, descartar códigos fora do catálogo, índice de grupo → id do grupo, copiar colunas extras, escolhas de optativa e matrícula.
- [ ] Momentos → planejamentos salvos (nome e data de criação).
- [ ] Horários do protótipo: descartar os blocos digitados (a agenda passa a vir das matrículas) e registrar no relatório.
- [ ] Usuário sem perfil: criar com o curso padrão `cc`.
- [ ] Idempotente, com `--dry-run`, `--usuario <uid>`, uma transação por usuário e relatório de anomalias.
- [ ] **Senhas: migração preguiçosa do hash do Firebase (opção B, §11.3)**, para cerca de 10 usuários:
  - [ ] Exportar as contas com `firebase auth:export` (traz `passwordHash` e `salt` de cada usuário).
  - [ ] Copiar do Console do Firebase os parâmetros do scrypt modificado (Authentication → Users → ⋮ → *Password hash parameters*: `base64_signer_key`, `base64_salt_separator`, `rounds`, `mem_cost`). Guardar fora do repositório.
  - [ ] Colunas novas em `ALUNO`: `firebase_uid`, `senha_hash_legado`, `senha_salt_legado`, com `senha` nula até a conversão.
  - [ ] Implementar em `infra/` um verificador do scrypt modificado do Firebase, atrás da porta `HasherDeSenha`.
  - [ ] No login: se o aluno ainda tem hash legado, verificar com o algoritmo do Firebase; se a senha estiver certa, gravar o hash novo (argon2/bcrypt) e apagar os campos legados, na mesma transação.
  - [ ] Testar com uma conta de teste criada no Firebase antes de migrar as contas reais.
  - [ ] Depois que todos tiverem entrado (ou após um prazo), apagar os campos legados que restarem e pedir redefinição de senha a esses usuários.
- [ ] Avisar aos usuários migrados que reimportem o Falta Cursar, porque "Sem período fixo" não era persistido no protótipo (§11.2).
- [ ] Verificação: contagens, paridade visual por amostragem, integridade, login (§11.5).
- [ ] Cutover e LGPD: dump fora do repositório e apagado no fim; revogar a conta de serviço (§11.6).

## 14. Testes de paridade (§12)

- [ ] No projeto Flutter: gerar golden files a partir do `EstadoGrafo`, com data fixa (semestre atual = 2026.2).
- [ ] No GradeFlow: rodar os mesmos cenários contra o domínio Python e comparar JSON a JSON.
- [ ] Cenários T1–T14 (§12), cada um declarando se espera o comportamento **herdado** ou **corrigido**:
  - [ ] T1 grade geral · T2 bloqueio por pré-requisito · T3 limite de créditos (30 aceita, 31 bloqueia) · T4 cascata · T5 co-requisitos
  - [ ] T6 grupos OU (0, 1, >1 satisfeitos) · T7 escolha de grupo e reencaixe · T8 optativa com créditos nulos
  - [ ] T9 opção que é pré-requisito · T10 concluir com dependentes · T11 importação (corrigido: menor período pendente no período atual) · T12 salvar/restaurar
  - [ ] T13 colunas · T14 ciclo
- [ ] Testes novos para as correções: cascata recusada ao estourar 30 ou violar requisito; optativa recusada ao estourar 30.
- [ ] Agenda: blocos montados a partir das matrículas, inclusive após cancelar (substitui o T15 do protótipo).
- [ ] Um teste por fluxo de exceção dos casos de uso (RNF-16).
