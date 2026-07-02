from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.dependencies import get_consensus_repository
from app.api.v1.schemas import CastVoteRequest, ConsensusResponse
from app.application.consensus.use_cases import VoteConsensus
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/{consensus_id}", response_model=ConsensusResponse)
def cast_vote(
    consensus_id: UUID, payload: CastVoteRequest, consensus_repository=Depends(get_consensus_repository)
):
    use_case = VoteConsensus(consensus_repository)
    try:
        consensus = use_case.execute(
            consensus_id=consensus_id,
            participant_mode=payload.participant_mode,
            in_favor=payload.in_favor,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ConsensusResponse(
        id=consensus.id, topic=consensus.topic, summary=consensus.summary, status=consensus.status.value
    )
