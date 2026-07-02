from fastapi.testclient import TestClient

from app.main import app

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
    assert len(response.json()["messages"]) == 2
