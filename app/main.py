import logging

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

logging.basicConfig(
    level=logging.INFO,
    format=settings.logging_format,
    datefmt=settings.logging_dt_format
)

app = FastAPI(title=settings.app_title,
              description=settings.app_description)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
