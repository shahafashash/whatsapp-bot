from fastapi import FastAPI

from app.config import configure_logging

configure_logging()

app = FastAPI()


# def create_app() -> FastAPI:
#     configure_logging()
#     _ = get_settings()
#     app = FastAPI()
    
#     return app