from fastapi.testclient import TestClient

from app.api.dependencies import get_conversational_assistant
from app.domain.chat.interfaces import ConversationalAssistant
from app.main import app


class FakeAssistant(ConversationalAssistant):
    def reply(self, conversation):
        return "¿Podrías contarme un poco más sobre eso?"


app.dependency_overrides[get_conversational_assistant] = lambda: FakeAssistant()

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_start_conversation_and_send_message():
    response = client.post(
        "/api/v1/chat/conversations", json={"participant_mode": "anonymous", "topic": "educacion"}
    )
    assert response.status_code == 201
    conversation = response.json()
    assert len(conversation["messages"]) == 1

    response = client.post(
        f"/api/v1/chat/conversations/{conversation['id']}/messages",
        json={"content": "Falta inversión en educación rural."},
    )
    assert response.status_code == 200
    messages = response.json()["messages"]
    assert len(messages) == 3
    assert messages[-1]["author"] == "assistant"
    assert messages[-1]["content"] == "¿Podrías contarme un poco más sobre eso?"
