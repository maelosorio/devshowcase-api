"""
Camada Controller (aqui chamada de "router", termo padrao do FastAPI)
para o recurso Profile (Perfil do Desenvolvedor).

Endpoints exigidos pela atividade:
    POST /api/profiles          -> cadastro de perfil com validações
    GET  /api/profiles/{id}     -> buscar perfil por id
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.errors import DuplicateResourceError, ResourceNotFoundError

router = APIRouter(prefix="/api/profiles", tags=["Perfis"])


@router.post("", response_model=schemas.ProfileOut, status_code=status.HTTP_201_CREATED)
def criar_perfil(dados: schemas.ProfileCreate, db: Session = Depends(get_db)):
    # Regra de negócio: e-mail precisa ser único
    ja_existe = db.query(models.Profile).filter(models.Profile.email == dados.email).first()
    if ja_existe:
        raise DuplicateResourceError(f"Já existe um perfil cadastrado com o e-mail: {dados.email}")

    perfil = models.Profile(**dados.model_dump())
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil


@router.get("/{profile_id}", response_model=schemas.ProfileOut)
def buscar_perfil(profile_id: int, db: Session = Depends(get_db)):
    perfil = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not perfil:
        raise ResourceNotFoundError(f"Perfil não encontrado com o ID: {profile_id}")
    return perfil
