"""Modelos SQLAlchemy ORM.

Mapean 1:1 las entidades de dominio (app.domain.*.entities) a tablas
PostgreSQL. Usados por los repositorios Postgres en repositories.py cuando
`Settings.repository_backend == "postgres"` (ver docs/04-arquitectura.md).
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ConversationModel(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    participant_mode: Mapped[str] = mapped_column(String(20))
    topic: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    messages: Mapped[list["ChatMessageModel"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ChatMessageModel.created_at",
    )


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    conversation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("conversations.id"))
    author: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    conversation: Mapped["ConversationModel"] = relationship(back_populates="messages")


class CycleModel(Base):
    __tablename__ = "cycles"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    opens_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    closes_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ConsensusModel(Base):
    __tablename__ = "consensuses"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    cycle_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("cycles.id"))
    topic: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String(20))

    votes: Mapped[list["VoteModel"]] = relationship(
        back_populates="consensus", cascade="all, delete-orphan"
    )


class VoteModel(Base):
    __tablename__ = "votes"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    consensus_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("consensuses.id"))
    participant_mode: Mapped[str] = mapped_column(String(20))
    in_favor: Mapped[bool] = mapped_column(Boolean)
    cast_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    consensus: Mapped["ConsensusModel"] = relationship(back_populates="votes")
