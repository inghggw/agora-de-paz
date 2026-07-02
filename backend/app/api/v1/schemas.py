from uuid import UUID

from pydantic import BaseModel

from app.domain.chat.value_objects import ParticipantMode


class StartConversationRequest(BaseModel):
    participant_mode: ParticipantMode
    topic: str | None = None


class SendMessageRequest(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: UUID
    author: str
    content: str


class ConversationResponse(BaseModel):
    id: UUID
    topic: str | None
    messages: list[MessageResponse]


class CastVoteRequest(BaseModel):
    participant_mode: ParticipantMode
    in_favor: bool


class ConsensusResponse(BaseModel):
    id: UUID
    topic: str
    summary: str
    status: str


class SynthesizeConsensusRequest(BaseModel):
    cycle_id: UUID
    topic: str
    texts: list[str]
