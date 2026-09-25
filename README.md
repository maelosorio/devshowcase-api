# DevShowcase API (Python + FastAPI)

API backend da plataforma DevShowcase — Atividades Avaliativas 1 e 2 (Programação Backend, UESPI/UAPI).

Entidades e relacionamentos (conforme pedido na atividade):
- `Profile` 1 : N `Project`
- `Project` N : N `Technology`
- `Project` 1 : N `Feedback`

## Checklist com o que está pronto

**Atividade 1**
- [x] Projeto configurado (FastAPI + SQLAlchemy + Pydantic)
- [x] Entidades Profile, Project, Technology, Feedback com os relacionamentos corretos
- [x] Camada de persistência (SQLAlchemy) e DTOs de entrada/saída (Pydantic) com validação
- [x] `POST /api/profiles`, `GET /api/profiles/{id}`
- [x] `POST /api/technologies`, `GET /api/technologies`
- [x] `POST /api/projects`, `GET /api/projects`

**Atividade 2**
- [x] `POST /api/projects/{id}/feedbacks` — nota 1 a 5 + comentário, recalcula a nota média do projeto
- [x] `PUT /api/projects/{id}/upvote` — incrementa upvotes/estrelas
- [x] `GET /api/projects` com filtro por tecnologia (`?technology=Python`) e paginação (`?page=1&size=10`)
- [x] Tratamento global de erros (400, 404, validação) com JSON padronizado
- [x] Documentação interativa via Swagger/OpenAPI (o FastAPI já gera automaticamente)
- [ ] **Falta você fazer:** banco PostgreSQL na nuvem + deploy no Render (passo a passo na seção 5)

> Testei tudo isso no meu ambiente antes de te mandar — todos os endpoints, o cálculo de nota média, upvote, filtro, paginação e os erros 400/404 funcionaram certinho.

---

## 1. Como rodar no seu computador (VS Code)

1. Verifique se tem Python instalado: no terminal, rode `python --version` (precisa ser 3.10+). Se não tiver, baixe em https://www.python.org/downloads/ — **atenção**: no instalador do Windows, marque a caixinha **"Add python.exe to PATH"** antes de clicar em instalar.
2. Abra a pasta `devshowcase-api-py` no VS Code, abra um terminal (Ctrl+`) e crie um ambiente virtual:
   ```
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   ```
   venv\Scripts\activate
   ```
   (o prompt do terminal deve passar a mostrar `(venv)` no início)
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
5. Rode a API:
   ```
   uvicorn app.main:app --reload
   ```
6. Se aparecer `Application startup complete`, a API está em `http://localhost:8000`.

Por padrão ela usa **SQLite** (um arquivo `devshowcase.db` que aparece na pasta) — não precisa instalar nenhum banco pra testar local.

---

## 2. Como testar

**Swagger UI (mais fácil, direto no navegador):**
```
http://localhost:8000/docs
```
Clique em qualquer endpoint → "Try it out" → preencha o JSON → "Execute".

**Postman** (a atividade pede pra demonstrar com o Postman no vídeo):
1. Baixe o Postman: https://www.postman.com/downloads/
2. Crie uma nova requisição, método e URL conforme a tabela abaixo
3. Na aba "Body" → "raw" → "JSON", cole o corpo da requisição

### Roteiro de teste sugerido (o mesmo que eu testei):

1. **Criar perfil** — `POST http://localhost:8000/api/profiles`
```json
{
  "name": "Ismael Osório",
  "email": "ismael@example.com",
  "bio": "Estudante de ADS e desenvolvedor",
  "github": "github.com/ismael",
  "linkedin": "linkedin.com/in/ismael",
  "portfolio": "ismael.dev",
  "skills": ["Java", "Python", "Spring Boot"]
}
```
Resposta esperada: `201`, com o `id` do perfil criado (provavelmente `1`).

2. **Buscar perfil** — `GET http://localhost:8000/api/profiles/1`

3. **Criar tecnologia** — `POST http://localhost:8000/api/technologies`
```json
{ "name": "Python" }
```

4. **Listar tecnologias** — `GET http://localhost:8000/api/technologies`

5. **Criar projeto** — `POST http://localhost:8000/api/projects`
```json
{
  "title": "Sistema de Controle Financeiro",
  "description": "App desktop em Python para controle de gastos pessoais",
  "profile_id": 1,
  "technologies": ["Python", "SQLite"],
  "medias": ["https://github.com/ismael/financeiro"]
}
```

6. **Listar projetos com filtro e paginação** — `GET http://localhost:8000/api/projects?technology=Python&page=1&size=10`

7. **Dar um feedback (nota + comentário)** — `POST http://localhost:8000/api/projects/1/feedbacks`
```json
{ "rating": 5, "comment": "Muito bom!" }
```

8. **Dar upvote** — `PUT http://localhost:8000/api/projects/1/upvote` (sem corpo)

9. **Testar erro 404** — `GET http://localhost:8000/api/profiles/999` (não existe)
Resposta esperada:
```json
{
  "timestamp": "...",
  "status": 404,
  "error": "Recurso Não Encontrado",
  "message": "Perfil não encontrado com o ID: 999",
  "path": "/api/profiles/999"
}
```

10. **Testar erro 400** — `POST http://localhost:8000/api/projects/1/feedbacks` com `"rating": 6` (fora do intervalo 1-5)
Resposta esperada: `400`, com a lista de erros de validação.

### Lista completa de endpoints

| Verbo | Rota | O que faz |
|---|---|---|
| POST | `/api/profiles` | cria perfil |
| GET | `/api/profiles/{id}` | busca perfil por id |
| POST | `/api/technologies` | cria tecnologia |
| GET | `/api/technologies` | lista tecnologias |
| POST | `/api/projects` | cria projeto |
| GET | `/api/projects` | lista projetos (filtro `?technology=` e paginação `?page=&size=`) |
| GET | `/api/projects/{id}` | busca um projeto (conta como visualização) |
| PUT | `/api/projects/{id}/upvote` | incrementa upvotes |
| POST | `/api/projects/{id}/feedbacks` | cria feedback (nota 1-5 + comentário), recalcula a média |

---

## 3. Subir para o GitHub

Dentro da pasta do projeto:
```
git init
git add .
git commit -m "Atividades 1 e 2 - DevShowcase API (Python/FastAPI)"
```
Crie um repositório vazio no GitHub (sem README) e depois:
```
git remote add origin https://github.com/SEU_USUARIO/devshowcase-api.git
git branch -M main
git push -u origin main
```

---

## 4. Banco PostgreSQL na nuvem (Supabase ou Render)

**Opção Supabase** (gratuito, rápido de configurar):
1. Crie uma conta em https://supabase.com e um novo projeto
2. Em "Project Settings" → "Database", copie a "Connection string" (modo "URI")
3. Ela vai ser parecida com: `postgresql://postgres:[SUA-SENHA]@db.xxxxx.supabase.co:5432/postgres`

**Opção Render PostgreSQL:**
1. No painel do Render, "New" → "PostgreSQL"
2. Depois de criado, copie a "Internal Database URL" (ou "External", se for acessar de fora do Render)

Guarde essa URL — você vai usar como variável de ambiente no próximo passo.

---

## 5. Deploy no Render (a API em produção)

1. No Render, "New" → "Web Service" → conecte seu repositório do GitHub
2. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Na aba **"Environment"**, adicione a variável:
   - `DATABASE_URL` = a connection string do Supabase/Render que você copiou no passo 4 (troque `postgresql://` por `postgresql+psycopg2://` se der erro de dialeto — geralmente não precisa)
4. Clique em "Deploy". Quando terminar, sua API estará em algo como `https://devshowcase-api-py.onrender.com`, e o Swagger em `.../docs`.

---

## 6. Sobre a entrega (conforme pedido no SIGAA)

**Atividade 1:** PDF com 2 links — repositório GitHub + vídeo não listado no YouTube (5-8 min, webcam se apresentando, tela compartilhada, testando os endpoints).

**Atividade 2:** PDF com 3 links — repositório GitHub + link público da API em produção (Render) + vídeo não listado no YouTube (mostrando também um erro 404 e um erro 400 sendo simulados no Postman).

---

## 7. Estrutura de pastas

```
app/
├── main.py          ponto de entrada, junta tudo
├── database.py       conexão com o banco (SQLite local / Postgres em produção)
├── models.py         entidades (tabelas do banco)
├── schemas.py        DTOs de entrada/saída, com validação
├── errors.py         tratamento global de erros
└── routers/
    ├── profiles.py
    ├── technologies.py
    └── projects.py
```
