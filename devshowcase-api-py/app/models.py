"""
Camada Model: representa as tabelas do banco de dados como classes Python.
Cada classe = uma tabela. Cada atributo = uma coluna.
Isso e feito com o SQLAlchemy (o "ORM" do Python, equivalente ao Hibernate do Java).

Entidades e relacionamentos (conforme pedido na atividade):
    Profile  1 : N  Project
    Project  N : N  Technology
    Project  1 : N  Feedback
"""
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, Float, ForeignKey, DateTime, Table, JSON
)
from sqlalchemy.orm import relationship

from app.database import Base

# Tabela de associacao para o relacionamento N:N entre Project e Technology.
# Nao vira uma classe propria porque so guarda os IDs dos dois lados.
project_technology = Table(
    "project_technology",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("technology_id", ForeignKey("technologies.id"), primary_key=True),
)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    bio = Column(Text, nullable=True)
    github = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    portfolio = Column(String, nullable=True)
    # Lista de competencias (ex: ["Java", "Python"]) guardada como JSON
    skills = Column(JSON, default=list)

    # "back_populates" liga esse relacionamento com o "profile" la na classe Project
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    projects = relationship("Project", secondary=project_technology, back_populates="technologies")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    profile = relationship("Profile", back_populates="projects")

    technologies = relationship("Technology", secondary=project_technology, back_populates="projects")

    # Galeria de midias/links (URLs), guardada como lista JSON
    medias = Column(JSON, default=list)

    # Metricas de interacao
    views = Column(Integer, default=0, nullable=False)
    upvotes = Column(Integer, default=0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    feedbacks = relationship("Feedback", back_populates="project", cascade="all, delete-orphan")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)  # nota de 1 a 5
    comment = Column(Text, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="feedbacks")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
