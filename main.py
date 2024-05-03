import asyncio
from app.config import get_settings
from app.utils.whatsapp import WhatsappService
from app.models.whatsapp import WhatsappMessageType

if __name__ == '__main__':
    settings = get_settings()
    phone_number = settings.recipient_waid
    message = 'Hello, World!'


    whatsapp_service = WhatsappService()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(whatsapp_service.send_text_message(phone_number, message, preview_url='false'))
    loop.close()