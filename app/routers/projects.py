"""
Router de Project - o recurso central da API.

Endpoints exigidos pela atividade:
    POST /api/projects                    -> cadastro de projeto com validações
    GET  /api/projects                    -> listagem com filtro por tecnologia e paginação
    POST /api/projects/{id}/feedbacks     -> cadastrar nota (1-5) + comentário, atualiza a média
    PUT  /api/projects/{id}/upvote        -> incrementa as curtidas/estrelas do projeto

Também incluímos GET /api/projects/{id} (buscar um projeto específico),
que não é exigido explicitamente mas é útil pra demonstrar no vídeo
(inclusive pra mostrar o erro 404 quando o ID não existe).
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.errors import ResourceNotFoundError
from app.routers.technologies import buscar_ou_criar_tecnologia

router = APIRouter(prefix="/api/projects", tags=["Projetos"])


def _para_saida(projeto: models.Project) -> schemas.ProjectOut:
    """Monta o DTO de saída a partir da entidade do banco (junta dados de outras tabelas)."""
    return schemas.ProjectOut(
        id=projeto.id,
        title=projeto.title,
        description=projeto.description,
        profile_id=projeto.profile_id,
        profile_name=projeto.profile.name,
        technologies=[t.name for t in projeto.technologies],
        medias=projeto.medias or [],
        views=projeto.views,
        upvotes=projeto.upvotes,
        average_rating=round(projeto.average_rating, 2),
        feedback_count=len(projeto.feedbacks),
        created_at=projeto.created_at,
    )


def _buscar_projeto_ou_404(db: Session, project_id: int) -> models.Project:
    projeto = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not projeto:
        raise ResourceNotFoundError(f"Projeto não encontrado com o ID: {project_id}")
    return projeto


@router.post("", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def criar_projeto(dados: schemas.ProjectCreate, db: Session = Depends(get_db)):
    perfil = db.query(models.Profile).filter(models.Profile.id == dados.profile_id).first()
    if not perfil:
        raise ResourceNotFoundError(f"Perfil não encontrado com o ID: {dados.profile_id}")

    tecnologias = [buscar_ou_criar_tecnologia(db, nome) for nome in dados.technologies]

    projeto = models.Project(
        title=dados.title,
        description=dados.description,
        profile_id=perfil.id,
        technologies=tecnologias,
        medias=dados.medias,
    )
    db.add(projeto)
    db.commit()
    db.refresh(projeto)
    return _para_saida(projeto)


@router.get("", response_model=list[schemas.ProjectOut])
def listar_projetos(
    db: Session = Depends(get_db),
    technology: str | None = Query(default=None, description="Filtra projetos que usam essa tecnologia"),
    page: int = Query(default=1, ge=1, description="Número da página (começa em 1)"),
    size: int = Query(default=10, ge=1, le=100, description="Quantos projetos por página"),
):
    query = db.query(models.Project)

    if technology:
        query = query.join(models.Project.technologies).filter(models.Technology.name.ilike(technology))

    total_de_projetos = query.count()
    projetos = (
        query.order_by(models.Project.id)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return [_para_saida(p) for p in projetos]


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def buscar_projeto(project_id: int, db: Session = Depends(get_db)):
    projeto = _buscar_projeto_ou_404(db, project_id)
    # Regra de negócio: toda consulta a um projeto específico conta como visualização
    projeto.views += 1
    db.commit()
    db.refresh(projeto)
    return _para_saida(projeto)


@router.put("/{project_id}/upvote", response_model=schemas.ProjectOut)
def dar_upvote(project_id: int, db: Session = Depends(get_db)):
    projeto = _buscar_projeto_ou_404(db, project_id)
    projeto.upvotes += 1
    db.commit()
    db.refresh(projeto)
    return _para_saida(projeto)


@router.post("/{project_id}/feedbacks", response_model=schemas.FeedbackOut, status_code=status.HTTP_201_CREATED)
def criar_feedback(project_id: int, dados: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    projeto = _buscar_projeto_ou_404(db, project_id)

    feedback = models.Feedback(rating=dados.rating, comment=dados.comment, project_id=projeto.id)
    db.add(feedback)
    db.flush()  # grava no banco (sem fechar a transação) para já conseguirmos contar esse feedback
    db.refresh(projeto)  # recarrega o projeto para que projeto.feedbacks inclua o novo registro

    # Regra de negócio: recalcula a nota média do projeto toda vez que chega um feedback novo
    todas_as_notas = [f.rating for f in projeto.feedbacks]
    projeto.average_rating = sum(todas_as_notas) / len(todas_as_notas)

    db.commit()
    db.refresh(feedback)
    return feedback
