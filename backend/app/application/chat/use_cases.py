from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domain.chat.entities import ChatMessage, Conversation
from app.domain.chat.interfaces import ChatRepository


class StartConversation:
    def __init__(self, chat_repository: ChatRepository) -> None:
        self._chat_repository = chat_repository

    def execute(self, participant_mode, topic: str | None = None) -> Conversation:
        conversation = Conversation(participant_mode=participant_mode, topic=topic)
        conversation.add_message(
            author="assistant",
            content="¿Cuál es el mayor desafío que ves en tu ciudad hoy?",
        )
        self._chat_repository.save(conversation)
        return conversation


class SendMessage:
    """Registra el mensaje del ciudadano. La respuesta del asistente (síntesis
    incremental vía Ollama) se conecta en la Etapa 3 de la hoja de ruta."""

    def __init__(self, chat_repository: ChatRepository) -> None:
        self._chat_repository = chat_repository

    def execute(self, conversation_id: UUID, content: str) -> ChatMessage:
        conversation = self._chat_repository.get(conversation_id)
        if conversation is None:
            raise NotFoundError(f"Conversation {conversation_id} not found")
        message = conversation.add_message(author="citizen", content=content)
        self._chat_repository.save(conversation)
        return message
