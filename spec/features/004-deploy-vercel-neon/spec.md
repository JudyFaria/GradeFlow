# Spec: Deploy na Vercel com banco no Neon

- **ID**: 004
- **Status**: Aprovada
- **Data**: 2026-11-16

Requisitos: RNF-10, RNF-17 (SRS); AGENTS.md (Deploy, Segurança e privacidade, Frontend).
TO-DO: seção 1.1 inteira (projeto na Vercel com deploy automático na `main`; banco no Neon pela integração do Marketplace; conferir `StaticFiles` na Vercel; migrações e seed no Neon fora do ciclo de requisição; variáveis de produção só no painel). Continua a feature 003, que deixou o código pronto para ler `DATABASE_URL`.

## História de usuário

**Como** pessoa que desenvolve o GradeFlow,
**quero** a aplicação publicada na Vercel, com deploy automático a cada push na `main` e banco PostgreSQL no Neon,
**para que** o sistema rode em produção com HTTPS, sem segredos no repositório e sem gravar em disco (RNF-10, RNF-17).

Não há ator final (Aluno ou Coordenação) nem fluxo de negócio. A página inicial e `/saude` continuam públicas.

## Critérios de aceitação

- [ ] CA1: Dado o repositório ligado ao projeto na Vercel, quando se faz push na `main`, então um deploy de produção é criado automaticamente e conclui sem erro.
- [ ] CA2: Dada a URL de produção, quando se acessa `/`, então a página inicial do `frontend/` é servida com HTML, CSS e JS externos, e a CSP `default-src 'self'` está presente na resposta.
- [ ] CA3: Dada a URL de produção, quando se consulta `/saude`, então a resposta é `{"status": "ok"}`, e um caminho inexistente responde 404 em `{"detail": ...}`.
- [ ] CA4: Dado um acesso por `http://`, quando a requisição chega à Vercel, então ela é atendida só por HTTPS (redirecionada ou recusada) (RNF-10).
- [ ] CA5: Dado o banco criado no Neon pela integração do Marketplace, quando se roda `python -m infra.migrar` apontando para ele, então a tabela de controle `migracoes_aplicadas` existe e a execução repetida não reaplica nada.
- [ ] CA6: Dada a aplicação em produção, quando `DATABASE_URL` está definida só no painel da Vercel, então nenhum arquivo do repositório nem o histórico do git contém a URL de conexão, senha ou token.
- [ ] CA7 (exceção): Dada a ausência de `DATABASE_URL` em produção, quando a aplicação sobe, então `/` e `/saude` respondem normalmente, e uma rota que dependa do banco responde 500 genérico, sem expor a causa (CA2 e CA3 da feature 003).
- [ ] CA8 (exceção): Dada uma migração que falha no Neon, quando o comando roda, então ela é desfeita, o erro nomeia a migração e o banco de produção não fica meio migrado (CA6 da feature 003).
- [ ] CA9 (exceção): Dado um deploy cujo front não é servido pela função (arquivos estáticos ausentes), quando se acessa `/`, então o problema é detectado na verificação pós-deploy e o front passa a ser servido no formato que a Vercel serve direto (TO-DO 1.1), sem mudar o contrato da API.
- [ ] CA10: Dada a aplicação em execução na Vercel, quando atende requisições, então nenhuma gravação em disco ocorre (sistema de arquivos somente leitura).
- [ ] CA11: Dado o repositório, quando se lê a seção "Comandos" do `AGENTS.md`, então ela traz como verificar o deploy e como migrar o banco de produção.
- [ ] CA12: Dado o projeto, quando se roda `pytest` e `flake8`, então ambos passam sem erros.

## Regras de negócio

- R1: A conexão com o banco vem só de `DATABASE_URL`, definida no painel da Vercel (que a integração do Neon já injeta); nunca no repositório (AGENTS.md, Deploy).
- R2: Migrações e seed rodam fora do ciclo de requisição, por comando explícito, nunca na subida da aplicação nem a cada requisição (TO-DO 1.1; feature 003, R3).
- R3: O sistema de arquivos da Vercel é somente leitura; nada é gravado em disco (AGENTS.md, Deploy).
- R4: Push na `main` faz deploy em produção; nunca se faz commit nem push sem pedido explícito do usuário (AGENTS.md, Regras de trabalho).
- R5: Segredos de produção só no painel da Vercel; o segredo é fornecido pelo usuário e não passa por esta conversa nem por arquivos versionados.
- R6: Erros de infraestrutura nunca vazam credenciais (RNF-13; feature 003, R9).

## Fora do escopo

- Seed e carga dos JSONs no Neon (TO-DO seção 2): o comando de popular o banco ainda não existe. Esta feature só migra o schema (que ainda não tem tabelas de negócio).
- Segredo de sessão/token: o item do TO-DO fica registrado, mas a variável só é criada com a feature de autenticação (ver D3).
- Domínio próprio, monitoramento, rollback automatizado e ambientes além de produção e preview.
- Autenticação, telas e qualquer regra de negócio.

## Dúvidas em aberto

- Nenhuma.

## Decisões

- D1 (resolvida, pelo usuário, seguindo a recomendação): começar com o `StaticFiles` atual e verificar em deploy de preview; se `/` não servir, mover os estáticos para `public/`.
- D2 (resolvida, pelo usuário, seguindo a recomendação): o usuário roda a migração no Neon, na própria máquina, com a `DATABASE_URL` do Neon.
- D3 (resolvida, pelo usuário, seguindo a recomendação): o segredo de sessão/token fica para a feature de autenticação.
- D4 (resolvida, pelo usuário, seguindo a recomendação): validar num deploy de preview, a partir de uma branch diferente da `main`, antes de produção; o push só ocorre quando o usuário pedir (R4).
- D5 (resolvida, pelo usuário, seguindo a recomendação): `.vercelignore` para `docs/`, `spec/`, `tests/` e `DOCUMENTO_PONTE.md`.
