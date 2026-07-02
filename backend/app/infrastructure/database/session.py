from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.infrastructure.database.models import Base


def make_engine(settings: Settings) -> Engine:
    return create_engine(settings.database_url, pool_pre_ping=True)


def make_session_factory(settings: Settings) -> sessionmaker:
    return sessionmaker(bind=make_engine(settings), expire_on_commit=False, class_=Session)


def init_db(settings: Settings) -> None:
    """Crea las tablas si no existen. Suficiente para el MVP; una migración
    con Alembic reemplaza esto cuando el esquema empiece a evolucionar en
    producción (ver docs/04-arquitectura.md)."""
    Base.metadata.create_all(make_engine(settings))
