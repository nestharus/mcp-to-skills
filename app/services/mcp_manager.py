"""Placeholder for MCP metadata orchestration logic."""

from app.contracts.metadata_contract import FetchRequest


class MCPManager:
    """Encapsulates MCP metadata operations and lifecycle management.

    Phase 1 establishes the contract for initializing and shutting down MCP server
    subprocesses; future iterations will spawn the processes and issue JSON-RPC calls.
    """

    def __init__(self, mcp_servers: dict[str, dict]) -> None:
        """Capture MCP server definitions for later orchestration stages."""

        self._mcp_servers = mcp_servers

    def fetch(self, request: FetchRequest) -> dict[str, str]:  # noqa: ARG002
        # LATER: Implement metadata retrieval based on MCP endpoints.
        # request used later
        return {"NAME": "unknown", "DESCRIPTION": "Not implemented"}

    def shutdown(self) -> None:
        """Clean up any resources spawned for MCP servers.

        The current implementation is a placeholder; later versions will terminate
        subprocesses, close transport pipes, and ensure graceful shutdowns.
        """

        # (Phase 2): Terminate spawned MCP server processes
