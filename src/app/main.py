"""Application factory: creates the app, mounts routers, and registers exception handlers."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.infrastructure.psgc.reader import get_dataset
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers import health, root
from app.presentation.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    setup_logging(debug=settings.debug)
    await asyncio.to_thread(get_dataset)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.include_router(root.router)
    app.include_router(health.router)
    app.include_router(api_router, prefix="/api/v1")
    register_exception_handlers(app)
    return app


app = create_app()
