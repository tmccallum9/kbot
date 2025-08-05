from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class TextMessage(BaseModel):
    body: str


class Message(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextMessage] = None


class ContactProfile(BaseModel):
    name: str


class Contact(BaseModel):
    profile: ContactProfile
    wa_id: str


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: Optional[List[Contact]]
    messages: Optional[List[Message]]


class Change(BaseModel):
    field: str
    value: Value


class Entry(BaseModel):
    id: str
    changes: List[Change]


class WebhookPayload(BaseModel):
    object: str
    entry: List[Entry]
