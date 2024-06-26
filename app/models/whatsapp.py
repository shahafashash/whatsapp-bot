from enum import StrEnum
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict

from app.config import get_settings


class WhatsappMessageType(StrEnum):
    TEXT = "text"
    REACTION = "reaction"
    IMAGE = "image"
    LOCATION = "location"
    CONTACTS = "contacts"
    LIST = "list"
    BUTTON = "button"

class WhatsappWebhookChallenge(BaseModel):
    hub_challenge: str

class WhatsappWebhookStatus(BaseModel):
    status: Literal['ok', 'error']

class WhatsappMessageHeaders(BaseModel):
    content_type: Literal["application/json"] = "application/json"
    authorization: Literal[f"Bearer {get_settings().access_token}"] = f"Bearer {get_settings().access_token}"

class WhatsappMessagePayload(BaseModel):
    pass

class WhatsappMessage(BaseModel):
    messaging_product: Literal["whatsapp"] = "whatsapp"
    recipient_type: Literal["individual"] = "individual"
    to: str
    type: WhatsappMessageType

    model_config = ConfigDict(extra='allow')
    
    def _add_payload(self, payload: WhatsappMessagePayload) -> None:
        setattr(self, self.type.value, payload)

    def __init__(self, to: str, type: WhatsappMessageType, payload: WhatsappMessagePayload) -> None:
        super().__init__(to=to, type=type)
        self._add_payload(payload)


class WhatsappTextPayload(WhatsappMessagePayload):
    preview_url: Optional[Literal['false', 'true']] = 'false'
    body: str

class WhatsappTextMessage(WhatsappMessage):
    type: Literal[WhatsappMessageType.TEXT]
    
    def __init__(self, to: str, payload: WhatsappTextPayload) -> None:
        super().__init__(to=to, type=WhatsappMessageType.TEXT, payload=payload)

class WhatsappReactionMessage(WhatsappMessage):
    type: Literal[WhatsappMessageType.REACTION]
    
    def __init__(self, to: str, payload: WhatsappMessagePayload) -> None:
        super().__init__(to=to, type=WhatsappMessageType.REACTION, payload=payload)

class WhatsappReactionPayload(WhatsappMessagePayload):
    message_id: str
    emoji: str