from fastapi import FastAPI

from app.core.settings import Settings
from app.routes.metadata_router_v1 import router as metadata_router


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="MCP Metadata Broker")
    app.include_router(metadata_router, prefix="/api/metadata/v1")
    app.state.settings = settings  # type: ignore[attr-defined]
    return app
