# ADR 0007: Defer /livez, /readyz, /startupz Contracts

## Context

The application currently exposes a `/health` endpoint. Kubernetes-style liveness, readiness, and startup probes (`/livez`, `/readyz`, `/startupz`) are desirable but their exact contracts (payloads, checks, semantics) depend on the final architecture and operational needs. Prematurely standardizing these endpoints risks churn.

## Decision

- Continue to use `/health` as the interim health endpoint.
- Defer the definition and implementation of `/livez`, `/readyz`, and `/startupz` until a later phase where operational requirements are clear.
- Document this deferral in API and lifecycle documentation.

## Consequences

- Avoids locking in incomplete or incorrect health contracts.
- Requires operators to rely on `/health` for now.
- A future ADR will define the detailed behavior of the new endpoints when needed.

## References

- `docs/api.md` (health endpoints)
- `docs/LIFECYCLE.md` (application lifecycle and health behavior)
