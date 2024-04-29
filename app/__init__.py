from fastapi import FastAPI
from app.config import get_settings, configure_logging
from pydantic import BaseModel

configure_logging()

app = FastAPI()


# def create_app() -> FastAPI:
#     configure_logging()
#     _ = get_settings()
#     app = FastAPI()
    
#     return app