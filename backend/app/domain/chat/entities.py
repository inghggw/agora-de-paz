from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.chat.value_objects import ParticipantMode


@dataclass
class ChatMessage:
    conversation_id: UUID
    author: str  # "citizen" | "assistant"
    content: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Conversation:
    participant_mode: ParticipantMode
    id: UUID = field(default_factory=uuid4)
    topic: str | None = None
    messages: list[ChatMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add_message(self, author: str, content: str) -> ChatMessage:
        message = ChatMessage(conversation_id=self.id, author=author, content=content)
        self.messages.append(message)
        return message
