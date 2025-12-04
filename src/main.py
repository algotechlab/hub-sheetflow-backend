from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.application import app_router
from src.application.api.v1 import v1_tags_metadata
from src.application.api.v1.middlewares.exceptions import (
    custom_exception_handler,
)
from src.core.config.settings import get_settings
from src.core.domain.models import load_all_models
from src.core.exceptions.custom import (
    DomainException,
    InfrastructureException,
    MultipleException,
)

settings = get_settings()

title = f'{settings.APP_NAME} API v{settings.API_VERSION}'

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    docs_url='/docs' if settings.DEBUG else None,
    redoc_url='/redoc' if settings.DEBUG else None,
    openapi_tags=v1_tags_metadata,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

load_all_models()


app.add_exception_handler(DomainException, custom_exception_handler)
app.add_exception_handler(InfrastructureException, custom_exception_handler)
app.add_exception_handler(MultipleException, custom_exception_handler)
app.add_exception_handler(Exception, custom_exception_handler)

app.include_router(app_router)
