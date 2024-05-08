import asyncio

import uvicorn

from app import app
from app.config import get_settings
from app.utils.whatsapp import WhatsappService

if __name__ == '__main__':
    settings = get_settings()
    phone_number = settings.recipient_waid
    message = 'Hello, World!'


    whatsapp_service = WhatsappService()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(whatsapp_service.send_text_message(phone_number, message, preview_url='false'))
    loop.close()

    uvicorn.run(app, host='0.0.0.0', port=8000)