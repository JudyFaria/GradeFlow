# AGENTS.md

## Projeto
GradeFlow: app web para o aluno da PUC-Rio planejar os períodos que faltam cursar (grafo de disciplinas com pré e co-requisitos) e se matricular em turmas; a coordenação define a oferta de turmas. Requisitos completos em `docs/GradeFlow_SRS.pdf` (RF-nn, RNF-nn, RN-nn): cite o ID do requisito nas specs, nos testes e nos commits.

- Módulo do SAU (sistema acadêmico da universidade), que está fora do escopo. A integração é simulada: "falta cursar", grades e matrículas "vêm do SAU", mas não implemente comunicação real com ele.
- Atores: **Aluno** (cadastro, importação, grafo, catálogo, planejamentos salvos, matrícula) e **Coordenação** (só controle de oferta de turmas).
- Casos de uso: UC01 cadastro e seleção de curso; UC02 importar "falta cursar"; UC03 planejar períodos e matricular-se (grafo, catálogo, planejamentos salvos, matrícula); UC04 controlar oferta de turmas.
- Reaproveita o protótipo `grafo_disciplinas` (github.com/JudyFaria/grafo_disciplinas): visualização do grafo e verificação de pré/co-requisitos já existem; adapte em vez de reescrever.
- `TO-DO.md` tem as tarefas do porte do protótipo e, na seção 0, as decisões tomadas. Onde divergirem do SRS, as decisões do TO-DO prevalecem; o SRS não é alterado.

## Referência: `DOCUMENTO_PONTE.md`
Descrição detalhada do protótipo Flutter/Firebase (regras exatas, algoritmos, textos da interface, migração). É longo: **não leia inteiro**. Abra só a seção de que precisa, quando uma tarefa citar `§n` (no `TO-DO.md` ou numa spec) ou quando precisar do comportamento exato do protótipo. Liste os títulos com `grep -n "^#" DOCUMENTO_PONTE.md` e leia só o trecho da seção (do título dela até o próximo título do mesmo nível).

| Seção | Consulte quando for trabalhar em |
|-------|----------------------------------|
| §2 Glossário | termos do protótipo (slot, grupo ativo, cascata) |
| §3 Catálogo | carga dos JSONs e qualidade dos dados |
| §4 Modelo de domínio | `Semestre`, `Disciplina`, agregado `Plano` |
| §5 Regras e algoritmos | pré-requisitos, optativas, créditos, mover, cascata, colunas (pseudocódigo) |
| §6 Casos de uso | fluxos, importação do `.xlsx` (§6.1), horários (§6.2) |
| §7 Quirks | comportamentos a preservar ou corrigir (`[C]` no TO-DO) |
| §8 Front-end | geometria, cards, interações, setas SVG, drag-and-drop, paleta |
| §9 API | endpoints e contrato `PlanoView` |
| §11 Migração | Firestore → PostgreSQL e senhas legadas |
| §12 Testes de paridade | cenários T1–T14 |
| Apêndices A e B | textos exatos da interface e constantes |

Prevalência: o `AGENTS.md`, a `spec/constitution.md` e as decisões do `TO-DO.md` (seção 0) vencem o documento ponte. Não valem: as camadas do §9.1 (use as da constituição), o modelo do §10 (use o SRS, Apêndice B, com os ajustes de "Modelo de dados" abaixo) e as decisões em aberto do §13 (já resolvidas no TO-DO). Marcas: ✅ preservar, ⚠️ quirk com decisão no TO-DO, 🆕 sugestão, não regra.

## Regras de negócio (não negociáveis)
- **Movimentação no grafo**: só é aceita se respeitar pré e co-requisitos em relação ao período de destino (RN-04, RNF-15). Se violar, a disciplina fica na origem, a coluna de destino fica vermelha e a mensagem diz qual dependência e em que período ela está (RF-20).
- **Créditos por período: no máximo 30**: bloqueie a movimentação que levaria o período a mais de 30 (decisão que substitui o "< 30" do SRS em RN-06 e RF-21).
- **Códigos curriculares**: normal = 1 disciplina; optativo = escolher 1 do conjunto (ícone de setas ida e volta); eletivo = buscar disciplinas de qualquer curso até completar os créditos mínimos (ícone de planeta com lupa) (RN-05, RF-24, RF-25).
- **Eletivas**: contam no máximo 12 créditos de eletiva livre e 16 de eletiva de orientação (`orientacao` booleano, aprovada pelo coordenador). Excedente pode ser cursado, mas não é contabilizado (RN-15, RF-26).
- **Matrícula**: só com vaga disponível, sem choque de horário com as outras turmas escolhidas e com pré/co-requisitos atendidos (RN-10). Registrada apenas por ação explícita em "Confirmar matrícula", nunca automaticamente (RF-44). Registrar consome vaga; cancelar apaga a matrícula e libera a vaga (RN-14, RF-45, RF-47).
- **Turma**: capacidade de vagas > 0 (RN-08); um ou mais horários (`TURMA_HORARIO`); alertar conflito de horário com outra turma da mesma disciplina antes de salvar (RF-52); ao editar, alertar impacto em matrículas existentes (RF-53).
- **Oferta** é definida só pela coordenação; o aluno apenas consulta (RN-07).
- **Demanda para a coordenação**: só dados agregados por turma e disciplina; aluno identificado apenas pelo número de matrícula, nunca por dados pessoais (RN-13, RF-54).
- **Planejamento salvo** pertence a um aluno e só ele vê (RN-12). Falha ao salvar: avisar e manter o planejamento na sessão (RF-38).
- **Importação**: aceitar só `.xlsx`, sem limite de tamanho; tratar como dado, nunca executar; arquivo inválido não altera nada (RF-11, RNF-11). Após importar, o menor período pendente vai para o período atual e os demais seguem a partir dele. Sem importação, vale a grade sugerida mais atual do curso, carregada no cadastro (RF-06, RF-14).
- **Pré-requisitos que não são disciplina** ("118 créditos", "PORTUGUÊS (nivel 3)"): só exibir, nunca bloquear.
- Grades, disciplinas e oferta ficam no banco, nunca no código (RNF-17).

## Modelo de dados
Relacional, 20 tabelas (SRS, Apêndice B): `CURSO`, `GRADE_CURRICULAR`, `PERIODO`, `CODIGO`, `NORMAL`, `CONJUNTO_OPTATIVAS`, `OPTATIVA_DISCIPLINA`, `CONJUNTO_ELETIVAS`, `ELETIVA_DISCIPLINA`, `DISCIPLINA`, `GRUPO_PREREQUISITO` + `GRUPO_PREREQUISITO_ITEM` (grupos alternativos "OU" de itens exigidos juntos "E", como no protótipo; substituem o tipo `PRE` de `DISCIPLINA_REQUISITO`), co-requisitos (simétricos), `TURMA` (período letivo, capacidade, qtd. de alunos, status), `TURMA_HORARIO` (com `sala`, preenchida pela coordenação), `STATUS` (entidade separada: AP, CP, CL, EA, LT, RF, RM), `ALUNO` (matrícula, e-mail, usuário, senha, CR; mais `firebase_uid`, `senha_hash_legado` e `senha_salt_legado` só durante a migração dos usuários do protótipo), `ALUNO_CURSO`, `ALUNO_TURMA`, `FALTA_CURSAR`, `PLANEJAMENTO`, `PLANEJAMENTO_DISCIPLINA`. Um aluno pode ter vários cursos (RN-01). A qtd. de alunos da turma vem das matrículas.

## Segurança e privacidade
- Tudo exige login, exceto cadastro e login (RF-09, RNF-07).
- Senha só como hash com salt; nunca em texto claro nem em log (RNF-08).
- Autorização por perfil: oferta de turmas só para coordenação; aluno só acessa os próprios dados (RNF-09).
- HTTPS (RNF-10). Coletar só e-mail, usuário, curso e planejamentos; LGPD (RNF-12).

## Interface
- Português do Brasil, datas `dd/mm/aaaa`. Use a terminologia da universidade: Falta Cursar, período, turma, grade curricular, micro-horário.
- 11 telas descritas na seção 3.1 do SRS. Aluno: barra superior com seletor de curso + menu lateral (Planejamento, Importar Falta Cursar, Catálogo e turmas, Matrícula, Planejamentos salvos, Agenda, Resetar para grade oficial, Como usar, Sair). Agenda mostra horário, aula e sala das turmas em que o aluno está matriculado, de segunda a sexta; é diferente do micro-horário, usado para escolher turmas. Coordenação: menu lateral com "Oferta de turmas".
- Grafo: colunas "Período atual" (sinalizado), +1, +2…, cada uma também com o semestre `AA.S` (ex.: `+1 · 27.1`); cartão com nome e créditos; cabeçalho com total de créditos. Clique destaca em laranja o cartão e os relacionados, esmaece o resto; pré-requisito em linha contínua, co-requisito em tracejada, com legenda (RF-23).
- Arrastar e soltar com mouse, touchpad e toque; foco no desktop, layout adaptável (RF-17, RNF-19).
- Erros como avisos que mantêm o usuário na tela, explicando a causa e como proceder (RNF-13). Choque de horário: aviso com as turmas e o horário em conflito, opções Cancelar e Escolher outra turma (RF-30).
- Botão "Salvar planejamento" no grafo, no catálogo e na revisão da matrícula (RF-34). Em planejamentos salvos, o botão é "Restaurar como atual" (não "Abrir no grafo").

## Desempenho
Movimentação de cartão ≤ 1 s (p95, grade de até 80 disciplinas); grafo ≤ 3 s; catálogo ≤ 3 s; importação ≤ 5 s (RNF-01 a RNF-04).

## Testes
As verificações (pré/co-requisitos, créditos, vagas, choque de horário, limites de eletivas) ficam no domínio, isoladas da interface, e cada fluxo de exceção dos casos de uso tem pelo menos um teste (RNF-16).

## Comandos
- `pytest`: roda os testes.
- `flake8`: verifica o estilo (PEP-8).

## Tecnologias
Python, FastAPI, PostgreSQL (Neon em produção), pytest e flake8 no backend; HTML, CSS e JavaScript puros no frontend, sem framework nem etapa de build.

## Arquitetura
Clean architecture conforme `spec/constitution.md`: `app/` → `use_cases/` → `domain/`; `infra/` implementa as interfaces definidas em `use_cases/`. As dependências concretas são montadas só na inicialização da aplicação.

- `domain/`: entidades e regras puras (pré/co-requisitos, créditos, vagas, choque de horário, limites de eletivas). Não importa FastAPI, PostgreSQL nem outra camada.
- `use_cases/`: um caso de uso por ação; recebe os repositórios por injeção de dependência.
- `infra/`: repositórios PostgreSQL e leitura de `.xlsx`.
- `app/`: rotas FastAPI, sem regra de negócio.
- Erros: levante erros de domínio nos casos de uso, nunca `HTTPException`. O mapeamento para HTTP fica em `app/`.
- Privacidade: dado de outro aluno responde 404, não 403.
- Campo novo em entidade: atualize a entidade, o repositório em `infra/`, os schemas e rotas de `app/` e as telas em `frontend/`.
- Testes de casos de uso usam repositórios falsos em memória, nunca o banco.

## Frontend
- HTML, CSS e JS puros em `frontend/`, servidos pelo próprio FastAPI (`StaticFiles`) e consumindo a API. Nenhuma regra de negócio só no frontend: as verificações valem no domínio.
- Texto do usuário só entra no DOM via `textContent`, nunca `innerHTML`. CSP estrita: sem script ou estilo inline.

## Deploy
Vercel, com deploy automático a cada push na `main`. Banco PostgreSQL no Neon (integração do Marketplace da Vercel); a conexão vem da variável de ambiente `DATABASE_URL`, nunca do código. O sistema de arquivos da Vercel é somente leitura: não grave dados em disco.

## Regras de trabalho
- Tarefa pronta só quando `pytest` passa e `flake8` não aponta erros.
- Nunca faça commit nem push sem eu pedir. Push na `main` faz deploy em produção.
- Não adicione framework de frontend, build de frontend, outro linter ou formatador, nem dependências sem eu pedir.
- Pedido ambíguo: pergunte antes de implementar.