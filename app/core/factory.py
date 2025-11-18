from __future__ import annotations

import json
import logging
from collections.abc import AsyncGenerator, Callable, Sequence
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse, Response

from app.contracts.metadata_contract import MAX_VALIDATION_ERRORS
from app.core.settings import Settings
from app.routes.metadata_router_v1 import health_check
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
    app.state.settings = settings
    app.add_exception_handler(RequestValidationError, _exception_adapter)
    app.include_router(metadata_router, prefix="/api/metadata/v1")
    app.add_api_route(
        "/health",
        health_check,
        methods=["GET"],
        include_in_schema=False,
    )

    def custom_openapi() -> dict[str, object]:
        """Generate OpenAPI schema with capped validation error sizes."""
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            summary=app.summary,
            description=app.description,
            routes=app.routes,
        )

        components = schema.get("components", {})
        if not isinstance(components, dict):
            app.openapi_schema = schema
            return app.openapi_schema

        schemas = components.get("schemas", {})
        if not isinstance(schemas, dict):
            app.openapi_schema = schema
            return app.openapi_schema

        http_validation = schemas.get("HTTPValidationError")
        if isinstance(http_validation, dict):
            properties = http_validation.get("properties", {})
            if isinstance(properties, dict):
                detail = properties.get("detail")
                if isinstance(detail, dict):
                    detail["maxItems"] = MAX_VALIDATION_ERRORS
                    items = detail.get("items")
                    if isinstance(items, dict):
                        ref = items.get("$ref")
                        if isinstance(ref, str):
                            validation_name = ref.split("/")[-1]
                            validation_schema = schemas.get(validation_name)
                            if isinstance(validation_schema, dict):
                                v_props = validation_schema.get("properties", {})
                                if isinstance(v_props, dict):
                                    loc = v_props.get("loc")
                                    if isinstance(loc, dict):
                                        loc["maxItems"] = MAX_VALIDATION_ERRORS

        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
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


async def _exception_adapter(request: Request, exc: Exception) -> Response:
    if isinstance(exc, RequestValidationError):
        return await _validation_exception_handler(request, exc)
    raise exc


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
