"""Define the main entry point for the API."""
from fastapi import FastAPI
from mangum import Mangum

from openapi_retriever.api.routers.health.routes import ROUTER as health_router
from openapi_retriever.api.settings import (
    Settings,
    RUNTIME_SETTINGS_ATTRIBUTE_NAME,
)


APP = FastAPI(
    title="OpenAPI Retriever",
    description="API that allows search and retrieval of OpenAPI specifications.",
    version="0.0.0",
)
setattr(APP.state, RUNTIME_SETTINGS_ATTRIBUTE_NAME, Settings())
APP.include_router(health_router, prefix="/health", tags=["health"])


handler = Mangum(APP)
