"""
Camada de DTOs (aqui chamados de "schemas", que e o termo padrao no FastAPI).

Cada schema herda de BaseModel (Pydantic). O Pydantic valida os dados
AUTOMATICAMENTE antes do codigo da rota rodar - se faltar um campo
obrigatorio ou o tipo estiver errado, o FastAPI ja devolve um erro 422
sozinho, sem precisarmos escrever nenhum "if".

Convencao usada aqui:
    *Create -> dados de ENTRADA para criar um recurso
    *Out    -> dados de SAIDA (o que a API devolve pro cliente)
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ---------- Technology ----------

class TechnologyOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # permite converter direto de um objeto do SQLAlchemy


class TechnologyCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nome da tecnologia, ex: 'Python'")

    @field_validator("name")
    @classmethod
    def nome_nao_pode_ser_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("o nome da tecnologia não pode ser vazio")
        return v.strip()


# ---------- Profile ----------

class ProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nome completo")
    email: EmailStr
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    skills: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("o nome não pode ser vazio")
        return v.strip()


class ProfileOut(BaseModel):
    id: int
    name: str
    email: str
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    skills: list[str] = []

    class Config:
        from_attributes = True


# ---------- Feedback ----------

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Nota de 1 a 5")
    comment: str = Field(..., min_length=1, description="Comentário sobre o projeto")

    @field_validator("comment")
    @classmethod
    def comentario_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("o comentário não pode ser vazio")
        return v.strip()


class FeedbackOut(BaseModel):
    id: int
    rating: int
    comment: str
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Project ----------

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Título do projeto (não pode ser vazio)")
    description: Optional[str] = None
    profile_id: int = Field(..., description="ID do perfil dono do projeto")
    technologies: list[str] = Field(default_factory=list, description="Nomes das tecnologias usadas")
    medias: list[str] = Field(default_factory=list, description="URLs de imagens, vídeos, repositório, etc.")

    @field_validator("title")
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("o título não pode ser vazio")
        return v.strip()

    @field_validator("medias")
    @classmethod
    def midias_precisam_ser_urls_validas(cls, urls: list[str]) -> list[str]:
        for url in urls:
            if not (url.startswith("http://") or url.startswith("https://")):
                raise ValueError(f"'{url}' não é uma URL válida (precisa começar com http:// ou https://)")
        return urls


class ProjectOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    profile_id: int
    profile_name: str
    technologies: list[str] = []
    medias: list[str] = []
    views: int
    upvotes: int
    average_rating: float
    feedback_count: int
    created_at: datetime

    class Config:
        from_attributes = True
