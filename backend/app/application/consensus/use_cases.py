from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domain.chat.value_objects import ParticipantMode
from app.domain.consensus.entities import Consensus, ConsensusStatus, Vote
from app.domain.consensus.interfaces import CommonGoodFilter, ConsensusRepository, SynthesisEngine


class SynthesizeConsensus:
    """Genera una propuesta de consenso a partir de las conversaciones de un
    ciclo y la pasa por el filtro de bien común (docs/03-criterios-bien-comun.md)."""

    def __init__(
        self,
        consensus_repository: ConsensusRepository,
        synthesis_engine: SynthesisEngine,
        common_good_filter: CommonGoodFilter,
    ) -> None:
        self._consensus_repository = consensus_repository
        self._synthesis_engine = synthesis_engine
        self._common_good_filter = common_good_filter

    def execute(self, cycle_id: UUID, topic: str, raw_texts: list[str]) -> Consensus:
        summary = self._synthesis_engine.synthesize(topic=topic, texts=raw_texts)
        consensus = Consensus(cycle_id=cycle_id, topic=topic, summary=summary)
        if not self._common_good_filter.is_aligned(consensus.summary):
            consensus.status = ConsensusStatus.NOT_ALIGNED
        self._consensus_repository.save(consensus)
        return consensus


class VoteConsensus:
    def __init__(self, consensus_repository: ConsensusRepository) -> None:
        self._consensus_repository = consensus_repository

    def execute(self, consensus_id: UUID, participant_mode: ParticipantMode, in_favor: bool) -> Consensus:
        consensus = self._consensus_repository.get(consensus_id)
        if consensus is None:
            raise NotFoundError(f"Consensus {consensus_id} not found")
        consensus.votes.append(
            Vote(consensus_id=consensus_id, participant_mode=participant_mode, in_favor=in_favor)
        )
        self._consensus_repository.save(consensus)
        return consensus
