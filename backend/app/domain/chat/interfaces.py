from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domain.chat.entities import Conversation


class ChatRepository(ABC):
    @abstractmethod
    def save(self, conversation: Conversation) -> None: ...

    @abstractmethod
    def get(self, conversation_id: UUID) -> Conversation | None: ...

    @abstractmethod
    def list_since(self, since: datetime) -> list[Conversation]: ...


class ConversationalAssistant(ABC):
    """Puerto hacia el motor conversacional (LLM local vía Ollama, ver
    docs/02-metodologia.md#1-conversación-abierta)."""

    @abstractmethod
    def reply(self, conversation: Conversation) -> str: ...
