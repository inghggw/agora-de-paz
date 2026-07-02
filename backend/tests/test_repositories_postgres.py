from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import OperationalError

from app.core.config import Settings
from app.domain.chat.entities import Conversation
from app.domain.chat.value_objects import ParticipantMode
from app.domain.consensus.entities import Consensus, Cycle, Vote
from app.infrastructure.database.repositories import (
    PostgresChatRepository,
    PostgresConsensusRepository,
    PostgresCycleRepository,
)
from app.infrastructure.database.session import init_db, make_session_factory

settings = Settings(repository_backend="postgres")

try:
    _session_factory = make_session_factory(settings)
    init_db(settings)
    POSTGRES_AVAILABLE = True
except OperationalError:
    POSTGRES_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not POSTGRES_AVAILABLE, reason="Requiere PostgreSQL corriendo (ver backend/docker-compose.yml)"
)


def test_chat_repository_round_trip():
    repository = PostgresChatRepository(_session_factory)
    conversation = Conversation(participant_mode=ParticipantMode.VERIFIED, topic="seguridad")
    conversation.add_message(author="assistant", content="¿Cómo debería ser la seguridad en tu barrio?")
    conversation.add_message(author="citizen", content="Más presencia policial en el barrio.")

    repository.save(conversation)
    fetched = repository.get(conversation.id)

    assert fetched is not None
    assert fetched.topic == "seguridad"
    assert [m.content for m in fetched.messages] == [m.content for m in conversation.messages]

    since = datetime.now(timezone.utc) - timedelta(minutes=5)
    assert conversation.id in {c.id for c in repository.list_since(since)}


def test_consensus_repository_round_trip_and_vote_tally():
    cycle_repository = PostgresCycleRepository(_session_factory)
    now = datetime.now(timezone.utc)
    cycle = Cycle(opens_at=now, closes_at=now + timedelta(days=7))
    cycle_repository.save(cycle)

    repository = PostgresConsensusRepository(_session_factory)
    consensus = Consensus(cycle_id=cycle.id, topic="educacion", summary="Consenso emergente: prueba")
    repository.save(consensus)

    consensus.votes.append(
        Vote(consensus_id=consensus.id, participant_mode=ParticipantMode.VERIFIED, in_favor=True)
    )
    repository.save(consensus)

    fetched = repository.get(consensus.id)
    assert fetched is not None
    assert len(fetched.votes) == 1
    in_favor, total = fetched.tally()
    assert in_favor == 1.0
    assert total == 1.0
