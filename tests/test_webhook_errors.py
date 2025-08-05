import pytest
import copy
from fastapi.testclient import TestClient
from backend.main import app
import os

os.environ["WHATSAPP_API_KEY"] = "TEST_TOKEN"


sample_message_payload = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "some_id",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "1234567890",
                            "phone_number_id": "1234567890"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Test User"
                                },
                                "wa_id": "15555555555"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15555555555",
                                "id": "wamid.test",
                                "timestamp": "1688123456",
                                "type": "text",
                                "text": {
                                    "body": "This is a test message"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}

# ✅ Fixtures
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_payload():
    return copy.deepcopy(sample_message_payload)


# ✅ Tests
def test_webhook_missing_messages(client, sample_payload):
    payload = copy.deepcopy(sample_payload)
    payload["entry"][0]["changes"][0]["value"]["messages"] = []

    response = client.post("/webhook", json=payload)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "no message found"


def test_webhook_no_text_body(monkeypatch, client, sample_payload):
    payload = copy.deepcopy(sample_payload)
    payload["entry"][0]["changes"][0]["value"]["messages"][0].pop("text", None)

    async def mock_summarize_with_openai(text):
        assert text == "No text content"
        return "Summary fallback"

    monkeypatch.setattr("backend.utilities.summarize_with_openai", mock_summarize_with_openai)
    monkeypatch.setattr("backend.db.store_summary_to_supabase", lambda *a, **kw: None)
    monkeypatch.setattr("backend.utilities.send_whatsapp_reply", lambda *a, **kw: None)

    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_webhook_openai_failure(monkeypatch, client, sample_payload):
    payload = copy.deepcopy(sample_payload)

    async def mock_summarize_with_openai(text):
        raise Exception("OpenAI is down")

    monkeypatch.setattr("backend.utilities.summarize_with_openai", mock_summarize_with_openai)
    monkeypatch.setattr("backend.db.store_summary_to_supabase", lambda *a, **kw: None)
    monkeypatch.setattr("backend.utilities.send_whatsapp_reply", lambda *a, **kw: None)

    response = client.post("/webhook", json=payload)
    assert response.status_code in [200, 500]
