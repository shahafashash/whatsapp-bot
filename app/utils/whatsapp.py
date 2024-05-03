from typing import Any, Dict, Literal
import httpx
import urllib.parse
import logging
from app.config import Settings, get_settings
from app.models.whatsapp import WhatsappMessage, WhatsappMessageHeaders, WhatsappMessageType
from app.utils.factories import AbstractWhatsappMessageFactory, WhatsappTextMessageFactory, WhatsappReactionMessageFactory
from app.utils.general import SingletonMeta

class WhatsappService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        settings = get_settings()
        endpoint = f'{settings.version}/{settings.phone_number_id}/messages'

        self.__factories: Dict[WhatsappMessageType, AbstractWhatsappMessageFactory] = {
            WhatsappMessageType.TEXT: WhatsappTextMessageFactory,
            WhatsappMessageType.REACTION: WhatsappReactionMessageFactory
        }
        self.__headers: Dict[str, str] = WhatsappMessageHeaders().model_dump()
        self.__url: str = urllib.parse.urljoin(settings.whatsapp_api, endpoint)
    
    async def __send(self, message: WhatsappMessage) -> None:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.__url, headers=self.__headers, data=message.model_dump())
                response.raise_for_status()
                logging.info(f'Whatsapp message sent to {message.to}')
                logging.info(f'Whatsapp message response: {response.text}')
            except httpx.HTTPStatusError as e:
                logging.error(f'Error sending whatsapp message: {e}')

    async def send_text_message(self, to: str, body: str, preview_url: Literal['false', 'true'] = 'false') -> None:
        factory = self.__factories[WhatsappMessageType.TEXT]
        payload = factory.create_payload(body=body, preview_url=preview_url)
        message = factory.create_message(to=to, payload=payload)
        await self.__send(message)   

    async def send_reaction_message(self, to: str, message_id: str, emoji: str) -> None:
        factory = self.__factories[WhatsappMessageType.REACTION]
        payload = factory.create_payload(message_id=message_id, emoji=emoji)
        message = factory.create_message(to=to, payload=payload)
        await self.__send(message)

class WhatsappServiceValidator(metaclass=SingletonMeta):
    @staticmethod
    def is_valid_whatsapp_message(body: Dict[str, Any]) -> bool:
        try:
            return (
                body.get("object")
                and body.get("entry")
                and body["entry"][0].get("changes")
                and body["entry"][0]["changes"][0].get("value")
                and body["entry"][0]["changes"][0]["value"].get("messages")
                and body["entry"][0]["changes"][0]["value"]["messages"][0]
            )
        except KeyError as e:
            logging.error(f'Error validating whatsapp message: {e}')
            return False
    
    