
from typing import Dict
import logging
import hmac
import hashlib
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from app.models.whatsapp import WhatsappMessageWebhook, WhatsappMessageWebhookResponse
from app.config import get_settings

whatsapp_router = APIRouter(prefix='/whatsapp', tags=['whatsapp'])

# def is_valid_whatsapp_message(body: Dict[str, str]) -> bool:
#     return (
#         body.get("object")
#         and body.get("entry")
#         and body["entry"][0].get("changes")
#         and body["entry"][0]["changes"][0].get("value")
#         and body["entry"][0]["changes"][0]["value"].get("messages")
#         and body["entry"][0]["changes"][0]["value"]["messages"][0]
#     )

# async def verify_token(whatsapp_message_webhook: WhatsappMessageWebhook = Depends()) -> str:
#     settings = get_settings()
#     if whatsapp_message_webhook.hub_verify_token == settings.verify_token:
#         return whatsapp_message_webhook.hub_challenge
#     else:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token provided')

# async def verify_signature(request: Request, x_hub_signature: str = Header(None)) -> None:
#     settings = get_settings()
#     signature = request.headers.get('X-Hub-Signature-256')
#     if not signature:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Signature missing')
    
#     signature = signature.split('-256', maxsplit=1)[0]
#     data = await request.body()
#     data = data.decode('utf-8')
#     expected_signature = hmac.new(bytes(settings.app_secret, 'latin-1'), data.encode('utf-8'), hashlib.sha256).hexdigest()
#     if not hmac.compare_digest(signature, expected_signature):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Whatsapp signature verification failed')
    
    
# @whatsapp_router.post('/message', status_code=status.HTTP_200_OK)
# async def handle_whatsapp_message(request: Request, x_hub_signature: str = Header(None)) -> WhatsappMessageWebhookResponse:
#     await verify_signature(request, x_hub_signature)
#     body = await request.json()
#     logging.info(f'Whatsapp message received: {body}')
    
#     statuses = body.get('entry', {[]})[0].get('changes', {[]})[0].get('value', {}).get('statuses', [])
#     if statuses:
#         logging.info(f'Whatsapp message status: {statuses}')
    
#     try:
#         if is_valid_whatsapp_message(body):
            

# @whatsapp_router.get('/message', status_code=status.HTTP_200_OK)
# async def verify_whatsapp_message(whatsapp_message_webhook: WhatsappMessageWebhook = Depends(verify_token)) -> WhatsappMessageWebhookResponse:
#     if whatsapp_message_webhook.hub_mode and whatsapp_message_webhook.hub_verify_token:
#         if whatsapp_message_webhook.hub_mode == 'subscribe':
#             logging.info('Whatsapp webhook verified')
#             return whatsapp_message_webhook.hub_challenge
        
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Whatsapp webhook verification failed')
    
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Whatsapp webhook missing required parameters')


