from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.consensus.entities import Consensus, Cycle


class ConsensusRepository(ABC):
    @abstractmethod
    def save(self, consensus: Consensus) -> None: ...

    @abstractmethod
    def get(self, consensus_id: UUID) -> Consensus | None: ...

    @abstractmethod
    def list_by_cycle(self, cycle_id: UUID) -> list[Consensus]: ...


class CycleRepository(ABC):
    @abstractmethod
    def save(self, cycle: Cycle) -> None: ...

    @abstractmethod
    def current(self) -> Cycle | None: ...
