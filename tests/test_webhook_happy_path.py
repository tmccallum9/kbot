import json
import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os

os.environ["WHATSAPP_API_KEY"] = "TEST_TOKEN"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_payload():
    with open("tests/test_payload.json") as f:
        return json.load(f)


def test_webhook_success(monkeypatch, client, sample_payload):
    async def mock_summarize_with_openai(text):
        return "This is a mock summary."

    async def mock_send_whatsapp_reply(to, text):
        print(f"[MOCK] Sent message to {to}: {text}")

    monkeypatch.setattr("backend.utilities.summarize_with_openai", mock_summarize_with_openai)
    monkeypatch.setattr("backend.utilities.send_whatsapp_reply", mock_send_whatsapp_reply)
    monkeypatch.setattr("backend.db.store_summary_to_supabase", lambda *a, **kw: None)

    response = client.post("/webhook", json=sample_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
