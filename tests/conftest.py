# tests/conftest.py
import os
import sys
import pytest

# Add the root directory (parent of tests/) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["ENV"] = "test"


@pytest.fixture(scope="session", autouse=True)
def set_env_vars():
    os.environ["WHATSAPP_API_KEY"] = "TEST_TOKEN"
    os.environ["SUPABASE_URL"] = "Test_URL"
    os.environ["SUPABASE_KEY"] = "Test_key"
    os.environ["WHATSAPP_TOKEN"] = "Test_WhatsApp_Token"
    os.environ["WHATSAPP_PHONE_NUMBER_ID"] = "Test_Phone_ID"
    os.environ["OPENAI_API_KEY"] = "Test_OpenAI_Key"
    os.environ["WHATSAPP_VERIFY_TOKEN"] = "Test_Verify_Token"
