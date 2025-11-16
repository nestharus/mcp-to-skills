from __future__ import annotations

import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.core.settings import Settings
from app.routes.metadata_router_v1 import router as metadata_router
from app.services.mcp_manager import MCPManager

logger = logging.getLogger(__name__)


def _lifespan(settings: Settings) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        if settings.mcp_servers:
            app.state.mcp_manager = MCPManager(settings.mcp_servers)
            logger.info(
                "Initialized MCPManager for %d MCP server(s)",
                len(settings.mcp_servers),
            )

        try:
            yield
        finally:
            manager: MCPManager | None = getattr(app.state, "mcp_manager", None)
            if manager is not None:
                try:
                    manager.shutdown()
                except Exception:  # pragma: no cover - defensive logging
                    logger.exception("Failed to shutdown MCPManager cleanly")

    return lifespan


def create_app(settings: Settings) -> FastAPI:
    """Construct and configure the FastAPI application instance.

    Args:
        settings: Validated runtime options containing MCP server definitions.

    Returns:
        FastAPI: Application wired with orjson responses and MCP lifecycle hooks.

    The returned app exposes the MCP metadata API, serializes responses via
    ``orjson`` for performance, and wires a lifespan hook that spins up the
    ``MCPManager`` when MCP servers are configured and tears it down on shutdown.
    """

    app = FastAPI(
        title="MCP Metadata Broker",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        default_response_class=ORJSONResponse,
        lifespan=_lifespan(settings),
    )
    app.include_router(metadata_router, prefix="/api/metadata/v1")
    return app
