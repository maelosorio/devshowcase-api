# DevShowcase API

API feita em Python com FastAPI para a disciplina de Programação Backend (UESPI/UAPI) — Atividades Avaliativas 1 e 2.

A ideia da atividade era simular uma plataforma chamada "DevShowcase", onde desenvolvedores cadastram seu perfil e mostram os projetos que fizeram. As entidades e os relacionamentos pedidos:

- `Profile` 1 : N `Project`
- `Project` N : N `Technology`
- `Project` 1 : N `Feedback`

## O que está implementado

**Atividade 1**
- Entidades Profile, Project, Technology, Feedback com os relacionamentos corretos
- Persistência com SQLAlchemy e validação de dados com Pydantic
- `POST /api/profiles`, `GET /api/profiles/{id}`
- `POST /api/technologies`, `GET /api/technologies`
- `POST /api/projects`, `GET /api/projects`

**Atividade 2**
- `POST /api/projects/{id}/feedbacks` — nota de 1 a 5 + comentário, recalcula a média do projeto
- `PUT /api/projects/{id}/upvote` — incrementa upvotes
- `GET /api/projects` com filtro por tecnologia e paginação
- Tratamento de erros (400 e 404) com resposta em JSON
- Documentação automática via Swagger (`/docs`)
- Banco PostgreSQL na nuvem + deploy no Render

## Como rodar localmente

1. Precisa de Python 3.10 ou mais recente.
2. Dentro da pasta do projeto, criar o ambiente virtual:
```
python -m venv venv
venv\Scripts\activate
```
3. Instalar as dependências:
```
pip install -r requirements.txt
```
4. Rodar a API:
```
uvicorn app.main:app --reload
```
5. A API fica disponível em `http://localhost:8000`. Sem configurar nada, ela usa SQLite (cria um arquivo `devshowcase.db` na pasta).

## Testando

Swagger (interativo, direto no navegador): `http://localhost:8000/docs`

Também testamos tudo pelo Postman, que é o que aparece no vídeo de demonstração.

### Endpoints

| Verbo | Rota | O que faz |
|---|---|---|
| POST | `/api/profiles` | cria perfil |
| GET | `/api/profiles/{id}` | busca perfil por id |
| POST | `/api/technologies` | cria tecnologia |
| GET | `/api/technologies` | lista tecnologias |
| POST | `/api/projects` | cria projeto |
| GET | `/api/projects` | lista projetos (filtro `?technology=` e paginação `?page=&size=`) |
| GET | `/api/projects/{id}` | busca um projeto |
| PUT | `/api/projects/{id}/upvote` | incrementa upvotes |
| POST | `/api/projects/{id}/feedbacks` | cria feedback (nota 1-5 + comentário) e recalcula a média |

## Estrutura do projeto

```
app/
├── main.py          ponto de entrada
├── database.py      conexão com o banco
├── models.py        entidades (tabelas)
├── schemas.py       validação de entrada/saída
├── errors.py        tratamento de erros
└── routers/
    ├── profiles.py
    ├── technologies.py
    └── projects.py
```

## Deploy

Banco PostgreSQL hospedado no Supabase/Render, com deploy contínuo no Render a partir do GitHub. As variáveis de ambiente (como `DATABASE_URL`) ficam configuradas direto no painel do Render, não no código.

## Entrega

**Atividade 1:** link do repositório + vídeo (não listado no YouTube) demonstrando os endpoints pelo Postman.

**Atividade 2:** link do repositório + link da API em produção + vídeo demonstrando os endpoints, incluindo os erros 400 e 404, pelo Postman.
