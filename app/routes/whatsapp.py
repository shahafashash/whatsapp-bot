import logging

from fastapi import APIRouter, HTTPException, Request, status

from app.config import get_settings
from app.models.whatsapp import WhatsappWebhookChallenge, WhatsappWebhookStatus
from app.utils.whatsapp import (WhatsappService, WhatsappServiceValidator,
                                WhatsappUtils)

whatsapp_router = APIRouter(prefix='/whatsapp', tags=['whatsapp'])

@whatsapp_router.get('/webhook', response_model=WhatsappWebhookChallenge, status_code=status.HTTP_200_OK)
async def verify_whatsapp_webhook(request: Request):
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')
    settings = get_settings()
    if mode and token:
        if mode == 'subscribe' and token == settings.verify_token:
            logging.info('Whatsapp webhook verified')
            return WhatsappWebhookChallenge(hub_challenge=challenge)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token provided')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing required parameters')
    
@whatsapp_router.post('/webhook', response_model=WhatsappWebhookStatus, status_code=status.HTTP_200_OK)
async def handle_whatsapp_webhook(request: Request):
    body = await request.json()
    logging.info(f'Whatsapp webhook received: {body}')
    
    statuses = body.get('entry', {[]})[0].get('changes', {[]})[0].get('value', {}).get('statuses', [])
    if statuses:
        logging.info(f'Whatsapp message status: {statuses}')
        return WhatsappWebhookStatus(status='ok')
    
    try:
        if WhatsappServiceValidator.is_valid_whatsapp_message(body):
            response = await WhatsappUtils.process_message(body)
            service = WhatsappService()
            settings = get_settings()
            await service.send_text_message(to=settings.recipient_waid, body=response)
            return WhatsappWebhookStatus(status='ok')

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid whatsapp message')
    except Exception as e:
        logging.error(f'Error processing whatsapp message: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error processing whatsapp message')

