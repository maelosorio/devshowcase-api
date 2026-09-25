"""
Configuracao da conexao com o banco de dados.

Por padrao (sem nenhuma configuracao) usamos SQLite, um banco que fica
num arquivo unico (devshowcase.db) na propria pasta do projeto - nao
precisa instalar nada pra testar local.

Em producao (quando fizer o deploy no Render), a variavel de ambiente
DATABASE_URL vai apontar pro PostgreSQL, e o codigo troca sozinho.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devshowcase.db")

# O driver que usamos pro PostgreSQL agora e o "psycopg" (versao 3), que precisa
# do dialeto escrito como "postgresql+psycopg://" em vez de so "postgresql://".
# Isso deixa a variavel de ambiente mais simples de copiar do Supabase/Render
# (que geralmente fornecem no formato antigo) sem voce precisar editar nada.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# connect_args so necessario pro SQLite (nao existe no Postgres)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Cada requisicao recebe sua propria "conexao" com o banco (sessao),
    e ela e fechada automaticamente no final - mesmo se der erro.
    O FastAPI injeta isso automaticamente em quem tiver: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
