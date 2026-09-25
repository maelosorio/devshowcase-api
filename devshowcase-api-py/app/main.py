"""
Ponto de entrada da aplicacao.

Rode com:  uvicorn app.main:app --reload
A API sobe em http://localhost:8000
A documentacao interativa (Swagger) fica automaticamente em http://localhost:8000/docs
"""
from fastapi import FastAPI

from app.database import Base, engine
from app.errors import register_error_handlers
from app.routers import profiles, technologies, projects

# Cria as tabelas no banco automaticamente, a partir das classes em models.py,
# caso elas ainda nao existam (equivalente ao ddl-auto=update do Hibernate)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevShowcase API",
    description="API backend da plataforma DevShowcase: perfis, projetos, tecnologias e feedbacks.",
    version="1.0.0",
)

register_error_handlers(app)

app.include_router(profiles.router)
app.include_router(technologies.router)
app.include_router(projects.router)


@app.get("/", tags=["Status"])
def raiz():
    """Rota simples só pra confirmar que a API está no ar."""
    return {"status": "ok", "mensagem": "DevShowcase API está rodando. Veja /docs para a documentação."}
