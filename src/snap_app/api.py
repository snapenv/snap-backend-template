"""Snap App Template REST API."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import coloredlogs
from fastapi import FastAPI

from snap_app.core.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    # Startup events:
    # - Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # - Add coloredlogs' colored StreamHandler to the root logger.
    coloredlogs.install()
    yield
    # Shutdown events.


app = FastAPI(lifespan=lifespan, title=settings.APP_TITLE)


@app.get("/compute")
async def compute(n: int = 42) -> int:
    """Compute the result of a CPU-bound function.

    Returns
    -------
        int: fibonacci result
    """

    def fibonacci(n: int) -> int:
        return n if n <= 1 else fibonacci(n - 1) + fibonacci(n - 2)

    result = await asyncio.to_thread(fibonacci, n)
    return result
