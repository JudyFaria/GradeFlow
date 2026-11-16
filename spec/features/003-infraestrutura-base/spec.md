# Spec: Infraestrutura base (PostgreSQL, migrações, front estático e relógio)

- **ID**: 003
- **Status**: Implementada
- **Data**: 2026-11-16

Requisitos: RNF-16, RNF-17 (SRS); AGENTS.md (Frontend, Deploy, Testes, Comandos).
TO-DO: seção 1, itens "Configurar FastAPI, PostgreSQL, migrações de schema, `pytest` e `flake8`", "Servir o front (HTML, CSS e JS puros) pelo FastAPI com `StaticFiles`", "Criar a porta `Relogio` (`hoje()`) e injetá-la no domínio" e "Preencher a seção 'Comandos' do `AGENTS.md`". Continua a feature 002 (D5), que deixou estes itens para depois.

## História de usuário

**Como** pessoa que desenvolve o GradeFlow,
**quero** a conexão com o PostgreSQL, um mecanismo de migrações de schema, o front estático servido pelo FastAPI e uma porta de relógio injetável, com os comandos documentados,
**para que** as funcionalidades seguintes persistam dados no banco, apareçam numa tela e dependam da data atual sem acoplar o domínio ao relógio do sistema (RNF-16, RNF-17).

Não há ator final (Aluno ou Coordenação) nem fluxo de negócio nesta feature. A única tela é uma página inicial mínima, sem login, só para provar que o front é servido.

## Critérios de aceitação

- [x] CA1: Dada a variável de ambiente `DATABASE_URL` válida, quando a aplicação precisa do banco, então a conexão é aberta a partir dela; a URL não aparece no código nem em logs.
- [x] CA2 (exceção): Dada a ausência de `DATABASE_URL`, quando se tenta abrir a conexão (ou rodar migrações), então a falha é explícita, em português, dizendo que a variável falta; a aplicação continua iniciando e `/saude` responde, pois a montagem das dependências não exige banco (CA2 da feature 002).
- [x] CA3 (exceção): Dado um banco inacessível ou URL inválida, quando se tenta conectar, então o erro é traduzido para um erro de infraestrutura sem expor usuário, senha ou host; a rota afetada responde 500 genérico (CA6 da feature 002).
- [x] CA4: Dado um banco vazio, quando se roda o comando de migração, então as migrações pendentes são aplicadas em ordem e registradas; nenhuma tabela de negócio é criada por esta feature.
- [x] CA5: Dado um banco já migrado, quando o comando roda de novo, então nada é reaplicado (idempotente).
- [x] CA6 (exceção): Dada uma migração que falha, quando o comando roda, então ela é desfeita por inteiro, não é registrada como aplicada, as seguintes não rodam e o erro é mostrado com o nome da migração.
- [x] CA7: Dada a aplicação em execução, quando se acessa `/`, então a página inicial do `frontend/` é servida (HTML, CSS e JS externos), e `/saude` e as demais rotas da API continuam respondendo normalmente (a API não é encoberta pelos arquivos estáticos).
- [x] CA8: Dada qualquer resposta que sirva o front, quando se examinam os cabeçalhos, então há uma Content-Security-Policy estrita (sem `unsafe-inline`), e os arquivos de `frontend/` não contêm script nem estilo inline nem `innerHTML`.
- [x] CA9 (exceção): Dado um caminho inexistente no front, quando é acessado, então a resposta é 404 no formato padrão de erro da API, sem expor caminhos do servidor.
- [x] CA10: Dada a porta `Relogio`, quando um caso de uso ou regra de domínio precisa da data atual, então a recebe por injeção (`hoje()`), e um relógio falso em teste fixa a data; nenhum módulo de `domain/` nem `use_cases/` chama `datetime.now()`/`date.today()`.
- [x] CA11: Dado o relógio de produção, quando `hoje()` é chamado, então devolve a data atual do sistema.
- [x] CA12: Dada a seção "Comandos" do `AGENTS.md`, quando se lê, então traz rodar a aplicação, testar, verificar estilo e migrar, cada um funcionando como descrito.
- [x] CA13: Dado o projeto, quando se roda `pytest` e `flake8`, então ambos passam sem erros, sem exigir banco (testes que precisam de PostgreSQL só rodam se houver banco de teste configurado; ver D2).

## Regras de negócio

- R1: Dependências apontam para dentro; a conexão e o relógio concretos vivem em `infra/` e só `app/dependencias.py` os instancia (constituição, seção 1).
- R2: A conexão vem só de `DATABASE_URL`, nunca do código (AGENTS.md, Deploy).
- R3: Migrações rodam fora do ciclo de requisição, por comando explícito, nunca na subida da aplicação (a Vercel tem sistema de arquivos somente leitura; TO-DO 1.1).
- R4: Nenhuma gravação em disco em tempo de execução (AGENTS.md, Deploy).
- R5: Grades, disciplinas e oferta ficam no banco, nunca no código (RNF-17); esta feature não cria nenhum desses dados.
- R6: Texto do usuário só entra no DOM via `textContent`; CSP estrita, sem script ou estilo inline (AGENTS.md, Frontend).
- R7: Nenhuma regra de negócio só no frontend (AGENTS.md, Frontend).
- R8: A data atual entra no domínio só por injeção (TO-DO 1, item `Relogio`, origem **[N]**; o protótipo chamava `DateTime.now()` em três pontos).
- R9: Erros de infraestrutura nunca vazam credenciais nem detalhes internos ao cliente (RNF-13, constituição).

## Fora do escopo

- Tabelas de negócio, `seed` e carga dos JSONs (TO-DO seção 2); repositórios concretos de negócio.
- Deploy na Vercel, criação do banco no Neon, variáveis de produção, HTTPS (TO-DO 1.1; RNF-10). Esta feature só deixa o código pronto para ler `DATABASE_URL`.
- Autenticação, sessão/token e proteção "tudo exige login" (RF-09, RNF-07): feature própria. A página inicial e `/saude` são públicas.
- Telas do SRS (seção 3.1), grafo, catálogo.
- Comando para popular o banco: entra com a carga de dados (TO-DO seção 2); a seção "Comandos" o registra como pendente.

## Dúvidas em aberto

- Nenhuma.

## Decisões

- D1 (resolvida, pelo usuário): migrações como arquivos SQL numerados em `infra/migracoes/`, aplicados por executor próprio (`python -m infra.migrar`) com tabela de controle; sem Alembic.
- D2 (resolvida, pelo usuário): `psycopg` 3 autorizado no `requirements.txt`; testes de `infra/` contra PostgreSQL real só quando `TEST_DATABASE_URL` existir (ignorados caso contrário).
- D3 (resolvida, pelo usuário): uma conexão por requisição, aberta sob demanda, sem pool.
- D4 (resolvida, pelo usuário, seguindo a recomendação): CSP `default-src 'self'` (sem `unsafe-inline`), aplicada a todas as respostas, API e front. Serve para o navegador recusar scripts e estilos que não venham do próprio sistema, reduzindo o dano de uma falha de XSS.
