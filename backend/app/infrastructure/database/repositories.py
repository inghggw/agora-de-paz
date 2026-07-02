"""Implementaciones concretas de los repositorios del dominio.

Incluye repositorios en memoria (desarrollo local y tests sin depender de
PostgreSQL) y repositorios reales sobre SQLAlchemy/PostgreSQL, seleccionables
vía `Settings.repository_backend` (ver app/api/dependencies.py y
docs/04-arquitectura.md).
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.domain.chat.entities import ChatMessage, Conversation
from app.domain.chat.interfaces import ChatRepository
from app.domain.chat.value_objects import ParticipantMode
from app.domain.consensus.entities import Consensus, ConsensusStatus, Cycle, Vote
from app.domain.consensus.interfaces import ConsensusRepository, CycleRepository
from app.infrastructure.database.models import (
    ChatMessageModel,
    ConsensusModel,
    ConversationModel,
    CycleModel,
    VoteModel,
)


class InMemoryChatRepository(ChatRepository):
    def __init__(self) -> None:
        self._conversations: dict[UUID, Conversation] = {}

    def save(self, conversation: Conversation) -> None:
        self._conversations[conversation.id] = conversation

    def get(self, conversation_id: UUID) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def list_since(self, since: datetime) -> list[Conversation]:
        return [c for c in self._conversations.values() if c.created_at >= since]


class InMemoryConsensusRepository(ConsensusRepository):
    def __init__(self) -> None:
        self._consensuses: dict[UUID, Consensus] = {}

    def save(self, consensus: Consensus) -> None:
        self._consensuses[consensus.id] = consensus

    def get(self, consensus_id: UUID) -> Consensus | None:
        return self._consensuses.get(consensus_id)

    def list_by_cycle(self, cycle_id: UUID) -> list[Consensus]:
        return [c for c in self._consensuses.values() if c.cycle_id == cycle_id]


class InMemoryCycleRepository(CycleRepository):
    def __init__(self) -> None:
        self._cycles: dict[UUID, Cycle] = {}
        self._current_id: UUID | None = None

    def save(self, cycle: Cycle) -> None:
        self._cycles[cycle.id] = cycle
        self._current_id = cycle.id

    def current(self) -> Cycle | None:
        if self._current_id is None:
            return None
        return self._cycles.get(self._current_id)


def _conversation_from_model(model: ConversationModel) -> Conversation:
    conversation = Conversation(
        participant_mode=ParticipantMode(model.participant_mode),
        id=model.id,
        topic=model.topic,
        created_at=model.created_at,
    )
    conversation.messages = [
        ChatMessage(
            conversation_id=model.id,
            author=m.author,
            content=m.content,
            id=m.id,
            created_at=m.created_at,
        )
        for m in model.messages
    ]
    return conversation


class PostgresChatRepository(ChatRepository):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def save(self, conversation: Conversation) -> None:
        with self._session_factory() as session:
            model = session.get(ConversationModel, conversation.id)
            if model is None:
                model = ConversationModel(
                    id=conversation.id,
                    participant_mode=conversation.participant_mode.value,
                    topic=conversation.topic,
                    created_at=conversation.created_at,
                )
                session.add(model)
                session.flush()
            persisted_ids = {m.id for m in model.messages}
            for message in conversation.messages:
                if message.id not in persisted_ids:
                    session.add(
                        ChatMessageModel(
                            id=message.id,
                            conversation_id=conversation.id,
                            author=message.author,
                            content=message.content,
                            created_at=message.created_at,
                        )
                    )
            session.commit()

    def get(self, conversation_id: UUID) -> Conversation | None:
        with self._session_factory() as session:
            model = session.get(ConversationModel, conversation_id)
            return _conversation_from_model(model) if model else None

    def list_since(self, since: datetime) -> list[Conversation]:
        with self._session_factory() as session:
            stmt = select(ConversationModel).where(ConversationModel.created_at >= since)
            return [_conversation_from_model(m) for m in session.scalars(stmt)]


def _consensus_from_model(model: ConsensusModel) -> Consensus:
    consensus = Consensus(
        cycle_id=model.cycle_id,
        topic=model.topic,
        summary=model.summary,
        id=model.id,
        status=ConsensusStatus(model.status),
    )
    consensus.votes = [
        Vote(
            consensus_id=model.id,
            participant_mode=ParticipantMode(v.participant_mode),
            in_favor=v.in_favor,
            id=v.id,
            cast_at=v.cast_at,
        )
        for v in model.votes
    ]
    return consensus


class PostgresConsensusRepository(ConsensusRepository):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def save(self, consensus: Consensus) -> None:
        with self._session_factory() as session:
            model = session.get(ConsensusModel, consensus.id)
            if model is None:
                model = ConsensusModel(
                    id=consensus.id,
                    cycle_id=consensus.cycle_id,
                    topic=consensus.topic,
                    summary=consensus.summary,
                    status=consensus.status.value,
                )
                session.add(model)
                session.flush()
            else:
                model.summary = consensus.summary
                model.status = consensus.status.value
            persisted_ids = {v.id for v in model.votes}
            for vote in consensus.votes:
                if vote.id not in persisted_ids:
                    session.add(
                        VoteModel(
                            id=vote.id,
                            consensus_id=consensus.id,
                            participant_mode=vote.participant_mode.value,
                            in_favor=vote.in_favor,
                            cast_at=vote.cast_at,
                        )
                    )
            session.commit()

    def get(self, consensus_id: UUID) -> Consensus | None:
        with self._session_factory() as session:
            model = session.get(ConsensusModel, consensus_id)
            return _consensus_from_model(model) if model else None

    def list_by_cycle(self, cycle_id: UUID) -> list[Consensus]:
        with self._session_factory() as session:
            stmt = select(ConsensusModel).where(ConsensusModel.cycle_id == cycle_id)
            return [_consensus_from_model(m) for m in session.scalars(stmt)]


class PostgresCycleRepository(CycleRepository):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def save(self, cycle: Cycle) -> None:
        with self._session_factory() as session:
            model = session.get(CycleModel, cycle.id)
            if model is None:
                session.add(CycleModel(id=cycle.id, opens_at=cycle.opens_at, closes_at=cycle.closes_at))
            session.commit()

    def current(self) -> Cycle | None:
        with self._session_factory() as session:
            stmt = select(CycleModel).order_by(CycleModel.opens_at.desc()).limit(1)
            model = session.scalars(stmt).first()
            if model is None:
                return None
            return Cycle(id=model.id, opens_at=model.opens_at, closes_at=model.closes_at)
