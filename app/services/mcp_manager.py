"""Placeholder for MCP metadata orchestration logic."""

from app.contracts.metadata_contract import FetchRequest


class MCPManager:
    """Encapsulates operations against the MCP catalog."""

    def fetch(self, request: FetchRequest) -> dict[str, str]:
        # LATER: Implement metadata retrieval based on MCP endpoints.
        # request used later
        return {"NAME": "unknown", "DESCRIPTION": "Not implemented"}
