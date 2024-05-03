from typing import Optional
import sys
import logging
import re
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    access_token: str
    app_id: str
    app_secret: str
    recipient_waid: str
    version: str
    phone_number_id: str
    verify_token: str
    whatsapp_api: Optional[str] = 'https://graph.facebook.com'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @field_validator('access_token')
    def validate_access_token(cls, value: str) -> str:
        if not re.match(r'^[0-9a-zA-Z]+$', value):
            raise ValueError('Invalid access token')
        return value
    
    @field_validator('app_id')
    def validate_app_id(cls, value: str) -> str:
        if not str.isnumeric(value):
            raise ValueError('Invalid app id')
        return value
    
    @field_validator('app_secret')
    def validate_app_secret(cls, value: str) -> str:
        if not re.match(r'^[0-9a-z]+$', value):
            raise ValueError('Invalid app secret')
        return value
    
    @field_validator('recipient_waid')
    def validate_recipient_waid(cls, value: str) -> str:
        # check that the recipient_waid is a valid phone number with country code
        if not re.match(r"^\+(?:[0-9\-\(\)\/\.]\s?){6, 15}[0-9]{1}$", value):
            raise ValueError('Invalid recipient waid')    
        return value
    
    @field_validator('version')
    def validate_version(cls, value: str) -> str:
        if not re.match(r'^v[0-9]+$', value):
            raise ValueError('Invalid version')
        return value
    
    @field_validator('phone_number_id')
    def validate_phone_number_id(cls, value: str) -> str:
        if not str.isnumeric(value):
            raise ValueError('Invalid phone number id')
        return value
    

@lru_cache()
def get_settings():
    return Settings()

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )