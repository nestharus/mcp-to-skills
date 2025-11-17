## Purpose

- Capture advanced patterns and best practices for building fast, resilient, production-ready FastAPI services, with emphasis on latency, concurrency, scalability, authentication, and clean architecture.

## Main Topics

- Performance: async connection pools (e.g., asyncpg/Motor), multi-layer caching (in-memory + Redis), batching, bulk endpoints, and background/offloaded work.
- Serialization and async: orjson, Pydantic v2 performance features, response model tuning, and async concurrency patterns (semaphores, TaskGroup, streaming, graceful shutdown).
- Gateway and middleware: rate limiting with Redis, compression (GZipMiddleware), trusted hosts, HTTP/2/keep-alive tuning, and timing/logging middleware.
- SOLID and clean architecture: SRP via routers/services/repositories, dependency inversion, DAO/service layers, and three-tier structures.
- Advanced features: streaming responses, WebSockets, connection reuse via lifespan events, concurrency vs. parallelism, and memory optimization (singleton pools, leak detection).
- Project structure and deployment: modular organization, DI and configuration, running multiple workers, uvloop, containerization, and serverless considerations.
- Authentication and authorization: OAuth2 password flow, JWT tokens, RBAC with dependency classes, and multi-tenant patterns.
- Task queues: Celery integration for long-running/background tasks, task status endpoints, and caching of task results.
- Testing and observability: pytest patterns, TestClient usage, metrics and tracing (Prometheus/OpenTelemetry), structured logging, and profiling.

## Opinions/Guidelines

- Use persistent async connection pools instead of per-request connections to reduce latency and resource churn.
- Apply layered caching (function-level LRU + Redis) with clear TTLs and invalidation strategies for hot paths.
- Batch external calls and use bulk endpoints where possible to reduce round-trips.
- Offload non-critical or CPU-bound work using background tasks, thread pools, or process pools; keep request handlers focused on I/O.
- Prefer orjson and Pydantic v2 for fast serialization/validation, tuning response models to avoid unnecessary overhead.
- Use semaphores to control concurrency against external services and avoid overload.
- Reuse HTTP clients and DB connections via lifespan hooks or dependency singletons; avoid recreating them per-request.
- Use streaming responses for large payloads or long-running streams rather than loading everything into memory.
- Implement rate limiting, compression, and trusted host middleware at the edge of the application.
- Enforce SOLID principles: keep routers thin, services focused on business rules, and repositories focused on persistence.
- Depend on abstractions rather than concrete implementations, enabling easier testing and swapping of infrastructure.
- Use OAuth2 + JWT for authentication and RBAC for authorization in production contexts.
- Offload long-running or unreliable external work to Celery workers, with clear status and result-checking endpoints.
- Maintain strong observability with metrics, tracing, and structured logs baked into middleware and services.

## Assumptions

- Targeting high-throughput, production workloads that justify complex performance and scalability optimizations.
- A relational or document database is in use, along with an async driver or ORM (e.g., asyncpg, SQLAlchemy, Motor).
- Redis or equivalent is available for caching, rate limiting, and as a Celery broker/backing store.
- Celery and worker infrastructure exist or will be provisioned for background processing.
- Authentication and authorization are required for most endpoints, using JWT and role/permission checks.
- Monitoring infrastructure (Prometheus, OpenTelemetry, Sentry/Honeycomb, etc.) is available for metrics and traces.
- The team is comfortable with async/await, concurrency primitives, and SOLID/clean architecture concepts.

## Staleness Indicators

- Assumes libraries and infrastructure (async DB drivers, Redis, Celery, JWT/auth packages, observability stack) that are not present in this project’s `pyproject.toml`.
- Describes high-throughput, low-latency scenarios that exceed the current early-stage, mostly stubbed API implementation.
- Uses examples and version details (Python 3.11+, specific library APIs) that may drift from this project’s actual runtime (Python 3.12.x now, 3.14+ target).
- Provides detailed patterns for streaming, WebSockets, and rate limiting that are not yet on the roadmap for this service.
- Assumes a mature deployment environment (multiple workers, Kubernetes/serverless) not represented in current project tooling.

## Tags

- architecture
- fastapi
- performance
- latency
- async
- concurrency
- caching
- connection-pools
- background-tasks
- serialization
- middleware
- rate-limiting
- compression
- solid-principles
- clean-architecture
- authentication
- authorization
- oauth2
- jwt
- rbac
- celery
- task-queues
- routing
- versioning
- testing
- observability
- deployment
- production
- best-practices

## Preliminary Target Docs

- Likely to become `docs/fastapi-best-practices.md` or be merged with the API patterns guide into a comprehensive FastAPI architecture/performance reference.
- Architecture and SOLID content overlaps with STYLE_6 and `api-patterns-guide.md` and should be consolidated into a single architecture section.
- Performance content (connection pools, caching, concurrency, background work) is distinctive and should likely live in a focused performance/latency chapter.
- Authentication/authorization sections could be extracted into a future `docs/auth-guide.md` if/when auth is added.
- Deployment/operations patterns may feed into a separate `docs/deployment-guide.md` or `docs/operations-guide.md` once infrastructure solidifies.
 - Many production/performance patterns should only be adopted in later lifecycle phases and must be reconciled with `docs/LIFECYCLE.md` before rollout.

## Red Flags

- Extensive overlap with `api-patterns-guide.md` on clean architecture, DI, layering, and testing; unmanaged duplication would be hard to maintain.
- Significant overlap with STYLE_6 for layered architecture and SRP/DIP, increasing the risk of conflicting advice.
- Many recommendations depend on infrastructure (DB, Redis, Celery, JWT/auth stack, observability stack) that does not exist in this repo yet.
- Authentication and RBAC sections are advanced and may be premature for current unauthenticated, stub endpoints.
- Celery and task queue patterns assume long-running/background work not yet defined in this project.
- Middleware and gateway optimizations (rate limiting, compression, HTTP/2 tuning) may be unnecessary overhead at current scale.
- Memory and concurrency deep dives (GIL behavior, pools, zero-copy, tracemalloc) might overwhelm readers at this project’s maturity level.
- Uses generic domains (users/items/movies) rather than the MCP metadata domain, so examples require translation.
- Testing recommendations (pytest + TestClient + fixtures) should be reconciled with existing `docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`, and `tests/conftest.py`.
- Observability advice assumes external services (Prometheus, OpenTelemetry, Sentry/Honeycomb) not present in this repo, which could mislead implementers.

## References

- docs/to_integrate/fastapi-best-practices.md
- docs/to_integrate/api-patterns-guide.md
- working/phase1/summaries/docs/to_integrate/STYLE_6.summary.md
- app/routes/metadata_router_v1.py
- app/services/mcp_manager.py
- app/core/dependencies.py
- pyproject.toml
- docs/TEST.md
- docs/TESTING_ARCHITECTURE.md
- tests/conftest.py
- working/phase1/summaries/README.summary.md
- working/phase1/summaries/docs/LIFECYCLE.summary.md
