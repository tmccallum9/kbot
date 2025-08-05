from openai import AsyncOpenAI, OpenAIError
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def summarize_with_openai(text: str) -> str:
    """
    Generate a summary of the input chat text using OpenAI GPT-4.
    """
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a concise WhatsApp group chat summarizer."},
                {"role": "user", "content": f"Summarize the following chat:\n\n{text}"}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        return f"⚠️ OpenAI API error: {str(e)}"


async def send_whatsapp_reply(to: str, text: str):
    """
    Send a text message via the WhatsApp Cloud API.
    """
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload, headers=headers)
