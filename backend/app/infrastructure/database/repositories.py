"""Implementaciones concretas de los repositorios del dominio.

Por ahora son repositorios en memoria (útiles para desarrollo local y tests
sin depender de PostgreSQL). La implementación con SQLAlchemy sobre
`models.py` llega junto con el resto de la Etapa 2/4 de la hoja de ruta.
"""

from datetime import datetime
from uuid import UUID

from app.domain.chat.entities import Conversation
from app.domain.chat.interfaces import ChatRepository
from app.domain.consensus.entities import Consensus, Cycle
from app.domain.consensus.interfaces import ConsensusRepository, CycleRepository


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
