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

def test_webhook_missing_messages(client):
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "test_id",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp"
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "no message found"

def test_webhook_no_text_body(monkeypatch, client, sample_payload):
    sample_payload["entry"][0]["changes"][0]["value"]["messages"][0].pop("text", None)

    async def mock_summarize_with_openai(text):
        assert text == "No text content"
        return "Summary fallback"

    monkeypatch.setattr("backend.utils.summarize_with_openai", mock_summarize_with_openai)
    monkeypatch.setattr("backend.db.store_summary_to_supabase", lambda *a, **kw: None)
    monkeypatch.setattr("backend.utils.send_whatsapp_reply", lambda *a, **kw: None)

    response = client.post("/webhook", json=sample_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_webhook_openai_failure(monkeypatch, client, sample_payload):
    async def mock_summarize_with_openai(text):
        raise Exception("OpenAI is down")

    monkeypatch.setattr("backend.utils.summarize_with_openai", mock_summarize_with_openai)
    monkeypatch.setattr("backend.db.store_summary_to_supabase", lambda *a, **kw: None)
    monkeypatch.setattr("backend.utils.send_whatsapp_reply", lambda *a, **kw: None)

    response = client.post("/webhook", json=sample_payload)
    assert response.status_code in [200, 500]
