from typing import Any, Dict
from app.models.whatsapp import (
    WhatsappMessageType, 
    WhatsappMessage, 
    WhatsappMessagePayload,
    WhatsappTextMessage,
    WhatsappTextPayload,
)

class WhatsappMessageFactory:
    message_type_map = {
        WhatsappMessageType.TEXT: WhatsappTextMessage,
        # WhatsappMessageType.REACTION: WhatsappReactionMessage,
        # WhatsappMessageType.IMAGE: WhatsappImageMessage,
        # WhatsappMessageType.LOCATION: WhatsappLocationMessage,
        # WhatsappMessageType.CONTACTS: WhatsappContactsMessage,
        # WhatsappMessageType.LIST: WhatsappListMessage,
        # WhatsappMessageType.BUTTON: WhatsappButtonMessage,
    }

    @staticmethod
    def create_message(message_type: WhatsappMessageType, phone_number: str, payload: WhatsappMessagePayload) -> WhatsappMessage:
        """Create a message object based on the message type.

        Args:
            message_type (WhatsappMessageType): The type of message to create.
            phone_number (str): The phone number to send the message to.
            payload (Any): The payload of the message.

        Returns:
            WhatsappMessage: The message object.
        
        Raises:
            ValueError: If the message type is invalid.
        """
        message_class = WhatsappMessageFactory.message_type_map.get(message_type)
        if message_class is None:
            raise ValueError(f'Invalid message type: {message_type}')
        
        message = message_class(to=phone_number, payload=payload)
        return message
    
class WhatsappPayloadFactory:
    message_payload_map = {
        WhatsappMessageType.TEXT: WhatsappTextPayload,
        # WhatsappMessageType.REACTION: WhatsappReactionPayload,
        # WhatsappMessageType.IMAGE: WhatsappImagePayload,
        # WhatsappMessageType.LOCATION: WhatsappLocationPayload,
        # WhatsappMessageType.CONTACTS: WhatsappContactsPayload,
        # WhatsappMessageType.LIST: WhatsappListPayload,
        # WhatsappMessageType.BUTTON: WhatsappButtonPayload,
    }

    @staticmethod
    def create_payload(message_type: WhatsappMessageType, payload: Dict[str, Any]) -> WhatsappMessagePayload:
        """Create a message payload object based on the message type.

        Args:
            message_type (WhatsappMessageType): The type of message to create.
            payload (Dict[str, Any]): The payload of the message.

        Returns:
            WhatsappMessagePayload: The message payload object.

        Raises:
            ValueError: If the message type is invalid.
        """
        payload_class = WhatsappPayloadFactory.message_payload_map.get(message_type)
        if payload_class is None:
            raise ValueError(f'Invalid message type: {message_type}')
        
        return payload_class(**payload)