from dataclasses import dataclass
from uuid import UUID

from app.domain.chat.value_objects import ParticipantMode


@dataclass
class StartConversationInput:
    participant_mode: ParticipantMode
    topic: str | None = None


@dataclass
class SendMessageInput:
    conversation_id: UUID
    content: str


@dataclass
class MessageOutput:
    id: UUID
    author: str
    content: str
