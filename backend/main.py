from fastapi import FastAPI, HTTPException
import os
from models import WebhookPayload
from utilities import summarize_with_openai, send_whatsapp_reply
from db import store_summary_to_supabase
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


@app.post("/webhook")
async def whatsapp_webhook(payload: WebhookPayload):
    if not payload.entry or not payload.entry[0].changes:
        raise HTTPException(status_code=400, detail="Malformed payload")

    try:
        message = payload.entry[0].changes[0].value.messages[0]
    except (IndexError, AttributeError):
        return {"status": "no message found"}

    message_text = message.text.body if message.text else "No text content"
    sender_id = message.from_

    # Generate summary with OpenAI
    summary = await summarize_with_openai(message_text)

    # Store in Supabase
    store_summary_to_supabase(sender_id, message_text, summary)

    # Send reply back
    await send_whatsapp_reply(sender_id, summary)

    return {"status": "ok"}


@app.get("/webhook")
def verify_token(mode: str = "", challenge: str = "", verify_token: str = ""):
    if mode == "subscribe" and verify_token == VERIFY_TOKEN:
        return int(challenge)
    return {"status": "not verified"}
