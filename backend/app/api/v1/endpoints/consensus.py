from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.dependencies import get_common_good_filter, get_consensus_repository, get_synthesis_engine
from app.api.v1.schemas import ConsensusResponse, SynthesizeConsensusRequest
from app.application.consensus.use_cases import SynthesizeConsensus

router = APIRouter(prefix="/consensus", tags=["consensus"])


@router.post("/synthesize", response_model=ConsensusResponse, status_code=201)
def synthesize_consensus(
    payload: SynthesizeConsensusRequest,
    consensus_repository=Depends(get_consensus_repository),
    synthesis_engine=Depends(get_synthesis_engine),
    common_good_filter=Depends(get_common_good_filter),
):
    use_case = SynthesizeConsensus(consensus_repository, synthesis_engine, common_good_filter)
    consensus = use_case.execute(cycle_id=payload.cycle_id, topic=payload.topic, raw_texts=payload.texts)
    return _to_response(consensus)


@router.get("/{consensus_id}", response_model=ConsensusResponse)
def get_consensus(consensus_id: UUID, consensus_repository=Depends(get_consensus_repository)):
    consensus = consensus_repository.get(consensus_id)
    if consensus is None:
        raise HTTPException(status_code=404, detail=f"Consensus {consensus_id} not found")
    return _to_response(consensus)


def _to_response(consensus) -> ConsensusResponse:
    return ConsensusResponse(
        id=consensus.id, topic=consensus.topic, summary=consensus.summary, status=consensus.status.value
    )
