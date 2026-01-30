from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from .api import router as api_router

from .api.api_v1.exception_handlers import api_exception_handler, unhandled_exception_handler
from .core.config import settings
from .core.logging import setup_logging
from .db import db_session
from .core.exceptions.base import ApiException
from .model import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await db_session.dispose()


app = FastAPI(
    lifespan=lifespan,
    log_level="info",
)

app.add_exception_handler(ApiException, api_exception_handler)  # type: ignore
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.run.host, port=settings.run.port, reload=True)
