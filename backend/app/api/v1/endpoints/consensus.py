from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.dependencies import get_consensus_repository
from app.api.v1.schemas import ConsensusResponse

router = APIRouter(prefix="/consensus", tags=["consensus"])


@router.get("/{consensus_id}", response_model=ConsensusResponse)
def get_consensus(consensus_id: UUID, consensus_repository=Depends(get_consensus_repository)):
    consensus = consensus_repository.get(consensus_id)
    if consensus is None:
        raise HTTPException(status_code=404, detail=f"Consensus {consensus_id} not found")
    return ConsensusResponse(
        id=consensus.id, topic=consensus.topic, summary=consensus.summary, status=consensus.status.value
    )
