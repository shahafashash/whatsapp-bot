from typing import Any, Dict
import httpx
import urllib.parse
import logging
from app.config import Settings, get_settings
from app.models.whatsapp import WhatsappMessage, WhatsappMessageHeaders, WhatsappTextPayload, WhatsappMessageType
from app.utils.factories import WhatsappMessageFactory, WhatsappPayloadFactory

class WhatsappService:
    def __init__(self, message_factory: WhatsappMessageFactory, payload_factory: WhatsappPayloadFactory) -> None:
        settings = get_settings()
        endpoint = f'{settings.version}/{settings.phone_number_id}/messages'

        self.__message_factory = message_factory
        self.__payload_factory = payload_factory
        self.__headers = WhatsappMessageHeaders().model_dump()
        self.__url = urllib.parse.urljoin(settings.whatsapp_api, endpoint)

    def __prepare_message(self, phone_number: str, message_type: WhatsappMessageType, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare a whatsapp message object.

        Args:
            phone_number (str): The phone number to send the message to.
            message_type (WhatsappMessageType): The type of message to prepare.
            payload (Dict[str, Any]): The payload of the message.

        Returns:
            Dict[str, Any]: The body of the message.

        Raises:
            ValueError: If the message type is invalid.
        """
        payload_model = self.__payload_factory.create_payload(message_type, payload)
        message = self.__message_factory.create_message(message_type, phone_number, payload_model)
        return message.model_dump()
    
    async def send_whatsapp_message(self, phone_number: str, message_type: WhatsappMessageType, payload: Any) -> None:
        """Send a whatsapp message.

        Args:
            phone_number (str): The phone number to send the message to.
            message_type (WhatsappMessageType): The type of message to send.
            payload (Any): The payload of the message.
        """
        message = self.__prepare_message(phone_number, message_type, payload)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.__url, headers=self.__headers, data=message)
                response.raise_for_status()
                logging.info(f'Whatsapp message sent to {phone_number}')
                logging.info(f'Whatsapp message response: {response.text}')
            except httpx.HTTPStatusError as e:
                logging.error(f'Error sending whatsapp message: {e}')

            


            

