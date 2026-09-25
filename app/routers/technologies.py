"""
Router de Technology.

Endpoints exigidos pela atividade:
    POST /api/technologies  -> cadastro de tecnologia com validações
    GET  /api/technologies  -> listagem de todas as tecnologias
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.errors import DuplicateResourceError

router = APIRouter(prefix="/api/technologies", tags=["Tecnologias"])


@router.post("", response_model=schemas.TechnologyOut, status_code=status.HTTP_201_CREATED)
def criar_tecnologia(dados: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    # Regra de negócio: não deixar cadastrar a mesma tecnologia duas vezes
    ja_existe = db.query(models.Technology).filter(models.Technology.name.ilike(dados.name)).first()
    if ja_existe:
        raise DuplicateResourceError(f"A tecnologia '{dados.name}' já está cadastrada")

    tecnologia = models.Technology(name=dados.name)
    db.add(tecnologia)
    db.commit()
    db.refresh(tecnologia)
    return tecnologia


@router.get("", response_model=list[schemas.TechnologyOut])
def listar_tecnologias(db: Session = Depends(get_db)):
    return db.query(models.Technology).all()


def buscar_ou_criar_tecnologia(db: Session, nome: str) -> models.Technology:
    """
    Regra de negócio "find or create", usada pelo router de Project:
    se a tecnologia já existe, reaproveita; senão, cria uma nova.
    Evita duplicar "Python", "python", "PYTHON" como linhas diferentes.
    """
    nome = nome.strip()
    tecnologia = db.query(models.Technology).filter(models.Technology.name.ilike(nome)).first()
    if tecnologia:
        return tecnologia
    tecnologia = models.Technology(name=nome)
    db.add(tecnologia)
    db.flush()  # gera o ID sem precisar commitar ainda
    return tecnologia
