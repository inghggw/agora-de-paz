"""Asistente conversacional del chat ciudadano, respaldado por un LLM local
vía Ollama (independencia tecnológica, docs/01-problema-y-vision.md,
principio 7).
"""

from app.domain.chat.entities import Conversation
from app.domain.chat.interfaces import ConversationalAssistant
from app.infrastructure.ai.ollama_client import OllamaClient

SYSTEM_PROMPT = (
    "Eres el asistente conversacional de Ágora de Paz, una plataforma de "
    "gobernanza participativa. Conversas con un ciudadano de Ibagué, Tolima, "
    "Colombia sobre los desafíos de su ciudad. Haz preguntas abiertas y "
    "breves para profundizar en el tema, sin dar tu propia opinión política "
    "ni proponer soluciones: tu rol es escuchar y ayudar a que la persona "
    "elabore su punto de vista."
)


class OllamaConversationalAssistant(ConversationalAssistant):
    def __init__(self, client: OllamaClient) -> None:
        self._client = client

    def reply(self, conversation: Conversation) -> str:
        transcript = "\n".join(
            f"{'Ciudadano' if m.author == 'citizen' else 'Ágora'}: {m.content}"
            for m in conversation.messages
        )
        prompt = f"{SYSTEM_PROMPT}\n\n{transcript}\nÁgora:"
        return self._client.generate(prompt).strip()
