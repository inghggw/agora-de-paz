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


class SynthesisEngine(ABC):
    """Motor de síntesis: agrupa conversaciones de un ciclo y propone
    consensos (docs/02-metodologia.md#3-síntesis-por-ia)."""

    @abstractmethod
    def synthesize(self, topic: str, texts: list[str]) -> str: ...


class CommonGoodFilter(ABC):
    """Filtro de bien común, núcleo ético y auditable del sistema
    (docs/03-criterios-bien-comun.md)."""

    @abstractmethod
    def is_aligned(self, summary: str) -> bool: ...
