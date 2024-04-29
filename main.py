import asyncio
from app.config import get_settings
from app.utils.whatsapp import WhatsappService
from app.utils.factories import WhatsappMessageFactory, WhatsappPayloadFactory
from app.models.whatsapp import WhatsappMessageType

if __name__ == '__main__':
    settings = get_settings()
    phone_number = settings.recipient_waid
    message = 'Hello, World!'
    payload = {'body': message}

    whatsapp_service = WhatsappService(WhatsappMessageFactory, WhatsappPayloadFactory)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(whatsapp_service.send_whatsapp_message(phone_number, WhatsappMessageType.TEXT, payload))
    loop.close()