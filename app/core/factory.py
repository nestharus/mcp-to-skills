from __future__ import annotations

import json
import logging
from collections.abc import AsyncGenerator, Callable, Sequence
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import (
    validation_error_definition,
    validation_error_response_definition,
)
from fastapi.responses import ORJSONResponse

from app.contracts.metadata_contract import MAX_VALIDATION_ERRORS
from app.core.settings import Settings
from app.routes.metadata_router_v1 import health_check
from app.routes.metadata_router_v1 import router as metadata_router
from app.services.mcp_manager import MCPManager

logger = logging.getLogger(__name__)


validation_error_response_definition["properties"]["detail"]["maxItems"] = MAX_VALIDATION_ERRORS
validation_error_definition["properties"]["loc"]["maxItems"] = MAX_VALIDATION_ERRORS


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
    app.state.settings = settings
    app.add_exception_handler(
        RequestValidationError,
        _validation_exception_handler,
    )
    app.include_router(metadata_router, prefix="/api/metadata/v1")
    app.add_api_route(
        "/health",
        health_check,
        methods=["GET"],
        include_in_schema=False,
    )
    return app


async def _validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> ORJSONResponse:
    sanitized_errors = _sanitize_validation_errors(exc.errors())
    try:
        settings = request.app.state.settings
    except AttributeError:
        settings = None
    if isinstance(settings, Settings):
        include_error_body_flag = settings.include_error_body
    else:
        include_error_body_flag = False

    body_content = None
    if include_error_body_flag:
        try:
            raw_body = await request.body()
            body_content = json.loads(raw_body) if raw_body else None
        except Exception:  # pragma: no cover - defensive fallback
            body_content = None
    logger.info(
        "Validation error on %s %s: %s",
        request.method,
        request.url.path,
        sanitized_errors,
    )
    response_content: dict[str, Any] = {"detail": sanitized_errors}
    if include_error_body_flag:
        response_content["body"] = body_content
    return ORJSONResponse(
        status_code=400,
        content=response_content,
    )


def _sanitize_validation_errors(errors: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for error in errors:
        transformed = dict(error)
        ctx = transformed.get("ctx") or {}
        transformed["ctx"] = {key: str(value) for key, value in ctx.items()}
        sanitized.append(transformed)
        if len(sanitized) >= MAX_VALIDATION_ERRORS:
            break
    return sanitized
