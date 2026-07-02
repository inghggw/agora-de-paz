from dataclasses import dataclass
from uuid import UUID

from app.domain.chat.value_objects import ParticipantMode


@dataclass
class CastVoteInput:
    consensus_id: UUID
    participant_mode: ParticipantMode
    in_favor: bool


@dataclass
class ConsensusOutput:
    id: UUID
    topic: str
    summary: str
    status: str
