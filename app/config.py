from typing import Optional
import sys
import logging
from functools import lru_cache
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

@lru_cache()
def get_settings():
    return Settings()

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )