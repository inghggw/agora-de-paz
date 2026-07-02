from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domain.chat.entities import ChatMessage, Conversation
from app.domain.chat.interfaces import ChatRepository, ConversationalAssistant


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
    """Registra el mensaje del ciudadano y genera la respuesta del asistente
    conversacional (LLM local vía Ollama, docs/02-metodologia.md#1-conversación-abierta)."""

    def __init__(self, chat_repository: ChatRepository, assistant: ConversationalAssistant) -> None:
        self._chat_repository = chat_repository
        self._assistant = assistant

    def execute(self, conversation_id: UUID, content: str) -> ChatMessage:
        conversation = self._chat_repository.get(conversation_id)
        if conversation is None:
            raise NotFoundError(f"Conversation {conversation_id} not found")
        conversation.add_message(author="citizen", content=content)
        reply = self._assistant.reply(conversation)
        assistant_message = conversation.add_message(author="assistant", content=reply)
        self._chat_repository.save(conversation)
        return assistant_message
