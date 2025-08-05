import json
import pytest
from fastapi.testclient import TestClient
from backend.main import app

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

    def mock_store_summary_to_supabase(user_id, raw_text, summary):
        print(f"[MOCK] Saved summary for {user_id}: {summary}")

    async def mock_send_whatsapp_reply(to, text):
        print(f"[MOCK] Sent message to {to}: {text}")

    monkeypatch.setattr("backend.utils.summarize_with_openai", mock_summarize_with_openai)
    monkeypatch.setattr("backend.db.store_summary_to_supabase", mock_store_summary_to_supabase)
    monkeypatch.setattr("backend.utils.send_whatsapp_reply", mock_send_whatsapp_reply)

    response = client.post("/webhook", json=sample_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
