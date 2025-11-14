"""Admin UI utilities for MCP metadata broker."""


def get_admin_dashboard() -> dict[str, str]:
    """Return placeholder dashboard metadata until the Phase 3 admin UI ships.

    The current payload exposes only a `status` key so the UI can render a stub
    view. Phase 3 will extend this shape to include keys like `metrics`,
    `server_health`, `config_summary`, and `action_links` once the admin
    experience is fully implemented.
    """
    # (Phase 3): Expand to return real dashboard data (server metrics, health status,
    # config editor links)
    return {"status": "dashboard placeholder"}
