from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.api.dependencies import get_chat_repository
from app.api.v1.schemas import (
    ConversationResponse,
    MessageResponse,
    SendMessageRequest,
    StartConversationRequest,
)
from app.application.chat.use_cases import SendMessage, StartConversation
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/conversations", response_model=ConversationResponse, status_code=201)
def start_conversation(payload: StartConversationRequest, chat_repository=Depends(get_chat_repository)):
    use_case = StartConversation(chat_repository)
    conversation = use_case.execute(participant_mode=payload.participant_mode, topic=payload.topic)
    return _to_response(conversation)


@router.post("/conversations/{conversation_id}/messages", response_model=ConversationResponse)
def send_message(
    conversation_id: UUID, payload: SendMessageRequest, chat_repository=Depends(get_chat_repository)
):
    use_case = SendMessage(chat_repository)
    try:
        use_case.execute(conversation_id=conversation_id, content=payload.content)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    conversation = chat_repository.get(conversation_id)
    return _to_response(conversation)


def _to_response(conversation) -> ConversationResponse:
    return ConversationResponse(
        id=conversation.id,
        topic=conversation.topic,
        messages=[
            MessageResponse(id=m.id, author=m.author, content=m.content) for m in conversation.messages
        ],
    )
