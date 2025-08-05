from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class TextMessage(BaseModel):
    body: str


class Message(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextMessage]


class Value(BaseModel):
    messaging_product: str
    metadata: Dict
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
