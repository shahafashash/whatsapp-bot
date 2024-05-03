from abc import ABC, abstractmethod
from app.models.whatsapp import (
    WhatsappMessage, 
    WhatsappMessagePayload,
    WhatsappTextMessage,
    WhatsappTextPayload,
    WhatsappReactionMessage,
    WhatsappReactionPayload,
)


class AbstractWhatsappMessageFactory(ABC):
    """Interface for creating WhatsappMessage and WhatsappMessagePayload objects."""
    @staticmethod
    @abstractmethod
    def create_message(to: str, payload: WhatsappMessagePayload) -> WhatsappMessage:
        """Creates a WhatsappMessage object with the given payload.

        Args:
            to (str): The phone number to send the message to.
            payload (WhatsappMessagePayload): The payload of the message.

        Returns:
            WhatsappMessage: The message object.
        """
        pass

    @staticmethod
    @abstractmethod
    def create_payload(*args, **kwargs) -> WhatsappMessagePayload:
        """Creates a WhatsappMessagePayload object with the given keyword arguments.

        Returns:
            WhatsappMessagePayload: The message payload object.
        """
        pass

class WhatsappTextMessageFactory(AbstractWhatsappMessageFactory):
    @staticmethod
    def create_message(to: str, payload: WhatsappMessagePayload) -> WhatsappTextMessage:
        return WhatsappTextMessage(to=to, payload=payload)

    @staticmethod
    def create_payload(body: str, preview_url: str) -> WhatsappTextPayload:
        return WhatsappTextPayload(body=body, preview_url=preview_url)

class WhatsappReactionMessageFactory(AbstractWhatsappMessageFactory):
    @staticmethod
    def create_message(to: str, payload: WhatsappMessagePayload) -> WhatsappReactionMessage:
        return WhatsappReactionMessage(to=to, payload=payload)

    @staticmethod
    def create_payload(message_id: str, emoji: str) -> WhatsappReactionPayload:
        return WhatsappReactionPayload(message_id=message_id, emoji=emoji)