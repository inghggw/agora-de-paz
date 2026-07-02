from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from app.domain.chat.value_objects import ParticipantMode

VERIFIED_VOTE_WEIGHT = 1.0
ANONYMOUS_VOTE_WEIGHT = 0.5
APPROVAL_THRESHOLD = 0.5


class ConsensusStatus(str, Enum):
    PROPOSED = "proposed"
    NOT_ALIGNED = "not_aligned"  # rechazado por el filtro de bien común
    VOTING = "voting"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Cycle:
    opens_at: datetime
    closes_at: datetime
    id: UUID = field(default_factory=uuid4)


@dataclass
class Vote:
    consensus_id: UUID
    participant_mode: ParticipantMode
    in_favor: bool
    id: UUID = field(default_factory=uuid4)
    cast_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def weight(self) -> float:
        return VERIFIED_VOTE_WEIGHT if self.participant_mode == ParticipantMode.VERIFIED else ANONYMOUS_VOTE_WEIGHT


@dataclass
class Consensus:
    cycle_id: UUID
    topic: str
    summary: str
    id: UUID = field(default_factory=uuid4)
    status: ConsensusStatus = ConsensusStatus.PROPOSED
    votes: list[Vote] = field(default_factory=list)

    def tally(self) -> tuple[float, float]:
        """Retorna (peso_a_favor, peso_total)."""
        in_favor = sum(v.weight for v in self.votes if v.in_favor)
        total = sum(v.weight for v in self.votes)
        return in_favor, total

    def resolve(self) -> ConsensusStatus:
        in_favor, total = self.tally()
        if total == 0:
            return self.status
        ratio = in_favor / total
        self.status = ConsensusStatus.APPROVED if ratio > APPROVAL_THRESHOLD else ConsensusStatus.REJECTED
        return self.status
